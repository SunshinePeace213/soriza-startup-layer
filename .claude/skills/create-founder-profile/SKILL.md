---
name: create-founder-profile
description: Onboard a founder into the Soriza Startup Layer. Use when the founder says "create/set up/build my founder profile", "onboard me", "tell Claude about me/my background", "tailor advice to my situation", "set up the startup layer for me", or wants to give Claude their background before the Idea Stage. Interviews once and writes a reusable founder profile (background, skills/unfair advantage, interests, location, risk appetite, team, time + interaction preferences) to docs/founder-profile.md, then wires the CLAUDE.md @import so every idea-stage skill auto-loads it. Re-runnable — reads an existing profile and only asks about missing or changed fields.
when_to_use: |
  Use when the founder says "create my founder profile", "set up my profile", "build my
  profile", "onboard me", "tell Claude about my background", "founder profile", "set up
  the startup layer for me", "make Claude tailor advice to me", "update my profile", or
  asks how to give Claude their background before starting the Idea Stage. This is the
  onboarding step upstream of the whole Idea Stage (every idea-stage skill reads the profile).
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash
---

# Create Founder Profile

Onboarding step for the Soriza Startup Layer. Interview the founder once, write a reusable **founder-level profile** to `docs/founder-profile.md`, and wire the `CLAUDE.md` `@import` so every idea-stage skill loads it automatically and tailors its advice. Profile facts are per-founder data; `CLAUDE.md` stays founder-agnostic so anyone can clone this layer and run their own profile.

## When this skill applies

- "Create / set up / build my founder profile"
- "Onboard me" / "set up the startup layer for me"
- "Tell Claude about my background so it tailors advice"
- "Update my profile" (re-run to edit specific fields)

## Gotchas

- **The `@import` path is resolved relative to `CLAUDE.md`'s location (repo root).** Write it exactly as `@docs/founder-profile.md` — no leading slash, no `./`. A wrong path silently fails to load and the profile never reaches the skills.
- **When `CLAUDE.md` already has content, append — never overwrite, and never add a second top-level `#` heading.** The block leads with an `##` heading and goes in after a blank line so it nests under whatever is already there. Check for the import by **exact line match** (`@docs/founder-profile.md`), not a loose substring — a substring check would see a malformed `@/docs/...` variant as "already present" and skip the repair, or miss it and add a duplicate.
- **`CLAUDE.md` must stay founder-agnostic.** Never write founder-specific facts (name, background, preferences) into `CLAUDE.md` — only the generic instruction block + the `@import` line go there. The facts live *only* in `docs/founder-profile.md`. Putting facts in `CLAUDE.md` breaks reusability for a second founder.
- **Interaction preferences are profile data, not `CLAUDE.md` rules.** Tone / answer style / formats go in the profile's `## Interaction preferences` section so they travel with the founder. `CLAUDE.md` only says "honor the founder's stated preferences."
- **Judge the `notes`/Other text, never the option label.** A founder can click a shape option and leave `notes` empty — that's a non-answer. Read the free text; if a needed field is blank, ask one refinement round before writing it as "(not specified)".
- **On re-run, don't re-ask filled fields.** Read the existing profile first and grill only on empty or explicitly-changed sections (same idempotent pattern as `/sharpen-hypothesis` resuming a `hypothesis.md`).

## Interaction model

**All intake goes through `AskUserQuestion`.** Most founder fields are free text — route it through the auto-provided "Other" option and the `notes` field; the labeled options are *shape templates* showing what a good answer looks like, not the data itself. Invite the founder to type specifics in `notes` in each question prompt. The founder owns the facts; you provide shape.

Batch related fields into multi-question `AskUserQuestion` calls (up to 4 questions per call) rather than one round per field — onboarding should feel quick, not like an interrogation.

## Workflow

Goal: produce `docs/founder-profile.md` from the agreed schema and ensure `CLAUDE.md` imports it. Ordered where order is real (resume → grill → confirm → write → wire); within each step the work is goal-oriented.

### 1. Resume if a profile exists

If `docs/founder-profile.md` exists, read it. Treat each section as filled or empty/weak; grill only on the empty or weak ones. **If every section is filled**, skip grilling and jump to step 3 (show the draft and confirm) — the founder is just revisiting.

If the founder named specific fields to change ("update my interests"), grill only those.

### 2. Grill on the founder-level schema

Cover the fields below, grouped into as few `AskUserQuestion` calls as cover them. Free-text fields use shape options + `notes`/Other.

**Core (always capture):**

- **Name** — for addressing and doc provenance.
- **Background & domain expertise** — career history, industries, what they've built. Feeds the founder-market-fit dimension in `/generate-ideas`.
- **Skills & unfair advantage** — technical skills, distribution access, network, insider knowledge. The "why you specifically." Heavily weighted in idea scoring.
- **Interests / what excites them** — domains and problems they're drawn to. Steers idea generation toward things they'll stick with.
- **Location & serviceable geography** — where they are + markets/languages they can credibly serve. A hard constraint in `/generate-ideas`.
- **Risk & regulatory appetite** — tolerance for regulated spaces, deep-tech timelines, capital risk. Filters which idea shapes are viable.

