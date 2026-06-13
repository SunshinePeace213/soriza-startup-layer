# Dynamic Workflows: when a task wants its own harness

A *dynamic workflow* is the `Workflow` tool: Claude writes a JS orchestration script on the
fly (`agent()` / `parallel()` / `pipeline()`) that fans out subagents **deterministically**.
Saved ones live at `.claude/workflows/<name>.js`. The `Workflow` tool's own description is the
authoritative authoring guide and is always in context the moment you'd write one — this file
is about the **decision** (is a workflow the right shape, and which shape), not about
re-teaching `agent()`/`pipeline()`.

## The reframe — a workflow is an orchestration layer, not a 5th artifact type

`decision-tree.md` routes here when the core of the work is *orchestration* (fan-out,
multi-stage pipeline, verification panel, scale beyond one context). But a dynamic workflow is
**not** a sibling of skill/command/subagent on the "pick one" axis. It runs headless to
completion and returns a value — it is almost never the thing the user invokes. So a workflow
is normally **paired** with one of the other artifacts:

- a thin **skill fronts** a saved workflow (the user-facing trigger), or
- a skill **emits an ad-hoc workflow** at its own runtime ("a harness for every task").

"This should be a workflow" therefore answers a *different* question than "skill vs subagent" —
it's orthogonal. The build target is usually *a saved workflow plus a thin trigger skill*, not
"a workflow instead of a skill."

## The conservative bar — escalate from inline-spawn only when fan-out is load-bearing

Two defaults pull against reaching for a workflow, and both are correct:

- **4.8 spawns fewer subagents by default** (`4-8-principles.md §5`) — usually right; most work
  is better done inline than fanned out.
- **The `Workflow` tool must not fire without explicit user opt-in** — it can spawn dozens of
  agents on a large shared token budget. The opt-in exists because the cost is real.

So the bar is high. Escalate from "spawn a couple of subagents inline" to a dynamic workflow
**only when at least one signal below is a correctness requirement** — something the result is
wrong without, not a nice-to-have:

| Load-bearing signal | Why inline / prose fails it |
|---|---|
| **Deterministic fan-out** | "Must reliably spawn N" — a prose "spawn N subagents" instruction under-fires on 4.8 (the exact pain Phase 5 fixes); `agent()` calls execute every time |
| **Adversarial verification / independent perspectives** | Refute-panels and judge-panels need genuinely isolated contexts; one context grading its own work is not independent |
| **Scale beyond one context** | Audits, migrations, broad sweeps whose inputs would flood a single window |
| **Loop-until-dry / loop-until-budget** | Unknown-size discovery that keeps spawning until K dry rounds or a token target |
| **Multi-stage pipeline, per-item independence** | find→verify→synthesize over enough items that inline spawning is unreliable — a couple of stages over a couple of items is still inline work |

Those five signals are the decision face of why isolation and determinism matter; three failure
modes the "harness for every task" article names sit behind them, each one the bar guards against
— though deterministic fan-out and multi-stage independence earn the bar on their own, without a
named mode. **Agentic laziness** (the model declaring done at 35 of 50): decompose into focused
subagents so no single agent faces the whole slog, and loop until the work is actually dry.
**Self-preferential bias** (Claude favouring its own output when it judges it): verify in a
separate, independent context, not the one that produced the work. **Goal drift** (fidelity lost
across many turns and compactions): give each subtask a fresh context window so the original
constraints don't decay. If no load-bearing *signal* from the bar is in play, none of these is
either — inline is fine.

**Hold the line the other way too — do *not* use a workflow when:**

- it's a one-off you can just do now, or the work is linear with no real fan-out;
- the orchestration is conversational / interactive — a workflow runs headless to completion,
  so anything needing a human mid-run belongs in a skill (put the human gate at the boundary,
  the way the idea-stage skills stop at a founder-signature gate);
- each step needs the filesystem *during* orchestration — workflow scripts can't touch it
  (this is exactly why prompt-architect keeps `scripts/` outside its workflows);
- the only justification is "there's some parallelism." Parallelism alone is not the bar; a
  load-bearing signal is.

Whenever a skill launches a workflow — fronted *or* emitted ad hoc — make the fan-out **cost
legible** first: a trigger that silently launches a 30-agent run is a cost surprise. Name the
scale and get explicit opt-in.

## Which shape — picking the rung

Only Rung 1 is free. **Rungs 2–4 all fire the `Workflow` tool, so they require the load-bearing
bar AND explicit opt-in to be cleared *first*** — once you're past the bar, how much the
orchestration *shape varies* run-to-run only chooses *among* the workflow rungs (ad-hoc vs
saved); variability by itself never clears the bar. With that settled, pick the lowest rung that
meets the need:

