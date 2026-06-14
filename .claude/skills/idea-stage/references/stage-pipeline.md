# Stage pipeline — the 9-step canon, gates, artifact→step map, state-audit, handoffs

The canonical spine of the Idea Stage. **9 steps; gate number = step number; the gate sits at the
step's end.** Each step is its own founder-gated skill; the founder advances between them. State is
**declared** in `ideas/<slug>/STATE.md` (machine-readable) AND **derived live** from which artifacts
exist — the dashboard renders both and alarms on drift (see *State-audit* below).

This reference is the canonical pipeline spec (step cards + state layer). The legacy stage
order (disconfirm / market-map / solution-design / idea-stage-exit as standalone stages) is **RETIRED**
— absorbed into the steps below (see *Legacy skills retired* below).

## The steps

| # | Step skill | Entry-guard (must exist first) | Produces (in `ideas/<slug>/`) | Gate | Founder control |
|---|---|---|---|---|---|
| 1 | `generate-ideas` | thesis or seed-list (arg) | `_exploration/<thesis>/slate.md` → pick → scaffold `seed.md`, `STATE.md`, `gates/criteria-g2.yaml` (locked), ledgers, `ACTIVE` | **G1** | the pick |
| 2 | `sharpen-hypothesis` | scaffolded folder (`seed.md`) | `hypothesis.md` | **G2** | dimension content + sign |
| 3 | `kill-scan` *(new)* | `hypothesis.md` | `kill-scan.md` + ledger entries (disqualifiers + demand-scan) | **G3** | disqualifier override |
| 4 | `pressure-test` (α) | `neutral-brief.md` (from `make_brief.py`) + ledger | `pressure-report-alpha.md` + `predictions.jsonl` + **G5 `kill-criteria.json` locked** | **G4** *(triple lock)* | read `change_my_mind`; sign proceed/pivot |
| 5 | `customer-discovery-design` → *(human interviews)* → `customer-discovery-synthesis` | α OPEN assumptions + demand-scan entries | `customer-discovery/cowork-runpack.md`, `kill-criteria.json`, `interviews/*.md`, `customer-discovery.md` | **G5** | interviews, commitments, send approval |
| 6 | `pressure-test --beta` | `customer-discovery.md` + full ledger | `pressure-report-beta.md` (every claim cites a ledger ID) | **G6** | **the main kill decision** — go/pivot/kill stamp |
| 7 | `market-sizing` | `customer-discovery.md` + `hypothesis.md` | `market-sizing.md` (bottom-up TAM/SAM/SOM, buyer, trends) | **G7** | read only — **size never kills** |
| 8 | `startup-brief` | `market-sizing.md` (+ upstream) | `startup-brief.md` (drift audit + premortem + locked G9 PoC criteria + GO/NO-GO) | **G8** | GO/NO-GO stamp + every ❌ drift row |
| 9 | `build-poc` | `startup-brief.md` = GO | `poc/{poc-brief.md, reactions.md, mvp-input.md}` | **G9** | the pretotype + 5 conversations + direction |

Legacy skills retired and removed: `disconfirm` →
**`pressure-test`** (α/β); `market-map` → **`kill-scan`** (complaint-mining) + **`market-sizing`**
(sizing/buyer/trends); `solution-design` + `idea-stage-exit` → **`startup-brief`**. All four
replacement skills are live.

## Declared vs derived — the state-audit (the dashboard's drift alarm)

Two layers, reconciled on every dashboard render:

- **Declared**: `STATE.md` frontmatter — `current_step` / `step_name` / `status` / `owner` /
  `next_action` / `gates:`. Machine-readable; hooks, gates and the board depend on it.
- **Derived**: the **latest artifact present** in `ideas/<slug>/` maps to a step (table below);
  the **next action** is the step whose entry-guard is now satisfied.

