# Verification report: prompt-architect "dynamic-workflow sense" upgrade

Verified by two dynamic-workflow runs (dogfooding the capability the upgrade teaches).
Design contract: `prompt-architect-dynamic-workflows.md`.

## Round 1 — full verification (`verify-dynamic-workflow-sense`, 16 agents)

**Phase 1 — decision accuracy (12 labeled "build X" scenarios, deterministic scoring):**

| Metric | Result |
|---|---|
| Workflow-warranted accuracy | **12/12** |
| Shape accuracy | **12/12** |
| **False-positive workflow** (the #1 risk) | **0** |
| False-negative workflow | 0 |
| Misroutes | none |

The trap near-misses all routed correctly: `pr-review-3files` (3–4 files, parallelism without a
load-bearing signal) → **inline, not a workflow**; `refactor-2-callsites` → **just do it**;
`security-subagent` (tool/model/memory) → **subagent, not a workflow**; `adhoc-codebase-qa`
(shape varies run-to-run) → **ad-hoc emit, not a saved workflow**.

**Phase 2 — adversarial content review (3 independent skeptics):** all three found the
conservative-bar and §5/opt-in axis **genuinely clean** — the reference reinforces default-inline
rather than over-recommending. Findings landed in the *authoring* half only.

**Verdict: `go-with-fixes`.** Five must-fixes, all authoring-half quality/consistency defects
(none moved a routing decision):

1. **Tip-1 self-contradiction** — the Gotchas section re-taught `Workflow`-spec mechanics the file said it wouldn't restate.
2. **Rung-4 self-contradiction** — "standalone / no user-facing trigger" exemplars (`artifact-eval`, `description-optimize`) are actually called by name from prompt-architect's body.
3. **Ad-hoc-emit skipped the opt-in gate** — cost-legibility was written only for the fronted case.
4. **Repeated constraints** — meta pure-literal stated 3×, filesystem prohibition 2×.
5. **Missing ladder gate** — no reminder that rungs 2–4 require the bar + opt-in *first*.

## Fixes applied

All five must-fixes + two calibration nice-to-haves (rung-1 "bar not met" annotation; multi-stage
signal qualified by scale). Gotchas collapsed to a spec pointer; rung 4 redefined as
"invoked by name as an internal step from another skill/workflow's body"; rung 2 + the general
cost-legibility line brought inside the opt-in gate; constraints de-duplicated; ladder gate added.

## Round 2 — re-verification (`reverify-dynamic-workflow-sense`, 4 agents)

3 fresh skeptics re-checked each must-fix against the edited text + hunted regressions; synthesis
returned a verdict.

**Verdict: `merge-with-trivia`.** 3/5 must-fixes resolved unanimously (Rung-4, ad-hoc opt-in,
ladder gate); 2 "partial" — cosmetic de-dup residue (a forbidden-call parenthetical; the
filesystem example stated twice). **No correctness/contradiction defects; no high/medium
regressions.** The only ≥2-skeptic new finding was a low-severity over-repetition of the opt-in
rule, called non-blocking and partly deliberate.

## Post-round-2 tightening (applied)

- Dropped the literal banned-call names from the Failure-modes parenthetical (closes the Tip-1 residue).
- Gave the filesystem prohibition a single home (do-not-use bar) + a back-reference from Failure-modes (closes the 2× residue).
- Narrowed the ladder gate so it no longer overstates item/stage-count as "among-rung only" (item-count *is* a bar signal).
- Cross-ref label for `artifact-eval` updated off the retired "standalone" wording.

Net: the decision sense is verified perfect (12/12, 0 false positives) and the reference is
internally consistent after tightening. `quick_validate` → "Skill is valid!"
