# Output Template — `market-research.md`

The top-level deliverable. A synthesis with a point of view, not a verdict and not a fact-dump. Read in Step 5; the five provenance docs under `market-research/` are the evidence it cross-references.

The **Market Read is a recommendation, not a gate** — the founder is not asked to accept or override it (that's `/pressure-test`'s mechanic, not this stage's). Keep the whole file tight; each section is a few lines, not an essay.

```markdown
# Market Research: <slug>

> **This is desk research synthesizing public evidence — competitor sites, reviews, market
> data, trend signals — not customer validation.** A strong Market Read means the public
> evidence is favorable; it is not proof that customers will pay. Take the wedge and the
> flagged disconfirmation targets into customer discovery. Re-run this stage whenever the
> hypothesis evolves.

## Market Read
**<enter | enter-narrower | reposition | reconsider>** — 1–2 sentences of rationale tied to the evidence below.

## Positioning & Wedge
The unresolved complaint (from review-synthesis) this idea is uniquely placed to own, and the angle of attack.

## Strongest Threat
The single most-dangerous competitor and the steelman's core "they win, you lose" argument — plus the survival bar it implies.

## Sizing Reality
SOM + willingness-to-pay + budget-holder, in 2–3 lines. Bootstrapper framing: is this a business at the founder's scale?

## Timing
Net tailwind/headwind across the three trends — one line, with the dominant driver named.

## Problem–Solution-Fit
**<strong | weak | none>** — does the hypothesis address the top unresolved complaints?

## Hypothesis Updates Flagged
Evidence that contradicts or should sharpen the hypothesis. Route to `/sharpen-hypothesis` — do NOT edit hypothesis.md here.
- <update> — what the evidence says

## Provenance
- `market-research/competitive-landscape.md`
- `market-research/review-synthesis.md`
- `market-research/market-sizing.md`
- `market-research/trends.md`
- `market-research/competitor-steelman.md`
```

If a workstream ran inline (no spawn tool) or came back thin, note it in the relevant section — e.g. *"(review signal thin — single-source; treat as a discovery target, not validation)"*. Honesty about weak signal is the point; a confident read on no evidence is the failure mode.
