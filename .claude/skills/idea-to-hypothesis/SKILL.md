---
name: idea-to-hypothesis
description: |
  Thin orchestrator for the Idea Stage of Soriza Startup Layer — runs the whole
  on-ramp in one flow when the founder has research/a thesis but no idea AND wants
  to land on a testable hypothesis. Wires three existing skills with the founder in
  the loop: /generate-ideas (10 ideas → 1-3 picks) → founder commits to ONE pick →
  hands that pick's Hypothesis seed to /sharpen-hypothesis (which still interviews and
  can still refuse) → then offers /pressure-test. It generates nothing and sharpens
  nothing itself; it removes the manual copy-paste between steps and keeps every human
  gate intact.
when_to_use: |
  Use when the founder wants to go from research to a testable hypothesis in one pass —
  "turn my research into a hypothesis I can pressure-test", "generate ideas AND sharpen
  one", "take me from this thesis to something testable", "ideas then hypothesis", "run
  the whole idea stage", "I have research but no idea — get me to a hypothesis". Do NOT
  use for a single step: "just generate ideas" routes to /generate-ideas; "sharpen my
  hypothesis" / "I already have a concrete idea" routes to /sharpen-hypothesis directly.
argument-hint: "[theme-slug]"
allowed-tools: AskUserQuestion, Read, Glob, Skill
effort: high
---

# Idea to Hypothesis

A **thin orchestrator** over the Idea Stage on-ramp. The founder has done research — a thesis, a market they watch, issues spotted on the web — but no concrete idea, and wants to come out the other side with a *testable hypothesis* ready for `/pressure-test`. This skill walks them through the existing pipeline without the manual copy-paste between steps.

- **Input:** the founder's research/thesis (or an `ideas.md` already produced this session).
- **Does:** `/generate-ideas` → founder commits to **one** pick → passes that pick's **Hypothesis seed** into `/sharpen-hypothesis` → offers `/pressure-test`.
- **Owns no files.** It reads `ideas.md` and routes; the wrapped skills write their own outputs in their own namespaces.

## When this skill applies

- "Turn my research into a hypothesis I can pressure-test."
- "Generate ideas and then sharpen the best one into something testable."
- "Run the whole idea stage for me — I have a thesis but no idea yet."

Out of scope (route elsewhere): just brainstorming a menu (`/generate-ideas`), sharpening an idea the founder *already* has (`/sharpen-hypothesis`), adversarial review (`/pressure-test`). If the founder hands you a concrete idea or problem, don't generate alternatives — send them straight to `/sharpen-hypothesis`.

## Gotchas

- **This skill generates nothing and sharpens nothing itself.** It is pure orchestration. All ideas come from `/generate-ideas`; all sharpening (and the power to *refuse*) stays in `/sharpen-hypothesis`. If you find yourself writing ideas or composing a hypothesis sentence here, stop — you're doing a wrapped skill's job.
- **One pick, not three.** `/generate-ideas` recommends 1-3; here the founder commits to exactly **one** to carry forward. That focus gate is the point — a founder who tries to sharpen three hypotheses at once sharpens none. They can come back for the others later (the menu persists in `ideas.md`).
- **Never write into `docs/ideas-stages/`.** That namespace is `/sharpen-hypothesis`'s — it creates the per-idea folder and `hypothesis.md` itself. This orchestrator only *reads* `docs/idea-exploration/<theme>/ideas.md` and passes the seed forward as input. Writing a scaffold there yourself would (a) break the documented ownership boundary and (b) risk tripping sharpen-hypothesis's "all sections filled → skip the grill" path. Pass the seed as text; let sharpen-hypothesis own its file. This is enforced structurally, not just by convention: this skill carries no write-capable tool (`allowed-tools` is read + ask + route only), so it *cannot* write into any namespace — no hook needed.
- **The seed pre-fills the grill, it doesn't replace it.** A Hypothesis seed is four *provisional, "to be tested"* guesses (Who / How Often / How Severely / Status Quo). When you hand them to `/sharpen-hypothesis`, it still grills all four dimensions — the seed just makes its questions sharper and saves the founder a blank page. The interview, the specificity bar, and the rejection criteria are fully intact. If sharpen-hypothesis **refuses** the idea, this orchestrator refuses too: surface the rejection and offer the founder a different pick from the menu.
- **Never auto-fire `/pressure-test`.** It's an expensive 4-round, 4-6-persona panel. After `hypothesis.md` exists, *offer* it via `AskUserQuestion` — the founder opts in. Auto-running it (especially on multiple picks) is exactly the false-positive trap the pipeline exists to avoid.
- **Don't re-run `/generate-ideas` if a menu already exists.** If the founder just ran it, or an `ideas.md` for the theme is already on disk, skip generation and jump to the pick. Re-running burns research budget and produces a different menu mid-flow.

