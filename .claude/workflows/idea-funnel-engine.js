export const meta = {
  name: 'idea-funnel-engine',
  description: 'Idea-Stage Validator engine (v2) — a lean-startup tester. Generates ideas founder-BLIND, screens FIT (durable capability only), sharpens to testable hypotheses, runs an expert-debate disconfirmation that produces a Brief (interview questions, NOT kills), detects niche-first real demand, then at a CHECKPOINT drops ONLY the 3 fatal flaws, ranks survivors by demand strength (founder-fit shown as a separate, unfused tiebreaker), caps top-K=1, and builds a SEALED Phase A customer-discovery pack. Never returns empty unless every seed hit a fatal flaw. Stops before any outreach is sent. Launched by the /idea-funnel skill.',
  phases: [
    { title: 'Setup', detail: 'read prior ledger (resurrect) + resolve cap K' },
    { title: 'Generate', detail: 'grounding sweep + founder-BLIND seed generation (thesis mode)' },
    { title: 'Fit-screen', detail: 'FIT axis — durable capability/legal/geo/language only; ignore $/time' },
    { title: 'Hypothesis', detail: 'sharpen into a testable hypothesis (founder-blind)' },
    { title: 'Disconfirmation', detail: 'expert debate → Disconfirmation Brief (interview questions, no kill)' },
    { title: 'Demand-detection', detail: 'niche-first real-demand mining (no size kill)' },
    { title: 'Checkpoint', detail: 'drop ONLY the 3 fatal flaws · rank by demand · cap top-K' },
    { title: 'Phase A', detail: 'sealed customer-discovery DESIGN pack for the top-K (drafts only)' },
    { title: 'Persist', detail: 'write the stateful ledger (demand + fit unfused) + shortlist' },
  ],
}

// ---------- helpers ----------
function slugify(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'untitled'
}
// CWD-bug fix: every file-writing agent must anchor paths at the git repo root regardless of the
// caller's (possibly polluted) working directory. v1 inherited a polluted CWD and wrote files
// nowhere, which then killed ideas by-default on "missing" files. We inline this directive into the
// prompt of every agent that reads or writes repo files.
const REPO_ANCHOR =
  'PATHS: resolve every path below against the GIT REPOSITORY ROOT, not your current working ' +
  'directory. First run `git rev-parse --show-toplevel` to find the repo root and treat all ' +
  'relative paths as relative to it; if that is unavailable, Glob for the nearest matching file ' +
  'under the repo. Never write to or read from the bare CWD — a polluted CWD silently sends writes ' +
  'nowhere. Create parent directories before writing.'

const LENS_MAP = {
  marketplace: ['peter-thiel-perspective', 'jeff-bezos-perspective', 'charlie-munger-perspective'],
  'e-commerce': ['jeff-bezos-perspective', 'charlie-munger-perspective', 'garry-tan-perspective'],
  'trading/fintech': ['nassim-taleb-perspective', 'charlie-munger-perspective', 'elon-musk-perspective'],
  trading: ['nassim-taleb-perspective', 'charlie-munger-perspective', 'elon-musk-perspective'],
  fintech: ['nassim-taleb-perspective', 'charlie-munger-perspective', 'elon-musk-perspective'],
  'ai-agent': ['peter-thiel-perspective', 'elon-musk-perspective', 'garry-tan-perspective'],
  'content/community': ['jeff-bezos-perspective', 'naval-ravikant-perspective', 'garry-tan-perspective'],
  content: ['jeff-bezos-perspective', 'naval-ravikant-perspective', 'garry-tan-perspective'],
  community: ['jeff-bezos-perspective', 'naval-ravikant-perspective', 'garry-tan-perspective'],
  'services/gig': ['tom-eisenmann-perspective', 'jeff-bezos-perspective', 'ben-horowitz-perspective'],
  services: ['tom-eisenmann-perspective', 'jeff-bezos-perspective', 'ben-horowitz-perspective'],
  'hardware-adjacent': ['elon-musk-perspective', 'nassim-taleb-perspective', 'tom-eisenmann-perspective'],
  'regulated-adjacent': ['nassim-taleb-perspective', 'charlie-munger-perspective', 'tom-eisenmann-perspective'],
  default: ['peter-thiel-perspective', 'charlie-munger-perspective', 'jeff-bezos-perspective'],
}
// Accept the canonical compound idea_types the seed-generator + lens-map emit (e.g. 'trading/fintech')
// AND split tokens, so disconfirmation routing can't silently fall through to default.
function normType(ideaType) { return String(ideaType || 'default').toLowerCase().trim() }
function lensesFor(ideaType) {
  const raw = normType(ideaType)
  if (LENS_MAP[raw]) return LENS_MAP[raw]
  for (const tok of raw.split('/')) if (LENS_MAP[tok]) return LENS_MAP[tok]
  return LENS_MAP.default
}
function lensTypeKnown(ideaType) {
  const raw = normType(ideaType)
  return !!LENS_MAP[raw] || raw.split('/').some(tok => LENS_MAP[tok])
}

