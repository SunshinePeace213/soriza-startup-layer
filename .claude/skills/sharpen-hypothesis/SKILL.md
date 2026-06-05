---
name: sharpen-hypothesis
description: |
  Second Idea-Stage stage: sharpen a chosen idea into a TESTABLE problem hypothesis (who, how-often, how-severe, status-quo) + lean value/growth hypotheses. Interactive, no web research (a hypothesis is to TEST, not prove). Use for "sharpen my hypothesis", "make my idea testable", "what's next".
when_to_use: |
  Gate: a scaffolded idea exists but no hypothesis.md yet. Not arguing against the idea (/disconfirm) or sizing it (/market-map).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, AskUserQuestion
effort: high
---

# Sharpen Hypothesis

Turn the picked idea into a testable hypothesis. **Founder-aware and interactive:** the skill drafts, you
refine with your domain knowledge, and everything stays **"provisional, to-be-tested."** **No web
research** — sharpening makes a claim *specific and falsifiable*; the truth is tested by real users later
(`market-map` grounds it, the interviews validate it). Researching to "prove" it here would manufacture
false certainty — the loss-of-objectivity trap.

## When this applies

- A scaffolded `ideas/<slug>/` exists (from `/generate-ideas`) and you ask to sharpen / make it testable,
  or "what's next".
- **Entry guard:** if no idea folder exists, point to `/generate-ideas`.

## What it does (goal + constraints)

Goal: `ideas/<slug>/hypothesis.md` — a sharp, falsifiable problem hypothesis + the value & growth
hypotheses.

- Read `ideas/<slug>/seed.md`, the exploration `grounding.md`, `lean-startup`, and
  `docs/founder-profile.md`.
- **Draft** the four dimensions, each made specific: **WHO** (named role + context + segment, not
  "businesses") · **HOW OFTEN** (a frequency) · **HOW SEVERE** (a cost/pain magnitude) · **STATUS QUO**
  (what they do about it now). Mark each **provisional, to-be-tested**.
- Surface the lean-startup **value hypothesis** (will they find it valuable enough to switch/pay?) +
  **growth hypothesis** (how do new users discover it?) as named assumptions for the downstream stages.
- **Founder refines** / injects real domain specifics via `AskUserQuestion` (a `notes` escape hatch).
- **Kill only if** it cannot be made testable after one sharpening pass (a dimension stays irreducibly
  vague / the claim is unfalsifiable). When on the fence, advance — a testable hypothesis about a
  weak-looking idea *advances* (its weakness becomes the thing the interviews test).

## Gotchas

- The tool list **excludes** WebSearch/WebFetch on purpose — sharpen, don't prove.
- Specific ≠ true. The four dimensions are concrete *claims*, flagged provisional; their truth is what
  customer discovery exists to settle.

## Output

`ideas/<slug>/hypothesis.md` (`assets/hypothesis-template.md`). Next: `/disconfirm` and `/market-map`.

## References

- `assets/hypothesis-template.md` — the hypothesis structure.
