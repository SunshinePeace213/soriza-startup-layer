# Idea-Stage Validator (`/idea-funnel`) — design & build plan

Design rationale lives in [CONTEXT.md](../../CONTEXT.md) and
[ADR-0001](../adr/0001-funnel-kills-on-evidence-not-debate.md) /
[ADR-0002](../adr/0002-validator-runtime-is-a-dynamic-workflow.md) /
[ADR-0003](../adr/0003-cowork-repo-bridge-is-a-windows-side-shared-folder.md). This doc is the
file-level build plan only.

Core principle: **reuse the existing subagents as evidence-gatherers; add new judge/gate agents that
emit the schema verdicts; the Workflow script is the glue.**

## File manifest

### CREATE — gate / judge subagents (`.claude/agents/`)
| File | Role | Output |
|---|---|---|
| `seed-generator.md` | thesis + grounding evidence → N thin Candidate seeds, wide (no narrow) | schema: `seed[]` |
| `fmf-screen.md` | **Gate 0** — seed + `founder-profile.md` → advance/kill | schema: `{verdict, reason, score}` |
| `sharpen-gate.md` | **Gate 1** — seed → testable? + who/often/severity/status-quo | schema: `{verdict, fields, reason}` |
| `objection-lens.md` | **parameterized by expert name** — channels one `*-perspective` lens (via its lens-card in `expert-lens-map.md`, reading the full `{expert}-perspective/SKILL.md` only when needed) → that expert's single strongest disconfirming objection. Called once per selected expert as a parallel `agent()`. Workflows orchestrate subagents, NOT skills — so the perspective skills are the *source*, this agent is the runtime. | schema: `{expert, objection}` |
| `disconfirmation-judge.md` | **Gate 2** — seed + objections + market evidence + size → verdict | schema: `{verdict, reason, score, strongest_unrebutted}` |
| `cd-design-gate.md` | **Gate 3** — survivor → sealed run-pack file + reachability | schema: `{reachable, verdict, runpack_path}` |

### CREATE — references (`.claude/skills/idea-funnel/references/`)
| File | Role |
|---|---|
| `expert-lens-map.md` | idea-type → 3–4 expert lenses (+ steelman) for Gate 2, **plus a compact lens-card per expert** (the one question + what it kills) that `objection-lens` uses by default; new experts (via `nuwa-skill`) become usable by adding a card here — no workflow change |
| `gate-rubrics.md` | the tunable kill **thresholds** per gate (the bars) |
| `ledger-schema.md` | ledger columns (incl. a **coverage-gap** field per [ADR-0004](../adr/0004-gate2-uses-a-closed-expert-roster-gaps-are-logged.md)) + stable Candidate-ID scheme |

### CREATE — runtime glue & front door
| File | Role |
|---|---|
| `.claude/workflows/idea-funnel.js` | the Workflow: normalize → grounding → seed-gen → Gate 0→1→2 (bar-to-kill) → cap (K from profile) → Gate 3 → return ledger data |
| `.claude/skills/idea-funnel/SKILL.md` | launcher: parse args (list / thesis / K), launch the workflow, write ledger + shortlist + run-packs, render the board, handle appeal/resurrect |

### CREATE — eval fixtures (`docs/skill-designs/idea-funnel/fixtures/`)
Labelled should-advance (`personalized-ai-digest`, a real pass) + should-kill candidates per gate
(a regulated/deep-tech idea → FMF kill; a vague idea → sharpen kill; a no-moat me-too → Gate 2 kill).

### EDIT
| File | Change |
|---|---|
| `.claude/skills/idea-to-hypothesis/SKILL.md` | superseded by the funnel — deprecate + redirect to `/idea-funnel` (it only ever wired 3 stages) |
| `CLAUDE.md` | update the pipeline description to add the funnel + its entry point |
| `.claude/skills/customer-discovery/SKILL.md` | make the run-pack output path configurable to the Cowork share (`/mnt/c/dev/soriza-cowork/`) |

### REUSE — no edit (called by the funnel as evidence-gatherers)
`startup-idea-researcher` (grounding sweep) · `market-researcher` (Gate 2 evidence) ·
`competitor-steelman` (Gate 2 objection) · `customer-discovery-personas-worker` (Gate 3 materials).

