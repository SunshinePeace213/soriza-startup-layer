---
name: lean-startup
description: |
  The Lean Startup method as APPLIED tools for the Idea Stage: Build-Measure-Learn, the value vs
  growth hypothesis, the MVP-type chooser (video / concierge / Wizard-of-Oz / functional), validated
  learning vs vanity metrics + innovation accounting, the 10 pivot types + "runway = pivots left", and
  the "should we even build this?" gate. Read inline by sharpen-hypothesis, solution-design,
  idea-stage-exit, and build-poc; also invocable standalone. Use for "what's the cheapest test?",
  "which MVP type?", "is this a vanity metric?", "should we pivot or persevere?", "what kind of pivot
  is this?", "how much runway do we have?", or "should we even build this?".
when_to_use: |
  Trigger on "cheapest experiment / MVP", "minimum viable product", "video/concierge/Wizard-of-Oz
  MVP", "value hypothesis", "growth hypothesis", "vanity metric", "validated learning", "innovation
  accounting", "pivot or persevere", "what pivot type", "runway as pivots", "build-measure-learn",
  "should we even build this".
allowed-tools: Read, Glob
---

# Lean Startup — validate before you build

The engine under the whole Idea Stage: treat the venture as a series of experiments whose product is
**validated learning**, not shipped features. This skill is the *applied* method — the decision rules
the stages reach for — not a book summary. The default it pushes against: building feels like progress,
so a founder ships instead of learning. The cure is to keep the **learning ahead of the building.**

## When this applies

- **Inline-read by stages:** `sharpen-hypothesis` (value + growth hypotheses), `solution-design` (MVP
  type + pivots), `idea-stage-exit` ("should we build?"), `build-poc` (the MVP-type chooser).
- **Standalone:** "what's the cheapest test of this?", "which MVP type?", "is that a vanity metric?",
  "should we pivot or persevere — and which pivot?", "what's my real runway?"

**Out of scope.** These are *validation-and-decision* tools — not for writing application code,
debugging, or general technical how-to. If the request is an implementation task, answer it normally;
don't wrap it in MVP / pivot / metrics framing.

## Build-Measure-Learn (minimized)

The unit of progress is **validated learning**; everything not needed to produce the *next* learning is
waste. The operative question is never "what should we build?" but **"what is the smallest experiment
that produces the next decision-changing learning, fastest?"** Minimize total time through the loop.

## The two hypotheses every idea rests on

- **Value hypothesis** — does it deliver real value: will they actually switch to it / pay for it?
- **Growth hypothesis** — how do *new* customers discover it?

Both are **claims to test**, not facts to assert. `sharpen-hypothesis` names them so the downstream
stages know what the interviews and the PoC must trip or clear.

## MVP-type chooser (cheapest path to learning)

A PoC/MVP is the *minimum* that completes one BML loop — often **not code.** Pick the cheapest type that
answers the actual question:

| Type | What it is | Choose when |
|---|---|---|
| **Video** (Dropbox) | a short demo standing in for the product | the value is graspable from a demo; you're testing *desire/demand* |
| **Concierge** (Food on the Table) | you deliver the service **by hand** to a few real customers | you must learn the *workflow* and what "valuable" means before automating |
| **Wizard-of-Oz** (Aardvark) | a real front-end, humans faking the backend | you're testing whether people use the *output*, before building the engine |
| **Functional single-interaction** | build *only* the one core interaction | the reaction depends on touching a working thing |

**Rule:** non-code beats code when it answers the question. The MVP "challenges quality" on purpose —
when you don't yet know who the customer is, you don't yet know what quality means.

## Validated learning vs vanity metrics (the guard)

- **Vanity metrics** (cumulative totals, signups, downloads, page views) only ever go up and flatter you.
- **Actionable metrics** (cohort behaviour, conversion, retention, willingness-to-pay) inform a decision.
- **Innovation accounting:** pick the metric that, *if it moved, would change your next decision.* A
  number that can't change a decision is vanity — drop it.

## Pivot or persevere — the 10 pivot types

When evidence challenges a load-bearing hypothesis, you **pivot**: a *structured* change of one
fundamental assumption to test a new strategic hypothesis — not a random restart, and not quietly
soldiering on. Name the pivot (the loop-backs and synthesis verdicts use these):

1. **Zoom-in** — one feature becomes the whole product.
2. **Zoom-out** — the product becomes one feature of a bigger whole.
3. **Customer-segment** — right product, wrong customer.
4. **Customer-need** — same customer, a different (often adjacent) problem.
5. **Platform** — app ↔ platform.
6. **Business-architecture** — high-margin/low-volume ↔ low-margin/high-volume.
7. **Value-capture** — how you monetize.
8. **Engine-of-growth** — sticky / viral / paid.
9. **Channel** — how you reach customers.
10. **Technology** — same solution, different underlying tech.

**Runway = the number of pivots you have left**, not months of cash. You extend it by *shortening the
time between pivots* — fail fast, learn, re-aim.

## The 3 growth engines (flagged — mostly later-stage)

- **Sticky** — retention; new-acquisition-rate must exceed churn.
- **Viral** — the viral coefficient (each user brings >1).
- **Paid** — LTV must exceed CAC, with margin to spare.

In the **Idea Stage**, you only need to *name which engine the idea would depend on* — the real tuning
is MVP/Launch work. Flag it; don't build for it yet.

## "Should we even build this?" (the exit gate)

The era's question is no longer "can we build it?" (you can) but **"should we?"** and **"can this become
a sustainable business?"** Before committing to build, check the BML loop is aimed at a real, valuable,
reachable problem — not at being productively busy on the wrong thing. `idea-stage-exit` runs this
against the pre-registered kill-criteria.
