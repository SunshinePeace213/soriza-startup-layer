# Kill-Criteria Anchoring

The thing that makes this synthesis different from eyeballing transcripts: **discovery exists to
trip-or-clear the kill criteria the founder pre-registered from the funnel's `disconfirmation-brief.md`**
— not to "learn about users" in the abstract. Each **OPEN assumption** + its matching **interview
question** in that brief becomes one criterion, and every synthesis scores real behaviour against a
*locked* threshold.

## The anchoring pattern

For each OPEN assumption (with its interview question) in `disconfirmation-brief.md`, build:

```
OPEN ASSUMPTION (verbatim from disconfirmation-brief.md open_assumptions[].assumption)
  → INTERVIEW QUESTION        (the brief's matching interview_questions[] entry — already past-behaviour shaped)
  → TRIP-THRESHOLD            (the pre-registered number that decides TRIPPED vs CLEARED)
  → DEFLECTION PROBE          (the follow-up for the dodge this question usually draws)
```

The interview questions in the brief are already Mom-Test / past-behaviour shaped (the disconfirmation
judge built them that way). Your job in synthesis is to attach a **trip-threshold** to each and score
behaviour against it — not to redesign the question.

Worked examples (for an `personalized-ai-digest`-style idea — use the founder's real brief):

> **Open assumption:** *"What would have to be true: users will pay a non-zero price against free
> alternatives."*
> **Interview question (from the brief):** *"Tell me about the last time you paid for something to keep up
> with AI — a course, a newsletter, a tool. What pushed you to actually put a card in?"*
> **Threshold:** ever-paid proportion `<10%` → TRIPPED; `≥20%` → CLEARED; in between → INCONCLUSIVE.
> **Probe (on the dodge "I'd pay for the right thing"):** *"Set aside what you'd pay for — what did you actually pay for, most recently?"*

> **Open assumption:** *"What would have to be true: the behaviour is driven by real need, not identity/FOMO."*
> **Interview question (from the brief):** *"Walk me through what you actually did in the last 7 days to keep up with AI — did you try a tool or ship something, or only read?"*
> **Threshold:** took-concrete-action proportion `<30%` → TRIPPED (it's FOMO); `≥30%` → CLEARED.
> **Probe:** *"What was the most recent thing you read about and then actually used? When?"*

The non-negotiable framing rule: **query the relevant past, not the imagined future.** "Would you use…",
"do you think you'd…", "how likely are you to…" all produce socially-desirable noise. "Tell me about the
last time…" produces behaviour. (See `mom-test-audit.md`.)

## `kill-criteria.json` — write once, then locked

Encode each criterion once in Step S0. After interview data exists, **never edit a threshold** — that is
the goalpost-moving this whole design prevents. The OPEN assumptions in `disconfirmation-brief.md` are
phrased as "What would have to be true: …" — pick the scoring `type` from what the assumption claims and
the threshold *you* set when locking it:

| What the OPEN assumption claims | `type` | Fields |
|---|---|---|
| "**≥X%** [do a supporting thing] (else it fails)" → trip if **<X%** | `support_proportion` | `field`, `clear_at`, `trip_below`, `min_n` |
| "at least **N in 10** [do a supporting thing]" → use the rate, e.g. 3/10 → `clear_at`=`trip_below`=0.30 | `support_proportion` | same |
| "a refuting thing stays under **X%**" → trip if it goes above | `against_proportion` | `field`, `trip_at`, `clear_below`, `min_n` |
| "the **majority** do NOT [a refuting thing]" → trip if the majority do | `against_majority` | `field`, `min_n` |
| qualitative ("you can name a signal the incumbent lacks…") | `manual` | — (the model judges in prose) |

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
     "source": "disconfirmation-brief.md open assumption #1",
     "type": "support_proportion", "field": "ever_paid_comparable",
     "clear_at": 0.20, "trip_below": 0.10, "min_n": 8},
    {"id": "fomo-not-need", "label": "Behaviour is FOMO, not need",
     "source": "disconfirmation-brief.md open assumption #2",
     "type": "support_proportion", "field": "took_concrete_action",
     "clear_at": 0.30, "trip_below": 0.30, "min_n": 8},
    {"id": "native-good-enough", "label": "Native personalization is good enough",
     "source": "disconfirmation-brief.md open assumption #3",
     "type": "against_majority", "field": "native_suffices", "min_n": 8},
    {"id": "no-capturable-signal", "label": "No capturable signal the labs lack",
     "source": "disconfirmation-brief.md open assumption #4", "type": "manual"}
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

Write this to `ideas/<slug>/customer-discovery/synthesis/round-<N>-scoring.json`, then run
`scripts/score_criteria.py ideas/<slug>/customer-discovery/kill-criteria.json ideas/<slug>/customer-discovery/synthesis/round-<N>-scoring.json`
(Step S3 — pass full `ideas/<slug>/…` paths; the script runs from the repo root). It applies each locked threshold and returns per-criterion `TRIPPED` / `CLEARED` /
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
