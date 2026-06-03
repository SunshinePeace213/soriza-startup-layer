---
name: generate-ideas
description: |
  Optional on-ramp to the Idea Stage of Soriza Startup Layer — sits upstream of
  /sharpen-hypothesis. For a founder who has researched a thesis or spotted issues/trends
  on the web but has NO concrete startup idea yet. Collects latest info from the internet
  (parallel research subagents + domain knowledge), generates 10 startup ideas, then
  narrows to the 1-3 most suitable with explanation, cited references, and a ready-to-paste
  hypothesis seed. Writes an ideas.md under docs/idea-exploration/, which feeds
  /sharpen-hypothesis next.
when_to_use: |
  Use when the founder says "generate startup ideas", "help me come up with ideas", "turn
  this thesis/research into startup ideas", "I found these issues/trends on the web — what
  could I build", "I have research but no idea yet", "give me startup ideas from this
  market", or pastes web research / observations and asks what to build. Do NOT use when
  the founder already has a concrete idea or problem to sharpen or test — that routes to
  /sharpen-hypothesis ("sharpen my hypothesis", "is this testable") and then /pressure-test.
argument-hint: "[theme-slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, WebSearch, WebFetch, Agent, Task, Glob
effort: high
---

# Generate Ideas

Optional **on-ramp to the Idea Stage** of the Soriza Startup Layer, upstream of `/sharpen-hypothesis`. The founder who triggers this has done research — a thesis, a market they keep watching, issues they spotted on the web — but no concrete startup idea to hand the next skill. Turn that research into 10 grounded startup ideas, narrow to the 1-3 most suitable with explanation + references, and hand each pick forward as a ready-to-draw hypothesis.

- **Input:** the founder's pasted research (thesis / observations / URLs) + a short context intake.
- **Output:** `docs/idea-exploration/<theme-slug>/ideas.md` — 10-idea menu, 1-3 deep-dive picks, references.
- **Downstream:** founder carries one pick's *Hypothesis seed* into `/sharpen-hypothesis`.

## When this skill applies

- "I've been researching X — generate some startup ideas I could build."
- "I keep seeing this problem on the web but don't know what to build."
- Founder pastes notes / links / a market thesis and asks "what's the opportunity here?"
- "Give me ideas from this space, then tell me which are worth pursuing."

Out of scope: drawing the actual hypothesis (`/sharpen-hypothesis`), adversarial persona review (`/pressure-test`), market sizing / business model / GTM, customer discovery. If the founder *already* has a concrete idea, send them straight to `/sharpen-hypothesis` — don't generate alternatives they didn't ask for.

## Gotchas

