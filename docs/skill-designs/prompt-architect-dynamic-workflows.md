# Design contract: "Dynamic-Workflow Sense" for `prompt-architect`

Source: `/grill-me` session (2026-06-04). Topic: upgrade `prompt-architect` so it has a
sense of *when* to use a dynamic workflow — for building a workflow, skill, or command —
following the "A harness for every task" dynamic-workflows release (Thariq Shihipar & Sid
Bidasaria). This is the grilled design contract; `/prompt-architect` executes it.

## Problem

`prompt-architect`'s decision logic (`references/decision-tree.md`) knows skill vs command
vs subagent, and the skill *uses* dynamic workflows internally (Phases 5–6: `artifact-eval`,
`description-optimize`). But it has **no decision sense for when a task itself wants a dynamic
workflow**. The machinery exists; the judgment does not. The repo already proves the target
pattern: a thin skill (`/idea-funnel`) fronting a saved workflow (`idea-funnel-engine.js`).

## Resolved decisions (grill)

1. **Scope — both senses, decision-first.**
   - Sense 1 (build target): recognize when the right answer is a *saved* dynamic workflow
     (`.claude/workflows/<name>.js`), usually fronted by a thin trigger skill.
   - Sense 2 (internal orchestration): know when an artifact it builds should orchestrate
     via a dynamic workflow at *its own* runtime instead of inline subagent spawning.
   - **Out of scope:** a new Phase-5 eval pipeline for JS workflow scripts.

2. **Rubric calibration — conservative load-bearing bar.** Escalate from the 4.8 inline-spawn
   default to a workflow ONLY when ≥1 signal below is a *correctness requirement*, not a
   nice-to-have. Lowest false-positive rate; must not contradict `4-8-principles.md §5` or the
   `Workflow` tool's explicit-opt-in gate.

3. **Footprint — dedicated reference + thin hub pointers** (matches the skill's Tip-3
   progressive-disclosure architecture).

4. **Authoring — lean.** Decision + house conventions + point at the `Workflow` built-in spec
   and the repo's live `*.js` exemplars. No `workflow-template.md` (would duplicate the
   `Workflow` spec — Tip-1 violation + upstream-sync burden). Validation of a drafted workflow =
   structural sanity (`meta` block present, phases match) + one real-input dry-run, NOT the
   `meta-skill-grader` loop.

5. **Verification — two-phase bespoke ad-hoc workflow** (dogfoods the patterns the upgrade
   teaches), run after the draft.

## Key reframe (must be explicit in the reference)

A dynamic workflow is **not a 5th mutually-exclusive artifact type.** It is an *orchestration
layer* that is usually **fronted by a thin skill** (the trigger) — or emitted ad hoc at
runtime. "Build target" means *a saved workflow, usually paired with a thin trigger skill* —
not "instead of a skill."

## The conservative bar — load-bearing signals

Escalate to a dynamic workflow only when ≥1 is a correctness requirement:

| Signal | Why inline/prose fails |
|---|---|
| Deterministic fan-out | "Must reliably spawn N" — 4.8 prose under-fires (§5; the exact Phase-5 pain) |
| Adversarial verification / independent perspectives | Refute-panels & judge-panels need real isolation |
| Scale beyond one context | Audits / migrations / sweeps flood the window |
| Loop-until-dry / loop-until-budget | Unknown-size discovery |
| Multi-stage pipeline, per-item independence | find→verify→synthesize without a barrier |

**Guardrails (anti-eager half):** respect the explicit-opt-in gate; make fan-out cost legible;
NOT for one-offs, conversational/interactive flows, or filesystem-during-orchestration needs.

## The "which shape" ladder (lean — not a quadrant chart)

1. **Inline spawn** (default) — light fan-out inside a skill/subagent; honor §5.
2. **Skill emits an ad-hoc workflow at runtime** — task shape varies per run ("a harness for
   every task").
3. **Thin skill fronts a saved workflow** — stable, complex, reused orchestration (the
   `/idea-funnel` → `idea-funnel-engine.js` pattern).
4. **Standalone saved workflow** — pure orchestration utility, no user trigger (`artifact-eval`).

## File changes

| File | Change |
|---|---|
| `references/dynamic-workflows.md` **(new)** | Bar + signals + guardrails + the 4-shape ladder + house conventions (placement at `.claude/workflows/<name>.js`, skill-fronts wiring, naming) + authoring *pointers* (the `Workflow` spec + live `*.js` exemplars) + lean validation (sanity + one dry-run) |
| `references/decision-tree.md` | New *orthogonal* branch near the top: "Is the core **orchestration** (fan-out / pipeline / verify / scale)? → dynamic workflow, usually fronted by a thin skill → see `dynamic-workflows.md`." State explicitly it is NOT a 5th exclusive type |
| `SKILL.md` Phase 1 | One-line pointer: consult `dynamic-workflows.md` when the work smells like orchestration |
| `references/4-8-principles.md` §5 | Cross-link: when fan-out is load-bearing, escalate inline-spawn → dynamic workflow → see `dynamic-workflows.md` |
| `references/decision-tree.md` reference index in `SKILL.md` | Add the new reference to the "Design & drafting" list |

## Verification workflow (bespoke, ad-hoc, run after the draft)

- **Phase 1 — Decision-accuracy.** 8–12 labeled "build X" scenarios (gold ∈ {workflow, skill,
  subagent, inline near-miss}); one agent per scenario reads the *upgraded* skill
  (`decision-tree.md` + `dynamic-workflows.md`) and decides; a judge scores each pick vs gold →
  accuracy + **false-positive-workflow rate** (the #1 risk). The discriminating tests are the
  near-misses: e.g. "3 independent files to edit, no determinism need" → inline (NOT a
  workflow); "stable reused 4-gate pipeline" → skill-fronts-saved-workflow; "one-off audit
  right now" → just do it.
- **Phase 2 — Adversarial content review.** N skeptics attack `dynamic-workflows.md` for
  over-recommending workflows, contradicting §5 / the opt-in gate, or Tip-1 duplication;
  majority-refute survives.
- **Synthesis.** go/no-go verdict + concrete fixes → feeds the iterate step.

## Execution notes for `/prompt-architect`

- Phase 1 (DESIGN): **skip** — this contract is the shared understanding.
- Phase 2 (DRAFT): create/edit the files above. The artifact under change is the
  `prompt-architect` skill itself (recursive/meta upgrade).
- Phase 3 (REVIEW): anti-patterns gate — specifically check no contradiction with §5 / the
  opt-in gate, and no `Workflow`-spec duplication (Tip 1).
- Phase 4 (PLACE): in place (editing the existing skill in the worktree).
- Phase 5 (VALIDATE): run the **bespoke two-phase verification workflow** above — NOT the
  generic `artifact-eval` — because we're verifying a decision-sense upgrade to references.
- Phase 6 (TRIGGER): **skip** — the skill's trigger description already covers workflows; we're
  not changing triggering.
- Phase 7 (SHIP): report files changed + verification verdict.
