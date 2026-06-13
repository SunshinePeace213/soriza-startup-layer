---
stage: pressure_alpha
status: report
p_agg: 0.0                         # aggregated calibration prediction — NEVER a verdict
p_distribution: {}                 # {persona: p_success} after the cross-exam round
open_assumptions: ["<a1>", "<a2>", "<a3>", "<a4>", "<a5>"]   # 5–8, each with a question below
fatal_flag: none                   # none | illegal | demand_provably_negative (cited; founder weighs, not killed)
predictions_locked: false          # true once one line per persona is in predictions.jsonl
token_estimate: "<n>k"             # fan-out cost for this run
---

# Pressure-test α — <slug>

The right risks to go trip-or-clear with real people, and a calibrated read of how the panel sees the
odds. **Nothing here kills.** Every subjective objection is an OPEN assumption to test; `p_success` is a
prediction logged for calibration, not a screen.

## Calibration — p_success

| Persona | Independent p | Cross-exam p | Revision note | Base-rate ref |
|---|---|---|---|---|
| <thiel> | 0.0 | 0.0 | <why revised, or —> | <class> |
| … | | | | |

**p_agg:** `<value>` — read as "the panel's calibrated guess at the odds going into discovery", logged to
`predictions.jsonl`. Not a go/no-go.

## Ranked risks

1. **<risk>** — <expert/lens> · <the objection, one line> · status: `OPEN` | `closed-by-fact`
2. …

## Open assumptions → interview questions

5–8 rows. Each is the load-bearing belief that, if false, the idea breaks — phrased so a real user's
past behaviour can disprove it.

| # | Assumption (what would have to be true) | From | Mom-Test question (past behaviour) |
|---|---|---|---|
| 1 | <assumption> | <lens> | <"tell me about the last time you…"> |

## Steelman & change-my-mind (read every row before signing)

| Persona | Strongest reason it works (steelman) | What would change my p (change_my_mind) |
|---|---|---|
| <thiel> | <…> | <…> |

## Competitor steelman

The single most dangerous competitor: **<name>**. <one-line why they win>. Full case:
`disconfirmation/competitor-steelman.md`.

## Closed by fact (only hard, checkable facts close an objection)

- <objection> — **closed:** <legality / technical feasibility fact + source>, or "none".

## Fatal-flaw flag (if any)

`<none>` — or `<illegal | demand_provably_negative>` with **cited objective evidence** (surfaced for the
founder to weigh at G4; never a desk kill).

## Cost

Fan-out: <N seats × 2 rounds + steelman + judge> ≈ `<token_estimate>`.
