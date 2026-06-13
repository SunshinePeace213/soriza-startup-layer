---
name: startup-brief
description: |
  Idea-Stage step 8 — crystallize the final solution concept, drift-audit it against the problem
  discovery VALIDATED (not the one assumed), blind red-team it, run an Eisenmann premortem, lock the
  G9 PoC kill-criteria, and stamp GO / NO-GO. Use for "startup brief", "am I ready to build",
  "go / no-go", "design my solution", "drift audit".
when_to_use: |
  Gate: runs at current_step 8 (after market-sizing; a customer-discovery.md Discovery Read is the
  floor). This is the main build/no-build stamp — proceeding past a tripped/overridden kill-criterion
  is a stamped override. Not sizing (/market-sizing), not editing the claim (/sharpen-hypothesis), and
  not building the PoC (/build-poc consumes the locked criteria-g9.yaml this step writes).
argument-hint: "[slug]"
disable-model-invocation: true
allowed-tools: Read, Glob, Write, Bash, Agent, AskUserQuestion
effort: high
---

# Startup Brief — crystallize, challenge, and stamp GO / NO-GO

Step 8 of the **Idea Stage**. Takes the validated evidence for one idea and turns it into a **designed,
challenged, premortem'd, stamped** solution concept. It merges the retired `solution-design` (concept +
drift audit + blind red-team + ranked assumptions) and `idea-stage-exit` (the deliberate exit decision)
into one brief. The load-bearing question — the Playbook's reality checkpoint — is the **drift audit**:
does the design serve the problem *discovery revealed*, not the one the founder *assumed going in*? This
founder's documented failure mode IS drift (*concede the diagnosis, keep the prescription*), so the
audit, the blind red-team, and the on-record GO/NO-GO all exist to stop it.

- **Input:** `ideas/<slug>/` upstream chain — `customer-discovery.md` (required floor) + `hypothesis.md`,
  `kill-scan.md`, `pressure-report-alpha.md`, `pressure-report-beta.md`, `market-sizing.md` (folded if
  present) + `evidence-ledger.jsonl` + `docs/founder-profile.md`.
- **Output:** `ideas/<slug>/startup-brief.md` (the GO/NO-GO card) + provenance under `startup-brief/` +
  a locked `gates/criteria-g9.yaml`.
- **Worker:** the `solution-red-team` subagent (`.claude/agents/`), dispatched BLIND.

## When this applies

- `STATE.md` shows `current_step: 8`; "startup brief", "am I ready to build", "go/no-go", "drift audit",
  "design my solution", "what's next" after market-sizing.
- **Entry guards:** no `customer-discovery.md` → point to `/customer-discovery-synthesis`. `current_step
  < 8` / no `market-sizing.md` → point to the missing step (`/market-sizing` for step 7). Write nothing.

## Gotchas

- **The drift audit is the point — never let "concede the diagnosis, keep the prescription" through.**
  Measure the concept against the **reconstructed** validated baseline (hypothesis + unapplied deltas
  from the script), never the stale `hypothesis.md`. A `❌ still solving the old problem` row is a
  finding, not a nuisance to soften. The validator requires the drift-audit table + a verdict marker;
  honesty is the founder's signature.
- **G8 is the main build/no-build stamp.** Unlike α/β (the desk never kills), this is a deliberate
  GO/NO-GO the founder signs. Proceeding past a tripped/overridden kill-criterion (e.g. a KILL Discovery
  Read overridden at G6) is an explicit, stamped Override line. Never silently design a corpse.
- **The `solution-red-team` MUST run in a separate context, dispatched BLIND.** It gets the validation
  docs + the founder-confirmed concept wedge but NOT your draft card — blind by construction means it
  generates its own assumptions and drift suspicions, so the reconcile catches what the draft missed.
  An agent grading its own design rationalizes it. (4.8 degrade: if no `Agent` tool, run it as an
  adversarial fresh-framing second pass and tell the founder it is weaker without context isolation.)