1. **Inline spawn** — *the case where the bar was not met — including a signal that matched in kind but not at a scale where inline is unreliable.* The skill/subagent body says "spawn
   subagents in parallel when fanning out across independent items; do single-item work inline."
   Light, occasional fan-out. Honors §5; no workflow fires.
2. **Skill emits an ad-hoc workflow at runtime** — the skill body authors a `Workflow({script})`
   per task. Right when the orchestration *shape varies* run-to-run, so there's nothing stable to
   save ("a harness for every task"). This is the most *invisible* launch shape, so the emitting
   skill must still surface the fan-out scale and get explicit opt-in before the tool fires — the
   opt-in gate applies here too, not just to saved workflows.
3. **Thin skill fronts a saved workflow** — `.claude/workflows/<name>.js` holds stable, complex,
   reused orchestration; a dedicated thin skill is the trigger (`Workflow({name})`). The repo's
   `/artifact-eval` → `artifact-eval.js` is exactly this.
4. **Standalone saved workflow** — `.claude/workflows/<name>.js` invoked **by name as an internal
   step from another skill or workflow's body**, rather than fronted by its own dedicated trigger
   skill. prompt-architect's `artifact-eval` and `description-optimize` are this: prompt-architect
   calls them from its Phase 5/6 body via `Workflow({ name })`.

## House conventions for a saved workflow (the build-target case)

- **Placement:** `.claude/workflows/<name>.js` (project). Name it for the job, hyphen-case,
  matching the `meta.name` inside.
- **The `meta` block is required and must be a pure literal** — `name` + `description`, optional
  `phases` whose titles match the `phase()` calls. No variables, calls, or spreads in it.
- **Skill-fronts wiring:** the fronting skill stays thin — its body's job is to gather inputs,
  surface the fan-out cost (per the bar above), then call `Workflow({ name: '<name>', args })`.
  Keep the orchestration in the `.js`; keep judgment/interaction in the skill. `artifact-eval`'s
  SKILL.md is the model.
- **Gate at the boundary, not mid-run:** if a human decision is needed, return up to it and let
  the fronting skill handle it; don't try to pause a headless workflow.

## Authoring — point at the spec and the live exemplars, don't duplicate

The `Workflow` tool description already covers `agent()`, `parallel()`, `pipeline()`, schemas,
resume, the budget object, and the quality patterns (adversarial verify, loop-until-dry,
multi-modal sweep, completeness critic). It's in context whenever you write a workflow — use it
as the reference rather than restating it here. The "harness for every task" article also names
some useful shapes — **classify-and-act**, **tournament**, and **generate-and-filter** — read it
for the details. They're shapes, not bar-clearers: a 3-attempt tournament or a
generate-and-filter over a couple of ideas is still inline (rung 1); reach for a workflow only on
a load-bearing instance at a scale where inline is unreliable. For shape, read the repo's own:

- `.claude/workflows/artifact-eval.js` — skill-fronted (`/artifact-eval`) and also called by name
  from prompt-architect's body: with-artifact-vs-baseline per item + a grader agent, schema-validated.
  The richest in-repo example.
- `.claude/workflows/description-optimize.js` — a compact utility called by name from prompt-architect's
  body. Compact pipeline shape.

## Validating a drafted workflow (lean — no eval pipeline)

A saved workflow is **not** put through the `meta-skill-grader` loop (that's for
skill/command/subagent artifacts). Validate it lightly:

- **Structural sanity:** the `meta` block satisfies the House-conventions rule above; `phases`
  titles line up with `phase()` calls; concurrent fan-out uses `parallel()`/`pipeline()` rather
  than a hand-rolled loop.
- **One real-input dry-run:** invoke it on the smallest realistic input, watch `/workflows`, and
  confirm it returns the expected shape. Use `resumeFromRunId` for cheap re-runs while iterating
  — an unchanged prefix replays from cache.

## Failure modes

The authoring failure modes live in the `Workflow` tool description (in context whenever you
write a workflow), not here — restating them is the Tip-1 duplication this file is built to
avoid: resume constraints, the `pipeline()`-vs-`parallel()`-barrier choice, loop-until-dry
dedup, and the shared `budget` object. The one constraint that shapes the *artifact boundary* —
workflow scripts can't touch the filesystem — sits in the do-not-use bar above; it's why file
I/O stays in the fronting skill or in kept scripts. Add real gotchas here the first time one
bites in practice.

## Cross-references

- ["A harness for every task" (Anthropic)](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) — source for the three failure modes + the named patterns
- `decision-tree.md` — the orthogonal "is the core orchestration?" branch routes here
- `4-8-principles.md §5` — fewer subagents by default; this file is when to override that
- `../../../workflows/artifact-eval.js` — the skill-fronts-workflow + called-by-name exemplar
- `../../../workflows/description-optimize.js` — called-by-name internal-step exemplar
- the `Workflow` tool description — the authoritative authoring reference
