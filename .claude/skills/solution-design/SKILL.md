---
name: solution-design
description: |
  Fifth step in the Idea Stage of Soriza Startup Layer — crystallizes AND challenges the final
  solution concept for ONE idea that has been through /customer-discovery. Mines the concept latent in
  the validated evidence, articulates it (founder confirms), then attacks it: a drift audit (does the
  design serve the problem discovery VALIDATED, not the one the hypothesis ASSUMED?), the three most
  load-bearing assumptions + what would have to be true, alternatives, scale conditions — with a blind,
  separate-context solution-red-team adversary. Writes solution-design.md with a non-binding Concept
  Read (build / narrow / redesign / reconsider) + an MVP Brief. Reads customer-discovery.md; never
  edits hypothesis.md.
when_to_use: |
  Use when the founder says "design my solution", "design the solution", "solution concept",
  "final solution concept", "develop and challenge my concept", "red-team my solution", "what
  assumptions does my design make", or "what's next" WHEN a customer-discovery.md exists in the idea's
  docs/ideas-stages folder but solution-design.md does not yet (precedence: no hypothesis.md →
  /sharpen-hypothesis; hypothesis.md only → /pressure-test; pressure-test.md → /market-research;
  market-research.md → /customer-discovery; customer-discovery.md → here). Do NOT trigger to edit
  hypothesis.md (/sharpen-hypothesis), size the market (/market-research), run/synthesize interviews
  (/customer-discovery), or for software/architecture/code-level design — this is startup
  solution-concept design.
argument-hint: "[slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob, Agent, Task, WebSearch, WebFetch, Skill
effort: high
---

# Solution Design

Fifth step in the **Idea Stage** of the Soriza Startup Layer. Takes the validated evidence for one idea
and turns it into a **designed, challenged, final solution concept** — then checks the one thing the
Playbook says matters most: does the design address the problem *discovery revealed*, not the problem
the founder *assumed going in*? Source method: *The Founder's Playbook: Building an AI-Native Startup* —
"Design your final solution concept" (develop **and challenge** from every angle: gaps, alternatives,
scale, and the assumed-vs-validated reality check).

- **Input:** `docs/ideas-stages/<slug>/customer-discovery.md` (required floor) + `hypothesis.md`, `pressure-test.md`, `market-research.md` (folded if present) + `docs/founder-profile.md`.
- **Output:** `docs/ideas-stages/<slug>/solution-design.md` (the action card) + provenance under `solution-design/`.
- **Worker:** the `solution-red-team` subagent (`.claude/agents/`), read at runtime.

## The spine — assumed → validated (why this stage exists)

This skill is a **crystallize-then-challenge engine**. The concept already exists *implicitly* across the
upstream docs; the skill's job is to articulate it sharply (the founder confirms — they own the design),
then attack it. The load-bearing attack is the **drift audit**: discovery may have *revised the
diagnosis*, and the failure mode this whole stage guards against is keeping the old prescription anyway.

The trap inside the trap: **the "validated problem" is not just `customer-discovery.md`.** Every upstream
stage emits a *"Hypothesis Updates Flagged"* block, and only `/sharpen-hypothesis` may fold those back
into `hypothesis.md`. Mid-pipeline, `hypothesis.md` is usually **stale**. So the validated baseline you
measure the concept against = **original hypothesis + all accumulated, possibly-unapplied flagged
deltas** from pressure-test, market-research, and discovery. `scripts/build_delta_ledger.py` assembles
those verbatim so none is silently dropped before the reasoning starts.

## When this skill applies

- Founder has a `customer-discovery.md` at `docs/ideas-stages/<slug>/` and asks "what's next"
- "Design my solution", "solution concept", "final solution concept", "design the solution"
- "Develop and challenge my concept", "what are my design's load-bearing assumptions"

Out of scope: editing `hypothesis.md` (`/sharpen-hypothesis`); market sizing / competitor mapping
(`/market-research`); the adversarial persona panel (`/pressure-test`); running or synthesizing
interviews (`/customer-discovery`); MVP/build work (the next stage, not yet built).

## Gotchas

