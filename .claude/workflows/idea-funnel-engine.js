export const meta = {
  name: 'idea-funnel-engine',
  description: 'Idea-Stage Validator engine — distill many startup ideas through founder-fit, testability, an evidence-based disconfirmation screen, and customer-discovery design into a ranked Shortlist. Stops at the human SEND gate. Launched by the /idea-funnel skill.',
  phases: [
    { title: 'Setup', detail: 'read prior ledger + derive cap K from the founder profile' },
    { title: 'Top of funnel', detail: 'grounding sweep + seed generation (thesis mode)' },
    { title: 'Gate 0 — FMF', detail: 'founder-market-fit screen' },
    { title: 'Gate 1 — Testability', detail: 'sharpen into a testable hypothesis' },
    { title: 'Gate 2 — Disconfirmation', detail: 'expert objections + market evidence → kill/advance' },
    { title: 'Gate 3 — CD Design', detail: 'sealed Cowork run-pack for survivors' },
    { title: 'Persist', detail: 'write the stateful ledger + shortlist' },
  ],
}

// ---------- helpers ----------
function slugify(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'untitled'
}
function lensesFor(ideaType) {
  const M = {
    marketplace: ['peter-thiel-perspective', 'jeff-bezos-perspective', 'charlie-munger-perspective'],
    'e-commerce': ['jeff-bezos-perspective', 'charlie-munger-perspective', 'garry-tan-perspective'],
    trading: ['nassim-taleb-perspective', 'charlie-munger-perspective', 'elon-musk-perspective'],
    fintech: ['nassim-taleb-perspective', 'charlie-munger-perspective', 'elon-musk-perspective'],
    'ai-agent': ['peter-thiel-perspective', 'elon-musk-perspective', 'garry-tan-perspective'],
    content: ['jeff-bezos-perspective', 'naval-ravikant-perspective', 'garry-tan-perspective'],
    community: ['jeff-bezos-perspective', 'naval-ravikant-perspective', 'garry-tan-perspective'],
    services: ['tom-eisenmann-perspective', 'jeff-bezos-perspective', 'ben-horowitz-perspective'],
    'hardware-adjacent': ['elon-musk-perspective', 'nassim-taleb-perspective', 'tom-eisenmann-perspective'],
    'regulated-adjacent': ['nassim-taleb-perspective', 'charlie-munger-perspective', 'tom-eisenmann-perspective'],
    default: ['peter-thiel-perspective', 'charlie-munger-perspective', 'jeff-bezos-perspective'],
  }
  return M[ideaType] || M.default
}
function mkCandidate(seed) {
  const id = seed.id || ('cand-' + slugify(seed.title || seed.problem))
  return {
    id, slug: id.replace(/^cand-/, ''),
    title: seed.title || seed.problem || id,
    seed: { problem: seed.problem || '', who: seed.who || '', why_now: seed.why_now || '' },
    idea_type: seed.idea_type || 'default',
    status: 'advancing', killed_at: null, rank: null,
    gates: { gate0_fmf: null, gate1_sharpen: null, gate2_disconfirmation: null, gate3_cd_design: null },
  }
}

