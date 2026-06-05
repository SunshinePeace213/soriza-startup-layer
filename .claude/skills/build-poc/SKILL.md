---
name: build-poc
description: |
  Final stage of the Idea Stage: build a lightweight PROOF-OF-CONCEPT (NOT an MVP) and run it past 5 real
  users. Phase-aware — scope (list what to build + explicit non-goals; pick the cheapest archetype:
  video / concierge / Wizard-of-Oz / functional single-interaction), build (the single core interaction,
  in its own coding session + worktree), then synthesize the 5 reactions into a direction
  (keep-building / pivot / back-to-the-drawing-board) + an MVP-scope handoff to the next layer. Use for
  "build a PoC / prototype", "build the proof of concept", "what should the PoC do", "scope my prototype",
  "synthesize my PoC feedback".
when_to_use: |
  Gate: an idea-stage-exit.md = GO exists for the idea. Not the MVP build (that's the next layer) and not idea defensibility (/forward-deployed-founder).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Bash, Agent, AskUserQuestion
effort: high
---

# Build PoC — the lightweight prototype

Put the validated idea in front of real humans with the **minimum surface area** to get a genuine
reaction — then let those reactions decide keep-building vs back-to-the-drawing-board.

**A PoC is NOT an MVP.** It's a throwaway, learning-only prototype (often fake-backed) to provoke a
genuine reaction to the *solution* — deliberately **not** the first shippable product. Over-building it
into an MVP is the failure mode this stage guards against; the MVP layer (next) answers "what to build
*first*" and locks scope there.

## When this applies

- `idea-stage-exit.md` = **GO** exists; "build a PoC / prototype", "what should the PoC do", "scope my
  prototype", "synthesize my PoC feedback".
- **Entry guard:** no GO exit → point to `/idea-stage-exit`.

## Phase-aware (resumes by detecting which artifacts exist)

1. **Scope** *(no `poc-brief.md`)* — list the **build scope** (the single core interaction + the minimum
   to make it *touchable*) **and explicit NON-GOALS** (everything dropped — not needed for learning; this
   IN/OUT list is the anti-scope-creep guard); **pick the archetype** by cheapest-path-to-learning
   (video / concierge / Wizard-of-Oz / functional — non-code is a feature, read `lean-startup` MVP types;
   scope to a solo build, read `solo-founder`); write `poc-brief.md`; scaffold a build session.
2. **Build** *(`poc-brief.md` exists, no prototype)* — for a functional archetype, build **only** the
   single core interaction, in its **own focused coding session + worktree** (keep the code build out of
   this validation context). Non-code archetypes skip this entirely.
3. **Synthesize** *(reactions exist)* — score the **5 target-user reactions** → a **direction decision**
   (keep-building / pivot / back-to-the-drawing-board — the BML loop-back) **+** an **MVP-scope-input
   handoff** (`mvp-input.md`) the next layer consumes. build-poc produces the *input*; it does **not** lock
   the MVP.

## Gotchas

- **PoC ≠ MVP.** If you're adding features "for completeness," stop — that's the trap. Cut to the single
  core interaction.
- **The 5 conversations are the deliverable, not the code.** A video/concierge/Wizard-of-Oz PoC that gets
  a real reaction beats a polished build that doesn't.

## Output

`ideas/<slug>/poc/{poc-brief.md (scope + non-goals), reactions.md (5-user synthesis + direction),
mvp-input.md (handoff)}`. **Ends the Idea Stage** → hands to the MVP layer.

## References

- `assets/poc-brief-template.md`; `lean-startup` (MVP types / validated learning), `solo-founder` (scope).
