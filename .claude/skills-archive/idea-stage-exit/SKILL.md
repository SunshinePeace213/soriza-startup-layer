---
name: idea-stage-exit
description: |
  The deliberate GO/NO-GO that ends Idea-Stage validation: restate the VALIDATED problem, check the three exit-criteria + Lean's "should we even build this?" against pre-registered kill-criteria, stamp GO/NO-GO. Use for "am I ready to build", "should I build this", "go / no-go", "idea-stage exit".
when_to_use: |
  Gate: a solution-design.md exists for the idea. Not designing the solution (/solution-design) or building the PoC (/build-poc).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, AskUserQuestion
---

# Idea-Stage Exit — the GO / NO-GO

The conscious decision that ends validation. Making "is this worth building?" an explicit, on-record act
is the guard against this founder's documented failure mode — *concede the diagnosis, keep the
prescription* (drift). This is a deliberate stamp, not a soft gate.

## When this applies

- `solution-design.md` exists; "am I ready to build", "should I build this", "go/no-go", "is this worth a
  prototype".
- **Entry guard:** no `solution-design.md` → point to `/solution-design`.

## What it does (goal + constraints)

Goal: `ideas/<slug>/idea-stage-exit.md` with a stamped **GO** or **NO-GO**.

- **Re-state the VALIDATED problem** — the one `customer-discovery.md` revealed, not the one the
  hypothesis assumed.
- **Check the three exit-criteria** (read `lean-startup` for the "should we even build this?" gate):
  1. **Is the problem real & specific?** — name exactly who, how often, how severe, what they do now.
  2. **Does the solution address the VALIDATED problem?** — per `solution-design`'s drift audit, not the
     assumed problem.
  3. **Is there enough signal to justify building?** — the kill-criteria scorecard; not certainty (waiting
     for it is its own failure), but a reasoned bet over an act of faith.
- **Surface any TRIPPED kill-criterion loudly.** Proceeding past one is an explicit, stamped **override**
  (the founder's documented failure mode lives here).
- `AskUserQuestion`: the founder stamps **GO** (→ `/build-poc`) or **NO-GO** (→ pivot / keep-discovering /
  drop). Record the rationale.

## Output

`ideas/<slug>/idea-stage-exit.md` (`assets/idea-stage-exit-template.md`). Next on **GO**: `/build-poc`. On
**NO-GO**: route per the reason (PIVOT → `/sharpen-hypothesis`; KEEP-DISCOVERING → more interviews via the
sealed pack; DROP → promote another `slate.md` idea).

## References

- `assets/idea-stage-exit-template.md`; the "should we even build this?" gate + value/growth check in
  `lean-startup`.
