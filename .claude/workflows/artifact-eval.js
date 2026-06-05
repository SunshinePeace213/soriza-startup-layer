export const meta = {
  name: 'artifact-eval',
  description: 'Run a Claude Code artifact (skill/command/subagent) against eval prompts vs a baseline, grade each run with meta-skill-grader, and return pass-rate deltas. Replaces prompt-architect Phase 5 prose-spawn + the claude -p loop. Spawning is deterministic, so it works even on 4.8 which under-fires prose "spawn N subagents" instructions.',
  phases: [
    { title: 'Run', detail: 'with-artifact + baseline per eval, in parallel' },
    { title: 'Grade', detail: 'meta-skill-grader scores each run against its assertions' },
  ],
}

// args = {
//   artifactPath:   string,                         // path to the artifact under test
//   artifactType:   'skill' | 'command' | 'subagent',
//   artifactName:   string,                         // frontmatter name (for subagent agentType + skill/command reference)
//   iterationDir:   string,                         // absolute path to <workspace>/iteration-N
//   graderRubricPath: string,                       // path to agents/meta-skill-grader.md
//   evals: [{ name: string, prompt: string, assertions: string[], files?: string[] }]
// }
// Accept args whether the harness forwards them as a parsed object OR a JSON string
// (the Workflow `args` field is typed `any`; some harnesses pass it through verbatim as text).
let a = args || {}
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }
const { artifactPath, artifactType, artifactName, iterationDir, graderRubricPath, evals } = a

// Validates what meta-skill-grader returns; the agent also writes the full grading.json to disk.
const GRADING_SCHEMA = {
  type: 'object',
  required: ['summary', 'expectations'],
  properties: {
    summary: {
      type: 'object',
      required: ['passed', 'failed', 'total', 'pass_rate'],
      properties: {
        passed: { type: 'integer' },
        failed: { type: 'integer' },
        total: { type: 'integer' },
        pass_rate: { type: 'number' },
      },
    },
    expectations: {
      type: 'array',
      items: {
        type: 'object',
        required: ['text', 'passed', 'evidence'],
        properties: {
          text: { type: 'string' },
          passed: { type: 'boolean' },
          evidence: { type: 'string' },
        },
      },
    },
    eval_feedback: {
      type: 'object',
      properties: {
        overall: { type: 'string' },
        suggestions: { type: 'array', items: { type: 'object' } },
      },
    },
  },
}

const filesNote = (ev) => (ev.files && ev.files.length) ? `Input files: ${ev.files.join(', ')}. ` : ''

// "With-artifact" run. For a subagent, the worker IS the artifact (spawned via agentType),
// so the prompt is the bare task. For a skill/command, instruct the executor to use it by name.
const withRunPrompt = (ev, outDir) =>
  artifactType === 'subagent'
    ? `${filesNote(ev)}${ev.prompt}\n\nSave all deliverables to ${outDir}/outputs/ and write a brief transcript of what you did to ${outDir}/transcript.md.`
    : `Use the ${artifactType} "${artifactName}" (defined at ${artifactPath}) to complete this task. ${filesNote(ev)}${ev.prompt}\n\nSave all deliverables to ${outDir}/outputs/ and write a brief transcript of what you did to ${outDir}/transcript.md.`

const baselineRunPrompt = (ev, outDir) =>
  `Complete this task with no custom skill/command/subagent — your default behavior only. ${filesNote(ev)}${ev.prompt}\n\nSave all deliverables to ${outDir}/outputs/ and write a brief transcript of what you did to ${outDir}/transcript.md.`

const graderPrompt = (ev, runDir) =>
  `Read the rubric at ${graderRubricPath} and follow it exactly. Grade the run in ${runDir}:\n` +
  `- expectations: ${JSON.stringify(ev.assertions)}\n` +
  `- transcript_path: ${runDir}/transcript.md\n` +
  `- outputs_dir: ${runDir}/outputs\n` +
  `Write grading.json to ${runDir}/grading.json and return the same object.`

const rows = await pipeline(
  evals,
  // Stage 1 — RUN: with-artifact + baseline, guaranteed parallel spawn.
  async (ev) => {
    const withDir = `${iterationDir}/${ev.name}/with`
    const baseDir = `${iterationDir}/${ev.name}/baseline`
    await parallel([
      () => agent(withRunPrompt(ev, withDir), {
        phase: 'Run', label: `with:${ev.name}`,
        ...(artifactType === 'subagent' ? { agentType: artifactName } : {}),
      }),
      () => agent(baselineRunPrompt(ev, baseDir), { phase: 'Run', label: `base:${ev.name}` }),
    ])
    return { ev, withDir, baseDir }
  },
  // Stage 2 — GRADE: meta-skill-grader per side, schema-validated.
  async ({ ev, withDir, baseDir }) => {
    const [withGrade, baseGrade] = await parallel([
      () => agent(graderPrompt(ev, withDir), { phase: 'Grade', label: `grade-with:${ev.name}`, schema: GRADING_SCHEMA }),
      () => agent(graderPrompt(ev, baseDir), { phase: 'Grade', label: `grade-base:${ev.name}`, schema: GRADING_SCHEMA }),
    ])
    const wr = withGrade?.summary?.pass_rate ?? null
    const br = baseGrade?.summary?.pass_rate ?? null
    log(`${ev.name}: with ${wr} vs baseline ${br}`)
    return { eval: ev.name, with_pass_rate: wr, baseline_pass_rate: br, delta: (wr ?? 0) - (br ?? 0), eval_feedback: withGrade?.eval_feedback ?? null }
  }
)

// The script does the aggregation math; only the summary returns to the conversation.
// Detailed grading.json files live in each run dir for scripts.aggregate_benchmark + the eval viewer.
const ok = rows.filter(Boolean)
const mean = (xs) => xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null
const withMean = mean(ok.map(r => r.with_pass_rate).filter(x => x != null))
const baseMean = mean(ok.map(r => r.baseline_pass_rate).filter(x => x != null))

return {
  artifact: artifactName,
  artifactType,
  iterationDir,
  per_eval: ok,
  overall: { with_pass_rate: withMean, baseline_pass_rate: baseMean, delta: (withMean ?? 0) - (baseMean ?? 0) },
  next: `grading.json written per run — run \`python3 -m scripts.aggregate_benchmark ${iterationDir} --artifact-type ${artifactType} --artifact-name ${artifactName}\` then the eval-viewer for the full benchmark + review UI.`,
}