// Stage indices for resurrect/appeal: a resurrected candidate re-enters at its kill stage. The only
// kill stages in v2 are fit-screen, hypothesis, and the checkpoint (which is post-research).
const STAGE_INDEX = { 'fit-screen': 0, hypothesis: 1, checkpoint: 2 }

// Map a 0-100 demand-signal word to a number so the checkpoint can rank by demand strength.
function demandStrengthNum(strength) {
  if (typeof strength === 'number' && isFinite(strength)) return strength
  switch (String(strength || '').toLowerCase().trim()) {
    case 'strong': return 80
    case 'moderate': return 55
    case 'thin': return 25
    case 'provably-negative': case 'provably negative': return 0
    default: return 30
  }
}

function mkCandidate(seed) {
  const id = seed.id || ('cand-' + slugify(seed.title || seed.problem))
  return {
    id, slug: id.replace(/^cand-/, ''),
    title: seed.title || seed.problem || id,
    seed: { problem: seed.problem || '', who: seed.who || '', why_now: seed.why_now || '' },
    idea_type: seed.idea_type || 'default',
    status: 'advancing', killed_at: null, rank: null, resumeFrom: -1,
    // Two unfused axes (spec §4): demand (blind, primary rank) + fit (aware, tiebreaker).
    demand: null, fit: null, fatal_flaw: null, fatal_evidence: null,
    stages: {
      fit_screen: null, hypothesis: null, disconfirmation: null,
      demand_detection: null, checkpoint: null, phase_a: null,
    },
  }
}

// ---------- schemas (match the v2 agent contracts exactly) ----------
const SEED_SCHEMA = { type: 'object', required: ['seeds'], properties: { seeds: { type: 'array', items: { type: 'object', required: ['title', 'problem', 'who', 'why_now', 'idea_type'], properties: { id: { type: 'string' }, title: { type: 'string' }, problem: { type: 'string' }, who: { type: 'string' }, why_now: { type: 'string' }, idea_type: { type: 'string' } } } } } }
const KCAP_SCHEMA = { type: 'object', required: ['k'], properties: { k: { type: 'integer' }, rationale: { type: 'string' } } }
const READER_SCHEMA = { type: 'object', required: ['run_history_found'], properties: { run_history_found: { type: 'boolean' }, latest_run_label: { type: 'string' }, settled: { type: 'array', items: { type: 'object', properties: { candidate_id: { type: 'string' }, status: { type: 'string' }, killed_at: { type: ['string', 'null'] }, score: { type: 'number' }, resurrect: { type: 'boolean' } } } }, resurrected: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, title: { type: 'string' }, seed: { type: 'object' }, idea_type: { type: 'string' }, killed_at: { type: ['string', 'null'] }, gates: { type: 'object' } } } } } }

