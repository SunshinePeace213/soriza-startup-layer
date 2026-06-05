---
name: idea-stage
description: |
  The Idea Stage map + dashboard for the Soriza startup layer. Shows where every idea sits in the
  founder-gated pipeline (generate → hypothesis → disconfirm → market → discovery → solution → exit →
  PoC), the next action for each, and the validated-learning + pivot ledger (runway = pivots left).
  A map and router, NOT an orchestrator — it points you at the next stage skill; each stage you run
  deliberately. Use for "where am I in the idea stage", "what's next", "idea stage status", "show my
  ideas", "which idea should I work on", "what's my runway", or to orient before/after running a stage.
when_to_use: |
  Trigger on "idea stage status / dashboard", "where am I", "what's next on <idea>", "show my ideas /
  slate", "which idea should I work on", "what's my runway / how many pivots left", "the idea pipeline",
  or whenever the founder is orienting across ideas. NOT for running a stage (route to that stage's
  skill) and NOT for editing an idea's artifacts.
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
2. **Derive each idea's stage live** from which artifacts exist — no status file to drift (the
   artifact→stage map is in `references/stage-pipeline.md`).
3. Render the **board**: per idea — current stage · the **next action** (the next stage skill to run,
   per `stage-pipeline.md`) · the latest verdict (Discovery Read / Concept Read / GO-NO-GO) · the
   **pivot count** (runway).
4. Read `ideas/<slug>/learning-log.md` for the validated-learning + pivot history.
5. **Route** the founder to the next skill. If they confirm a pivot or a key learning, append it to
   `learning-log.md` (the BML record; runway = pivots left, not months of cash — see `lean-startup`).

## The pipeline (the map)

```
generate-ideas → (founder picks 1) → sharpen-hypothesis → disconfirm → market-map
  → customer-discovery-design → [founder interviews, days] → customer-discovery-synthesis
  → solution-design → idea-stage-exit (GO/NO-GO) → build-poc  ⟶ exits to the MVP layer
loop-backs: synthesis or PoC can return PIVOT → re-enter sharpen-hypothesis (or generate-ideas for a
segment pivot); each pivot decrements runway.
```

## Reference files

- `references/stage-pipeline.md` — the canonical order, each stage's entry-guard, the artifact→stage
  derivation, the loop-back edges, and the handoff frontmatter fields. Read this to render the board.
- `references/doctrine-map.md` — which doctrine skill each stage inline-reads.
- `references/expert-lens-map.md` — the `disconfirm` persona panel (core-3 + specialist + steelman).