- **The drift audit is the point — never let "concede the diagnosis, keep the prescription" through.** This founder's documented failure mode IS drift: discovery revised the diagnosis, the design keeps serving the old prescription. Measure the concept against the **reconstructed** validated baseline (hypothesis + unapplied deltas), never the stale `hypothesis.md`. A `❌ still solving the old problem` row is a finding, not an inconvenience to soften.
- **A KILL Discovery Read is a loud stop, not a speed bump.** This stage gathers **no new evidence about the problem** — designing a slick concept proves nothing about whether the killed problem is real. The only legitimate proceed: the founder contests the kill as an *artifact* (e.g. coverage skew — no founders interviewed, marketer truncated) AND designs only the *narrowed* concept the cleared evidence supports. Surface it at Gate 1; stamp the override on record. Never silently design a corpse. `customer-discovery.md` is **append-round**, so the binding verdict is the **latest** round (the ledger script selects it); aim any narrowing at the script's `cleared_criteria`.
- **The `solution-red-team` MUST run in a separate context, dispatched BLIND.** It gets the validation docs + the founder-confirmed concept wedge but NOT the main agent's draft card. Blind by construction = it generates its own assumptions and drift suspicions independently, so the reconcile catches assumptions the draft never listed. An agent grading its own design rationalizes it (the customer-discovery-bias-check principle).
- **The Concept Read is non-binding — do not overclaim it as a gate.** Like `/market-research`'s Market Read, it's a recommendation, not a pass/fail verdict the founder must "accept." Proceeding past a KILL is the only thing stamped as an override.
- **Never edit `hypothesis.md`.** This skill *flags* hypothesis updates and routes to `/sharpen-hypothesis`, which owns that file. Writing into it duplicates ownership and breaks the contract the other stages depend on.
- **No persona panel here.** The `*-perspective` advisors live exclusively at `/pressure-test`. You may run ONE named perspective skill as an a-la-carte design lens if the founder asks (e.g. `/steve-jobs-perspective` for "is this focused / whole-widget?") — but never reconstruct the panel or its verdict machinery.
- **Don't re-run market research or discovery.** WebSearch/WebFetch are for *light* verification only (does an "alternative" already exist; is a scale-economics claim sane). Re-deriving the competitive landscape or re-interviewing is scope creep into the prior stages.
- **Create `solution-design/` (and `rounds/`) before dispatching the worker / running scripts.** Writes to a fixed path fail if the parent doesn't exist (mirrors the sibling stages).
- **Degrade gracefully if no spawn tool.** If neither `Agent` nor `Task` exists, run the red-team as a deliberately adversarial *second pass* in a fresh framing — and tell the founder it is weaker without context isolation, because a same-context self-critique is structurally compromised.

## Interaction model

Hybrid, like the sibling stages: **concept-confirm gate → autonomous challenge → final review**, with
founder decisions routed through `AskUserQuestion` (a `notes` escape hatch on every choice — house
style; read `/customer-discovery` or `/market-research` for voice). One phase, two gates — there is no
external interlude (crystallize → challenge → card is continuous). Quality scales with reasoning depth —
run at `high` effort or above; the worker carries its own.

## Workflow

Goal: crystallize the concept the validated evidence supports, challenge it (drift + assumptions +
alternatives + scale) with a blind adversary, and write a `solution-design.md` action card on
confirmation. Steps are ordered where order is real (guard before scope-lock; ledger before drift audit;
confirm the concept before attacking it; rank before featuring; reconcile before the card); within each
step the bullets are constraints, not a script.

### Step 1 — Resolve slug, entry guard, read docs

If invoked with a slug, use it. Otherwise `glob docs/ideas-stages/*/` for ideas with a
`customer-discovery.md`: exactly one → use it (state which in chat); more than one → `AskUserQuestion`;
none → if idea folders exist but none has `customer-discovery.md`, point at `/customer-discovery`; if no
idea folders, point at `/sharpen-hypothesis`. Stop.