// ---------- schemas ----------
const VERDICT = { verdict: { type: 'string', enum: ['advance', 'kill'] }, score: { type: 'number' }, reason: { type: 'string' } }
const SEED_SCHEMA = { type: 'object', required: ['seeds'], properties: { seeds: { type: 'array', items: { type: 'object', required: ['title', 'problem', 'who', 'why_now', 'idea_type'], properties: { id: { type: 'string' }, title: { type: 'string' }, problem: { type: 'string' }, who: { type: 'string' }, why_now: { type: 'string' }, idea_type: { type: 'string' } } } } } }
const KCAP_SCHEMA = { type: 'object', required: ['k'], properties: { k: { type: 'integer' }, rationale: { type: 'string' } } }
const READER_SCHEMA = { type: 'object', required: ['run_history_found'], properties: { run_history_found: { type: 'boolean' }, latest_run_label: { type: 'string' }, settled: { type: 'array', items: { type: 'object', properties: { candidate_id: { type: 'string' }, status: { type: 'string' }, killed_at: { type: ['string', 'null'] }, score: { type: 'number' }, resurrect: { type: 'boolean' } } } } } }
const FMF_SCHEMA = { type: 'object', required: ['candidate_id', 'verdict', 'score', 'reason'], properties: { candidate_id: { type: 'string' }, ...VERDICT, hard_fail: { type: ['string', 'null'] } } }
const SHARPEN_SCHEMA = { type: 'object', required: ['candidate_id', 'verdict', 'score', 'reason'], properties: { candidate_id: { type: 'string' }, ...VERDICT, testable: { type: 'boolean' }, hypothesis: { type: 'object', properties: { who: { type: 'string' }, how_often: { type: 'string' }, how_severe: { type: 'string' }, status_quo: { type: 'string' }, sentence: { type: 'string' } } }, hypothesis_path: { type: ['string', 'null'] } } }
const OBJECTION_SCHEMA = { type: 'object', required: ['expert', 'objection', 'rebut_if', 'severity'], properties: { candidate_id: { type: 'string' }, expert: { type: 'string' }, objection: { type: 'string' }, rebut_if: { type: 'string' }, severity: { type: 'number' } } }
const JUDGE_SCHEMA = { type: 'object', required: ['candidate_id', 'verdict', 'score', 'reason'], properties: { candidate_id: { type: 'string' }, ...VERDICT, strongest_unrebutted: { type: 'string' }, coverage_gap: { type: ['string', 'null'] }, market: { type: 'object', properties: { tam: { type: 'string' }, sam: { type: 'string' }, som: { type: 'string' }, timing: { type: 'string' } } } } }
const CD_SCHEMA = { type: 'object', required: ['candidate_id', 'verdict', 'reachable'], properties: { candidate_id: { type: 'string' }, verdict: { type: 'string', enum: ['advance', 'kill'] }, reachable: { type: 'boolean' }, runpack_path: { type: ['string', 'null'] }, reason: { type: 'string' } } }
const WRITER_SCHEMA = { type: 'object', required: ['run_label'], properties: { run_label: { type: 'string' }, ledger_path: { type: 'string' }, ledger_json_path: { type: 'string' }, shortlist_path: { type: 'string' }, shortlist: { type: 'array', items: { type: 'string' } } } }

// ---------- run ----------
const a = args || {}
const thesisSlug = slugify(a.thesis || (Array.isArray(a.seeds) ? 'founder-seeds' : 'idea-funnel'))
const coworkShare = a.coworkSharePath || null

// Setup — prior ledger + cap K
phase('Setup')
const prior = await agent(
  `Read prior funnel ledgers under docs/ideas-stages/_funnel-runs/. Resurrect IDs (treat as NOT settled): ${JSON.stringify(a.resurrect || [])}. Return the settled candidates from the latest run.`,
  { agentType: 'ledger-reader', schema: READER_SCHEMA, phase: 'Setup', label: 'ledger-reader' }
)
const settledKilled = new Set()
const priorSettled = []
if (prior && prior.run_history_found && Array.isArray(prior.settled)) {
  for (const s of prior.settled) {
    priorSettled.push(s)
    if (s.status === 'killed' && !s.resurrect) settledKilled.add(s.candidate_id)
  }
}

let kVal = a.k
let capacityRationale = a.k ? `explicit k=${a.k}` : ''
if (!kVal) {
  const cap = await agent(
    `Read docs/founder-profile.md. From time-commitment, founding-team status, and risk appetite, return the default number of customer-discovery campaigns this founder can run well AT ONCE (part-time solo => 1; full-time team => up to team size; cap at 5). Output {k, rationale}.`,
    { agentType: undefined, schema: KCAP_SCHEMA, phase: 'Setup', label: 'capacity', model: 'haiku' }
  )
  kVal = cap && cap.k ? cap.k : 1
  capacityRationale = (cap && cap.rationale) || 'defaulted to 1 (part-time solo)'
}
log(`Cap K = ${kVal} (${capacityRationale})`)

