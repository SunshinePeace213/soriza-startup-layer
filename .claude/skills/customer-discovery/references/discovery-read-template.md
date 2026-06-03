# Output Template — `customer-discovery.md`

The top-level deliverable: a Discovery Read that scores REAL interview evidence against the LOCKED
kill-criteria thresholds, two-list-style, with an independent bias-check. It is **semi-binding**: the
per-criterion scorecard is mechanical (the script's statuses, verbatim — no relitigating); the overall
call is the founder's soft judgment, with proceeding past a TRIPPED criterion stamped as an override.

Append a new `## Round <N> (<date>)` section each synthesis round rather than overwriting — the founder
watches the read evolve as `n` grows. Keep each section tight.

```markdown
# Customer Discovery: <slug>

> **This Read scores real interview evidence against the kill criteria you pre-registered in
> pressure-test.md BEFORE collecting data. Thresholds are locked. n is small — read the caveats.
> "They said they'd pay" is not willingness-to-pay; only behaviour counts.**

## Discovery Read — Round <N> (<date>, n=<N>)
**<CONTINUE | PIVOT | KILL | KEEP-DISCOVERING>** — 1 line + 1–2 sentences of rationale tied to the
evidence below. Non-binding; if proceeding past a TRIPPED criterion, see the Override line.

## Kill-Criteria Scorecard
*(Statuses verbatim from `scripts/score_criteria.py` against the locked `kill-criteria.json`.)*

| Criterion (from pressure-test.md) | Threshold (LOCKED) | Evidence | n | Status |
|---|---|---|---|---|
| <label> | <e.g. <10% pay → trip> | <2/12 ever paid> | <12> | TRIPPED / CLEARED / INCONCLUSIVE / MANUAL / ERROR |

For each `MANUAL` criterion, judge it in prose here and mark it explicitly as a judgment, not a count.
For each `INCONCLUSIVE` with `small_sample`, say so — it needs more interviews, not a verdict. An `ERROR`
row means `kill-criteria.json` is malformed for that criterion — fix the JSON and re-run rather than
recording a status by hand.

## Evidence — two lists
**Supports the hypothesis**
- <signal> — <interview ids>

**Challenges the hypothesis**
- <signal> — <interview ids>

*(If the supports list is much longer than the challenges list, the Bias-check interrogates whether that
asymmetry is in the data or in the hope — per the Playbook exercise.)*

## Coverage & skew
*(The scorer's `coverage` block is **interview-only** — who you actually interviewed, by persona. If a
`prospects-<date>.csv` snapshot exists, fold in the orthogonal not-reached / never-replied dimension; if
not, say coverage is interview-only this round.)*
Interviewed by persona: <PM n, marketer n, developer n, founder n>. Gaps that bias any number — e.g.
"willingness-to-pay 18% is founders only; zero marketers reached, so the denominator is skewed."

## Bias-check (independent agent)
<the customer-discovery-bias-check agent's challenge, folded in: where the read pattern-matches to hope rather than
data, each point tied to an interview, and the single most likely way the founder is fooling themselves.
Do NOT soften the scorecard to accommodate this — surface the tension.>

## Hypothesis Updates Flagged
Evidence that should sharpen or correct the hypothesis. Route to `/sharpen-hypothesis` — do NOT edit
hypothesis.md here.
- <update> — what the interviews showed

## Override (only if proceeding past a TRIPPED criterion)
*(Only when the overall call is CONTINUE or PIVOT; a KILL or KEEP-DISCOVERING call never carries an override line.)*
<call> | Override: founder proceeded past TRIPPED <criterion> on <ISO-date>

---

## Provenance
- `customer-discovery/kill-criteria.json` — the locked thresholds
- `customer-discovery/interviews/` — the transcripts scored this round
- `customer-discovery/synthesis/round-<N>-scoring.json` — this round's per-interview tags (scorer input)
- `customer-discovery/synthesis/round-<N>.md` — the script output + bias-check challenge for this round
- `customer-discovery/prospects-<date>.csv` — the coverage snapshot (optional; from the Cowork tracking sheet)
```

Honesty rule (mirrors `/market-research`): never present a small-n or coverage-skewed signal as
validation. A TRIPPED criterion that the founder overrides stays TRIPPED in the scorecard — the override
is recorded alongside it, not substituted for it.