- **Lock-ahead is enforced.** `advance_gate.py` refuses G8 unless `gates/criteria-g9.yaml` exists and is
  locked — the PoC kill-criteria are pre-registered before the build/no-build stamp, and never softened
  after the PoC runs. Lock them in step 7 of the workflow, before closing G8.
- **Never edit `hypothesis.md`.** This step *flags* hypothesis updates and routes to
  `/sharpen-hypothesis`; folding is that skill's exclusive right. Append `startup-brief` to STATE's
  `deltas_pending` if the brief flagged any.
- **No persona panel here.** The `*-perspective` advisors live in `/pressure-test`. You may run ONE
  named perspective as an a-la-carte design lens if the founder asks (e.g. `/steve-jobs-perspective` for
  "is this focused?") — never reconstruct the panel. The premortem uses Eisenmann's six patterns as a
  checklist (`references/premortem.md`), not the live persona.
- **Size never kills — already done.** Sizing was step 7; don't re-derive TAM or re-interview. Web is
  for *light* verification only, and that's the red-team worker's job, not the orchestrator's.

## Workflow

**Goal:** `ideas/<slug>/startup-brief.md` (GO/NO-GO) + locked `gates/criteria-g9.yaml` → the founder
reads every `❌` drift row and stamps GO/NO-GO at G8. Order is load-bearing where marked (guard before
scope; ledger before drift audit; confirm the concept before attacking it; rank before featuring;
premortem before the stamp; lock g9 before closing G8).

### Step 1 — Resolve slug, entry guard, read docs
If invoked with a slug, use it; else `glob ideas/*/` and read each `STATE.md` for `current_step: 8`.
Read, in order: `customer-discovery.md` (the floor), then `hypothesis.md`, `kill-scan.md`,
`pressure-report-alpha.md`, `pressure-report-beta.md`, `market-sizing.md`, `evidence-ledger.jsonl`, and
`docs/founder-profile.md` if present. Absent optional docs → note the baseline is thinner (the script
flags each in `warnings`); missing `customer-discovery.md` → refuse and point to
`/customer-discovery-synthesis`. Hold the latest-round Discovery Read verdict for the Decision.

### Step 2 — Resume check
If `ideas/<slug>/startup-brief.md` exists, `AskUserQuestion`: **Overwrite** (`mv startup-brief/
~/.Trash/` and proceed) · **Append a timestamped round** (keep the file; write `startup-brief/rounds/round-<N>.md`
and append a `## Round <N>` section) · **Skip** (print the existing Decision line, exit).

### Step 3 — Build the delta ledger + reconstruct the validated baseline
Create `ideas/<slug>/startup-brief/` first. Run the ledger script:
```bash
uv run "${CLAUDE_SKILL_DIR}/scripts/build_delta_ledger.py" ideas/<slug>
```
Write its JSON to `startup-brief/delta-ledger.md`. Then reconstruct the **validated baseline** (hypothesis
dimensions with each accumulated delta applied) → `startup-brief/validated-baseline.md`. This baseline,
not the stale `hypothesis.md`, is what the drift audit measures against. See `references/drift-audit.md`.

