# Startup Brief: hk-broker-recon

> Crystallizes, challenges, and stamps GO/NO-GO on the concept the validated evidence supports.
> The design must serve the problem DISCOVERY revealed — not the one the hypothesis ASSUMED.
> n is small (6 interviews); read the caveats.

## Decision

**GO** — the validated problem is real and narrowly specific (back-office ops at small HK
brokers, not the front-office traders the hypothesis assumed), the wedge serves the *validated*
job, and no G5/G6 kill-criterion tripped. Proceed to a PoC of the reconciliation-diff wedge.

## The Validated Problem

- **Who** — back-office operations staff at sub-50-headcount HK brokerages (NOT the traders the
  hypothesis first named). 4 of 6 interviewed (E-021, E-024, E-031, E-033).
- **How often** — daily, at T+1 settlement close. 3 of 6 spend ≥2h/day (E-022, E-031).
- **How severe** — a single missed break can trigger an SFC reportable error; two interviewees
  named a past fine (E-034, grade-2 quote).
- **Status quo** — Excel macros + a shared mailbox; one shop pays a part-timer just to reconcile
  (E-024, a grade-1 time commitment).

## The Solution Concept

- **Wedge** — a reconciliation-diff tool that ingests the broker's trade blotter + the clearing
  house file and flags only the *breaks*, ranked by SFC-reportability.
- **Validated who** — back-office ops leads at small HK brokers (narrowed from "brokers").
- **Core job it owns** — find-and-rank the settlement breaks before T+1 close.
- **What it deliberately does NOT do** — no trade booking, no front-office P&L, no auto-correction
  (read-only diff; the human still resolves the break).
- **Why it wins** — owned distribution via the founder's ex-clearing-desk network (E-005,
  founder-profile) + a data-access wedge incumbents price out of the small-broker segment.

## Drift Audit — assumed → validated

*(Baseline = original hypothesis.md + accumulated flagged deltas from kill-scan / pressure-report-alpha /
customer-discovery / pressure-report-beta, applied — see `startup-brief/validated-baseline.md`. Measured
against the reconstruction, never the stale hypothesis.md.)*

| Originally assumed (hypothesis.md) | What validation revealed (reconstructed baseline) | Serves the VALIDATED problem? |
|---|---|---|
| Front-office traders feel the recon pain | Traders delegate it; ops staff own it (E-021, E-031) | ✅ serves it — wedge now targets ops leads |
| Pain is the time cost (~2h/day) | The *fear* is the SFC-reportable error, not the hours (E-034) | ⚠️ drifting — ranking by reportability, but priced on time saved |
| They want full auto-reconciliation | They will not let a tool auto-correct a regulated record (E-033) | ✅ serves it — read-only diff, human resolves |
| Greenfield: no incumbent at this tier | A legacy vendor exists but prices out <50-head shops (E-041, market-sizing.md) | ✅ serves it — small-broker wedge is the gap |

Any ❌ or accumulation of ⚠️ pushes the decision toward NO-GO/redesign — stated, not laundered.

## Three Load-Bearing Assumptions

*(Top 3 of all material assumptions, ranked by leverage × uncertainty — statuses verbatim from
`scripts/rank_assumptions.py`. Adversary-raised assumptions that reached the top 3 are flagged.)*

| # | Assumption | Why load-bearing (what collapses if false) | What would have to be true | Current evidence (cited) | Cheapest test → PoC RAT |
|---|---|---|---|---|---|
| 1 | Ops leads will connect a live clearing-house file to a startup tool | No data → no diff → no product | ≥3/5 PoC users connect a real file, not a sample | 2/6 said they'd never share the raw file (E-033) — **adversary-raised** | Concierge onboarding; count live connections |
| 2 | Ranking by SFC-reportability is the value, not hours saved | Mispriced wedge; sells time when they buy risk-cover | Users act on the reportability rank first | severity quote E-034; not yet behaviourally confirmed | PoC: which break do they open first? |
| 3 | The founder's clearing-desk network is durable distribution | The whole GTM thesis | ≥2 warm intros convert to a PoC slot | 3 warm intros booked (E-005, E-007) | Already partly cleared |

Full ranked list below the top 3: see `startup-brief/assumptions.json`.

## Alternatives Considered

- **A spreadsheet template** — cheaper, but can't ingest the clearing file or rank by reportability;
  it's the status quo they already hate.
- **Sell to the clearing house, not the brokers** — bigger TAM, but a 12-month enterprise sale the
  founder can't fund. Rejected for the wedge; revisited at scale.

## Scale Conditions

- **Distribution** — the 1000th broker can't come from warm intros; needs an SFC-compliance-channel
  partnership or a clearing-house referral. Unproven.