`derived_step ≠ declared current_step` ⇒ **a drift alarm (render the row red)**. STATE gains
machine-readability without losing the original "no status file can silently rot" insurance.
Likewise, every `gates:` entry should reconcile with a `decision-log.md` DL-entry and a
`gates/criteria-g*.yaml` file (the W5 ledger-audit checks this three-way).

### Artifact → step derivation (for the derived layer)

`poc/reactions.md` → step 9 (done / looping) · `startup-brief.md` → step 8 done, next: build-poc (if
GO) · `market-sizing.md` → step 7 done, next: startup-brief · `pressure-report-beta.md` → step 6 done,
next: market-sizing · `customer-discovery.md` → step 5 done, next: pressure-test --beta ·
`customer-discovery/kill-criteria.json` (no synthesis yet) → step 5, next: run interviews then
customer-discovery-synthesis · `pressure-report-alpha.md` → step 4 done, next:
customer-discovery-design · `kill-scan.md` → step 3 done, next: pressure-test · `hypothesis.md` → step
2 done, next: kill-scan · only a scaffolded folder (`STATE.md` + `seed.md`, no `hypothesis.md`) → step
1 done, next: sharpen-hypothesis.

## Gate mechanics (read-only here; the script enforces)

Gates are written **ONLY** by `uv run scripts/advance_gate.py --slug <slug> --gate gN [--attest <id>]`
(Constitution Hard Rule #6). The script: validates the artifact (its pytest validator) → checks the
**locked** `criteria-gN.yaml` line by line → confirms `locked_at` predates the evidence → enforces
**lock-ahead** (`criteria-g(n+1).yaml` locked; g9 exempt) → appends the decision-log → writes STATE →
self-checks with `test_state`. Hand-editing the `gates:` block is denied by the `gates_guard` hook.

## Handoff frontmatter (the thin contract each artifact carries)

Each step writes ONE artifact whose **YAML frontmatter** the next step's entry-guard parses; the body
is the human-readable detail. Keep frontmatter thin (scalars + pointers); rich content lives in the
body; mechanically-scored data is the only `.json`.

| Artifact | Frontmatter fields |
|---|---|
| `hypothesis.md` | `stage, status, who, how_often, how_severe, status_quo, value_hypothesis, growth_hypothesis` |
| `kill-scan.md` | `stage, status, disqualifiers[], demand_signal, complaint_sources[]` |
| `pressure-report-alpha.md` | `stage, status, p_agg, open_assumptions[], interview_questions[]` |
| `customer-discovery/cowork-runpack.md` | `stage, status, reachable, sealed: true` |
| `customer-discovery.md` | `stage, status, verdict (CONTINUE\|PIVOT\|KILL\|KEEP-DISCOVERING), tripped[], round` |
| `pressure-report-beta.md` | `stage, status, recommendation (go\|pivot\|kill), resolved_predictions[]` |
| `market-sizing.md` | `stage, status, som, buyer, trends[]` |
| `startup-brief.md` | `stage, status, decision (GO\|NO-GO), drift_rows[], exit_criteria_met` |
| `poc/reactions.md` | `stage, status, archetype, direction (keep\|pivot\|redraw)` |

## Loop-backs (BML is a loop)

- `customer-discovery-synthesis` verdict **PIVOT** → re-enter `sharpen-hypothesis` (or `generate-ideas`
  for a customer-segment pivot); log the pivot type + decrement runway in `learning-log.md`.
- **KILL / INVALIDATED** → drop, or promote another `slate.md` idea.
- `pressure-test --beta` (G6) is the **main kill decision**; `build-poc` reactions **pivot / redraw** →
  back to `sharpen-hypothesis` or `startup-brief`.

## Kill philosophy

The desk almost never kills — it produces context + interview questions; the **founder** decides
advance/pivot/persevere. The only **desk** kill is a hard, checkable fact at `kill-scan` (legality /
technical impossibility), and even that is a founder-stamped override. Subjective merit dies only to
real users (steps 5–6) + the founder's signature. `p_success` is a calibration prediction, **never a
verdict**.