Read, in order: `customer-discovery.md` (the floor), then `hypothesis.md`, `pressure-test.md`,
`market-research.md`, and `docs/founder-profile.md` if present. If `pressure-test.md` /
`market-research.md` are absent, do not refuse — note in chat that the validated baseline will be
thinner (the ledger script flags each missing doc in its `warnings`).

**Entry guard:** if `customer-discovery.md` is missing, refuse with exactly: *"No customer-discovery at
`docs/ideas-stages/<slug>/customer-discovery.md`. Run /customer-discovery first — solution design must
serve the problem discovery validated, and without it there's only the assumed problem."* Stop. Write nothing.

Read the **Discovery Read verdict** (`CONTINUE` / `PIVOT` / `KILL` / `KEEP-DISCOVERING`) and hold it for Gate 1. `customer-discovery.md` is **append-round** — the binding verdict is the **latest** round; Step 3's ledger script selects it and lists every round in `discovery_read_rounds`.

### Step 2 — Resume check

If `docs/ideas-stages/<slug>/solution-design.md` already exists, fire `AskUserQuestion`:
- **Overwrite from scratch** — `rm -rf docs/ideas-stages/<slug>/solution-design/` and proceed.
- **Append a timestamped round** — keep the file; write provenance under `solution-design/rounds/round-<N>.md` (date via `date +%F`) and append a `## Round <N> (<date>)` section. Append-round records how the concept *evolved* across redesigns.
- **Skip and exit** — print the existing Concept Read line, do nothing else.

### Step 3 — Build the delta ledger + reconstruct the validated baseline

Create the output directory first: `docs/ideas-stages/<slug>/solution-design/`.

Run the ledger script so no flagged delta is dropped before reasoning:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build_delta_ledger.py" docs/ideas-stages/<slug>
```
It prints JSON: the **latest-round** Discovery verdict (`verdict_source` flags a prose-guess when no
Discovery-Read heading parsed), the TRIPPED **and CLEARED** criteria, any override, and every *"Hypothesis
Updates Flagged"* block across the docs **verbatim** (with `warnings` listing missing docs and any deviated
header — trust this field). Write it to `solution-design/delta-ledger.md`. Then reconstruct the **validated baseline** —
original hypothesis dimensions (who / frequency / severity / what-they-do-now) with each accumulated
delta applied — and write `solution-design/validated-baseline.md`. This baseline, not the stale
`hypothesis.md`, is what the drift audit measures against. See `references/drift-audit.md`.

### Step 4 — Crystallize the concept · Gate 1 (concept-confirm)

Extract, don't ask blank. From the docs, crystallize a *draft* concept: **wedge** (narrowest first
version), **validated who** (narrowed by discovery), **core job/workflow it owns**, **what it
deliberately does NOT do**, and the **win thesis** (tie to the founder's stated unfair advantage, read
from `docs/founder-profile.md`, + any defensible signal discovery surfaced). See
`references/solution-design-template.md` for the shape.

Fire one `AskUserQuestion` that shows the crystallized concept and lets the founder confirm/correct in `notes`:
- The concept (wedge / validated-who / core job / non-goals / win thesis). **This is the highest-leverage human input** — a wrong crystallization aims the whole challenge at a strawman.
- Surface the **Discovery verdict**. If `KILL`: state it loudly and make proceeding the explicit, narrow override (contest-as-artifact + design only the narrowed concept). If `PIVOT`: confirm the concept is the *pivoted* one. If `KEEP-DISCOVERING`: confirm this is a *provisional* concept whose top assumptions route back to `/customer-discovery`.
- Optionally offer ONE a-la-carte perspective lens (e.g. `/steve-jobs-perspective`) — only if the founder wants it.

### Step 5 — Autonomous challenge

With the confirmed concept, run the challenge:

1. **Dispatch `solution-red-team` (blind, separate context).** Use the dispatch template below; the worker reads `references/red-team-brief.md`. It gets the docs + the confirmed wedge but **not** your draft card, and returns: its own top load-bearing assumptions, where the concept still serves the *assumed* problem, how it fails at scale, and the single most-likely self-deception. Write its raw output to `solution-design/red-team.md`. **Degrade:** if no spawn tool, run it as an adversarial fresh-framing second pass and flag it weaker.
2. **Reason the Drift Audit** over the ledger + validated baseline (`references/drift-audit.md`): the assumed→validated table, marking each row `✅ serves it / ⚠️ drifting / ❌ still solving the old problem`.
3. **Extract & rank assumptions.** Assemble every material assumption (yours + the adversary's) into `solution-design/assumptions.json`, each scored `leverage` and `uncertainty` (1–5) per `references/assumption-ranking.md`, then:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/rank_assumptions.py" docs/ideas-stages/<slug>/solution-design/assumptions.json
```
It ranks by leverage×uncertainty, features the **top 3**, and flags any `source: adversary` assumption that lands in the top 3 (an assumption you never listed is among your riskiest). Each top assumption gets its **cheapest test → MVP RAT**.
4. **Reconcile** your draft against the blind adversary and write `solution-design/reconciliation.md` — every assumption or drift the adversary found that you missed is surfaced as a finding, not buried.

