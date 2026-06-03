export const meta = {
  name: 'description-optimize',
  description: 'Optimize a skill/command description for reliable triggering: score the current description against labelled should-trigger / should-not-trigger queries (majority vote), propose improvements, and keep the best by held-out test score. Replaces the retired claude -p run_loop apparatus — uses in-session token budget, no separate CLI billing. Skills/commands only; subagents are user-invoked.',
  phases: [
    { title: 'Split', detail: 'deterministic train/test split of the labelled queries' },
    { title: 'Optimize', detail: 'score → propose → keep best by held-out test score' },
  ],
}

// args = {
//   artifactName: string,
//   artifactType: 'skill' | 'command',
//   currentDescription: string,
//   queries: [{ query: string, should_trigger: boolean }],   // ~20: half should-trigger, half near-miss
//   maxIterations?: number (default 4),
//   runsPerQuery?: number (default 3),
// }
const { artifactName, artifactType, currentDescription, queries } = args
const MAX_ITERS = args.maxIterations ?? 4
const RUNS = args.runsPerQuery ?? 3

if (artifactType === 'subagent') {
  return { error: 'Description optimization does not apply to subagents — they are user-invoked, not auto-triggered from a description.' }
}

const VOTE_SCHEMA = {
  type: 'object',
  required: ['would_trigger'],
  properties: { would_trigger: { type: 'boolean' }, reason: { type: 'string' } },
}
const DESC_SCHEMA = {
  type: 'object',
  required: ['description'],
  properties: { description: { type: 'string' } },
}

phase('Split')
// Deterministic ~60/40 stride split (no Math.random in workflows).
const train = queries.filter((_, i) => i % 5 < 3)
const test = queries.filter((_, i) => i % 5 >= 3)
log(`split: ${train.length} train / ${test.length} test`)

// Accuracy of a description over a query set: majority vote of RUNS judgments per query.
async function triggerScore(description, set, tag) {
  const perQuery = await parallel(set.map((q, qi) => async () => {
    const votes = await parallel(Array.from({ length: RUNS }, (_, r) => () =>
      agent(
        `You decide whether a Claude Code ${artifactType} would AUTO-TRIGGER for a user message, based ONLY on its description (how Claude matches skills to intent).\n` +
        `${artifactType} name: ${artifactName}\n` +
        `Description:\n"""${description}"""\n\n` +
        `User message:\n"""${q.query}"""\n\n` +
        `Independent judgment #${r}: would this ${artifactType} auto-trigger here? Decide strictly — would Claude actually reach for it given that description and message?`,
        { phase: 'Optimize', label: `${tag}:q${qi}:r${r}`, schema: VOTE_SCHEMA }
      )
    ))
    const surviving = votes.filter(Boolean)
    const yes = surviving.filter(v => v.would_trigger).length
    // Threshold over surviving votes, not the fixed RUNS denominator, so a flaky/failed
    // judgment isn't silently counted as a "no-trigger" vote.
    const predicted = surviving.length ? yes > surviving.length / 2 : false
    return predicted === q.should_trigger ? 1 : 0
  }))
  return perQuery.length ? perQuery.reduce((a, b) => a + b, 0) / perQuery.length : 0
}

phase('Optimize')
let best = {
  description: currentDescription,
  train: await triggerScore(currentDescription, train, 'base-train'),
  test: await triggerScore(currentDescription, test, 'base-test'),
}
const history = [{ iter: 0, train: best.train, test: best.test, description: best.description }]
log(`iter 0 (current): train ${best.train.toFixed(2)} test ${best.test.toFixed(2)}`)

for (let i = 1; i <= MAX_ITERS; i++) {
  const proposal = await agent(
    `Improve this Claude Code ${artifactType} description so it triggers on the should-trigger cases and stays silent on the should-not cases. Follow Thariq Tip 6 (write for the model, name specific user phrasings, be slightly emphatic) and the 4.8 anti-patterns (no "CRITICAL/MUST" shouting — that over-triggers). Keep it within ~1,536 chars.\n\n` +
    `Current description:\n"""${best.description}"""\n\n` +
    `TRAIN queries (with labels):\n${JSON.stringify(train, null, 0)}\n\n` +
    `Current train accuracy: ${best.train.toFixed(2)}. Return only the improved description text.`,
    { phase: 'Optimize', label: `propose:iter${i}`, schema: DESC_SCHEMA }
  )
  if (!proposal) continue
  const cand = {
    description: proposal.description,
    train: await triggerScore(proposal.description, train, `t${i}-train`),
    test: await triggerScore(proposal.description, test, `t${i}-test`),
  }
  history.push({ iter: i, train: cand.train, test: cand.test, description: cand.description })
  log(`iter ${i}: train ${cand.train.toFixed(2)} test ${cand.test.toFixed(2)} (best test ${best.test.toFixed(2)})`)
  if (cand.test > best.test) best = cand   // select by HELD-OUT test score to avoid overfitting the train set
}

return {
  artifact: artifactName,
  best_description: best.description,
  best_train_score: best.train,
  best_test_score: best.test,
  history,
}
