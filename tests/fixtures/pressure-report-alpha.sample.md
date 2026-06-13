---
stage: pressure_alpha
status: report
p_agg: 0.34
p_distribution: {thiel: 0.30, eisenmann: 0.28, munger: 0.44}
open_assumptions: ["manual reconciliation costs >=2h/month", "no tool already owns this workflow", "broker will pay >=HK$500/mo", "compliance allows third-party access", "a solo founder can reach this niche"]
fatal_flag: none
predictions_locked: true
token_estimate: "47k"
---

# Pressure-test α — hk-broker-recon

The right risks to go trip-or-clear with real people, and a calibrated read of how the panel sees the
odds. **Nothing here kills.** Every subjective objection is an OPEN assumption to test; `p_success` is a
prediction logged for calibration, not a screen.

## Calibration — p_success

| Persona | Independent p | Cross-exam p | Revision note | Base-rate ref |
|---|---|---|---|---|
| thiel | 0.28 | 0.30 | raised after Munger's distribution point | vertical SaaS seed survival |
| eisenmann | 0.25 | 0.28 | — | false-start pattern base rate |
| munger | 0.40 | 0.44 | — | toll-bridge workflow lock-in |

**p_agg:** `0.34` — read as "the panel's calibrated guess at the odds going into discovery", logged to
`predictions.jsonl`. Not a go/no-go.

## Ranked risks

1. **Willingness to pay unproven** — eisenmann · brokers may absorb the pain rather than pay · status: `OPEN`
2. **Incumbent spreadsheet inertia** — thiel · Excel is free and good-enough · status: `OPEN`
3. **Compliance wall** — munger · third-party data access may be barred · status: `OPEN`

## Open assumptions → interview questions

5–8 rows. Each is the load-bearing belief that, if false, the idea breaks — phrased so a real user's
past behaviour can disprove it.

| # | Assumption (what would have to be true) | From | Mom-Test question (past behaviour) |
|---|---|---|---|
| 1 | Manual reconciliation costs >=2h each month-end | eisenmann | tell me about the last month-end close — what did you actually do? |
| 2 | No existing tool already owns this workflow | thiel | what did you try before settling on your current setup? |
| 3 | A broker will pay >=HK$500/mo to remove it | eisenmann | when did you last pay for a tool to save admin time — how much? |
| 4 | Compliance permits third-party reconciliation access | munger | walk me through how an outside vendor got data access last time |
| 5 | A solo founder can reach this niche without a sales team | thiel | how did you find the last back-office tool you adopted? |

## Steelman & change-my-mind (read every row before signing)

| Persona | Strongest reason it works (steelman) | What would change my p (change_my_mind) |
|---|---|---|
| thiel | a real toll-bridge workflow once embedded | seeing 3 brokers who already hacked their own scripts |
| eisenmann | acute recurring pain at a fixed calendar moment | a broker paying real money in week one |
| munger | switching cost rises with reconciled history | a single compliance officer green-lighting access |

## Competitor steelman

The single most dangerous competitor: **incumbent Excel templates**. They are free, trusted, and already
in every workflow. Full case: `disconfirmation/competitor-steelman.md`.

## Closed by fact (only hard, checkable facts close an objection)

- "Reconciliation is legally prohibited for third parties" — **closed:** none; SFC rules permit licensed
  data processors with consent (no hard wall found).

## Fatal-flaw flag (if any)

`none` — no illegal or demand-provably-negative issue established with cited objective evidence.

## Cost

Fan-out: 3 seats × 2 rounds + competitor-steelman + judge ≈ `47k`.