### Step 6 — Synthesize the action card

Read `references/solution-design-template.md`. Compose `solution-design.md` (draft in chat first) with all
nine sections: **Concept Read** (`build` / `narrow` / `redesign` / `reconsider`, 1 line + rationale, non-binding),
**The Solution Concept**, **Drift Audit**, **Three Load-Bearing Assumptions** (script-ranked top 3),
**Alternatives Considered**, **Scale Conditions**, **Challenge** (the red-team + reconciliation gaps),
**MVP Brief** (the forward contract), **Hypothesis Updates Flagged**. Apply the honesty rule: a `❌`
drift row or an unsupported top-3 assumption pushes the Read toward `redesign` / `reconsider` — do not
launder it into `build`.

### Step 7 — Final review and write

Print the full draft card in chat. Fire `AskUserQuestion`:
- **Ship it** → write `solution-design.md` (provenance is already on disk; for append-round, also write `solution-design/rounds/round-<N>.md`).
- **Proceed past a KILL Discovery Read** *(only offered when the verdict was KILL and the founder is proceeding)* → write the file and stamp: `<Read> | Override: founder proceeded past KILL Discovery Read on <ISO-date> — concept narrowed to <wedge>`.
- **Refine** → founder names what to redo in `notes`; return to the relevant step.
- **Abort** → write nothing; provenance stays on disk.

### Step 8 — Exit message (route by Concept Read)

- `build` / `narrow`: *"Solution design written. Next: the MVP stage (not yet built) will consume the MVP Brief — the wedge, the prioritized riskiest-assumption-tests, the validated profile, the non-goals. Build the cheapest test of the #1 assumption first."*
- `redesign`: *"The drift audit flagged the concept is still serving the assumed problem. Re-run /solution-design (Refine) on the corrected concept before building."*
- `reconsider`: *"The load-bearing assumptions aren't supported (or discovery was KILL). Step back: more /customer-discovery on the riskiest assumptions, or /sharpen-hypothesis to rework the problem."*
- If **Hypothesis Updates Flagged** is non-empty: *"The design flagged hypothesis updates — run /sharpen-hypothesis <slug> to apply them, then re-run the downstream stages."*

## Subagent dispatch template

Literal template. Substitute `<UPPER_PLACEHOLDERS>` at dispatch. **Resolve `${CLAUDE_SKILL_DIR}` to this
skill's absolute path** when composing — the subagent runs in its own context and won't expand it.
Do not set model/effort on the dispatch — the `solution-red-team` frontmatter pins Opus + `xhigh`.

### solution-red-team (Step 5, dispatched BLIND — no draft card)