// Top of funnel — seeds
let seeds = []
if (Array.isArray(a.seeds) && a.seeds.length) {
  seeds = a.seeds
  log(`Ingesting ${seeds.length} founder-supplied seeds`)
} else if (a.thesis) {
  phase('Top of funnel')
  await agent(
    `Grounding sweep for thesis: "${a.thesis}". Research real trends, demand, and unsolved pains across facets (trends/why-now, existing solutions, demand-pain, adjacent markets) and WRITE a grounding doc to docs/idea-exploration/${thesisSlug}/research/grounding.md. Return the path.`,
    { agentType: 'startup-idea-researcher', phase: 'Top of funnel', label: 'grounding' }
  )
  const gen = await agent(
    `Expand thesis "${a.thesis}" into ${a.n || 10} thin Candidate seeds, WIDE (no narrowing). Read the grounding doc at docs/idea-exploration/${thesisSlug}/research/grounding.md and docs/founder-profile.md. Tag each with an idea_type.`,
    { agentType: 'seed-generator', schema: SEED_SCHEMA, phase: 'Top of funnel', label: 'seed-gen' }
  )
  seeds = (gen && gen.seeds) || []
  log(`Generated ${seeds.length} seeds`)
} else {
  return { error: 'Provide args.thesis (generate mode) or args.seeds (ingest mode).' }
}

const resurrectSet = new Set(a.resurrect || [])
const candidates = seeds.map(mkCandidate).filter(c => !settledKilled.has(c.id) || resurrectSet.has(c.id))
log(`${candidates.length} candidates enter the funnel (${settledKilled.size} prior kills skipped)`)

// ---------- gate stages (pipelined; each passes the candidate through, never null) ----------
async function gate0(c) {
  if (c.status === 'killed') return c
  const v = await agent(
    `Founder-Market-Fit screen (Gate 0). Candidate id=${c.id}, seed=${JSON.stringify(c.seed)}, title=${JSON.stringify(c.title)}. Read docs/founder-profile.md and .claude/skills/idea-funnel/references/gate-rubrics.md (Gate 0).`,
    { agentType: 'fmf-screen', schema: FMF_SCHEMA, phase: 'Gate 0 — FMF', label: `fmf:${c.id}`, model: 'haiku' }
  )
  c.gates.gate0_fmf = v
  if (!v || v.verdict === 'kill') { c.status = 'killed'; c.killed_at = 'gate-0' }
  return c
}
async function gate1(c) {
  if (c.status === 'killed') return c
  const ns = `docs/ideas-stages/${c.slug}/`
  const v = await agent(
    `Testability gate (Gate 1). Candidate id=${c.id}, seed=${JSON.stringify(c.seed)}, title=${JSON.stringify(c.title)}. Output namespace ${ns}; write hypothesis.md there on advance. Read .claude/skills/idea-funnel/references/gate-rubrics.md (Gate 1).`,
    { agentType: 'sharpen-gate', schema: SHARPEN_SCHEMA, phase: 'Gate 1 — Testability', label: `sharp:${c.id}`, model: 'haiku' }
  )
  c.gates.gate1_sharpen = v
  if (!v || v.verdict === 'kill') { c.status = 'killed'; c.killed_at = 'gate-1' }
  return c
}
async function gate2(c) {
  if (c.status === 'killed') return c
  const ns = `docs/ideas-stages/${c.slug}/`
  const lenses = lensesFor(c.idea_type)
  const hypo = c.gates.gate1_sharpen && c.gates.gate1_sharpen.hypothesis
  const objections = await parallel(lenses.map(slug => () => agent(
    `Objection lens. Channel ${slug} against candidate id=${c.id}: seed=${JSON.stringify(c.seed)}, hypothesis=${JSON.stringify(hypo)}. Read its lens-card in .claude/skills/idea-funnel/references/expert-lens-map.md. Fire ONE strongest disconfirming objection + what evidence would rebut it.`,
    { agentType: 'objection-lens', schema: OBJECTION_SCHEMA, phase: 'Gate 2 — Disconfirmation', label: `obj:${c.id}:${slug.replace('-perspective', '')}` }
  )))
  await parallel([
    () => agent(`Competitor steelman for candidate id=${c.id} (${JSON.stringify(c.title)}, ${JSON.stringify(c.seed)}). Write the steelman provenance to ${ns}market-research/competitor-steelman.md.`,
      { agentType: 'competitor-steelman', phase: 'Gate 2 — Disconfirmation', label: `steel:${c.id}` }),
    () => agent(`Market evidence sweep for candidate id=${c.id} (hypothesis=${JSON.stringify(hypo)}). Cover landscape, review-mining, TAM/SAM/SOM + buyer map, and trend read; WRITE ${ns}market-research.md.`,
      { agentType: 'market-researcher', phase: 'Gate 2 — Disconfirmation', label: `mkt:${c.id}` }),
  ])
  const v = await agent(
    `Disconfirmation judge (Gate 2). Candidate id=${c.id}, idea_type=${c.idea_type}. Objections (from lenses): ${JSON.stringify((objections || []).filter(Boolean))}. Read the steelman at ${ns}market-research/competitor-steelman.md and the market evidence at ${ns}market-research.md. Read .claude/skills/idea-funnel/references/gate-rubrics.md (Gate 2). Kill if the strongest objection stands unrebutted by evidence OR the market read fails. If a domain-specific lens would have been more decisive than ${JSON.stringify(lenses)}, name it as coverage_gap.`,
    { agentType: 'disconfirmation-judge', schema: JUDGE_SCHEMA, phase: 'Gate 2 — Disconfirmation', label: `judge:${c.id}` }
  )
  c.gates.gate2_disconfirmation = v
  if (!v || v.verdict === 'kill') { c.status = 'killed'; c.killed_at = 'gate-2' }
  return c
}

