---
name: build-poc
description: |
  Final Idea-Stage step (9): build a lightweight PROOF-OF-CONCEPT (not an MVP) — scope the cheapest archetype (video/concierge/Wizard-of-Oz/functional), build the one core interaction, synthesize 5 target-user reactions, and score them against the LOCKED G9 PoC criteria. Use for "build a PoC/prototype", "scope my prototype", "synthesize my PoC feedback".
when_to_use: |
  Gate: runs at current_step 9 (after startup-brief stamped GO at G8). Input is the brief + the LOCKED gates/criteria-g9.yaml. The desk never kills — the PoC's 5 conversations + the founder's signature settle keep/pivot/kill. Not the MVP build (the next layer) and not idea defensibility (/forward-deployed-founder).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Bash, Agent, AskUserQuestion
effort: high
---

# Build PoC — the lightweight prototype (step 9)

Put the validated idea in front of real humans with the **minimum surface area** to get a genuine
reaction, **score those reactions against the PoC kill-criteria locked at G8**, then let them decide
keep-building vs pivot vs kill. The 5 conversations are the deliverable, not the code.

**A PoC is NOT an MVP.** It's a throwaway, learning-only prototype (often fake-backed) to provoke a
genuine reaction to the *solution* — deliberately **not** the first shippable product. Over-building it
into an MVP is the failure mode this step guards against; the MVP layer (next) answers "what to build
*first*" and locks scope there. This is the terminal Idea-Stage step: a `keep` graduates to the MVP
layer, a `pivot`/`kill` loops back through the funnel.

## When this applies

- **`current_step: 9`** (G8 passed — a `startup-brief.md` carrying a **GO** stamp exists, and the PoC
  kill-criteria are pre-registered in a locked `gates/criteria-g9.yaml`). Triggers: "build a PoC /
  prototype", "what should the PoC do", "scope my prototype", "synthesize my PoC feedback", "what's next"
  after the startup brief.
- **Entry guard:** no `startup-brief.md` / step < 9 → point to `/startup-brief`. If `startup-brief.md`
  exists but `gates/criteria-g9.yaml` is missing or unlocked, **stop and report it** — the G9 criteria
  must be locked *before* the PoC runs (startup-brief step ⑤ locks them; lock-ahead enforces it at G8).
  Never hand-write or soften them here.

## Phase-aware (resumes by detecting which artifacts exist)

1. **Scope** *(no `poc-brief.md`)* — list the **build scope** (the single core interaction + the minimum
   to make it *touchable*) **and explicit NON-GOALS** (everything dropped — not needed for learning; this
   IN/OUT list is the anti-scope-creep guard); **pick the archetype** by cheapest-path-to-learning
   (video / concierge / Wizard-of-Oz / functional — non-code is a feature, read `lean-startup` MVP types;
   scope to a solo build, read `solo-founder`). Tie the 5-user reaction rubric to the **locked
   `criteria-g9.yaml`** so the test measures exactly what the founder pre-registered. Write `poc-brief.md`.
2. **Build** *(`poc-brief.md` exists, no prototype)* — for a **functional** archetype, build **only** the
   single core interaction, in its **own focused coding session + worktree** (keep the code build out of
   this validation context). Non-code archetypes (video / concierge / Wizard-of-Oz) skip this entirely —
   non-code is a win if it answers the question.
3. **Synthesize** *(reactions exist)* — score the **5 target-user reactions** against the locked
   `criteria-g9.yaml` into a **scorecard** → a **direction recommendation** (keep-building / pivot /
   kill — the BML loop-back; the panel scores, the founder signs) **+** an **MVP-scope-input handoff**
   (`mvp-input.md`) the next layer consumes. build-poc produces the *input*; it does **not** lock the MVP.

## Gotchas

- **PoC ≠ MVP.** If you're adding features "for completeness," stop — that's the trap. Cut to the single
  core interaction. The MVP layer locks scope; this step only produces its input.
- **The 5 conversations are the deliverable, not the code.** A video/concierge/Wizard-of-Oz PoC that gets
  a real reaction beats a polished build that doesn't.
