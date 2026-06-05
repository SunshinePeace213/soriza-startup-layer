# Stage pipeline — order, entry-guards, artifact→stage map, handoffs

The canonical spine of the Idea Stage. Each stage is its own founder-gated skill; the founder advances
between them. State is **derived live** from which artifacts exist in `ideas/<slug>/` (no status file).

## The stages

| # | Stage skill | Entry-guard (must exist first) | Produces (in `ideas/<slug>/`) | Reads doctrine |
|---|---|---|---|---|
| 1 | `generate-ideas` | thesis or seed-list (arg) | `_exploration/<thesis>/slate.md` → founder picks → scaffolds `ideas/<slug>/` | forward-deployed-founder, lean-startup |
| 2 | `sharpen-hypothesis` | the picked idea | `hypothesis.md` | lean-startup |
| 3 | `disconfirm` | `hypothesis.md` | `disconfirmation-brief.md` (+ `disconfirmation/`) | personas + FDF/lean angles |
| 4 | `market-map` | `hypothesis.md` | `market-research.md` (+ `market-research/`) | forward-deployed-founder |
| 5 | `customer-discovery-design` | `disconfirmation-brief.md` + `hypothesis.md` | `customer-discovery/cowork-runpack.md` + `customer-discovery/kill-criteria.json` | mom-test |
| 6 | `customer-discovery-synthesis` | `kill-criteria.json` + `customer-discovery/interviews/*.md` | `customer-discovery.md` (+ `synthesis/`) | — |
| 7 | `solution-design` | `customer-discovery.md` | `solution-design.md` (+ `solution-design/`) | lean-startup, FDF, solo-founder |
| 8 | `idea-stage-exit` | `solution-design.md` | `idea-stage-exit.md` | lean-startup |
| 9 | `build-poc` | `idea-stage-exit.md` = GO | `poc/{poc-brief.md, reactions.md, mvp-input.md}` | lean-startup, solo-founder |

## Artifact → stage derivation (for the dashboard)

The **latest** artifact present in `ideas/<slug>/` is the stage the idea has reached; the **next action**
is the stage whose entry-guard is now satisfied:

`poc/reactions.md` → done (or looping) · `idea-stage-exit.md` → next: build-poc (if GO) · `solution-design.md`
→ next: idea-stage-exit · `customer-discovery.md` → next: solution-design · `customer-discovery/kill-criteria.json`
(no synthesis yet) → next: run interviews then customer-discovery-synthesis · `market-research.md` +
`disconfirmation-brief.md` → next: customer-discovery-design · `disconfirmation-brief.md` (no market) →
next: market-map · `hypothesis.md` → next: disconfirm (+ market-map) · only a scaffolded folder → next:
sharpen-hypothesis.

## Handoff frontmatter (the thin contract each artifact carries)

Each stage writes ONE `<artifact>.md` whose **YAML frontmatter** is the handoff header the next stage's
entry-guard parses; the body is the human-readable detail. Keep frontmatter thin (scalars + pointers);
rich/nested content lives in the body; mechanical-scored data is the only `.json`.

| Artifact | Frontmatter fields |
|---|---|
| `hypothesis.md` | `stage, status, who, how_often, how_severe, status_quo, value_hypothesis, growth_hypothesis` |
| `disconfirmation-brief.md` | `stage, status, top_risks[], open_assumptions[], interview_questions[]` |
| `market-research.md` | `stage, status, demand_strength, reachable_niche, competitor_tiers, distribution_read` |
| `customer-discovery/cowork-runpack.md` | `stage, status, reachable, sealed: true` |
| `customer-discovery.md` | `stage, status, verdict (CONTINUE|PIVOT|KILL|KEEP-DISCOVERING), tripped[], round` |
| `solution-design.md` | `stage, status, concept_read (build|narrow|redesign|reconsider), wedge` |
| `idea-stage-exit.md` | `stage, status, decision (GO|NO-GO), exit_criteria_met` |
| `poc/reactions.md` | `stage, status, archetype, direction (keep|pivot|redraw)` |

## Loop-backs (BML is a loop)

- `customer-discovery-synthesis` verdict **PIVOT** → re-enter `sharpen-hypothesis` (or `generate-ideas`
  for a customer-segment pivot); log the pivot type + decrement runway in `learning-log.md`.
- **KILL / INVALIDATED** → drop, or promote another `slate.md` idea.
- `build-poc` reactions **pivot / redraw** → back to `sharpen-hypothesis` or `solution-design`.

## Kill philosophy

The desk almost never kills — it produces context + interview questions; the **founder** decides
advance/pivot/persevere. The only mechanical kill is a **pre-registered kill-criterion firing at
`customer-discovery-synthesis`** (founder may override on record). No fatal-flaw checkpoint, no fit-screen
kill-gate (founder-fit is just an input to `generate-ideas`' recommendation).
