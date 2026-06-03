# Soriza Startup Layer — Idea Stage

The Idea Stage is an interview-driven pipeline that takes a founder from raw research to a
validated solution concept. This glossary fixes the vocabulary for the **Idea-Stage Validator** —
a proposed orchestrator that runs many ideas through that pipeline as an automated distillation
funnel. It is a glossary only; mechanics and decisions live in prose, ADRs, and the skills.

## Language

**Idea-Stage Validator**:
The proposed orchestrator that runs many candidate ideas through the existing six-stage Idea
Stage pipeline automatically, killing weak ones at each gate and advancing only survivors. The
"VC incubator" engine.
_Avoid_: pipeline (means the stages themselves), workflow (overloaded — see below).

**Candidate**:
One startup idea moving through the Validator. Has a status at every gate (advancing / killed)
and an audit trail of why.
_Avoid_: idea (fine informally, but a Candidate is specifically one tracked unit in a funnel run).

**Funnel run**:
A single execution of the Validator over a batch of Candidates (e.g. 100 in → a handful out).
_Avoid_: loop (the founder's word for the current manual cycle — see Flagged ambiguities).

**Candidate seed**:
The thin, normalized entry form of a Candidate — problem · who · why-now, one paragraph, **no deep
research**. Everything entering the funnel (a founder-supplied list of any length, or thesis output)
is normalized to this. Deep research is deferred down-funnel to survivors.

**Seed-generator**:
A NEW lightweight generator that expands a thesis into N Candidate seeds **wide, without narrowing**.
In funnel mode the funnel's gates do the narrowing — not the generator. Distinct from the standalone
`/generate-ideas` skill, which narrows to 1–3 and is too research-heavy for the top of a funnel.

**Founder-Market-Fit gate** (Gate 0):
The first and cheapest kill gate. Screens each Candidate seed against `docs/founder-profile.md` —
serviceable geography, skills/unfair advantage, **low** risk/regulatory appetite, part-time capacity,
solo/low-capital — and kills founder-mismatched ideas before any research spend.

**Desk Funnel**:
The automated portion of the Validator — a single dynamic Workflow that runs the cheap, no-real-world
desk stages (generate → sharpen → disconfirmation pass → customer-discovery DESIGN) over a batch and
terminates at the Shortlist. Everything past it (SEND, full debate, interviews) is human + Cowork,
outside any workflow. See [ADR-0002](docs/adr/0002-validator-runtime-is-a-dynamic-workflow.md).

**Gate-subagent**:
A headless subagent (`.claude/agents/*.md`) the Desk Funnel calls as one stage; it emits a
schema-validated advance/kill verdict. Built/verified with prompt-architect. Distinct from the
**interactive skills**, which stay the human-facing path and are not called by the funnel.

**Launcher command**:
The saved Workflow command (`/idea-funnel`) the founder runs to start a Funnel run; the batch is
passed via the Workflow `args` global.

**Kill gate**:
A point in the pipeline where a Candidate is judged and either advances or is killed. Each of the
six stages ends in a gate. Distinct from a build step — a gate's only job is the advance/kill call.

**Judgment gate** vs **Irreversible gate**:
A **judgment gate** makes an advance/kill call from information already in hand (a rubric, pulled
evidence) — AI-decidable, automatable. An **irreversible gate** requires an outward, hard-to-undo
real-world action (sending cold outreach to real strangers) — kept human-approved by design. The
Validator automates judgment gates and stops at the one irreversible gate (customer-discovery SEND).

**Objection screen** (batch mode of pressure-test):
The funnel's cheap, automated form of pressure-test. Runs only the experts' opening disconfirming
objections (plus the competitor-steelman), then checks each against external evidence gathered the
same pass. Kills a Candidate when its strongest objection stands **unrebutted by evidence**. No
agent-fabricated founder voice, no multi-round debate. Contrast the **full debate**: the real
4-round, multi-persona panel with the founder defending — reserved for survivors only, run by a human.
_Avoid_: "the panel" (ambiguous — say objection screen for batch, full debate for survivors).

**Disconfirmation pass** (Gate 2 — the one expensive "evidence tier"):
The merged funnel gate where pressure-test's objection generation AND market sizing run as one
coupled research sweep: personas + competitor-steelman produce objections; one research pass produces
both the evidence that adjudicates them AND the TAM/SAM/SOM + buyer map + trend read. The single kill
call weighs all of it — kill if the strongest objection stands unrebutted **or** the market is too
small / closed / facing a timing headwind. One sweep, no double-paying for overlapping web research.

**Cut policy — bar-to-kill + cap-to-advance**:
At every cheap desk gate, an **absolute bar** kills any Candidate below the gate's threshold
(survivor count floats). At the **funnel exit** into the expensive human stage, a **top-K cap**
limits how many survivors advance (protects scarce human-interview capacity). Two rules, two points.
The cap's **default K is derived from the founder profile's capacity** (time commitment, founding-team
size, risk appetite) — not a constant — and is overridable per run via `args`. So the profile is
load-bearing at both funnel ends: it filters ideas IN (Founder-Market-Fit gate) and meters survivors OUT (the cap).

**Grounding sweep**:
A single shared web-research pass run ONCE per batch (via `startup-idea-researcher`) before the
seed-generator — real trends, demands, unsolved pains — so generated seeds are grounded in actual
demand, not invented. Amortized across all N seeds, so cheap per Candidate. Distinct from per-Candidate
deep research, which stays deferred to the Disconfirmation pass (Gate 2) on survivors only.

**Objection lens**:
One distilled expert (`*-perspective` skill) or the competitor-steelman acting in funnel mode as a
generator of a single characteristic disconfirming objection — NOT a debater. The experts prosecute;
external evidence judges; no fabricated founder defense (see [ADR-0001](docs/adr/0001-funnel-kills-on-evidence-not-debate.md)).
The full multi-round debate, where the founder defends, is preserved for survivors only. Per
Candidate, Gate 2 selects the **3–4 domain-matched lenses + competitor-steelman** via an
idea-type → expert-lens map; each fires ONE evidence-checked objection.

**Coverage gap** (closed roster + logged gaps):
Gate 2 draws lenses from a **closed roster** of distilled `*-perspective` experts. When the ideal lens
for a Candidate isn't distilled, the selector names it as **ideal-but-missing** and logs it to the
ledger's coverage-gap field — the funnel proceeds with the best available lenses, never auto-minting
mid-run. Minting a missing expert (via `nuwa-skill`) + adding its lens-card is **roster curation** —
a deliberate human step BETWEEN runs, never a funnel-runtime dependency. See
[ADR-0004](docs/adr/0004-gate2-uses-a-closed-expert-roster-gaps-are-logged.md).

**Funnel ledger**:
The run's scoreboard AND its cross-run memory — a **stateful, persisted** file keyed by stable
**Candidate ID** (`docs/ideas-stages/_funnel-runs/<run>/ledger.md`). One row per Candidate, a column
per gate, each cell = advanced/killed + one-line reason + score. A re-run reads it: killed Candidates
stay killed, sub-cap survivors stay queued, and a re-run promotes the next-ranked survivor without
re-running settled desk gates. **Appeal/resurrect** = flip a Candidate's status in the ledger and
re-run; it re-enters at the gate that killed it. Written by the session after the Workflow returns its
data (a workflow script can't write files itself).

**Shortlist**:
The capped set of survivors at the funnel exit (≤ K) presented to the founder for approval before
the irreversible SEND gate. The funnel proposes; the founder disposes.

**Stage → artifact map** (the existing pipeline this wraps):
generate-ideas → `idea-exploration/<theme>/ideas.md`; sharpen-hypothesis → `hypothesis.md`
(can refuse); pressure-test → `pressure-test.md`; market-research → `market-research.md`;
customer-discovery → `customer-discovery.md` (DESIGN automatable / SEND gated); solution-design →
`solution-design.md`. All per-idea files live under `docs/ideas-stages/<slug>/`.

**Cowork share**:
The Windows-side local folder (`C:\dev\soriza-cowork\`, seen from WSL2 as `/mnt/c/dev/soriza-cowork/`)
that bridges the repo and Cowork for the customer-discovery handoff — run-pack out, interview notes +
tracking sheet back. Holds small handoff files only; the repo stays native in WSL2. See
[ADR-0003](docs/adr/0003-cowork-repo-bridge-is-a-windows-side-shared-folder.md). Cowork cannot reach
the WSL2 repo directly (no UNC / network-share access), so this is a Windows-local folder, not the
WSL2 path; the run-pack stays sealed regardless. Drive remains a connector, not the file bridge.

## Flagged ambiguities

- **"The loop"** — the founder uses this for the current *manual, one-idea-at-a-time* cycle that
  wastes time. The Validator's batch execution is a **Funnel run**, not "the loop." Don't reuse
  "loop" for the new system.
- **"Valid / runnable idea"** — to be sharpened. Provisionally: a Candidate is *runnable* when it
  has enough of a seed to enter sharpen-hypothesis; it is *valid* only relative to a specific gate's
  kill criteria (testable-enough, evidence-supported, etc.). Not a single global property.
