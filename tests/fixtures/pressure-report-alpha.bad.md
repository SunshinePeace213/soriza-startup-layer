---
stage: pressure_alpha
status: report
p_agg: 1.5
p_distribution: {thiel: 0.30}
open_assumptions: ["only one assumption"]
fatal_flag: kill
predictions_locked: "yes"
token_estimate: "12k"
---

# Pressure-test α — bad-fixture

This report is deliberately malformed to prove the validator bites:
- p_agg is 1.5 (out of [0,1]) — α would be issuing a verdict, not a calibration.
- open_assumptions has 1 entry (needs 5-8).
- fatal_flag is "kill" (not an allowed enum; α never kills).
- predictions_locked is a string, not a boolean.
- most required sections are missing.

## Cost

Fan-out estimate only; every other required section is absent on purpose.