### REMOVE
None up front. After the funnel is verified and `idea-to-hypothesis` is fully superseded, optionally
delete it. Don't delete prematurely.

### Auto-created at runtime (not by us)
`docs/ideas-stages/_funnel-runs/<run>/ledger.md` + shortlist + sealed run-packs.

## Development steps (ordered)

- **Phase 0 — Prereqs.** Enable Cowork (Claude Desktop, paid plan); run `/setup-cowork` *inside
  Cowork*; connect Gmail/Calendar/Drive; create `C:\dev\soriza-cowork\`; allowlist WebSearch/WebFetch
  so the Workflow's agents don't hit mid-run permission prompts.
- **Phase 1 — Cheap gates (highest leverage).** Build `fmf-screen` + `sharpen-gate` via
  prompt-architect; eval each against fixtures with `artifact-eval`. These two kill ~70% at near-zero
  cost, so they earn their keep first.
- **Phase 2 — Seed generation.** Build `seed-generator`; wire the grounding sweep (reuse
  `startup-idea-researcher`); verify N grounded thin seeds from a thesis.
- **Phase 3 — Gate 2 (the expensive tier).** Build `expert-lens-map`, `objection-lens`,
  `disconfirmation-judge`; reuse `market-researcher` + `competitor-steelman` for evidence; eval the
  judge against fixtures (does the strongest unrebutted objection actually kill?).
- **Phase 4 — Gate 3.** Wire `cd-design-gate` / `personas-worker` to emit the sealed run-pack to the
  Cowork share; soft-kill on no reachable audience.
- **Phase 5 — Workflow glue.** Write `idea-funnel.js`: pipeline the gates, bar-to-kill + cap-from-
  profile, stateful-ledger read/write (return data → session writes). **Run on a small slice (5–10
  seeds) first** to gauge spend (per the workflows docs).
- **Phase 6 — Launcher skill.** Build `idea-funnel/SKILL.md` (repurpose `idea-to-hypothesis`): args
  parsing, ledger rendering, appeal/resurrect; deprecate `idea-to-hypothesis`.
- **Phase 7 — End-to-end verification.** Known-good + known-bad batch; confirm advance/kill
  correctness + sensible kill-reasons (the false-kill / false-pass check); tune `gate-rubrics.md`.
- **Phase 8 — Wrap.** Update `CLAUDE.md`; final `CONTEXT.md` pass; save the run as `/idea-funnel`;
  set model tiers per gate (haiku for Gate 0/1, opus for Gate 2).

## As-built (deviations from the plan above)

Built on branch `idea-funnel`. Three intentional deviations:

1. **Engine renamed to avoid a command-name collision.** A saved workflow already *is* its `/name`
   command, so the engine ships as `.claude/workflows/idea-funnel-engine.js` (`/idea-funnel-engine`)
   and a thin front-door **skill** `.claude/skills/idea-funnel/SKILL.md` owns the friendly `/idea-funnel`
   command — it gathers inputs, calls the Workflow tool on the engine, and renders the ledger. (The plan
   assumed one file at `.claude/workflows/idea-funnel.js`.)
2. **Two ledger helper agents added** that the plan folded into "the session writes the ledger": a
   workflow script can't write files, so `ledger-reader` (stateful re-run: read prior ledger, skip
   settled) and `ledger-writer` (persist `ledger.json` + `ledger.md` + `shortlist.md`, derive run-label
   by Glob — no timestamps) do it as real subagents inside the run.
3. **`idea-to-hypothesis` repurposed as a deprecation signpost** (routing table to `/idea-funnel` and
   the standalone skills), not as the launcher — the launcher is the new `idea-funnel` skill.

Models built in (overridable in the engine's `agent()` calls): haiku for Gate 0/1 + ledger helpers,
sonnet for seed-generator / objection-lens / cd-design, opus for the disconfirmation-judge.

Status: all artifacts written and the engine JS passes `node --check`. NOT yet run live — Phase 7
(small-slice eval against the fixtures) is the next step and needs a thesis/seed input + spends tokens.