### Step 4 — Crystallize the concept · Gate A (concept-confirm)
From the docs, crystallize a *draft* concept: **wedge**, **validated who** (narrowed by discovery), **core
job**, **non-goals**, **win thesis** (tie to the founder's stated edge). Fire one `AskUserQuestion`
showing the crystallized concept (a `notes` escape hatch) — **the highest-leverage human input; a wrong
crystallization aims the whole challenge at a strawman**. Surface the Discovery verdict: if it was KILL
(overridden at G6), confirm the concept is the *narrowed* one the cleared evidence supports.

### Step 5 — Autonomous challenge
1. **Dispatch `solution-red-team` (blind, separate context)** via the template below — docs + confirmed
   wedge, NOT your draft. It writes `startup-brief/red-team.md`: its own load-bearing assumptions, drift,
   scale-failure, the single self-deception.
2. **Reason the Drift Audit** over the ledger + validated baseline (`references/drift-audit.md`): the
   assumed→validated table, each row `✅ serves it / ⚠️ drifting / ❌ still solving the old problem`.
3. **Extract & rank assumptions.** Assemble every material assumption (yours + the adversary's) into
   `startup-brief/assumptions.json` (per `references/assumption-ranking.md`), then:
   ```bash
   uv run "${CLAUDE_SKILL_DIR}/scripts/rank_assumptions.py" ideas/<slug>/startup-brief/assumptions.json
   ```
   It ranks by leverage×uncertainty, features the **top 3**, and flags any `source: adversary` assumption
   in the top 3 (one you never listed is among your riskiest). Each top assumption → its cheapest test (a
   PoC RAT).
4. **Reconcile** your draft against the blind adversary → `startup-brief/reconciliation.md`; every
   assumption/drift it found that you missed is surfaced as a finding, not buried.

### Step 6 — Premortem (Eisenmann six-pattern)
Run the premortem (`references/premortem.md`): assume it failed in 18 months — assess all six patterns
(Bad Bedfellows / False Starts / False Positives / Speed Trap / Help Wanted / Cascading Miracles), each
`applies / mitigated / live`. Multiply the Cascading-Miracles probabilities and state the combined odds.
A live, unmitigated early-stage pattern pushes the Decision toward NO-GO.

### Step 7 — Exit-criteria check + lock the G9 PoC kill-criteria (lock-ahead)
Check the three exit criteria (problem real & specific / solution serves the VALIDATED problem / enough
signal to justify building — a reasoned bet, not certainty). Then derive the **PoC kill-criteria** from
the top load-bearing assumptions (each a concrete threshold the PoC is scored against), confirm them with
the founder (`AskUserQuestion`), and write `gates/criteria-g9.yaml` **locked**:
```yaml
gate: g9
slug: <slug>
locked: true
locked_at: <run `date +%FT%T%:z`>
criteria:
  - {id: g9-1, desc: "<≥3 of 5 PoC users do X — tests assumption #1>", check: human}
  - {id: g9-2, desc: "<concrete threshold tied to assumption #2>", check: human}
  - {id: g9-3, desc: "<concrete threshold — e.g. ≥1 cold non-network user>", check: human}
  - {id: g9-4, desc: "All open α/β predictions resolved", check: human}
```
PoC outcomes are judged by the founder + the 5 conversations, so g9 criteria are `check: human`. The
write is schema-checked by `test_criteria`; never softened after lock.

### Step 8 — Synthesize the brief · Gate B (GO/NO-GO)
Read `assets/startup-brief-template.md`. Draft `startup-brief.md` in chat with **all** required sections
(the validator requires Decision / Drift Audit table / Premortem / Exit-Criteria / PoC Kill-Criteria /
PoC Brief, plus ≥2 upstream citations and a bold GO/NO-GO stamp). Apply the honesty rule: a `❌` drift
row, an unsupported top-3 assumption, or a live early-stage premortem pattern pushes the Decision to
NO-GO/redesign — do not launder it into GO. Fire `AskUserQuestion`: **Stamp GO** · **Stamp NO-GO** ·
**Refine** (founder names what to redo) · **Abort** (provenance stays, no brief). On stamp, write
`startup-brief.md`; the `schema_on_write` hook runs `test_startup_brief` — on stderr feedback, fix and
rewrite. If Hypothesis Updates Flagged is non-empty, append `startup-brief` to STATE `deltas_pending`;
flip the step-8 checklist item to `done: true`.

### Step 9 — Close G8 + route
```bash
uv run scripts/advance_gate.py --slug <slug> --gate g8 --result <GO|NO-GO> --attest g8-2
```
It enforces the brief validator + lock-ahead (criteria-g9 locked) and advances to step 9.
- **GO** → *"Startup brief stamped GO. Next: `/build-poc <slug>` — it consumes the PoC Brief and scores
  the PoC against the locked `gates/criteria-g9.yaml`."*
- **NO-GO** → route per the reason: **PIVOT** → `/sharpen-hypothesis`; **KEEP-DISCOVERING** → more
  interviews via the sealed pack; **DROP** → promote another `slate.md` idea. (Don't call advance_gate
  with GO if the founder chose NO-GO; record the NO-GO and its routing.)
- If **Hypothesis Updates Flagged** is non-empty: *"Re-run `/sharpen-hypothesis <slug>` to fold the
  flagged deltas before the downstream steps."*

## Subagent dispatch template

Literal template. Substitute `<UPPER_PLACEHOLDERS>` at dispatch. **Resolve `${CLAUDE_SKILL_DIR}` to this
skill's absolute path** — the subagent runs in its own context and won't expand it. Do not set
model/effort on the dispatch — the `solution-red-team` frontmatter pins Opus + `xhigh`.

```
You are the solution-red-team for a committed startup idea that has passed sharpen-hypothesis, kill-scan, pressure-test α/β, customer-discovery-synthesis, and market-sizing. You are NOT a balanced reviewer — find where this solution concept fails and where the founder is fooling themselves. You are BLIND: you get the validation evidence and the bare concept wedge, NOT the founder's drafted brief, so your assumptions and drift findings are independent.

First: Read ${CLAUDE_SKILL_DIR}/references/red-team-brief.md and follow it.

The concept wedge (founder-confirmed): <WEDGE_ONE_LINER + VALIDATED_WHO + CORE_JOB + NON_GOALS>

Context (the validation evidence):
- Reconstructed validated baseline (assumed problem + applied deltas): <VALIDATED_BASELINE>
- Delta ledger (every flagged update + Discovery verdict + tripped/cleared/unsettled criteria + overrides, verbatim): <DELTA_LEDGER>
- Hypothesis / pressure-test α+β / market-sizing highlights: <UPSTREAM_HIGHLIGHTS>
- Founder edge + constraints (from founder-profile.md): <FOUNDER_CONTEXT>

Produce, independently (your own list — do not reverse-engineer the founder's): (1) your top load-bearing assumptions, each with why it's load-bearing + what would have to be true; (2) drift — every place the concept still serves the ASSUMED problem rather than the VALIDATED one, citing the delta/verdict; (3) scale failure — distribution, unit economics, defensibility, founder-edge durability; (4) the single most likely self-deception, one line. Cite evidence; do not soften to be fair.

Write your challenge to: ideas/<SLUG>/startup-brief/red-team.md
Return one line naming the concept + the doc path — not the contents.
```

## Workers, references, assets & scripts

- **Worker:** `solution-red-team` (`.claude/agents/`), dispatched BLIND in Step 5.
- **References:** `references/drift-audit.md` (Steps 3, 5), `references/assumption-ranking.md` (Step 5),
  `references/premortem.md` (Step 6), `references/red-team-brief.md` (read by the worker at dispatch).
- **Assets:** `assets/startup-brief-template.md` — the validator-shaped card (Steps 4, 8).
- **Scripts:** `scripts/build_delta_ledger.py` (every flagged delta + Discovery verdict + criteria +
  overrides, verbatim), `scripts/rank_assumptions.py` (leverage×uncertainty, top-3, adversary flag).
- **Validator:** `tests/schemas/test_startup_brief.py` (drift table + premortem + PoC criteria + upstream
  citations + GO/NO-GO stamp). **Spec:** `docs/loop-engineering-reference-en.md` §2 (step 8).

## Composition

- **Upstream:** `/market-sizing` (step 7) precedes; the whole upstream chain supplies the evidence.
  Floor guard = `customer-discovery.md`.
- **Downstream:** `/build-poc` (step 9) consumes the **PoC Brief** + the LOCKED `gates/criteria-g9.yaml`.
  Hypothesis updates route back through `/sharpen-hypothesis`; a NO-GO routes per its reason.
