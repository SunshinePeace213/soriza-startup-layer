# Output template — `docs/idea-exploration/<theme-slug>/ideas.md`

Shapes the 10-idea menu (Step 5) and the file written after the founder confirms picks (Step 9). Keep market sizing / business model / GTM out — those belong to later pipeline stages. No hard word cap, but menu entries are one-liners and deep dives run ≈150-250 words each.

## File structure

```markdown
# Idea Exploration: <theme>

## Research thesis
<2-4 sentences: the founder's thesis/observations as you understood them, plus the
sharpest 1-2 things the research confirmed or complicated. Names the founder context
(focus, constraints) that steered generation.>

## The 10 ideas
1. **<Name>** — <one-line pitch>. *Who:* <target user>. *Wedge:* <entry mechanism>. *Why now:* <the recent shift>.
2. ...
(exactly 10, genuinely distinct from each other)

## Recommended picks
<the 1-3 deep dives — see schema below>

## References
1. <URL> — <what it supports>
2. ...
(every factual "why now" / competitor / demand claim in the picks traces to a numbered source)
```

## Menu-entry schema (each of the 10)

One line, four slots: **Name** — pitch · *Who* · *Wedge* · *Why now*. Tight enough to scan all 10 at once. Distinctness is the bar — different user, wedge, or angle, not 10 reskins of one idea.

## Deep-dive schema (each of the 1-3 picks)

```markdown
### Pick N: <Name>

**Problem it attacks** — <the specific pain, grounded in the demand findings>
**Target segment** — <who specifically>
**Wedge** — <the sharp entry point and why it's open>
**Why now** — <the recent shift that makes it live now> [refs: N, N]
**Status quo & competitors** — <what people do today / who serves this and the gap> [refs: N]
**Founder-market fit** — <why this founder, from the intake>
**Key risks** — <the 1-3 things most likely to make it fail>

**Hypothesis seed** — *(carry this into /sharpen-hypothesis)*
- **Who:** <a concrete segment to start from — industry+size+role, or demographic+behaviour>
- **How often:** <best guess at frequency, to be tested>
- **How severely:** <cost in time / $ / risk — derive a magnitude from the cited figures where the research supports one; otherwise give a qualitative magnitude ("hours/week", "a meaningful share of margin"). Mark it "to be tested" either way; never fabricate precise numbers to look rigorous.>
- **Status quo:** <what *this* Who does today instead — a compressed, segment-specific restatement of the pick's "Status quo & competitors" field, not left blank>
```

## Hypothesis seed — why it's the point

The seed pre-frames `/sharpen-hypothesis`'s four dimensions so the founder can paste it straight in and start sharpening rather than from a blank page. It's a *starting guess to test*, not a validated claim — phrase it that way ("to be tested", "best guess"). A pick whose seed can't fill all four slots with something concrete isn't ready to recommend; either sharpen the idea or drop it.

## References

Numbered list of source URLs from the research subagents, each annotated with what it supports. In-text claims in the picks cite by number (`[refs: 2, 5]`). This is the founder's audit trail — keep it real; don't invent citations to decorate a claim.