## Interaction model

Every founder decision routes through `AskUserQuestion` (pick one idea, run pressure-test or not) — matching the wrapped skills `/generate-ideas`, `/sharpen-hypothesis`, and `/pressure-test`. This skill adds no new question style; it just sequences the existing ones. Read any sibling skill for voice.

## Workflow

Goal: carry the founder from research to one sharpened, testable `hypothesis.md`, then hand them a clean choice about pressure-testing — without ever bypassing a wrapped skill's gate. Steps are ordered (a menu must exist before a pick; a pick before sharpening; sharpening before the pressure-test offer); within each step the bullets are constraints, not a script.

### Step 1 — Make sure a menu exists

- If an `ideas.md` for this theme already exists (founder just ran `/generate-ideas`, or `docs/idea-exploration/<theme-slug>/ideas.md` is on disk — use `Glob`/`Read` to check), use it. Don't regenerate.
- Otherwise invoke `/generate-ideas` (via the `Skill` tool, passing the `[theme-slug]` argument if given). Let it run its full flow — research, 10-idea menu, both checkpoints, the 1-3 recommended picks, and the `ideas.md` write. It owns that namespace and the founder's steer; don't shortcut its checkpoints.

### Step 2 — Commit to one pick

Read the recommended picks (the `## Recommended picks` deep dives) from `docs/idea-exploration/<theme-slug>/ideas.md`. Fire `AskUserQuestion` with the 1-3 picks as options (founder can also name a different menu idea in `notes`/Other):

- One option per recommended pick — the founder selects **exactly one** to carry into sharpening.
- If they pick a menu idea that has no deep dive / no Hypothesis seed, tell them the seed is what makes the handoff work and offer to either pick a recommended one or have `/generate-ideas` deep-dive their choice first.

### Step 3 — Hand the seed to `/sharpen-hypothesis`

- Read the chosen pick's **Hypothesis seed** block (the four bullets: Who / How Often / How Severely / Status Quo) from `ideas.md`.
- Invoke `/sharpen-hypothesis` (via the `Skill` tool), passing that seed as the founder's starting input — clearly framed as *provisional seed values to sharpen, not committed facts*. You are doing the copy-paste the founder would otherwise do by hand; that is this skill's entire value-add over running the steps separately.
- Then get out of its way. `/sharpen-hypothesis` runs its own interview, applies its own rejection criteria, composes the hypothesis sentence, and writes `docs/ideas-stages/<slug>/hypothesis.md`. Do not pre-empt, pre-compose, or skip any of that.
- **If it refuses:** surface the rejection plainly and fire `AskUserQuestion` — pick a different idea from the menu (return to Step 2) or stop here. Don't try to rescue a rejected idea by sharpening it yourself.

### Step 4 — Offer the pressure test

Once `hypothesis.md` exists, fire `AskUserQuestion`:

- **Pressure-test it now** — invoke `/pressure-test` on the new hypothesis.
- **Not yet** — print the handoff line and stop: *"`hypothesis.md` is ready under `docs/ideas-stages/<slug>/`. Run `/pressure-test` when you want the adversarial panel."*

Never run `/pressure-test` without this explicit opt-in.

## Scope

- **In:** sequencing `/generate-ideas` → one-pick gate → seed handoff to `/sharpen-hypothesis` → opt-in handoff to `/pressure-test`. Reading `ideas.md`. Killing the manual copy-paste between steps.
- **Out:** generating ideas, scoring/narrowing, drawing or composing the hypothesis, the four-dimension grill, rejection judgment, adversarial/persona review — every one of those belongs to a wrapped skill and stays there. Writing into `docs/ideas-stages/`. Market sizing / business model / GTM / customer discovery.

## Composition

- **Wraps:** `/generate-ideas` (Step 1), `/sharpen-hypothesis` (Step 3), `/pressure-test` (Step 4, opt-in).
- **Namespaces (untouched by this skill):** `/generate-ideas` owns `docs/idea-exploration/<theme>/`; `/sharpen-hypothesis` owns `docs/ideas-stages/<slug>/`. This orchestrator reads the former and writes neither.
- **Personas:** not used here — the `*-perspective` panel lives at `/pressure-test`, reached only by founder opt-in in Step 4.
- **Alternative entry:** a founder who wants only one step should invoke that step directly; this skill is for the end-to-end pass.
