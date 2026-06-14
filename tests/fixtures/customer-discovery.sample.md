# Customer Discovery: hk-broker-recon

> **This Read scores real interview evidence against the kill criteria pre-registered in the
> G4-locked kill-criteria.json BEFORE collecting data. Thresholds are locked. n is small — read the caveats.
> "They said they'd pay" is not willingness-to-pay; only behaviour counts.**

## Discovery Read — Round 1 (2026-06-10, n=9)
**CONTINUE** — the month-end reconciliation pain is real and recurring across small HK brokerages, and
two prospects already pay a part-timer to do it by hand. No criterion tripped; willingness-to-pay is the
open question carried into Round 2.

## Kill-Criteria Scorecard
*(Statuses verbatim from `scripts/score_criteria.py` against the locked `kill-criteria.json`.)*

| Criterion (from kill-criteria.json) | Threshold (LOCKED) | Evidence | n | Status |
|---|---|---|---|---|
| Pain is recurring, not one-off | <30% recurring → trip | 7/9 reconcile every close | 9 | CLEARED |
| Reconciling by hand today | <40% manual → trip | 8/9 do it in Excel by hand | 9 | CLEARED |
| Would pay for a fix | <10% ever paid → trip | 2/9 already pay a part-timer | 9 | INCONCLUSIVE |
| Decision sits with ops, not IT | qualitative | ops owns the close at 6/9 | 9 | MANUAL |

The willingness-to-pay row is INCONCLUSIVE with `small_sample` — it needs more interviews, not a verdict.
The decision-owner row is MANUAL: at the 9 shops interviewed, the ops/compliance lead owned the close and
the budget; I mark this a judgment, not a count.

## Evidence — two lists
**Supports the hypothesis**
- Month-end close runs 1.5–2 full days, every month — E-019, E-021
- Two shops already pay a part-time bookkeeper just for the close — E-023
- A missed break triggered a regulatory follow-up at one shop last year — E-025

**Challenges the hypothesis**
- One larger shop (8 reps) already has an off-the-shelf tool and no pain — E-027
- "I'd want to see it run a full close before paying" — nobody committed money — E-029

*(The supports list is longer than the challenges list; the Bias-check interrogates whether that asymmetry
is in the data or in the hope.)*

## Coverage & skew
Interviewed by persona: ops/compliance lead 6, owner-operator 2, outsourced bookkeeper 1. Gap: every
willingness-to-pay signal is from owner-operators or the two paying shops, so that denominator is skewed —
zero pure-IT stakeholders reached, which the MANUAL decision-owner row leans on.

## Bias-check (independent agent)
The read pattern-matches to hope on willingness-to-pay: "2/9 already pay a part-timer" is being read as
demand for THIS tool, but those shops pay a human they trust, not software — that is the single most likely
self-deception here. The recurring-pain and manual-today rows are well-evidenced and survive scrutiny. Do
not soften the INCONCLUSIVE row to CLEARED to make the round feel like a win.

## Hypothesis Updates Flagged
- The buyer may be the outsourced bookkeeper, not the in-house ops lead — 3 shops outsource the close
  entirely. Route back through `/sharpen-hypothesis` before Round 2; do not edit hypothesis.md here.

## Override (only if proceeding past a TRIPPED criterion)
*(No criterion TRIPPED this round — no override line.)*

---

## Provenance
- `customer-discovery/kill-criteria.json` — the locked thresholds
- `customer-discovery/interviews/` — the 9 notes scored this round
- `customer-discovery/synthesis/round-1-scoring.json` — per-interview tags (scorer input)
- `customer-discovery/synthesis/round-1.md` — script output + bias-check challenge