// Fit-screen — FIT axis. verdict keep|drop; fit_score ALWAYS present; durable-impossible => drop.
const FMF_SCHEMA = { type: 'object', required: ['id', 'verdict', 'fit_score'], properties: { id: { type: 'string' }, verdict: { type: 'string', enum: ['keep', 'drop'] }, fit_score: { type: 'number' }, reasons: { type: 'string' }, hard_fail: { type: ['string', 'null'] } } }
// Hypothesis gate — testability. verdict advance|kill.
const SHARPEN_SCHEMA = { type: 'object', required: ['candidate_id', 'verdict'], properties: { candidate_id: { type: 'string' }, verdict: { type: 'string', enum: ['advance', 'kill'] }, score: { type: 'number' }, reason: { type: 'string' }, testable: { type: 'boolean' }, hypothesis: { type: 'object', properties: { who: { type: 'string' }, how_often: { type: 'string' }, how_severe: { type: 'string' }, status_quo: { type: 'string' }, sentence: { type: 'string' } } }, hypothesis_path: { type: ['string', 'null'] } } }
// Objection lens — one objection → falsifiable assumption + interview question. NO verdict, NO kill.
const OBJECTION_SCHEMA = { type: 'object', required: ['expert', 'objection', 'falsifiable_assumption', 'interview_question'], properties: { candidate_id: { type: 'string' }, expert: { type: 'string' }, objection: { type: 'string' }, falsifiable_assumption: { type: 'string' }, interview_question: { type: 'string' }, severity: { type: 'number' } } }
// Disconfirmation judge — compiles a BRIEF, not a verdict. May only FLAG a fatal flaw with evidence.
const JUDGE_SCHEMA = { type: 'object', required: ['candidate_id', 'brief', 'fatal_flaw'], properties: { candidate_id: { type: 'string' }, brief: { type: 'object', properties: { ranked_risks: { type: 'array', items: { type: 'object', properties: { rank: { type: 'number' }, expert: { type: 'string' }, objection: { type: 'string' }, status: { type: 'string' }, closed_by: { type: ['string', 'null'] }, risk: { type: 'number' } } } }, open_assumptions: { type: 'array', items: { type: 'object', properties: { assumption: { type: 'string' }, from_objection: { type: 'string' }, why_open: { type: 'string' } } } }, interview_questions: { type: 'array', items: { type: 'string' } } } }, fatal_flaw: { type: 'string', enum: ['illegal', 'demand_provably_negative', 'none'] }, fatal_evidence: { type: ['string', 'null'] }, risk_score: { type: 'number' }, coverage_gap: { type: ['string', 'null'] }, brief_path: { type: ['string', 'null'] } } }
// Demand-detection — niche-first signal. NO verdict, NO size kill; may FLAG fatal flaw ② or ③.
const DEMAND_SCHEMA = { type: 'object', required: ['candidate_id', 'reachable', 'demand_signal_strength'], properties: { candidate_id: { type: 'string' }, reachable: { type: 'boolean' }, demand_signal_strength: { type: 'string' }, demand_provably_negative: { type: 'boolean' }, reachable_niche: { type: 'string' }, where_they_congregate: { type: 'string' }, unsolved_complaints: { type: 'array', items: { type: 'string' } }, signals: { type: 'array', items: { type: 'string' } }, market_path: { type: ['string', 'null'] }, evidence: { type: ['string', 'null'] } } }
// Phase A — cd-design. Soft gate: kills ONLY on no reachable audience (flaw ③).
const CD_SCHEMA = { type: 'object', required: ['candidate_id', 'verdict', 'reachable'], properties: { candidate_id: { type: 'string' }, verdict: { type: 'string', enum: ['advance', 'kill'] }, reachable: { type: 'boolean' }, runpack_path: { type: ['string', 'null'] }, reason: { type: 'string' } } }
const WRITER_SCHEMA = { type: 'object', required: ['run_label'], properties: { run_label: { type: 'string' }, ledger_path: { type: 'string' }, ledger_json_path: { type: 'string' }, shortlist_path: { type: 'string' }, shortlist: { type: 'array', items: { type: 'string' } } } }

// ---------- run ----------
// Accept args whether the harness forwards them as a parsed object OR a JSON string
// (the Workflow `args` field is typed `any`, so some harnesses pass it through verbatim as text).
let a = args || {}
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { a = {} } }
const thesisSlug = slugify(a.thesis || (Array.isArray(a.seeds) ? 'founder-seeds' : 'idea-funnel'))
const coworkShare = a.coworkSharePath || null