- **Unit economics** — per-shop ACV is low (~HK$2k/mo); only works if onboarding is near-zero-touch.
- **Defensibility** — the diff logic is copyable; the moat is the data-access relationship + the
  reportability ruleset, which must stay ahead of the legacy vendor moving down-market.

## Challenge (independent blind solution-red-team)

The blind red-team (`startup-brief/red-team.md`) surfaced one assumption the draft missed —
**data-onboarding willingness** (now assumption #1, flagged adversary-raised) — and one drift the
draft under-weighted: the concept is still *priced* on hours-saved while discovery showed they buy
risk-cover (the ⚠️ row). Its single named self-deception: *"warm intros booked"* is being read as
*distribution solved* when it only clears the first 3 users, not the 1000th. Reconciliation gaps
folded into assumptions #1 and the scale section above; not softened.

## Premortem (Eisenmann six-pattern checklist)

It's 18 months later and this failed. Which pattern killed it?

1. **Good Idea, Bad Bedfellows** — solo founder, ex-clearing-desk; founder-market fit is strong. No
   co-founder conflict risk yet, but a compliance-domain hire is missing — low risk now.
2. **False Starts** — *mitigated*: 6 interviews ran before any build; this brief is the discovery gate.
3. **False Positives** — the live risk: 3 warm intros are friendly early adopters; mistaking their
   delight for the mainstream small-broker segment. PoC must test a cold (non-network) shop.
4. **Speed Trap** — not yet relevant (pre-scale); revisit at the MVP layer.
5. **Help Wanted** — the compliance/regulatory hire and the data-partnership are the senior gaps that
   would bite at scale; named now so they're not a surprise.
6. **Cascading Miracles** — needs two things to both land: data-onboarding willingness AND durable
   distribution. ~0.5 × ~0.5 ≈ 0.25, not 0.5 — the honest combined odds, surfaced not hidden.

## Exit-Criteria Check (the three)

1. **Is the problem real & specific?** — Yes. Back-office ops at <50-head HK brokers, daily at T+1,
   ≥2h/day for half, with a named regulatory fear (E-022, E-031, E-034).
2. **Does the solution address the VALIDATED problem?** — Yes, per the drift audit: read-only,
   reportability-ranked diff for ops leads. One ⚠️ (pricing) carried into the PoC, not ignored.
3. **Is there enough signal to justify building?** — A reasoned bet, not certainty: 3 grade-1/2
   commitments, no tripped kill-criterion, the data-onboarding RAT still open. Enough to PoC, not yet
   to scale.

## PoC Kill-Criteria (locked → G9)

The pre-registered criteria the PoC is scored against. Locked write-once in `gates/criteria-g9.yaml`
(lock-ahead — locked before this G8 stamp). Never softened after the PoC runs.

- **g9-1** — ≥3 of 5 PoC users connect a *live* clearing-house file (not a sample) in concierge
  onboarding. (Tests assumption #1; a miss = data-onboarding kills the wedge.)
- **g9-2** — ≥3 of 5 open the top reportability-ranked break first. (Tests assumption #2 — risk-cover,
  not hours.)
- **g9-3** — ≥1 of the 5 is a cold (non-network) shop, to test the False-Positive risk.
- **g9-4** — all open α/β predictions resolved.

## PoC Brief (forward contract → step 9)

- **Wedge** — read-only reconciliation-diff, breaks ranked by SFC-reportability.
- **Prioritized riskiest-assumption-tests** — (1) live-file onboarding, (2) reportability-first
  behaviour, (3) cold-shop adoption — in rank order.
- **Validated profile** — back-office ops leads at sub-50-head HK brokerages.
- **Non-goals** — no booking, no auto-correct, no front-office P&L.
- **Archetype hint** — Wizard-of-Oz concierge onboarding is enough to test g9-1/g9-2 cheaply.

## Hypothesis Updates Flagged

Route to `/sharpen-hypothesis` — do NOT edit hypothesis.md here.

- WHO narrows from "brokers" to "back-office ops leads at <50-head HK brokers" (E-021, E-031).
- SEVERITY reframes from time-cost to SFC-reportability fear (E-034).

## Override

*(Only when a kill-criterion tripped and the founder proceeds anyway. None tripped here.)*
None.

---

## Provenance

- `startup-brief/delta-ledger.md` — every flagged delta + Discovery verdict + tripped criteria, verbatim (script output)
- `startup-brief/validated-baseline.md` — the reconstructed problem the drift audit measures against
- `startup-brief/assumptions.json` — per-assumption leverage/uncertainty scores (ranker input)
- `startup-brief/red-team.md` — the blind solution-red-team's raw challenge
- `startup-brief/reconciliation.md` — draft vs blind adversary; gaps surfaced
