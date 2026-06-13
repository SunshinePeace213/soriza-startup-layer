---
stage: pressure_beta
status: report
recommendation: pivot
p_agg: 0.4
open_assumptions: ["Brokers will pay >=HK$500/mo once the pilot ends", "The pull is month-end close, not continuous reconciliation"]
predictions_resolved: ["p-003"]
fatal_flag: none
token_estimate: "180k"
---

# Pressure-test β — hk-broker-recon

The same founder-blind panel, now run over the Discovery Read. Every claim cites a ledger entry;
interview-derived claims cite grade ≤2. The panel recommends; the kill decision is the founder's
signature at G6.

## Recommendation

**`pivot`** — the reconciliation pain is real and someone paid for it: one broker spends 6–8h every
month-end on manual reconciliation (E-019) and has committed money to a concierge pilot (E-023). But the
α framing was wrong about *when* the pain bites — it is the two-day month-end close, not continuous daily
reconciliation, and competitor complaints cluster on the same close window (E-007). Pivot the wedge to a
month-end close assistant before scaling. This is a recommendation for the founder to sign or override,
not a desk verdict.

## Calibration — p_success

| Persona | Independent p | Cross-exam p | Revision note | Base-rate ref |
|---|---|---|---|---|
| thiel | 0.30 | 0.35 | raised after the paid-pilot commitment | vertical-SaaS seed survival |
| munger | 0.45 | 0.45 | — | SMB bookkeeping tools |
| bezos | 0.40 | 0.42 | slight raise on retention signal | workflow-tool adoption |

**p_agg:** `0.4` — a calibration prediction logged to `predictions.jsonl`, not a go/no-go.

## How the evidence moved the assumptions

| α open assumption | Discovery evidence (E-xxx) | Now: confirmed / killed / still open |
|---|---|---|
| Brokers spend ≥2h/wk on manual reconciliation | E-019: "those last two days of the month, I basically do nothing else" | confirmed (but concentrated at month-end) |
| They will pay ≥HK$500/mo for automation | E-023: agreed to a two-week concierge pilot at HK$500 | confirmed for the pilot, open at scale |
| Reconciliation errors drive competitor churn | E-007: competitor's top-three unresolved complaints all concern reconciliation | still open (review proxy, not interview) |

## Resolved α predictions

Appended to `predictions.jsonl` as supplement lines (same id, `resolved_by: pressure-beta`).

| Prediction id | Persona | Claim | p | Outcome | Brier |
|---|---|---|---|---|---|
| p-003 | munger | ≥3 of 10 interviewed brokers spent ≥2h on manual reconciliation in the last 30 days | 0.55 | true | 0.2025 |

## Ranked residual risks → interview questions

The assumptions still OPEN, each with its next past-behaviour question.

| # | Assumption | From | Mom-Test question | Cite |
|---|---|---|---|---|
| 1 | WTP holds beyond a subsidised pilot | lean-startup | "Tell me about the last back-office tool you renewed at >HK$500/mo — what made you keep paying?" | E-023 |
| 2 | The error-churn link is real, not a review artefact | competitor-steelman | "Walk me through the last time a reconciliation error cost you a client." | E-007 |

## Fatal-flaw flag (if any)

`none` — no legality or technical-feasibility wall surfaced; the open assumptions are demand/WTP risks the
founder tests with more close-window interviews.

## Cost

Fan-out: 5 seats × 2 rounds + competitor-steelman + judge ≈ `180k`.
