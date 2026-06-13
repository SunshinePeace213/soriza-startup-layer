---
stage: pressure_beta
status: report
recommendation: pivot             # go | pivot | kill — the panel RECOMMENDS; the founder's G6 signature decides
p_agg: 0.0                        # calibration prediction, not a verdict
open_assumptions: ["<a1>", "<a2>"]
predictions_resolved: []          # ids of g4 predictions resolved this run
fatal_flag: none                  # none | illegal | demand_provably_negative (cited)
token_estimate: "<n>k"
---

# Pressure-test β — <slug>

The same founder-blind panel, now run over the Discovery Read. **Every claim cites a ledger `E-xxx`**
(interview-derived claims cite grade ≤2). The panel recommends; the kill decision is the founder's
signature at G6.

## Recommendation

**`<go | pivot | kill>`** — <one-paragraph rationale, each load-bearing claim tagged with its `E-xxx`>.
This is a recommendation for the founder to sign or override, not a desk verdict.

## Calibration — p_success

| Persona | Independent p | Cross-exam p | Revision note | Base-rate ref |
|---|---|---|---|---|
| <thiel> | 0.0 | 0.0 | <…> | <class> |

**p_agg:** `<value>`.

## How the evidence moved the assumptions

| α open assumption | Discovery evidence (E-xxx) | Now: confirmed / killed / still open |
|---|---|---|
| <assumption> | <E-019: quote…> | <…> |

## Resolved α predictions

Appended to `predictions.jsonl` as supplement lines (same id, `resolved_by: pressure-beta`).

| Prediction id | Persona | Claim | p | Outcome | Brier |
|---|---|---|---|---|---|
| p-003 | munger | <claim> | 0.55 | true/false | 0.0 |

## Ranked residual risks → interview questions

For a `pivot` / `keep-discovering` outcome: the assumptions still OPEN, each with its next question.

| # | Assumption | From | Mom-Test question | Cite |
|---|---|---|---|---|
| 1 | <…> | <lens> | <…> | <E-xxx> |

## Fatal-flaw flag (if any)

`<none>` — or `<illegal | demand_provably_negative>` with cited objective evidence.

## Cost

Fan-out ≈ `<token_estimate>`.
