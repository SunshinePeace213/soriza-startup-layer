# Kill-Criteria Anchoring

The thing that makes this skill different from a generic interview-guide generator: **discovery exists
to trip-or-clear the kill criteria the founder pre-registered in `pressure-test.md`** — not to "learn
about users" in the abstract. So every interview question anchors to a specific criterion, and every
synthesis scores real behaviour against a *locked* threshold.

## The anchoring pattern

For each Kill Criterion / Disconfirmation Question in `pressure-test.md`, build:

```
CRITERION (verbatim from pressure-test.md)
  → PAST-BEHAVIOUR QUESTION   (queries a concrete past event, never a hypothetical future)
  → TRIP-THRESHOLD            (the pre-registered number that decides TRIPPED vs CLEARED)
  → DEFLECTION PROBE          (the follow-up for the dodge this question usually draws)
```

Worked examples (from the `personalized-ai-digest` pressure-test — use the founder's real file):

> **Criterion:** *"No willingness-to-pay against free — if <10–20% will pay any non-zero price → abandon."*
> **Question:** *"Tell me about the last time you paid for something to keep up with AI — a course, a newsletter, a tool. What pushed you to actually put a card in?"*
> **Threshold:** ever-paid proportion `<10%` → TRIPPED; `≥20%` → CLEARED; in between → INCONCLUSIVE.
> **Probe (on the dodge "I'd pay for the right thing"):** *"Set aside what you'd pay for — what did you actually pay for, most recently?"*

> **Criterion:** *"Behaviour is identity/FOMO, not need."*
> **Question** (Disconfirmation Q1): *"Walk me through what you actually did in the last 7 days to keep up with AI — did you try a tool or ship something, or only read?"*
> **Threshold:** took-concrete-action proportion `<30%` → TRIPPED (it's FOMO); `≥30%` → CLEARED.
> **Probe:** *"What was the most recent thing you read about and then actually used? When?"*

The non-negotiable framing rule: **query the relevant past, not the imagined future.** "Would you use…",
"do you think you'd…", "how likely are you to…" all produce socially-desirable noise. "Tell me about the
last time…" produces behaviour. (See `mom-test-audit.md`.)

## `kill-criteria.json` — write once, then locked

Encode each criterion once in Step D2. After interview data exists, **never edit a threshold** — that is
the goalpost-moving this whole design prevents. Pick the scoring `type` from how `pressure-test.md` phrases
the kill:

| Pressure-test phrasing | `type` | Fields |
|---|---|---|
| "if **<X%** [do a supporting thing] → abandon" | `support_proportion` | `field`, `clear_at`, `trip_below`, `min_n` |
| "if **<N/10** [do a supporting thing] → abandon" | `support_proportion` (use the rate, e.g. 3/10 → `clear_at`=`trip_below`=0.30) | same |
| "if [a refuting thing] above **X%** → abandon" | `against_proportion` | `field`, `trip_at`, `clear_below`, `min_n` |
| "if the **majority** [refuting thing] → abandon" | `against_majority` | `field`, `min_n` |
| qualitative ("if you cannot name a signal…") | `manual` | — (the model judges in prose) |

**Boundary rule:** a value exactly at `clear_at` resolves **CLEARED** (the test is `p ≥ clear_at`); a
value exactly at `trip_below` is **not** tripped (the test is `p < trip_below`). So for "if <30% → trip",
set `clear_at = trip_below = 0.30`: 30% reads CLEARED, 29% TRIPPED. Set `min_n` explicitly on every
auto-scored criterion — if you omit it the small-sample floor silently drops to 5.

`field` is a short snake_case boolean you will tag per interview. `support_*` fields measure a signal that
*helps* the hypothesis (ever_paid, took_action); `against_*` fields measure a signal that *refutes* it
(native_suffices). `clear_at == trip_below` collapses the inconclusive band to a single boundary.

```json
{
  "slug": "<slug>",
  "locked_on": "<YYYY-MM-DD>",
  "criteria": [
    {"id": "wtp-against-free", "label": "No willingness-to-pay against free",
     "source": "pressure-test.md Kill Criteria #1",
     "type": "support_proportion", "field": "ever_paid_comparable",
     "clear_at": 0.20, "trip_below": 0.10, "min_n": 8},
    {"id": "fomo-not-need", "label": "Behaviour is FOMO, not need",
     "source": "pressure-test.md Kill Criteria #2",
     "type": "support_proportion", "field": "took_concrete_action",
     "clear_at": 0.30, "trip_below": 0.30, "min_n": 8},
    {"id": "native-good-enough", "label": "Native personalization is good enough",
     "source": "pressure-test.md Kill Criteria #3",
     "type": "against_majority", "field": "native_suffices", "min_n": 8},
    {"id": "no-capturable-signal", "label": "No capturable signal the labs lack",
     "source": "pressure-test.md Kill Criteria #4", "type": "manual"}
  ]
}
```

## `scoring.json` — the per-interview tags (Step S2)

For each interview, read the transcript and judge the **behaviour**, not the stated intention, for each
criterion's `field`. A tag you can't determine from the transcript is omitted (null) — the scorer drops
it from that criterion's denominator rather than guessing.

```json
{
  "n_total": 12,
  "interviews": [
    {"id": "2026-06-12-jane-pm-acme", "persona": "PM",
     "tags": {"ever_paid_comparable": false, "took_concrete_action": true, "native_suffices": false}},
    {"id": "2026-06-13-li-dev-foo", "persona": "developer",
     "tags": {"ever_paid_comparable": true, "took_concrete_action": true}}
  ]
}
```

Write this to `docs/ideas-stages/<slug>/customer-discovery/synthesis/round-<N>-scoring.json`, then run
`scripts/score_criteria.py docs/ideas-stages/<slug>/customer-discovery/kill-criteria.json docs/ideas-stages/<slug>/customer-discovery/synthesis/round-<N>-scoring.json`
(Step S3 — pass full `docs/ideas-stages/<slug>/…` paths; the script runs from the repo root). It applies each locked threshold and returns per-criterion `TRIPPED` / `CLEARED` /
`INCONCLUSIVE` / `MANUAL` / `ERROR`, a `small_sample` flag when `n_scored < min_n`, and a per-persona
`coverage` breakdown (**interview-only — it does not read the prospects CSV**). `MANUAL` criteria you
judge in prose and mark explicitly; an `ERROR` row means this JSON is malformed for that criterion
(missing/typo'd threshold) — fix it and re-run, don't hand-grade around it. The script's statuses go into
the Read's scorecard **verbatim** — don't re-grade them by eye.

**`min_n` is pooled, not per-persona.** The scorer pools every interview across all personas for a
criterion's denominator; coverage skew is reported separately so you can judge whether a pooled number is
carried by one persona. So a multi-persona round needs more *total* interviews than any single persona
before a criterion clears `small_sample` — your "come back at ~5" is the first synthesis, and criteria
typically read `INCONCLUSIVE` until the pooled `n` clears `min_n`.
