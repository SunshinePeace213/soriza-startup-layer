---
name: idea-stage
description: |
  Idea-Stage map + dashboard: where each idea sits in the founder-gated 9-step pipeline (generate → hypothesis → kill-scan → pressure-α → discovery → pressure-β → sizing → startup-brief → PoC) and its next action. A router, not an orchestrator. Use for "idea stage status", "where am I", "what's next", "my runway".
when_to_use: |
  Use when orienting across ideas — not running a stage (route to that stage's skill) and not editing an idea's artifacts.
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, AskUserQuestion
---

# Idea Stage — map & dashboard

The founder's orientation layer across all ideas: which stage each idea has reached, the next action,
and the Build-Measure-Learn ledger (what's been validated, and how many pivots of runway remain). It is
a **map and a router**, not a driver — you run each stage skill deliberately; this shows you where you
are and where to go next. (The fully-automatic orchestration is a future layer; this validates the
human-gated version first.)

## When this applies

- "Where am I in the idea stage?" · "what's next on `<slug>`?" · "idea-stage status" · "show my ideas"
- "Which idea should I work on?" · "what's my runway / how many pivots left?"
- Run it anytime to orient — before starting a stage, or after finishing one.

Out of scope: running a stage (route to that stage's skill); editing an idea's artifacts.

## What it does

1. `glob ideas/*/` and `ideas/_exploration/*/` for the founder's work product.
2. **Reconcile two state layers** (the state-audit, per `references/stage-pipeline.md`): the
   **declared** step from each idea's `STATE.md` frontmatter (`current_step`/`status`/`next_action`)
   AND the **derived** step from which artifacts exist. `derived ≠ declared` ⇒ render that row **red**
   (a drift alarm) — STATE gains machine-readability without losing the "no status file silently rots"
   insurance.
3. Render the **board**: per idea — current step (1–9) · gate progress (the `gates:` block) · the
   **next action** (the next step skill to run) · the latest verdict (Discovery Read / β recommendation
   / GO-NO-GO) · the **pivot count** (runway) · any drift alarm.
4. Read `ideas/<slug>/learning-log.md` for the validated-learning + pivot history.
5. **Route** the founder to the next skill. If they confirm a pivot or a key learning, append it to
   `learning-log.md` (the BML record; runway = pivots left, not months of cash — see `lean-startup`).

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

## Reference files

- `references/stage-pipeline.md` — the canonical 9-step order, each step's entry-guard + gate, the
  declared-vs-derived **state-audit**, the artifact→step derivation, the loop-back edges, and the
  handoff frontmatter fields. Read this to render the board.
- `references/doctrine-map.md` — which doctrine skill each stage inline-reads.
- `references/expert-lens-map.md` — the `pressure-test` persona panel (core-3 + specialist + steelman).
