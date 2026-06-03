---
name: market-research
description: |
  Third step in the Idea Stage of Soriza Startup Layer — maps the market for ONE idea that has
  passed /pressure-test. Runs four parallel research workstreams (competitive landscape by tier
  plus a competitor steelman, customer-review synthesis, lean SOM-weighted TAM/SAM/SOM + buyer
  map, trend tailwind/headwind analysis) and synthesizes a market-research.md action card with a
  soft Market Read (enter / enter-narrower / reposition / reconsider), the strongest competitor
  threat, and flagged hypothesis updates. Reads the idea's hypothesis.md + pressure-test.md under
  docs/ideas-stages; writes market-research.md + provenance docs under the idea's market-research folder.
when_to_use: |
  Use when the founder says "market research", "size the market", "map my competition",
  "competitive landscape", "who are my competitors", "TAM SAM SOM", "TAM/SAM/SOM",
  "competitor analysis", "is the market big enough", or "is the timing right". Also trigger
  on "what's next" / "the next step" WHEN a pressure-test.md already exists in the idea's
  docs/ideas-stages folder but market-research.md does NOT yet exist (precedence: no
  hypothesis.md → /sharpen-hypothesis; hypothesis.md only → /pressure-test; pressure-test.md
  → /market-research; market-research.md exists → /customer-discovery; customer-discovery.md →
  /solution-design). Do NOT trigger when
  only hypothesis.md exists (that's /pressure-test's "what's next"), nor once market-research.md
  already exists (that hands off to /customer-discovery).
argument-hint: "[slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob, WebSearch, WebFetch, Agent, Task, Skill
effort: high
---

# Market Research

Third step in the **Idea Stage** of the Soriza Startup Layer. Maps the market around one idea that already survived `/pressure-test`: who competes, what their customers can't get solved, how big the reachable opportunity is, and whether the timing is a tailwind. The deliverable is a synthesis with a point of view — not a verdict, and not four piles of raw facts.

- **Input:** `docs/ideas-stages/<slug>/pressure-test.md` (+ `hypothesis.md`), both produced earlier in the pipeline.
- **Output:** `docs/ideas-stages/<slug>/market-research.md` (the action card) + five provenance docs under `market-research/`.
- **Workers:** the `market-researcher` and `competitor-steelman` subagents (`.claude/agents/`), read at runtime.

## When this skill applies

- Founder has a `pressure-test.md` at `docs/ideas-stages/<slug>/` and asks "what's next"
- "Market research", "size the market", "map my competition", "who are my competitors"
- "TAM/SAM/SOM", "competitor analysis", "is the market big enough", "is the timing right"
- The hypothesis evolved and the founder wants the research refreshed (this stage is repeatable)

Out of scope: editing `hypothesis.md` (that's `/sharpen-hypothesis`), the adversarial persona panel (that's `/pressure-test`, exclusively), customer discovery, solution-concept design (`/solution-design`), and MVP work (later stages).

## Gotchas

- **This is the expensive stage; the entry guard exists to protect spend.** Require `pressure-test.md`. The pipeline is ordered so the cheap armchair panel filters ideas *before* you pay for deep, Opus-heavy research. If `pressure-test.md` is missing, refuse and send the founder back — do not run an inline mini-pressure-test.
- **Read the verdict before spending.** A `kill-suggested` / `refine-hypothesis` / override verdict means the panel already doubted this idea. Research can resurrect it (evidence the panel lacked) or confirm the burial — but that is the founder's eyes-open call. Surface it at scope-lock and get explicit confirmation; never silently burn tokens on an idea the panel killed.
- **Never edit `hypothesis.md`.** This skill *flags* hypothesis updates and routes the founder to `/sharpen-hypothesis`, which owns that file. Writing into it duplicates ownership and breaks the contract the other stages depend on.
- **No persona panel here.** The `*-perspective` advisors (Thiel, Bezos, …) live exclusively at `/pressure-test`, and they critique *your* hypothesis. The competitor-steelman is a different animal — it *champions the incumbent*. Reusing the panel breaks the boundary the sibling skills document and aims the wrong voice at the task.
- **The Market Read is a recommendation, not a gate.** Unlike `/pressure-test`'s computed verdict, the founder is not asked to "accept" it. The Playbook frames market research as ongoing research repeated as the hypothesis evolves — over-claiming it as a pass/fail decision is the failure mode.
- **Create `market-research/` before dispatching subagents.** Workers Write to a fixed path; if the directory doesn't exist the Write fails and the fan-out aborts. (Mirrors `/pressure-test`'s subdir gotcha.)
- **Self-contained is the default; `/deep-research` is optional.** `/deep-research` is a global skill that may not be installed. The skill must work without it — the verify step baked into the W2/W3 dispatch covers the claim-checking. Only offer the deep-mode toggle when `/deep-research` is in your available-skills listing.
- **Don't overstate thin signal.** If the spawn tool is unavailable and you ran workstreams inline (shallower), or a workstream came back with weak evidence (review-mining often does), say so in chat and in the doc. A confident-but-ungrounded market read is worse than an honest "signal here is thin."

