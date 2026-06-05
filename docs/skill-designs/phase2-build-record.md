# Idea Stage v3 — Phase 2 Build & Verification Record

Phase 2 = the **founder-gated stage spine**. Built per the design contract (`idea-stage-v3-design.md`,
§3 + §6 + §7).

## What was built

**The index + shared config**
- `idea-stage` — the map/dashboard + BML/pivot ledger (derives stage-state live from artifacts; routes
  to the next skill; not an orchestrator). References: `stage-pipeline.md` (order + entry-guards +
  artifact→stage map + handoff frontmatter), `expert-lens-map.md` (the v3 disconfirm panel: core-3 +
  steelman + doctrine angles + ≤1 specialist), `doctrine-map.md` (from Phase 1).

**8 stage skills** (each with an `assets/` output template)
- `generate-ideas` (slate of 10 + advisory recommendation, founder picks; dual-track; distribution-weighted)
- `sharpen-hypothesis` (founder-aware draft-then-refine, NO web; value/growth hypotheses)
- `disconfirm` (core-3 panel + steelman + doctrine angles → Brief; no kill)
- `market-map` (parallel facet fan-out; full article scope; context-never-gate)
- `customer-discovery-design` (sealed pack, drafts-only, locks `kill-criteria.json`)
- `idea-stage-exit` (GO/NO-GO: 3 exit-criteria + "should we build this?")
- `build-poc` (phase-aware: scope → build-in-own-worktree → synthesize; PoC≠MVP; what-to-build + non-goals; `mvp-input` handoff)
- (+ `customer-discovery-synthesis` below)

**Rewired existing**
- `customer-discovery` → **`customer-discovery-synthesis`** (renamed dir + `name`; paths
  `docs/ideas-stages/`→`ideas/`; templates `references/`→`assets/`; fully repointed off `/idea-funnel`
  to `/sharpen-hypothesis` · `/disconfirm` · `/market-map` · `/customer-discovery-design`).
- `solution-design` — paths swapped; repointed off `/idea-funnel` and `/customer-discovery`; downstream
  now `/idea-stage-exit` → `/build-poc`.

**Cleanup (retired)**
- Skills: `idea-funnel` (+ its `references/`). Workflow: `idea-funnel-engine.js`. Agents: `ledger-reader`,
  `ledger-writer`, `fmf-screen`, `sharpen-gate` (absorbed into `/sharpen-hypothesis`).
- `cd-design-gate` → renamed **`customer-discovery-design-worker`** (file + internal `name`).
- All 10 kept worker agents swept: `docs/ideas-stages/`→`ideas/`, `idea-funnel/references/expert-lens-map.md`
  → `idea-stage/references/expert-lens-map.md`, description framing repointed to the v3 stages.
- `create-founder-profile` repointed (routes to `/generate-ideas`; the deleted-rubric mentions →
  the idea-stage skills; pipeline description updated to the v3 flow).

## Verification (prompt-architect)

- **`quick_validate`:** all **14 skills** (idea-stage, generate-ideas, sharpen-hypothesis, disconfirm,
  market-map, customer-discovery-design, customer-discovery-synthesis, solution-design, idea-stage-exit,
  build-poc, create-founder-profile, + the 3 Phase-1 doctrine skills) **and** the renamed subagent — **all valid**.
- **`artifact-eval`** (with-skill vs baseline, graded by `meta-skill-grader`) on the self-contained entry
  point `generate-ideas`: **2/2 pass** — the thesis prompt produced a doctrine-aligned slate with an
  advisory recommendation that leaves the pick to the founder; the **near-miss** (a growth plan for an
  existing business) **did not** get hijacked by the slate machinery. No skill defects found.
- Mid-pipeline stages (disconfirm/market-map/…/build-poc) are frontmatter-valid + Phase-3-reviewed;
  their full behavioural eval is an end-to-end pipeline run (founder-driven, needs real upstream artifacts).

## Repo cleanliness

Every **operational** idea-stage artifact is free of references to the retired funnel/ledger/rubrics.

**Known follow-up (out of Phase-2 scope):** `prompt-architect/references/{decision-tree,dynamic-workflows}.md`
still cite `/idea-funnel` → `idea-funnel-engine.js` as the canonical "thin-skill-fronts-a-workflow"
*teaching example*. That file is now removed, so the example is stale. Left as-is to avoid scope-creep
into the prompt-architect tooling — worth repointing to another bundled workflow when convenient.