- **G9 criteria are LOCKED — never soften a threshold after seeing reactions.** They were pre-registered
  in `gates/criteria-g9.yaml` at G8 (startup-brief step ⑤), *before* a single user saw the PoC. Score the
  reactions honestly against them; if the result is ugly, surface it and let the founder override **on the
  record** at G9 — do not relitigate the threshold to keep the idea alive.
- **Subjective merit dies to real users + the founder's signature — never the desk.** A weak-looking
  reaction is the founder's call to make (keep/pivot/kill), informed by the scorecard. The skill scores
  and recommends; the founder signs at G9.
- **Resolve open predictions.** Before closing G9, resolve every `predictions.jsonl` entry the PoC
  reactions now answer (append a supplement line — same `id`, `resolved`, `outcome`, `brier`,
  `resolved_by: build-poc`); the rest are cleared by the W10 calibration-review. Never modify a locked line.
- **G9 is a pure-human gate.** There is no auto-validator for the PoC artifacts (the gate signature table
  makes G9 the founder's pretotype + 5 conversations + direction). The scorecard is your reasoning; the
  founder's `--attest` is what closes it.

## Workflow (step 9)

**Goal:** `ideas/<slug>/poc/{poc-brief.md, reactions.md, mvp-input.md}` + the reactions scored against the
locked `criteria-g9.yaml` → the founder reads the 5 conversations + scorecard and stamps keep/pivot/kill
at G9, all open predictions resolved.

1. **Confirm state + load the locked criteria.** Read `ideas/<slug>/STATE.md` (`current_step: 9`). Read
   `startup-brief.md` (the validated solution concept + the three exit criteria) and the **locked**
   `gates/criteria-g9.yaml` (the PoC kill-criteria — `locked: true`). If either is missing/unlocked, apply
   the entry guard above and stop. (`poc/` already exists from scaffold.)
2. **Scope → `poc-brief.md`.** Run the Scope phase: single core interaction + IN/OUT non-goals, pick the
   archetype by cheapest-path-to-learning, and map the 5-user reaction rubric onto each `criteria-g9.yaml`
   criterion (so each conversation produces the signal that criterion needs). Write from
   `assets/poc-brief-template.md`.
3. **Build (functional only).** For a functional archetype, dispatch a **separate focused build session in
   its own worktree** — the code build stays out of this validation thread. Non-code archetypes skip this.
4. **Synthesize → score → `reactions.md` + `mvp-input.md`.** Capture the 5 target-user reactions, then
   **score each against the locked `criteria-g9.yaml`** into a scorecard (per-criterion `CLEARED` /
   `TRIPPED` / `INCONCLUSIVE`, with the conversation cited). Write `reactions.md` (the 5-user synthesis +
   scorecard + a direction *recommendation*: keep-building / pivot / kill) and `mvp-input.md` (what the
   next layer should lock as MVP scope). Update STATE `status` / `step_checklist` as the phase advances.
5. **Resolve open predictions.** For each open `predictions.jsonl` entry the reactions now settle, append
   a supplement line (same `id`, `resolved` date, `outcome`, `brier`, `resolved_by: build-poc`).
6. **Close G9.** The founder reads the 5 conversations + scorecard and stamps the direction. Run
   `uv run scripts/advance_gate.py --slug <slug> --gate g9 --result <keep|pivot|kill> --attest <g9 criterion ids>`
   — G9 is lock-ahead exempt and has no auto-validator; the `--attest` is the founder's signature. It
   marks the idea `done`.
   - **keep** → graduates to the **MVP layer**; **merging the PoC worktree to `main` is the graduation act**.
   - **pivot** → loops back: re-enter `/sharpen-hypothesis` for the sharpened problem (append to
     `learning-log.md` — runway = pivots left).
   - **kill** → back to the drawing board; promote another slate idea or close the idea out.

## Output

`ideas/<slug>/poc/{poc-brief.md (scope + non-goals), reactions.md (5-user synthesis + G9 scorecard +
direction), mvp-input.md (handoff)}` + every open prediction resolved. **Ends the Idea Stage** → a `keep`
hands to the MVP layer.

## References

- `assets/poc-brief-template.md`; `lean-startup` (MVP types / validated learning), `solo-founder` (scope).
- **Spec:** `docs/loop-engineering-reference-en.md` §2 (step 9), §3.5 (predictions resolution protocol).