## Interaction model

Hybrid: **scope-lock checkpoint → autonomous fan-out → final review.** Founder decisions route through `AskUserQuestion` with a `notes` escape hatch (house style — read `/pressure-test` or `/generate-ideas` for voice). Two thin gates bracket an autonomous core: the founder confirms the scope once up front and reviews the synthesis once at the end; everything between runs without interruption. This skill's quality scales with research depth — run it at `high` effort or above; the subagents carry their own effort.

## Workflow

Goal: lock scope, fan out five research workers in parallel, synthesize a `market-research.md` action card, and write it on confirmation. Steps are ordered where order is real (guard before scope-lock, scope-lock before fan-out, fan-out before synthesis); within each step the bullets are constraints, not a script.

### Step 1 — Resolve slug and entry guard

The founder never has to type the startup name — resolve the slug yourself, in this order:

1. If invoked with a slug (e.g. `/market-research personalized-ai-digest`), use it.
2. Otherwise `glob docs/ideas-stages/*/` for ideas that have a `pressure-test.md`:
   - **Exactly one** → use it automatically. Just state in chat which idea you're researching — no question.
   - **More than one** → fire `AskUserQuestion` listing them so the founder picks one (selecting, not typing).
   - **None** → if idea folders exist but none has a `pressure-test.md`, point the founder at `/pressure-test`; if there are no idea folders at all, point them at `/sharpen-hypothesis`. Stop.

Read `docs/ideas-stages/<slug>/pressure-test.md` and `hypothesis.md`.

**Entry guard:** if `pressure-test.md` is missing, refuse with exactly: *"No pressure-test at `docs/ideas-stages/<slug>/pressure-test.md`. Run /pressure-test first — market research runs on an idea that's already survived the panel."* Stop. Write nothing.

Read the verdict value on the line **under** the `## Verdict` heading of `pressure-test.md` (e.g. `**kill-suggested** — …`, not the heading line itself) and hold it for Step 3. Also pull the **open risks and the anti-thesis flag** from `pressure-test.md` (its disconfirmation questions / kill-criteria and the seat tagged anti-thesis) and hold them for the Step 4 `competitor-steelman` dispatch — they fill its `<RISKS>` slot.

### Step 2 — Resume check

If `docs/ideas-stages/<slug>/market-research.md` already exists, fire `AskUserQuestion`:

- **Overwrite from scratch** — `rm -rf docs/ideas-stages/<slug>/market-research/` and proceed
- **Append a timestamped new round** — keep the file; write new provenance under `market-research/<ISO-date>/` (get the date via `date +%F`) and append a `## Round <N> (<date>)` section to `market-research.md`
- **Skip and exit** — print the existing Market Read line, do nothing else

### Step 3 — Scope-lock checkpoint

Extract the scope from the idea docs rather than asking blank: from `hypothesis.md`/`pressure-test.md`, pull the **named competitors / incumbents**, the **segment**, the **geography**, and a **price hypothesis** (infer one if absent). Best-effort detect priors: `glob docs/idea-exploration/*/research/` — if a related theme's research exists, note it as available to fold in (no guaranteed slug↔theme mapping; founder confirms relevance). If the idea docs name no competitors (e.g. status quo is "nothing"), run a quick discovery search to propose a seed set for the founder to confirm rather than handing the steelman an empty list — W1 then expands it ("seed, not the ceiling").

Fire one `AskUserQuestion` that shows what you extracted and lets the founder confirm or correct in `notes`:

- Surface the pressure-test **verdict**. If it is `kill-suggested` / `refine-hypothesis` / override, state it plainly and make proceeding the explicit choice (*"the panel suggested killing this; research can resurrect it with evidence or confirm the burial — proceed?"*).
- Offer to fold in any detected `/generate-ideas` priors.
- **Deep-mode toggle** — offer this option *only if* `/deep-research` appears in your available-skills listing: routes W2 (reviews) and W3 (sizing) through `/deep-research` for adversarial claim-verification depth, at the cost of running those two sequentially rather than in parallel.

