---
stage: sharpen-hypothesis
status: testable   # testable | untestable
who: "<named role + context + segment>"
how_often: "<frequency>"
how_severe: "<cost / pain magnitude>"
status_quo: "<what they do about it now>"
value_hypothesis: "<will they find it valuable enough to switch / pay?>"
growth_hypothesis: "<how do new customers discover it?>"
---

# Hypothesis — <slug>

**Testable sentence (provisional, to-be-tested):** <who> experience <problem> <how often>, costing
<how severe>, because they currently <status quo>.

<!-- The 5 sections below ARE the validator's contract (tests/schemas/test_hypothesis.py):
     all five present, each dimension a falsifiable claim, HOW OFTEN + HOW SEVERE each carry a
     number, <=300 words, no web citations. Keep every claim flagged provisional. -->

## WHO
<named role + context + segment>. *Provisional.*

## HOW OFTEN
<frequency — include a number>. *Provisional.*

## HOW SEVERE
<cost / pain magnitude — include a number>. *Provisional, to-be-tested.*

## STATUS QUO
<what they do about it now>.

## VALUE & GROWTH
- **Value hypothesis** — <will they switch / pay?> *Provisional.*
- **Growth hypothesis** — <how do new customers discover it?> *Provisional.*

## Founder refinements

<domain specifics the founder injected; what they corrected from the draft>

## Hypothesis Updates Flagged

<none yet — later stages append here; only /sharpen-hypothesis folds these in>
