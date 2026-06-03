---
name: idea-funnel
description: |
  Run the Idea-Stage Validator — an automated distillation funnel that takes MANY startup ideas (a
  founder thesis to expand, or a supplied list) through founder-market-fit, testability, an
  evidence-based disconfirmation screen (expert objections judged by evidence, not debate), and
  customer-discovery design, killing weak ideas at each gate and returning a ranked Shortlist. Stops
  at the human SEND gate. Use for "validate these ideas", "run the idea funnel", "distill my ideas",
  "test 100 ideas", "run the whole idea stage". Launches the idea-funnel-engine workflow.
when_to_use: |
  Use when the founder wants to test/validate MANY ideas at once or expand a thesis into ideas and
  distill the best — "run the idea funnel", "validate these N ideas", "distill my ideas to the best
  one", "test these startup ideas", "run the whole idea stage automatically", "which of these ideas
  should I take to customers". For ONE idea through the human pipeline, route to /sharpen-hypothesis
  instead. For just a brainstorm menu (no funnel), /generate-ideas.
argument-hint: "[thesis | 'seeds']"
allowed-tools: Read, Glob, AskUserQuestion, Workflow
effort: high
---

# Idea-Stage Validator — `/idea-funnel`

The front door to the funnel. You gather the inputs, launch the **idea-funnel-engine** workflow, then
render the result. The engine holds all the orchestration (see
[CONTEXT.md](../../../CONTEXT.md), [ADR-0001–0004](../../../docs/adr/), and
[docs/skill-designs/idea-funnel.md](../../../docs/skill-designs/idea-funnel.md)). References for the
gates live in [`references/`](./references/).

## What the funnel does (one screen)

```
seeds (list, any N)  or  thesis ─► seed-generator (wide)
   └─► Gate 0 Founder-Market-Fit ─► Gate 1 Testability ─► Gate 2 Disconfirmation (objections+market)
       ─► CAP (top-K, K from profile) ─► Shortlist ─► Gate 3 CD-design (sealed run-packs)
       ═► ledger + shortlist  →  [HUMAN] approve → Cowork SEND (gated) → interviews → /solution-design
```

## Step 1 — Gather inputs (don't over-ask)

Determine which mode and collect only what's missing:

- **Thesis mode** — the founder gives a theme/thesis to expand. Need: `thesis` (string), optional `n`
  (seeds to generate, default 10).
- **Ingest mode** — the founder supplies their own ideas. Need: `seeds` — an array of
  `{ title, problem, who, why_now, idea_type? }`. Accept a pasted list and normalize it.
- **Optional for both:** `k` (Shortlist cap — DEFAULT is derived from the founder profile, so only set
  it if the founder overrides), `resurrect` (array of Candidate IDs to re-enter from a prior run),
  `coworkSharePath` (e.g. `/mnt/c/dev/soriza-cowork` per ADR-0003, to write run-packs to the Cowork
  share).

If neither a thesis nor seeds is available, ask one question to get one. Don't re-ask the cap or
anything already in `docs/founder-profile.md`.

## Step 2 — Launch the engine

Call the **Workflow** tool with the engine script and the assembled args:

- `scriptPath: ".claude/workflows/idea-funnel-engine.js"`
- `args: { thesis?, seeds?, n?, k?, resurrect?, coworkSharePath? }` — pass a real JSON object, not a
  string.

The run executes in the background; watch it with `/workflows`. It cannot pause for input (by design),
so let it run to the Shortlist.

## Step 3 — Render the result

The engine returns `{ run_label, ledger, shortlist_doc, shortlist, counts }` and the
**ledger-writer** has already written the board. Show the founder:

- The funnel counts (entered → killed per gate → cleared → shortlisted) and the cap K with its
  profile justification.
- The **Shortlist** (≤K) with each survivor's hypothesis and the strongest objection it survived — and
  the path to its sealed run-pack.
- Where the full board lives: `docs/ideas-stages/_funnel-runs/<run_label>/ledger.md`.

Then state the boundary plainly: *the funnel stops here.* Nothing has been sent. The next move is
human — review the Shortlist, then in Cowork connect Gmail/Calendar/Drive, open the run-pack, and
approve the first gated outreach batch.

## Step 4 — Appeal / resurrect (on request)

If the founder disagrees with a kill, they appeal: re-launch with `resurrect: ["cand-..."]` and the
killed Candidate re-enters the funnel. The ledger is stateful — settled Candidates aren't re-run
(cheap re-runs), and a re-run promotes the next-ranked survivor when the current one resolves.

## Boundaries

- **Never send outreach.** The funnel ends at the Shortlist + run-packs; sending is Cowork's job, gated
  per batch (ADR-0001/0003). This skill has no send tool.
- **Don't hand-orchestrate the gates.** The engine owns the pipeline; your job is launch + render.
- For ONE idea through the full human pipeline, use the standalone skills, not the funnel.