```
You are the solution-red-team for a committed startup idea that has been through sharpen-hypothesis, pressure-test, market-research, and customer-discovery. You are NOT a balanced reviewer — your job is to find where this solution concept fails and where the founder is fooling themselves. You are working BLIND: you do not get the founder's drafted design card, only the validated evidence and the bare concept wedge, so that your assumptions and drift findings are independent.

First: Read ${CLAUDE_SKILL_DIR}/references/red-team-brief.md and follow it.

The concept wedge (founder-confirmed): <WEDGE_ONE_LINER + VALIDATED_WHO + CORE_JOB + NON_GOALS>

Context (the validation evidence):
- Reconstructed validated baseline (assumed problem + applied deltas): <VALIDATED_BASELINE>
- Delta ledger (every flagged update + Discovery verdict + tripped criteria, verbatim): <DELTA_LEDGER>
- Hypothesis / pressure-test / market-research highlights: <UPSTREAM_HIGHLIGHTS>
- Founder edge + constraints (from founder-profile.md): <FOUNDER_CONTEXT>

Produce, independently:
1. Your OWN top load-bearing assumptions this concept depends on — the ones that, if false, collapse it. For each: why it's load-bearing + what would have to be true. (Do not try to guess the founder's list — generate yours from scratch.)
2. Drift: every place a concept built on this wedge is still serving the problem the hypothesis ASSUMED rather than the one discovery VALIDATED. Cite the delta/verdict.
3. Scale failure: how this breaks at scale (distribution, unit economics, defensibility, whether the founder's stated edge is durable).
4. The single most likely way this founder is fooling themselves here.

Be specific and cite the evidence. Do not soften to be fair — fairness is the main conversation's job.
Write your challenge to: docs/ideas-stages/<SLUG>/solution-design/red-team.md
Return one line naming the concept + the doc path — not the contents.
```

## Reference files

- `references/solution-design-template.md` — the 9-section `solution-design.md` card structure. Read in Steps 4 and 6.
- `references/drift-audit.md` — how to reconstruct the validated baseline (hypothesis + accumulated deltas) and build the assumed→validated table; what counts as drift. Read in Steps 3 and 5.
- `references/assumption-ranking.md` — the leverage×uncertainty rubric, the `assumptions.json` schema, the per-assumption row schema, and the RAT→MVP mapping. Read in Step 5.
- `references/red-team-brief.md` — the `solution-red-team` blind-challenge protocol. Read by the worker at dispatch.

## Bundled scripts

- `scripts/build_delta_ledger.py` — scans the idea's docs for every *"Hypothesis Updates Flagged"* block + the **latest-round** Discovery Read verdict (with `verdict_source`) + TRIPPED/CLEARED criteria + any override and prints them verbatim as JSON, so no flagged delta is dropped before reasoning. Degrades to listing (and raw-grepping) candidate sections when a header deviates. Stdlib-only; runs under `python3` or self-executes via `uv run --script`.
- `scripts/rank_assumptions.py` — reads `assumptions.json` (per-assumption leverage + uncertainty, 1–5), computes leverage×uncertainty, ranks, features the top 3, and flags adversary-sourced assumptions that reach the top 3. Bundled so the ranking can't be fudged by eye (mirrors `/customer-discovery`'s `score_criteria.py`). Stdlib-only.

## Composition

- **Upstream:** `/customer-discovery` writes the required `customer-discovery.md`; `/pressure-test`, `/market-research`, `/sharpen-hypothesis` supply the assumptions, positioning, and the assumed baseline. Floor guard = `customer-discovery.md`.
- **Downstream:** the **MVP stage (not yet built)** consumes `solution-design.md`'s **MVP Brief** — the wedge, the prioritized riskiest-assumption-tests, the validated profile, the non-goals. Hypothesis updates route back through `/sharpen-hypothesis`; a `reconsider` Read routes back to `/customer-discovery`.
- **Worker:** `solution-red-team` under `.claude/agents/`, dispatched at runtime.
- **Optional:** any one `*-perspective` skill as an a-la-carte design lens (never the full panel).

## Scope

- **In:** crystallizing the concept from the validated docs, the drift audit, the three-assumptions exercise (script-ranked), alternatives + scale conditions, the blind red-team + reconciliation, the action card + MVP Brief + provenance.
- **Out:** editing `hypothesis.md` (`/sharpen-hypothesis`). Market sizing / competitor mapping (`/market-research`). The persona panel (`/pressure-test`). Running/synthesizing interviews (`/customer-discovery`). MVP/build work (next stage). Inventing persona skills (`/nuwa-skill`).
