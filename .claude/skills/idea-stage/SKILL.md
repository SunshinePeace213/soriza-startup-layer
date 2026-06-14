---
name: idea-stage
description: |
  The orchestrator + map for the whole Idea Stage — the single front door to the founder-gated 9-step pipeline (generate → hypothesis → kill-scan → pressure-α → discovery → pressure-β → sizing → startup-brief → PoC). Loads the full workflow doctrine (pipeline canon, gates, two-round protocol, state layer, evidence + kill rules, doctrine routing) and drives the founder through it — sequencing, checklists, handoffs — stopping at every gate. Use for "idea stage status", "where am I", "what's next", "how does the idea stage work", "run / orient the idea-stage workflow", "my runway".
when_to_use: |
  Use to orient across ideas, to understand or drive the whole idea-stage workflow end-to-end, or to find the next action. It sequences and routes and carries the workflow doctrine; it NEVER auto-advances a gate (the founder signs every gate). To run one stage's deep work, it routes the founder to that stage's skill.
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, AskUserQuestion
---

# Idea Stage — the orchestrator

The single front door to the Idea Stage. Invoke it to **orient** (where each idea sits, what's next) and to
**understand or drive the whole workflow**: it carries the full pipeline doctrine and sequences the founder
through the 9 founder-gated steps — running checklists and managing the artifact handoffs between steps.

**It drives the flow; it does not make the founder's decisions.** Every gate is a founder signature
(`scripts/advance_gate.py` is the only gate-writer). The orchestrator sequences steps, renders state, and
routes to the next stage skill — but it **HALTS at every gate** and never auto-advances one. The desk almost
never kills; the founder decides advance / pivot / persevere on the evidence.

## Load order (read these when orienting or driving the workflow)

1. The invariants in the repo **`CLAUDE.md`** (write path, gates, evidence ingress, kill authority, hooks) —
   the always-on rules the hooks enforce on every write.
2. **`ideas/ACTIVE`** → the slug; then **`ideas/<slug>/STATE.md`** (declared step / owner / next_action).
3. This skill's reference files (below) for the step cards, gates, state-audit, doctrine + persona routing.

## When this applies

- "Where am I in the idea stage?" · "what's next on `<slug>`?" · "idea-stage status" · "show my ideas"
- "How does the idea stage work?" · "walk me through the workflow" · "run the idea-stage loop"
- "Which idea should I work on?" · "what's my runway / how many pivots left?"
- Run it anytime to orient — before starting a stage, after finishing one, or to load the whole doctrine.

Out of scope: doing a stage's deep work (route to that stage's skill); editing an idea's artifacts directly.

## The pipeline (the map)

```
1 generate-ideas → (founder picks 1) → 2 sharpen-hypothesis → 3 kill-scan → 4 pressure-test (α)
  → 5 customer-discovery-design → [founder interviews, days] → customer-discovery-synthesis
  → 6 pressure-test --beta (main kill) → 7 market-sizing → 8 startup-brief (GO/NO-GO)
  → 9 build-poc  ⟶ exits to the MVP layer
gate number = step number; the gate sits at the step's end (advance via scripts/advance_gate.py).
loop-backs: synthesis (G5) or PoC (G9) can return PIVOT → re-enter sharpen-hypothesis (or generate-ideas
for a segment pivot); each pivot decrements runway.
```

## How the orchestration runs (per step)

For the active idea, drive each step the same way — the loop the orchestrator runs:

1. **Reconcile state** (the state-audit): compare the **declared** step in `STATE.md` against the **derived**
   step (which artifacts exist — table in `references/stage-pipeline.md`). `derived ≠ declared` ⇒ a **drift
   alarm** (render that row red). STATE gains machine-readability without losing "no status file silently rots."
2. **Check the entry-guard**: the next step runs only once its input artifact exists (e.g. `pressure-test` α
   needs `neutral-brief.md`). Guards + produced artifacts: `references/stage-pipeline.md`.
3. **Run the step's checklist**: act only on `STATE.md` `step_checklist` items with `owner: agent`; if
   `owner: human`, prepare drafts and remind — never perform a founder-gated act for them.
4. **Route to the stage skill** for the deep work (the founder runs it): `generate-ideas`, `sharpen-hypothesis`,
   `kill-scan`, `pressure-test`, `customer-discovery-design` → `customer-discovery-synthesis`,
   `pressure-test --beta`, `market-sizing`, `startup-brief`, `build-poc`.
5. **Stop at the gate**: when a step's artifact is done, the founder reads the verdict and signs;
   `scripts/advance_gate.py --slug <slug> --gate gN` writes the gate (the orchestrator never edits `gates:`).
6. **Record the loop**: on a PIVOT/KILL verdict, append the pivot type + decrement runway in
   `ideas/<slug>/learning-log.md` (runway = pivots left, not months of cash — see `lean-startup`).

## Workflow doctrine (the rules this orchestrator applies)

The enforced invariants live in `CLAUDE.md` (hook-paired, always-on). This is the orchestration digest:

- **Write path**: only inside `ideas/<ACTIVE>/` and `ideas/_exploration/`.
- **Gates**: never hand-edit the `gates:` block — `advance_gate.py` only; it validates the artifact, checks the
  **locked** `criteria-gN.yaml` line-by-line, confirms lock-ahead, appends the decision-log, writes STATE.
- **Evidence**: web content enters artifacts ONLY via `evidence-ledger.jsonl` (the research agent is the single
  web entry point). Grades 1–5 (1 = first-party commitment … 4 = web source w/ URL … 5 = founder belief);
  cite external facts as `E-xxx`; interview claims cite grade ≤2.
- **Kill authority**: the only **desk** kill is a hard, checkable fact at `kill-scan` (legality / technical
  impossibility), and even that is a founder-stamped override. Subjective merit dies only to real users
  (steps 5–6) + the founder's signature. `p_success` is a calibration prediction, **never a verdict**.
- **Hypothesis**: never edit `hypothesis.md` outside `sharpen-hypothesis` — emit a flagged-delta block instead.

## The Two-Round Protocol (pressure-test α/β — steps 4 & 6)

`pressure-test` convenes a bounded panel (core-3 + competitor-steelman + doctrine angles + ≤1 specialist —
roster in `references/expert-lens-map.md`). Its **isolation is sacred** (hook-enforced):

- **Independent round**: every panel seat reads ONLY `neutral-brief.md` + `evidence-ledger.jsonl` — never a
  sibling's verdict before the cross-examination round (`objection-lens` holds no spawn tool; `SubagentStop`
  validates each seat's JSON before the judge sees it).
- **Cross-exam revisions**: a seat may revise `p_success` ONLY with a `revision_note` — never a silent overwrite.
- Each objection becomes a **falsifiable assumption + a Mom-Test interview question**; nothing here kills.

## Dashboard render

Per idea: current step (1–9) · gate progress (the `gates:` block) · next action (the next step skill) · the
latest verdict (Discovery Read / β recommendation / GO-NO-GO) · pivot count (runway) · any drift alarm.
Read `ideas/<slug>/learning-log.md` for the validated-learning + pivot history.

## Reference files

- `references/stage-pipeline.md` — the canonical 9-step spec: each step's entry-guard + produced artifact +
  gate, the declared-vs-derived **state-audit**, the artifact→step derivation, loop-back edges, handoff
  frontmatter. **The deep mechanics live here; this skill is the driver.**
- `references/doctrine-map.md` — which doctrine skill each stage inline-reads (FDF / lean-startup / solo-founder).
- `references/expert-lens-map.md` — the `pressure-test` persona panel (core-3 + specialist + steelman).