- **`<theme-slug>` is a research theme, never an idea.** This skill writes to `docs/idea-exploration/<theme>/`, a separate namespace from `docs/ideas-stages/<slug>/` where one slug = one idea. Keeping them separate is deliberate: many candidate ideas live under one theme here; one idea progresses through stages there. Never write into `docs/ideas-stages/` — that's `/sharpen-hypothesis`'s territory, and it creates the per-idea folder itself when the founder carries a pick forward.
- **Research subagents must return distilled findings + source URLs, not raw web dumps.** You synthesize 10 ideas from their output; raw search-result pages would blow the synthesis context and bury the signal. The template enforces this — hold the line on it.
- **Degrade gracefully if no spawn tool exists.** Unlike `/pressure-test`, subagent isolation here is only context hygiene, not load-bearing. Research dispatches the `startup-idea-researcher` agent type (`.claude/agents/startup-idea-researcher.md`); if `Agent`/`Task` or that agent type is unavailable, run the four research facets inline with WebSearch/WebFetch and keep only distilled findings — do NOT stop.
- **No distilled-persona panel here.** The `*-perspective` advisors (Thiel, Bezos, Munger…) live exclusively at `/pressure-test`. Narrowing 10→1-3 uses the transparent rubric, not a persona vote — reusing the panel would duplicate the next step and break the established boundary.
- **The Hypothesis seed is the load-bearing deliverable.** Each pick's seed pre-frames `/sharpen-hypothesis`'s four dimensions (Who / How Often / How Severely / Status Quo). It's what turns "basic understanding" into "able to draw a hypothesis." A pick without a usable seed hasn't done its job.
- **Generate exactly 10, narrow to 1-3 — not "around 10" or "the top few".** The count is the contract: 10 gives real range to choose from; 1-3 (only those clearing the rubric bar — it's fine to recommend just 1) keeps the founder focused.

## Interaction model

All founder decisions route through `AskUserQuestion` — the founder commits by picking an option and/or typing specifics in `notes` / the auto-provided "Other". The skill provides shape and perspective (research, idea shapes, the rubric); the founder owns the direction and the picks. This matches the sibling skills `/sharpen-hypothesis` and `/pressure-test`; read either for voice if unsure.

This skill's quality scales with research depth and synthesis quality — **run it at high effort or above**. The research subagents already carry `effort: high` in their own frontmatter, so you don't set model/effort on the spawn (Step 4).

## Workflow

Goal: research-ground the founder's thesis, generate 10 ideas, narrow to 1-3 with a hypothesis seed each, and write `ideas.md`. Steps are ordered where order is real (capture before research, research before generation, generation before narrowing); within each step the bullets are constraints, not a script.

### Step 1 — Capture research + founder context

If the founder pasted research with the invocation, use it. Otherwise fire one `AskUserQuestion` to capture the starting point (shape options: a thesis/trend they believe in / a problem space they keep noticing / a market or audience they want to serve — founder types the actual research in `notes`/Other).

Then run a **short** intake (1-3 `AskUserQuestion` rounds, not the deep grill `/sharpen-hypothesis` runs — the founder already did research) to capture founder context that makes ideas tailored rather than generic:

- **Domain focus** — which slice of the thesis to mine for ideas
- **Founder-market fit** — background, skills, unfair advantage, what excites them
- **Hard constraints** — B2B vs consumer, budget/capital, regulatory appetite, geography

Bundle these into as few questions as cover them. Capture the free text — it feeds both research and the rubric's founder-market-fit dimension.

### Step 2 — Guard

Two reasons to stop before generating:

- **Thin input** — after intake there's still no usable thesis or domain to ground ideas on (the founder gave nothing concrete). Ask once more; if still empty, decline rather than emit 10 hollow ideas. Tell them what sharper observation looks like and invite them back.
- **Clearly harmful** — the idea space is illegal/unethical (surveillance of minors, fraud enablement, etc.). Decline, mirroring `/sharpen-hypothesis`'s bar.

No testability gates here (identifiable-segment, painkiller tests) — that's `/sharpen-hypothesis`'s job. Ideation is meant to explore *before* the problem is sharp.

### Step 3 — Theme slug + resume

Propose a `<theme-slug>` derived from the research theme (e.g. `restaurant-inventory-waste`) as the recommended `AskUserQuestion` option with 2-3 alternates. This names the folder `docs/idea-exploration/<theme-slug>/` — it's a theme, not an idea. If invoked with a `[theme-slug]` argument, use it.

If `docs/idea-exploration/<theme-slug>/ideas.md` already exists, fire `AskUserQuestion`:
- **Overwrite from scratch** — regenerate fresh
- **Append a new round** — keep the file; add a `## Round <N> (<date>)` section with new ideas (pass a date in via Bash, e.g. `date +%F`)
- **Skip and exit** — print the existing picks, do nothing else

### Step 4 — Research the thesis (parallel)

Dispatch **3-4 `startup-idea-researcher` subagents in a single assistant message**, one per facet — invoke the `startup-idea-researcher` agent type (`.claude/agents/startup-idea-researcher.md`) and pass the **Research subagent template** below as each spawn's prompt. The subagent sets its own model and effort (`high`) in its frontmatter, so you don't set those on the spawn. Each returns a one-line confirmation + a findings path; the distilled findings + source URLs live in the file. Facets:

1. **Trends / why-now** — what changed recently (tech, regulation, behavior, cost curves) that makes this space live *now*
2. **Existing solutions & competitors** — who already serves this; where they fall short; what's saturated vs open
3. **Demand / pain validation** — evidence the founder's thesis is a real, felt problem (communities complaining, spend, workarounds, search/market signals). Community-pain evidence (forums, Reddit, reviews) surfaces poorly in a plain web search — use targeted site queries, and if this facet still comes back thin, say so rather than overstate weak signal as validation.
4. **Adjacent / analogous markets** — solutions in neighboring domains worth transplanting

When all report, Read each findings file (or, if you ran inline, you already hold the findings). Keep the source URLs — they become the References section.

**Degrade:** if no spawn tool exists, or the `startup-idea-researcher` agent type isn't registered, run the four facets inline with WebSearch/WebFetch using the same template, keeping only distilled findings + URLs. Do not stop — but tell the founder in chat that research ran inline (shallower, fewer parallel angles) so they can weigh how much to trust the citation depth.

### Step 5 — Generate 10 ideas

From the research findings + your domain knowledge, generate **exactly 10** startup ideas spanning the founder's thesis. Each is a tight menu entry (see `references/output-template.md`): name + one-line pitch + target user + wedge/mechanism + why-now. Make them genuinely distinct — vary the axis of attack across the set (target user, wedge, layer of the stack, demand-side vs cost-side, product vs marketplace vs service) so the 10 give real range, not 10 reskins of one idea.

### Step 6 — Checkpoint 1: menu steer

Print the 10 one-liners in chat. Fire `AskUserQuestion`:
- **On-target — narrow them** — proceed to the rubric
- **Regenerate with a different angle** — founder says what's off in `notes` (too B2B, wrong segment, too incremental…); regenerate the 10 and return here. Escape hatch for a whole batch that missed.
- **Let me flag favorites** — founder names ones to weight up in `notes`; carry that into the rubric

### Step 7 — Score and narrow to 1-3

Read `references/scoring-rubric.md`. Score all 10 on the five dimensions (pain severity, why-now timing, founder-market fit, wedge/defensibility, feasibility), then recommend the top **1-3** — only those clearing the bar; recommending a single strong idea beats padding to three. For each recommended pick, write the explanation tied to its scores. No persona panel, no script — this is transparent judgment scoring.

### Step 8 — Checkpoint 2: confirm picks

Present the 1-3 with their rubric-tied explanations. Fire `AskUserQuestion`:
- **Ship these** — proceed to write
- **Swap one** — founder names which menu idea to substitute in `notes`
- **Pick different** — founder chooses their own 1-3 from the menu in `notes`; you still write the deep dives for them

### Step 9 — Write `ideas.md` (only after confirmation)

`mkdir -p docs/idea-exploration/<theme-slug>/` via Bash, then Write `docs/idea-exploration/<theme-slug>/ideas.md` using the structure in `references/output-template.md`: research summary → 10-idea menu → 1-3 deep-dive picks (each with a **Hypothesis seed**) → numbered References. Deep dives keep market sizing / business model / GTM out — those belong to later stages.

Before declaring done, re-read the file and confirm it holds: exactly 10 numbered menu items, the agreed 1-3 picks, a four-slot Hypothesis seed (Who / How Often / How Severely / Status Quo) under every pick, and a numbered reference behind every why-now and competitor claim. The "exactly 10" contract is easy to break in a single Write pass — verify it, don't assume it.

### Step 10 — Exit message (chat, not in the file)

Print: *"Pick one to pursue first, run `/sharpen-hypothesis`, and paste its **Hypothesis seed** from `ideas.md`. Come back for the others when you're ready."*

## Research subagent template

Used two ways: as the **spawn prompt** when dispatching the `startup-idea-researcher` agent type (the agent's frontmatter already sets its model + `high` effort and holds the invariant distill-don't-dump / cite-URLs rules — this template supplies the per-facet specifics), and as the **inline fallback** when no spawn tool / the `startup-idea-researcher` agent is unavailable. Substitute `<UPPER_PLACEHOLDERS>` at dispatch. Dispatch all facets in one message. `<FACET_NAME>`/`<FACET_BRIEF>` come from the four facets in Step 4; `<FINDINGS_PATH>` is `docs/idea-exploration/<theme-slug>/research/<facet-name>.md`.

```
Research one facet of a founder's startup thesis. Your output feeds idea generation, so return DISTILLED findings, not raw pages — specific facts, numbers, names, and shifts, each with a source.

Facet: <FACET_NAME>
What to find: <FACET_BRIEF>

Founder's thesis / research:
<THESIS_AND_RESEARCH>
Founder context (constraints, focus): <FOUNDER_CONTEXT>

Use WebSearch/WebFetch to gather current information (prioritize recent sources). Reason hard about what actually matters for spotting startup opportunities in this space — don't just summarize the first results.

Use the Write tool to save your findings to:
<FINDINGS_PATH>

Output structure (Markdown):
# <FACET_NAME> — Findings
## Key findings
- <specific fact / shift / number / named player> — why it matters for an idea here
- ... (5-10 bullets, each tied to opportunity)
## Sources
1. <URL> — what it supports
2. ...

No preamble. Distilled signal only.
```

If running inline (no spawn tool), produce the same `Key findings` + `Sources` shape per facet directly in context.

## Reference files

- `references/scoring-rubric.md` — the five-dimension rubric and how to narrow 10→1-3. Read in Step 7.
- `references/output-template.md` — the `ideas.md` structure: menu-entry schema, deep-dive schema, Hypothesis-seed format, References format. Read before Step 5 (shapes the menu) and Step 9 (writes the file).

## Scope

- **In:** research-grounding the thesis with citations, generating 10 distinct ideas, transparent rubric narrowing to 1-3, the per-pick hypothesis seed and the handoff.
- **Out:** drawing the hypothesis itself (`/sharpen-hypothesis`), adversarial/persona review (`/pressure-test`), market sizing / business model / GTM, customer discovery. Inventing new persona skills (`/nuwa-skill`).

## Composition

- **Upstream:** none — this is an entry on-ramp.
- **Downstream:** `/sharpen-hypothesis` consumes a chosen pick's Hypothesis seed (founder pastes it). This skill never writes into `docs/ideas-stages/`.
- **Personas:** not used here. The `*-perspective` panel is `/pressure-test`'s. The `startup-idea-researcher` subagent is a generic web researcher, not a persona.