// Setup — prior ledger + cap K
phase('Setup')
const prior = await agent(
  `${REPO_ANCHOR}\n\nRead prior funnel ledgers under docs/ideas-stages/_funnel-runs/. Resurrect IDs (treat as NOT settled, and return their FULL prior records so they can re-enter the funnel): ${JSON.stringify(a.resurrect || [])}. Return: (1) settled — lightweight {candidate_id, status, killed_at, score, resurrect} for every prior candidate; (2) resurrected — the FULL candidate object {id, title, seed, idea_type, killed_at, gates} from the latest ledger.json for each resurrect id you find. Note: a 'queued-alive' candidate is NOT killed — report it as settled with its status so it is carried forward and re-considered against the cap.`,
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
const resurrectedFull = (prior && Array.isArray(prior.resurrected)) ? prior.resurrected : []

// Cap K — default 1 (spec §11). Only derive from the founder profile when not explicitly set.
let kVal = a.k
let capacityRationale = a.k ? `explicit k=${a.k}` : ''
if (!kVal) {
  const cap = await agent(
    `${REPO_ANCHOR}\n\nRead docs/founder-profile.md. From time-commitment (available hours/cadence), founding-team status (day-one people who can run a campaign), and capacity to run customer-discovery campaigns, return the number of customer-discovery campaigns this founder can run well AT ONCE — capacity scales with available hours and day-one headcount; cap at 5; when capacity is unknown or undeclared, default conservatively to 1. Do NOT read money/runway into this — capacity is about hours and headcount only. Output {k, rationale}.`,
    { agentType: undefined, schema: KCAP_SCHEMA, phase: 'Setup', label: 'capacity', model: 'haiku' }
  )
  kVal = cap && cap.k ? cap.k : 1
  capacityRationale = (cap && cap.rationale) || 'defaulted to 1 (conservative default when capacity is unknown)'
}
log(`Cap K = ${kVal} (${capacityRationale})`)

// Generate — founder-BLIND seeds (spec §5.1: NO founder profile in the seed-gen call)
let seeds = []
if (Array.isArray(a.seeds) && a.seeds.length) {
  seeds = a.seeds
  log(`Ingesting ${seeds.length} founder-supplied seeds`)
} else if (a.thesis) {
  phase('Generate')
  await agent(
    `${REPO_ANCHOR}\n\nGrounding sweep for thesis: "${a.thesis}". Research real trends, demand, and unsolved pains across facets (trends/why-now, existing solutions, demand-pain, adjacent markets) and WRITE a grounding doc to docs/idea-exploration/${thesisSlug}/research/grounding.md. Return the path.`,
    { agentType: 'startup-idea-researcher', phase: 'Generate', label: 'grounding' }
  )
  const gen = await agent(
    `${REPO_ANCHOR}\n\nExpand thesis "${a.thesis}" into ${a.n || 10} thin Candidate seeds, WIDE (no narrowing). Read the grounding doc at docs/idea-exploration/${thesisSlug}/research/grounding.md. Generation is FOUNDER-BLIND: do NOT read docs/founder-profile.md or any founder background, and never bend, narrow, or bias seeds toward a founder's market, skills, interests, goals, capital, or geography — drive every seed from the thesis + real demand in the grounding doc only. Go wide across different problems, audiences, and idea_types. Tag each seed with an accurate idea_type (drives downstream lens routing).`,
    { agentType: 'seed-generator', schema: SEED_SCHEMA, phase: 'Generate', label: 'seed-gen' }
  )
  seeds = (gen && gen.seeds) || []
  log(`Generated ${seeds.length} seeds (founder-blind)`)
} else {
  return { error: 'Provide args.thesis (generate mode) or args.seeds (ingest mode).' }
}

const resurrectSet = new Set(a.resurrect || [])
const candidates = seeds.map(mkCandidate).filter(c => !settledKilled.has(c.id) || resurrectSet.has(c.id))

// Resurrect/appeal: re-enter prior-killed candidates AT their kill stage, reconstructing any that
// aren't in the current seed set so a pure appeal isn't a silent no-op.
const byId = new Map(candidates.map(c => [c.id, c]))
for (const rc of resurrectedFull) {
  if (!rc || !rc.id) continue
  const resumeFrom = STAGE_INDEX[rc.killed_at] != null ? STAGE_INDEX[rc.killed_at] : 0
  if (byId.has(rc.id)) {
    const c = byId.get(rc.id)
    if (rc.gates) c.stages = { ...c.stages, ...rc.gates }
    c.status = 'advancing'; c.killed_at = null; c.resumeFrom = resumeFrom
  } else {
    const c = mkCandidate({ id: rc.id, title: rc.title, problem: rc.seed && rc.seed.problem, who: rc.seed && rc.seed.who, why_now: rc.seed && rc.seed.why_now, idea_type: rc.idea_type })
    if (rc.gates) c.stages = { ...c.stages, ...rc.gates }
    c.resumeFrom = resumeFrom
    candidates.push(c); byId.set(c.id, c)
  }
}
for (const rid of resurrectSet) {
  if (!byId.has(rid)) log(`⚠ resurrect id not found in seeds or prior ledger — ignored: ${rid}`)
}
log(`${candidates.length} candidates enter the funnel (${settledKilled.size} prior kills skipped; ${resurrectedFull.length} resurrected)`)

// ---------- desk stages (pipelined; each passes the candidate through, never null) ----------
// Spec §3: the ONLY desk kills are durable-impossible fit (fit-screen), untestable (hypothesis), and
// the 3 fatal flaws at the checkpoint. Disconfirmation and demand-detection NEVER kill — they only
// produce a Brief / a demand signal and may FLAG a fatal flaw for the checkpoint to adjudicate.

async function fitScreen(c) {
  if (c.status === 'killed') return c
  if (c.resumeFrom > 0) return c // resurrected past fit: keep prior verdict
  const v = await agent(
    `${REPO_ANCHOR}\n\nFit-screen (FIT axis). Candidate id=${c.id}, seed=${JSON.stringify(c.seed)}, title=${JSON.stringify(c.title)}. Read docs/founder-profile.md (and docs/founder-dossier.md only if a capability factor is ambiguous) and .claude/skills/idea-funnel/references/gate-rubrics.md (Fit-screen). Assess DURABLE capability/legal/geo/language fit and buildable surface ONLY. IGNORE money/time/runway entirely. DROP only on a durable-impossible mismatch (a market/language the founder cannot serve, a licence/regulated activity they are structurally barred from, or hardware/heavy-regulated outside the buildable surface); otherwise KEEP. ALWAYS emit fit_score 0-100 (on keep and on drop) for transparent ranking.`,
    { agentType: 'fmf-screen', schema: FMF_SCHEMA, phase: 'Fit-screen', label: `fit:${c.id}`, model: 'haiku' }
  )
  c.stages.fit_screen = v
  if (v && typeof v.fit_score === 'number') c.fit = { score: v.fit_score, reasons: v.reasons || '', hard_fail: v.hard_fail || null }
  if (!v || v.verdict === 'drop') {
    c.status = 'killed'; c.killed_at = 'fit-screen'
    c.fatal_flaw = (v && v.hard_fail) || 'durable-impossible founder mismatch'
    c.fatal_evidence = (v && v.reasons) || null
    log(`✖ ${c.id} killed at fit-screen — ${c.fatal_flaw}`)
  }
  return c
}

async function hypothesisGate(c) {
  if (c.status === 'killed') return c
  if (c.resumeFrom > 1) return c // resurrected past hypothesis: keep prior verdict
  const ns = `docs/ideas-stages/${c.slug}/`
  const v = await agent(
    `${REPO_ANCHOR}\n\nHypothesis gate (testability). FOUNDER-BLIND — do NOT read the founder profile. Candidate id=${c.id}, seed=${JSON.stringify(c.seed)}, title=${JSON.stringify(c.title)}. Output namespace ${ns}; on advance, write hypothesis.md there. Read .claude/skills/idea-funnel/references/gate-rubrics.md (Hypothesis gate). Sharpen to a testable hypothesis (who · how-often · how-severe · status-quo) in ONE pass. KILL only if it cannot be made testable after that pass — never on weak market, no moat, crowded space, or "might not pay". When on the fence, advance.`,
    { agentType: 'sharpen-gate', schema: SHARPEN_SCHEMA, phase: 'Hypothesis', label: `hypo:${c.id}`, model: 'haiku' }
  )
  c.stages.hypothesis = v
  if (!v || v.verdict === 'kill') {
    c.status = 'killed'; c.killed_at = 'hypothesis'
    c.fatal_flaw = 'untestable'
    c.fatal_evidence = (v && v.reason) || null
    log(`✖ ${c.id} killed at hypothesis — untestable (${(v && v.reason) || 'no testable hypothesis'})`)
  }
  return c
}

// Disconfirmation → Disconfirmation Brief (NO kill) + Demand-detection (NO size kill), in one stage.
async function disconfirmAndDemand(c) {
  if (c.status === 'killed') return c
  const ns = `docs/ideas-stages/${c.slug}/`
  const lenses = lensesFor(c.idea_type)
  if (!lensTypeKnown(c.idea_type)) log(`⚠ disconfirmation: unknown idea_type "${c.idea_type}" for ${c.id} — used default lenses (possible coverage gap)`)
  const hypo = c.stages.hypothesis && c.stages.hypothesis.hypothesis
  const hypoHint = hypo ? '' : ` (hypothesis not in memory — read it from ${ns}hypothesis.md)` // resurrect safety

  // Expert objection lenses (parallel) — each fires ONE objection → falsifiable assumption +
  // interview question. They never rebut, never kill.
  const objections = await parallel(lenses.map(slug => () => agent(
    `${REPO_ANCHOR}\n\nObjection lens — FOUNDER-BLIND. Channel ${slug} against candidate id=${c.id}: seed=${JSON.stringify(c.seed)}, hypothesis=${JSON.stringify(hypo)}${hypoHint}. Read its lens-card in .claude/skills/idea-funnel/references/expert-lens-map.md. Fire ONE strongest disconfirming objection, then CONVERT it into (a) a falsifiable_assumption and (b) one past-behaviour / Mom-Test interview_question a real user could answer. Do NOT rebut, do NOT render a verdict, NOTHING you raise kills the idea. Rate severity 0-100.`,
    { agentType: 'objection-lens', schema: OBJECTION_SCHEMA, phase: 'Disconfirmation', label: `obj:${c.id}:${slug.replace('-perspective', '')}` }
  )))

  // Evidence sweep (parallel): competitor-steelman (context, no kill) + demand-detection (niche-first).
  let demand = null
  await parallel([
    () => agent(`${REPO_ANCHOR}\n\nCompetitor steelman for candidate id=${c.id} (${JSON.stringify(c.title)}, ${JSON.stringify(c.seed)}, hypothesis=${JSON.stringify(hypo)}). Argue the strongest case the most dangerous incumbent WINS, then convert each load-bearing point into a falsifiable assumption + interview question. Map competitors as CONTEXT, NOT a kill — render NO verdict. Write the steelman provenance to ${ns}market-research/competitor-steelman.md.`,
      { agentType: 'competitor-steelman', phase: 'Disconfirmation', label: `steel:${c.id}` }),
    async () => {
      demand = await agent(`${REPO_ANCHOR}\n\nDemand-detection (niche-first, FOUNDER-BLIND) for candidate id=${c.id} (hypothesis=${JSON.stringify(hypo)}${hypoHint}). Mine existing PUBLIC conversations (Reddit/X/HN/forums/reviews) for real-user language + unsolved complaints: who already PAYS / COMPLAINS / HACKS a workaround, however small the niche. Map competitors as CONTEXT, not a kill. SIZE NEVER KILLS. Only FLAG fatal flaw ② demand_provably_negative (with hard, corroborated evidence) or ③ no reachable audience. WRITE ${ns}market-research.md. Return {candidate_id, reachable, demand_signal_strength (strong|moderate|thin|provably-negative), demand_provably_negative, reachable_niche, where_they_congregate, unsolved_complaints, signals, market_path, evidence}.`,
        { agentType: 'market-researcher', schema: DEMAND_SCHEMA, phase: 'Demand-detection', label: `demand:${c.id}` })
    },
  ])

  // Disconfirmation JUDGE — compiles the BRIEF (no verdict); may only FLAG a fatal flaw with evidence.
  const judge = await agent(
    `${REPO_ANCHOR}\n\nDisconfirmation judge (v2) — compile a Disconfirmation BRIEF, NOT a verdict. FOUNDER-BLIND. Candidate id=${c.id}, idea_type=${c.idea_type}. Objections (from lenses): ${JSON.stringify((objections || []).filter(Boolean))}. Read the steelman at ${ns}market-research/competitor-steelman.md and the demand evidence at ${ns}market-research.md. Read .claude/skills/idea-funnel/references/gate-rubrics.md (Disconfirmation). Rank objections by risk; convert each subjective one into an OPEN falsifiable assumption + interview question. Close an objection ONLY when a hard, checkable FACT settles it (legality / technical feasibility) — everything subjective (demand, WTP, behaviour, moat, competition, size) stays OPEN. You do NOT emit advance/kill. You may ONLY FLAG fatal_flaw "illegal" or "demand_provably_negative" with cited objective evidence; otherwise fatal_flaw="none". WRITE the brief to ${ns}disconfirmation-brief.md and return brief_path. If a domain-specific lens would have been more decisive than ${JSON.stringify(lenses)}, name it as coverage_gap.`,
    { agentType: 'disconfirmation-judge', schema: JUDGE_SCHEMA, phase: 'Disconfirmation', label: `judge:${c.id}` }
  )

  c.stages.disconfirmation = judge || { fatal_flaw: 'none' }
  c.stages.demand_detection = demand || null
  // Record the demand axis (blind, primary rank key).
  if (demand) {
    c.demand = {
      strength: demandStrengthNum(demand.demand_signal_strength),
      strength_label: demand.demand_signal_strength,
      reachable: demand.reachable !== false,
      reachable_niche: demand.reachable_niche || '',
      where_they_congregate: demand.where_they_congregate || '',
      unsolved_complaints: demand.unsolved_complaints || [],
      signals: demand.signals || [],
    }
  }
  // NO kill here. Carry any FLAGGED fatal flaw forward to the checkpoint, where it is adjudicated.
  return c
}

const processed = await pipeline(candidates, fitScreen, hypothesisGate, disconfirmAndDemand)

// ---------- CHECKPOINT (barrier) — the ONLY post-research kill: the 3 fatal flaws ----------
// Then rank survivors by DEMAND strength (primary), founder-fit as a separate tiebreaker (never
// fused), and cap top-K. Sub-cap survivors become 'queued-alive' (resurrectable), NEVER killed.
phase('Checkpoint')
for (const c of processed) {
  if (!c || c.status === 'killed') continue // already killed at fit-screen or hypothesis

  // Adjudicate the 3 fatal flaws with cited evidence (spec §3). Nothing else kills.
  let fatal = null, evidence = null
  const disc = c.stages.disconfirmation
  const dem = c.stages.demand_detection
  // ① illegal/impossible OR ② demand provably negative — flagged by the disconfirmation judge.
  if (disc && disc.fatal_flaw && disc.fatal_flaw !== 'none' && disc.fatal_evidence) {
    fatal = disc.fatal_flaw === 'illegal' ? 'illegal/impossible' : 'demand provably negative'
    evidence = disc.fatal_evidence
  }
  // ② demand provably negative — also surfaced by demand-detection (with corroborated evidence).
  if (!fatal && dem && dem.demand_provably_negative === true && dem.evidence) {
    fatal = 'demand provably negative'; evidence = dem.evidence
  }
  // ③ no reachable audience at all.
  if (!fatal && dem && dem.reachable === false) {
    fatal = 'no reachable audience'; evidence = dem.evidence || 'demand-detection found no reachable community/channel/list'
  }

  if (fatal) {
    c.status = 'killed'; c.killed_at = 'checkpoint'
    c.fatal_flaw = fatal; c.fatal_evidence = evidence
    c.stages.checkpoint = { verdict: 'killed', fatal_flaw: fatal, evidence, reason: `fatal flaw: ${fatal}` }
    log(`✖ ${c.id} killed at checkpoint — fatal flaw: ${fatal}`)
  } else {
    // Survives the desk. Default to queued-alive; the cap below promotes the top-K to shortlisted.
    c.status = 'queued-alive'
    c.stages.checkpoint = { verdict: 'queued-alive', fatal_flaw: null, reason: 'cleared the desk (no fatal flaw)' }
  }
}

// Rank survivors by demand strength PRIMARY; founder-fit is a SEPARATE tiebreaker (never blended).
const survivors = processed.filter(c => c && c.status !== 'killed')
survivors.sort((x, y) => {
  const dx = (x.demand && x.demand.strength) || 0
  const dy = (y.demand && y.demand.strength) || 0
  if (dy !== dx) return dy - dx
  const fx = (x.fit && x.fit.score) || 0 // tiebreaker only
  const fy = (y.fit && y.fit.score) || 0
  return fy - fx
})
survivors.forEach((c, i) => {
  c.rank = i + 1
  c.status = i < kVal ? 'shortlisted' : 'queued-alive'
  if (c.stages.checkpoint) c.stages.checkpoint.rank = c.rank
})
const shortlisted = survivors.filter(c => c.status === 'shortlisted')
log(`${survivors.length} cleared the desk; ${shortlisted.length} shortlisted (cap K=${kVal}); ${survivors.length - shortlisted.length} queued-alive`)

// ---------- Phase A — sealed customer-discovery DESIGN on the shortlist ----------
if (shortlisted.length) {
  phase('Phase A')
  await parallel(shortlisted.map(c => () => (async () => {
    const ns = `docs/ideas-stages/${c.slug}/`
    const out = coworkShare ? `${coworkShare}/${c.slug}-cowork-runpack.md` : `${ns}customer-discovery/cowork-runpack.md`
    const disc = c.stages.disconfirmation
    const openAssumptions = (disc && disc.brief && disc.brief.open_assumptions) || []
    const interviewQs = (disc && disc.brief && disc.brief.interview_questions) || []
    const v = await agent(
      `${REPO_ANCHOR}\n\nCustomer-discovery DESIGN (Phase A) for shortlisted survivor id=${c.id}, title=${JSON.stringify(c.title)}. Read ${ns}hypothesis.md, ${ns}disconfirmation-brief.md, and ${ns}market-research.md. Build the SEALED, self-contained run-pack: (1) target profile, (2) reachability map (named subreddits/X hashtags/forums/Discord/Slack/LinkedIn groups), (3) WARM LIST ★ of real people who already publicly complained — each {link · their words · drafted contextual reply/DM} (warm-first / Option A), (4) Mom-Test interview guide built FROM the open assumptions [${JSON.stringify(openAssumptions)}] / interview questions [${JSON.stringify(interviewQs)}], (5) secondary cold-email drafts, (6) tracking sheet (prospect · channel · status · follow-up · done). Write the SEALED pack to ${out}. Soft-kill ONLY if there is no reachable audience at all (flaw ③); never re-judge merit. NEVER send or post anything — drafts only.`,
      { agentType: 'cd-design-gate', schema: CD_SCHEMA, phase: 'Phase A', label: `cd:${c.id}` }
    )
    c.stages.phase_a = v || null
    if (v && v.verdict === 'kill') {
      // No reachable audience after all (flaw ③): drop from the shortlist, keep alive (not dead).
      c.status = 'queued-alive'; c.rank = null
      log(`↩ ${c.id} dropped from shortlist at Phase A — ${v.reason || 'no reachable audience'} (queued alive)`)
    }
    return c
  })()))
}

// ---------- Persist (ledger: demand + fit as SEPARATE unfused columns; never silently empty) ----------
phase('Persist')
// Dedupe: a candidate processed this run (incl. a resurrected one) overrides its prior-settled record.
const priorOnly = priorSettled.filter(s => !processed.some(c => c.id === s.candidate_id))
const writer = await agent(
  `${REPO_ANCHOR}\n\nPersist this funnel run. Thesis slug=${thesisSlug}. n=${a.n || (Array.isArray(a.seeds) ? a.seeds.length : 10)}. K=${kVal} (capacity: ${capacityRationale}). Follow .claude/skills/idea-funnel/references/ledger-schema.md exactly. Write ledger.json (machine state), ledger.md (the board), and shortlist.md. CRITICAL: record demand-strength and founder-fit as TWO SEPARATE, UNFUSED columns — demand is the primary rank key, fit is shown alongside as a tiebreaker; never blend them into one number. Persist EVERY candidate including killed ones with their killed_at + cited fatal_flaw/evidence (the ledger is the appeal surface — no silent kills). Sub-cap survivors are status 'queued-alive' (resurrectable), NOT killed. The board is NEVER empty unless literally every seed hit a fatal flaw. Dedupe by id — a candidate in "Results" overrides any prior record.\nResults (this run): ${JSON.stringify(processed)}\nPrior-only settled (not in this run; carry into the board): ${JSON.stringify(priorOnly)}`,
  { agentType: 'ledger-writer', schema: WRITER_SCHEMA, phase: 'Persist', label: 'ledger-writer' }
)

const counts = {
  entered: candidates.length,
  killed_fit_screen: processed.filter(c => c.killed_at === 'fit-screen').length,
  killed_hypothesis: processed.filter(c => c.killed_at === 'hypothesis').length,
  killed_checkpoint: processed.filter(c => c.killed_at === 'checkpoint').length,
  cleared_desk: survivors.length,
  shortlisted: survivors.filter(c => c.status === 'shortlisted').length,
  queued_alive: survivors.filter(c => c.status === 'queued-alive').length,
}
return {
  run_label: writer && writer.run_label,
  ledger: writer && writer.ledger_path,
  shortlist_doc: writer && writer.shortlist_path,
  shortlist: writer && writer.shortlist,
  counts,
}