The founder's confirmed `competitors / segment / geography / price hypothesis` become the scope every worker is seeded with. A wrong competitor set here poisons all five docs — this is the highest-leverage human input in the skill.

### Step 4 — Fan out the research workers (parallel)

Create the output directory first — the **provenance base** is `market-research/` normally, or `market-research/<ISO-date>/` if you chose append-round in Step 2 (substitute it as `<PROVENANCE_DIR>` in the dispatch templates):
```
docs/ideas-stages/<slug>/<PROVENANCE_DIR>/
```

**Default (self-contained):** dispatch all **five** subagents in a single assistant message so they run in parallel — four `market-researcher` dispatches (one per workstream) and one `competitor-steelman`. Use the dispatch templates below; the per-workstream briefs and provenance doc shapes live in `references/workstream-briefs.md`, which each worker reads. All four `market-researcher` dispatches run on the agent's pinned **Opus** (`xhigh` effort) — including **W2 (review-synthesis)**, whose ≥2-source verify and `strong`/`weak`/`none` Problem–Solution-Fit verdict are reasoning, not just retrieval. (To trim cost later, split W2 into a cheap Sonnet review-*gathering* sub-pass feeding an Opus verify/synthesis pass — never run the whole verdict on Sonnet.)

Workstream → provenance doc (substituted as `<WORKSTREAM_NAME>` / `<DOC_NAME>` in the template): W1 → `competitive-landscape.md`, W2 → `review-synthesis.md`, W3 → `market-sizing.md`, W4 → `trends.md`; the steelman → `competitor-steelman.md`.

