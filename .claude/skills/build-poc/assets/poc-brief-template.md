---
stage: build-poc
status: scoped   # scoped | built | synthesized
archetype: functional   # video | concierge | wizard-of-oz | functional
direction:   # set at synthesize (G9 result): keep | pivot | kill
---

# PoC Brief — <slug>

## The single core interaction

<the one interaction the solution depends on — the only thing the PoC must let a real user touch>

## Build scope — IN

- <only what's needed to make that one interaction touchable; nothing more>

## Non-goals — OUT (dropped; not needed for learning)

- <everything else: auth, settings, polish, breadth, a real backend if a fake one answers the question>

## Archetype + why

**<video | concierge | Wizard-of-Oz | functional>** — chosen because it's the cheapest path to the
learning we actually need, which is: <the value / quality-bar hypothesis this PoC tests>. (Non-code is a
win if it answers the question.)

## The 5-user test

- **Who** (from the validated profile): <…>
- **Reaction rubric — what to watch:** do they *get* it · do they *want* it · would they pay / switch ·
  where do they stumble.
- **Scored against the locked G9 criteria** (`gates/criteria-g9.yaml`): each conversation must produce the
  signal a pre-registered criterion needs — name which criterion each rubric line maps to.

---

*Filled at the synthesize phase:* `reactions.md` (the 5-user synthesis + the G9 scorecard + the direction
decision — keep-building / pivot / kill) and `mvp-input.md` (what the next layer should lock as the MVP
scope). build-poc produces the input; the MVP layer locks the scope. Close G9 via
`scripts/advance_gate.py --gate g9 --result <keep|pivot|kill> --attest <criterion ids>`.