const processed = await pipeline(candidates, gate0, gate1, gate2)

// ---------- cap (barrier): rank G2 survivors, take top-K ----------
const survivors = processed.filter(c => c && c.status !== 'killed')
survivors.sort((x, y) => ((y.gates.gate2_disconfirmation && y.gates.gate2_disconfirmation.score) || 0) - ((x.gates.gate2_disconfirmation && x.gates.gate2_disconfirmation.score) || 0))
survivors.forEach((c, i) => { c.rank = i + 1; c.status = i < kVal ? 'shortlisted' : 'advancing' })
const shortlisted = survivors.filter(c => c.status === 'shortlisted')
log(`${survivors.length} cleared the desk funnel; ${shortlisted.length} shortlisted (cap K=${kVal})`)

// ---------- Gate 3 — CD design on the shortlist ----------
if (shortlisted.length) {
  phase('Gate 3 — CD Design')
  await parallel(shortlisted.map(c => () => (async () => {
    const ns = `docs/ideas-stages/${c.slug}/`
    const out = coworkShare ? `${coworkShare}/${c.slug}-cowork-runpack.md` : `${ns}customer-discovery/cowork-runpack.md`
    const v = await agent(
      `Customer-discovery DESIGN (Gate 3) for shortlisted survivor id=${c.id}. Read ${ns}hypothesis.md and ${ns}market-research.md. Build target profile + reachability map + Mom-Test interview guide, then write a SEALED run-pack to ${out}. Soft-kill only if no reachable audience. Never send.`,
      { agentType: 'cd-design-gate', schema: CD_SCHEMA, phase: 'Gate 3 — CD Design', label: `cd:${c.id}` }
    )
    c.gates.gate3_cd_design = v
    if (v && v.verdict === 'kill') { c.status = 'advancing'; c.rank = null } // soft-kill: drop from shortlist, not dead
    return c
  })()))
}

// ---------- Persist ----------
phase('Persist')
const writer = await agent(
  `Persist this funnel run. Thesis slug=${thesisSlug}. K=${kVal} (capacity: ${capacityRationale}). Follow .claude/skills/idea-funnel/references/ledger-schema.md exactly. Write ledger.json, ledger.md (the board), and shortlist.md.\nResults (this run): ${JSON.stringify(processed)}\nPrior settled (carry into the board): ${JSON.stringify(priorSettled)}`,
  { agentType: 'ledger-writer', schema: WRITER_SCHEMA, phase: 'Persist', label: 'ledger-writer' }
)

const counts = {
  entered: candidates.length,
  killed_gate0: processed.filter(c => c.killed_at === 'gate-0').length,
  killed_gate1: processed.filter(c => c.killed_at === 'gate-1').length,
  killed_gate2: processed.filter(c => c.killed_at === 'gate-2').length,
  cleared_desk: survivors.length,
  shortlisted: survivors.filter(c => c.status === 'shortlisted').length,
}
return {
  run_label: writer && writer.run_label,
  ledger: writer && writer.ledger_path,
  shortlist_doc: writer && writer.shortlist_path,
  shortlist: writer && writer.shortlist,
  counts,
}