**Optional (capture if the founder offers it; don't force):**

- **Time commitment** — full-time vs side project, hours/week. Affects feasibility scoring and realistic scope.
- **Founding-team status** — solo vs co-founders, who's technical. Used by the pressure-test panel (Eisenmann's "good idea, bad bedfellows" / RAWI).
- **Prior startup experience** — first-timer vs repeat founder. Calibrates how much scaffolding vs bluntness the coaching uses.

**Interaction preferences (capture as the final round — these shape every future reply):**

- **Tone** — e.g. blunt and direct vs encouraging and supportive.
- **Answer style** — concise/lead-with-the-answer vs detailed/exploratory.
- **Preferred formats** — tables, bullets, prose, diagrams.

For the optional and preferences fields, offer a "skip / use default" path — a thin profile is fine and better than fabricated facts.

### 3. Show the draft and confirm

Print the full `docs/founder-profile.md` draft in chat using the structure in **Output constraints**. Then `AskUserQuestion` with: **Ship it** / **Refine a section** / **Abort**.

- **Ship it** → step 4.
- **Refine a section** → ask which section, return to grilling on that one only.
- **Abort** → write nothing, exit cleanly.

### 4. Write the profile (only after Ship)

Write `docs/founder-profile.md` with the confirmed content (`mkdir -p docs` first if the dir is absent).

### 5. Wire and verify the CLAUDE.md import

Read `CLAUDE.md` at the repo root (it may be empty or absent), then ensure **exactly one** correct import is present:

- **A line exactly equal to `@docs/founder-profile.md` already exists** → leave it; just confirm to the founder it's wired.
- **No import present** → add the founder-agnostic block below. If the file already has content, append it after a blank-line separator; if it's empty or absent, write the block as the whole file.
- **A malformed or commented variant exists** (`@/docs/...`, `@./docs/...`, a commented-out line) → fix it in place with `Edit` to the exact `@docs/founder-profile.md` form rather than adding a second line.

Never create a duplicate import or a second top-level `#` heading — the block leads with an `##` heading so it nests cleanly under any existing `CLAUDE.md` content.

Founder-agnostic block to ensure is present:

```markdown
## Soriza Startup Layer — founder profile

This project runs the Soriza Startup Layer — an interview-driven pipeline taking a founder
from idea to tested hypothesis (/generate-ideas → /sharpen-hypothesis → /pressure-test).

In all startup-layer work, tailor advice to the founder's background, skills, constraints,
and stated interaction preferences — prefer facts already in the profile over re-asking
them, and ask only when a needed field is missing. If no profile is imported (the file
below is missing or empty), suggest running /create-founder-profile before the idea-stage
skills.

@docs/founder-profile.md
```

Then in chat (not in any file): `Profile saved and wired. Next: run /generate-ideas (no idea yet) or /sharpen-hypothesis (you have one).`

## Output constraints

- **Profile path:** `docs/founder-profile.md` — exact, no variations.
- **Profile length:** ≤400 words; omit sections the founder skipped rather than padding.
- **Profile structure:** a `# Founder Profile: <name>` title (the founder's name goes in this title only — there is no `## Name` section), then `##` sections using these **exact short headings** in this order — Background & domain expertise / Skills & unfair advantage / Interests / Location & serviceable geography / Risk & regulatory appetite / Time commitment / Founding-team status / Prior startup experience / Interaction preferences. (Use `## Interests`, not the longer intake label.) **Interaction preferences is optional:** if the founder skipped all three, omit the section entirely; otherwise include it as `- Tone:` / `- Answer style:` / `- Preferred formats:` bullets, dropping any single bullet the founder skipped. No YAML frontmatter, no "next step" line inside the file.
- **CLAUDE.md:** founder-agnostic only — the generic `##` block + the `@docs/founder-profile.md` import line, nested under any existing content. Never founder-specific facts, never a second top-level `#` heading.

## Scope

- In: capturing founder-level facts + interaction preferences, writing `docs/founder-profile.md`, wiring/verifying the `CLAUDE.md` `@import`.
- Out: **startup-level / per-idea constraints** (budget, B2B-vs-consumer, target-market geography, stage) — deferred; those stay captured ad-hoc inside `/generate-ideas` and `/sharpen-hypothesis` for now.
- Out: editing the other skills. They consume the profile by **degrading gracefully** — using it if loaded, falling back to their own inline intake if absent. This skill only creates the profile and wiring; it does not modify those skills.
- Out: idea generation, hypothesis sharpening, market sizing, persona review — those are the downstream pipeline steps.