**Deep-mode (if toggled on):** dispatch W1, W4, and the steelman as parallel subagents; run **W2 and W3 through `/deep-research`** as sequential sub-steps. Invoke the Skill with a fully-specified research question that *embeds the W2/W3 output shape from `references/workstream-briefs.md`* (so it does not pause to clarify, and returns the fields Step 5 reads). Reshape the returned report into that exact shape, then write it under the same `<PROVENANCE_DIR>` the parallel workers use (so an append-round doesn't clobber the prior round) — W2 → `docs/ideas-stages/<slug>/<PROVENANCE_DIR>/review-synthesis.md`, W3 → `<PROVENANCE_DIR>/market-sizing.md` — so the synthesis's field reads (ranked complaint → Positioning, SOM → Sizing, `strong`/`weak`/`none` → Problem–Solution-Fit) find their inputs.

**Degrade:** if no `Agent`/`Task` spawn tool exists, run the four workstreams inline with WebSearch/WebFetch using the same briefs, keeping only distilled findings — do not stop. Run the steelman inline too, holding the hard adversarial frame. Tell the founder in chat that research ran inline (shallower, fewer parallel angles) so they can weigh citation depth.

When all workers report, Read each provenance doc to confirm content (an inline degrade run holds its findings in context — there are no docs to read). Print a one-line summary per workstream in chat.

### Step 5 — Synthesize the action card

Read all five provenance docs (or, if you ran inline, use the distilled findings you already hold). Read `references/output-template.md` for the action-card structure. Compose `market-research.md` (draft in chat first):

- **Market Read** — `enter` / `enter-narrower` / `reposition` / `reconsider`, one line + 1–2 sentences of rationale tied to the evidence. Non-binding.
- **Positioning & Wedge** — the unresolved complaint (from W2) this idea is uniquely placed to own.
- **Strongest Threat** — the single most-dangerous competitor and the steelman's core "they win, you lose" argument.
- **Sizing Reality** — SOM + willingness-to-pay + budget-holder, in 2–3 lines (from W3).
- **Timing** — net tailwind/headwind across the three trends (from W4).
- **Problem–Solution-Fit** — `strong` / `weak` / `none`, from whether the hypothesis addresses W2's top unresolved complaints.
- **Hypothesis Updates Flagged** — evidence that contradicts or should sharpen the hypothesis; route to `/sharpen-hypothesis`. Do not edit `hypothesis.md`.

Apply the honesty rule: flag any workstream that ran inline or came back thin; never present weak signal as validation.

### Step 6 — Final review and write

Print the full draft action card in chat. Fire `AskUserQuestion`:

- **Ship it** → write `docs/ideas-stages/<slug>/market-research.md` (provenance docs are already on disk; the action card cross-references them)
- **Refine** → founder names what to redo in `notes` (re-run a workstream, re-scope, re-weight the read); return to the relevant step
- **Abort** → no action card written; the provenance docs stay on disk; exit cleanly

### Step 7 — Exit message

- If **Hypothesis Updates Flagged** is non-empty: *"Market read written. The research flagged hypothesis updates — run `/sharpen-hypothesis <slug>` to apply them, then re-run `/pressure-test <slug>` before you build."*
- Otherwise: *"Market read written to market-research.md. Next: run `/customer-discovery <slug>` to take the wedge and disconfirmation targets into customer discovery with real people. Re-run this stage whenever the hypothesis evolves."*

## Subagent dispatch templates

Literal templates. Substitute `<UPPER_PLACEHOLDERS>` at dispatch — including `<PROVENANCE_DIR>` (Step 4) and `<DOC_NAME>` (the workstream→file mapping above). **Resolve `${CLAUDE_SKILL_DIR}` to this skill's absolute directory path when you compose each dispatch** — the subagent runs in its own context and won't expand the variable itself, so pass the already-resolved absolute path to `references/workstream-briefs.md`. Do not set model/effort on the dispatch — the `market-researcher` and `competitor-steelman` frontmatter pins Opus + `xhigh`.

### market-researcher (W1–W4)

```
You are the market-researcher for a committed startup idea that has passed sharpen-hypothesis and pressure-test. Reason hard about what matters for sizing and positioning THIS one idea — distill, quantify, cite, never dump.

First: Read ${CLAUDE_SKILL_DIR}/references/workstream-briefs.md and follow the brief for workstream: <WORKSTREAM_NAME>

Context:
- Hypothesis (full): <HYPOTHESIS_FULL_CONTENT>
- Scope-locked, founder-confirmed: competitors=<LIST>; segment=<SEGMENT>; geography=<GEO>; price hypothesis=<PRICE>
- Priors to build on (optional): <PRIOR_DOC_PATHS or "none">

Use WebSearch/WebFetch for current, primary evidence.
<IF W2 OR W3:> Adversarial verify: cross-check every load-bearing claim against ≥2 independent sources. Flag any claim you cannot verify rather than asserting it.

Write your findings to: docs/ideas-stages/<SLUG>/<PROVENANCE_DIR>/<DOC_NAME>.md
using the exact output shape given for this workstream in workstream-briefs.md.

Return one line naming the workstream + the doc path — not the findings; they live in the file.
```

### competitor-steelman

```
You will channel the strategist of this founder's most dangerous competitor. You are NOT a neutral analyst — you ARE the incumbent's strategist. Make the most compelling case that you beat this founder and that their differentiators are not defensible. No hedging, no both-sides.

First: Read ${CLAUDE_SKILL_DIR}/references/workstream-briefs.md and follow the competitor-steelman brief.

Context:
- Hypothesis (full): <HYPOTHESIS_FULL_CONTENT>
- Scope-locked competitor set (founder-confirmed): <LIST>
- Pressure-test open risks / anti-thesis flag, if any: <RISKS or "none">

Argue, per tier (direct / indirect / potential-acquirer / adjacent), why each genuinely threatens the founder — the real threat, not the easy-to-dismiss version. Then name the single most dangerous competitor and make the full "we win, you lose" case.

Write to: docs/ideas-stages/<SLUG>/<PROVENANCE_DIR>/competitor-steelman.md
Return one line + the doc path.
```

## Reference files

- `references/workstream-briefs.md` — the four `market-researcher` workstream briefs (W1–W4) and the `competitor-steelman` brief, each with its provenance-doc output shape. Workers read it at dispatch.
- `references/output-template.md` — the `market-research.md` action-card structure. Read in Step 5.

## Composition

- **Upstream:** `/pressure-test` writes the required `pressure-test.md`. Without it, this skill refuses.
- **Downstream:** `/customer-discovery` is the immediate next stage — it reads `market-research.md` (the wedge, buyer map, sizing reality) plus `pressure-test.md` (the Kill Criteria) to design interviews and score real evidence. `/solution-design` and then MVP work follow. Hypothesis updates route back through `/sharpen-hypothesis`.
- **Workers:** `market-researcher` and `competitor-steelman` under `.claude/agents/`, dispatched at runtime. New on a committed idea, not the ideation-tuned `startup-idea-researcher`.
- **Optional:** `/deep-research` for W2/W3 when installed and toggled on. Never a hard dependency.

## Scope

- **In:** locking scope from the idea docs, fanning out the four workstreams + steelman, synthesizing the action card, flagging hypothesis updates, writing the deliverable + provenance.
- **Out:** editing `hypothesis.md` (`/sharpen-hypothesis` owns it). The persona panel (`/pressure-test`'s, exclusively). Customer discovery / MVP. Inventing persona skills (`/nuwa-skill`).
