# Assumption Ranking — leverage × uncertainty → riskiest-assumption-tests

The Playbook's named exercise: *identify the three assumptions the design depends on most heavily, then
ask what would have to be true for each.* In lean terms each is a **riskiest-assumption-test (RAT)** — and
the cheapest test of each top assumption becomes a direct input to the MVP stage. Read this in Step 5.

The scariest move a founder makes here is quietly **demoting** the assumption they can't defend so it
never reaches the top 3. The ranking is therefore mechanical: you score, the script ranks. You can't fudge
the order by vibes (mirrors `/customer-discovery`'s `score_criteria.py`).

## The two axes (both 1–5)

- **Leverage (impact if wrong):** how much of the concept collapses if this assumption is false.
  `1` = a detail you'd patch; `5` = the whole concept is dead.
- **Uncertainty (how unknown):** how unvalidated this assumption is *right now*, given the evidence.
  `1` = discovery directly confirmed it; `5` = no evidence either way, or evidence points against it.

`score = leverage × uncertainty` (max 25). The **riskiest** assumptions — high on both — are the ones the
MVP must test first. An assumption with leverage 5 / uncertainty 1 is load-bearing but already validated:
important, not risky. One with leverage 5 / uncertainty 5 is where the company lives or dies unknown.

## `assumptions.json` schema (you assemble it, the script ranks it)

Include **every material assumption** — yours from crystallizing the concept AND the ones the blind
`solution-red-team` generated. Mark the source so the ranker can flag an adversary-raised assumption that
reaches the top 3 (an assumption you never listed is among your riskiest — a loud signal).

```json
{
  "slug": "personalized-ai-digest",
  "assumptions": [
    {
      "id": "wtp-senior-eng",
      "statement": "Staff+ engineers will pay for a private-signal digest the labs can't replicate",
      "leverage": 5,
      "uncertainty": 4,
      "source": "agent",
      "what_would_have_to_be_true": "≥X% of the narrowed segment pays after a free trial, not just intends to",
      "evidence": "2/10 ever paid, both senior — customer-discovery.md (boundary CLEAR, skewed)",
      "cheapest_test": "Paywalled private beta to 20 staff+ engineers; measure paid conversion"
    },
    {
      "id": "data-onboarding",
      "statement": "Senior engineers will actually upload repo/notebook signal to a startup",
      "leverage": 5,
      "uncertainty": 5,
      "source": "adversary",
      "what_would_have_to_be_true": "Target users connect a real data source in onboarding, not just say they would",
      "evidence": "Two of three who named the signal said they'd never upload it — customer-discovery.md",
      "cheapest_test": "Concierge onboarding with 5 users; measure how many connect a live source"
    }
  ]
}
```

- `leverage`, `uncertainty`: values in [1,5] (the script warns and clamps anything out of range).
- `source`: `agent` (you raised it), `adversary` (the blind red-team raised it), or `both`.
- `what_would_have_to_be_true`, `evidence`, `cheapest_test`: prose; carried into the card's table.

## Running the ranker

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/rank_assumptions.py" ideas/<slug>/startup-brief/assumptions.json
```

It prints JSON: the full ranked list (with `score` and `featured`), the `top_3` ids, and
`adversary_in_top_3` (adversary-sourced assumptions that reached the top 3). Put the top 3 in the card's
table with their `cheapest_test` as the **MVP RAT** column; list the rest below the table. If
`adversary_in_top_3` is non-empty, call it out in the Challenge section — it is a reconciliation finding.

## Tie-breaking

The script breaks ties by leverage (desc), then uncertainty (desc), then input order (stable) — so a
high-impact assumption ranks above an equal-score high-uncertainty-low-impact one. Don't re-order by hand.
