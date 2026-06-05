---
name: create-founder-profile
description: Onboard a founder into the Soriza Startup Layer with a comprehensive, VC-due-diligence-grade record. Use when the founder says "create/set up/build my founder profile", "onboard me", "tell Claude about me/my background", "tailor advice to my situation", "upgrade my profile", or wants to give Claude their background before the Idea Stage. Builds TWO tiers — a complete docs/founder-dossier.md (education, experience, skill levels, track record, finances, network, ambition; read on demand) and a lean docs/founder-profile.md summary generated from it (the @imported one every idea-stage skill auto-loads). Ingests a CV/LinkedIn/dump if offered, probes gaps, level-rates skills against an objective rubric, and is resumable across sessions. Re-runnable — reads existing files and only asks about missing or changed fields.
when_to_use: |
  Use when the founder says "create my founder profile", "set up my profile", "build my
  profile", "onboard me", "tell Claude about my background", "founder profile", "set up
  the startup layer for me", "make Claude tailor advice to me", "update my profile",
  "upgrade my profile", "make my profile comprehensive", or asks how to give Claude their
  background before starting the Idea Stage. This is the onboarding step upstream of the
  whole Idea Stage (every idea-stage skill reads the profile).
allowed-tools: AskUserQuestion, Read, Write, Edit, Bash, Glob
---

# Create Founder Profile

Onboarding step for the Soriza Startup Layer. Build a **two-tier founder record** and wire the
`CLAUDE.md` `@import` so every idea-stage skill loads the founder's context and tailors its advice:

- **`docs/founder-dossier.md`** — the complete, canonical record (VC-due-diligence depth). Read on
  demand by skills that want depth. The source of truth.
- **`docs/founder-profile.md`** — a lean summary **generated from the dossier**. This is the file
  `CLAUDE.md` `@import`s, so it loads into every session and is the one Gate 0 of the funnel scores.

Profile facts are per-founder data; `CLAUDE.md` and the funnel rubrics stay founder-agnostic so anyone
can clone this layer and run their own profile.

## When this skill applies

- "Create / set up / build / upgrade my founder profile"
- "Onboard me" / "set up the startup layer for me"
- "Make my profile comprehensive" / "tell Claude about my background so it tailors advice"
- "Update my profile" (re-run to edit specific fields or fill what's `(pending)`)

## Gotchas

- **The `@import` path is resolved relative to `CLAUDE.md`'s location (repo root).** Write it exactly
  as `@docs/founder-profile.md` — no leading slash, no `./`. A wrong path silently fails to load and
  the profile never reaches the skills. **Only the summary is imported — never `@import` the dossier**
  (it would load the whole heavy record into every session, the cost the tiering exists to avoid).
- **The summary is derived, not separately authored.** Write/update the dossier first, then regenerate
  the summary from it. If you edit one and not the other they drift, and the funnel scores a stale
  summary while the founder thinks the dossier is live.
- **A blank sensitive field must never flatter.** A hidden weak runway can't read as "no constraint."
  Record declines explicitly (`Runway: (declined)`) so Gate 0 scores capital conservatively rather
  than treating the gap as a free pass. See `references/dossier-schema.md` → sensitive fields.
- **Judge the `notes`/free text, never the option label.** A founder can click a shape option and
  leave `notes` empty — that's a non-answer. Read the free text; if a needed field is blank, ask one
  refinement round before writing it, or write `(pending)` if intake is being paused.
- **A level with no evidence is not a rating.** When the founder rates a skill (or claims a seniority),
  capture the evidence that earns it per `references/level-rubric.md`. If a rating has nothing behind
  it, challenge it once — don't silently record the optimistic label.
- **On re-run, don't re-ask filled fields.** Read the existing dossier (and summary) first and grill
  only on empty, `(pending)`, or explicitly-changed sections — the same idempotent pattern as the
  `/sharpen-hypothesis` stage resuming a `hypothesis.md`.
- **`CLAUDE.md` and the idea-stage skills stay founder-agnostic.** Founder facts live *only* in the
  dossier/summary. The skills hold the *general* standard and pull the founder's specifics from the
  profile at runtime — never hard-code one founder's situation (e.g. "part-time", a specific edge) into
  a skill. Doing so re-introduces the bias this design fixes.

## Interaction model

Intake runs **ingest-then-probe**: take any raw material the founder already has, then ask only for
what's missing or unverified — diligence works from documents, not interrogation.

- **Ingest first.** Invite the founder to paste a CV / LinkedIn export / GitHub profile / freeform
  brain-dump (or say "skip"). Parse whatever they give into the dossier sections before asking
  anything. A founder with a CV should answer far fewer questions than one starting blank.
- **Then probe gaps, through `AskUserQuestion`.** Most fields are free text — route it through the
  auto-provided "Other" option and the `notes` field; the labeled options are *shape templates*
  showing what a good answer looks like, not the data. Batch related fields (up to 4 questions/call).
- **Probe level claims.** When a skill or seniority is asserted without evidence, ask one Socratic
  follow-up for what backs it (what shipped, at what scale) — the reference-check posture.

## Workflow

Goal: produce a complete `docs/founder-dossier.md`, derive `docs/founder-profile.md` from it, and
ensure `CLAUDE.md` imports the summary. Order is real where marked (resume → ingest → grill core →
deep dives → derive summary → confirm → write → wire); within each step the work is goal-oriented.

### 1. Resume / migrate if files exist

Read `docs/founder-dossier.md` and `docs/founder-profile.md` if present.

- **Dossier exists** — treat each section as filled, `(pending)`, or weak; grill only the gaps and any
  section the founder named to change. If every section is filled, skip to step 5 (confirm).
- **Only the old thin `founder-profile.md` exists (no dossier)** — *migrate*: map its sections into
  the dossier structure (see `references/dossier-schema.md`), then grill the new/empty sections and
  run the level-probe over any skill claims the old profile stated flatly.

### 2. Ingest provided material

Ask the founder to paste a CV/LinkedIn/GitHub/dump or skip. Parse what's given into the dossier
sections; carry forward anything concrete (roles, dates, projects, links) so you don't re-ask it.

### 3. Grill the summary-critical core (Round 1)

Capture enough to write a usable summary and let the funnel run. The core fields and the exact
sections they map to are in `references/dossier-schema.md`; at minimum cover: location & languages,
skills & unfair advantage (level-rated), interests, risk & regulatory appetite, capital & runway
(bands; decline path), time & commitment, goals & ambition, and interaction preferences. Level-rate
skills against `references/level-rubric.md`.

### 4. Deep dives (optional, resumable)

Fill the remaining dossier sections (full education, per-role history, track record, network, grit &
prior attempts, founding-team detail). These are optional and can span sessions: if the founder wants
to stop, write the dossier with `(pending)` on the unreached sections — a later run resumes there.
"Good enough to proceed" is reached once Round 1 is done; offer to continue or stop.

### 5. Derive the summary, then confirm

Regenerate `docs/founder-profile.md` from the dossier per **Output constraints**. Print the full
summary draft in chat (the founder reviews the lean file the skills will actually load), then
`AskUserQuestion`: **Ship it** / **Refine a section** / **Keep filling the dossier** / **Abort**.

- **Ship it** → step 6. **Refine** → grill that section only. **Keep filling** → back to step 4.
- **Abort** → write nothing, exit cleanly.

### 6. Write the files (only after Ship)

Write `docs/founder-dossier.md` (complete record) and `docs/founder-profile.md` (derived summary).
`mkdir -p docs` first if the dir is absent.

### 7. Wire and verify the CLAUDE.md import

Read `CLAUDE.md` at the repo root (it may be empty or absent), then ensure **exactly one** correct
import of the summary is present:

- **A line exactly equal to `@docs/founder-profile.md` already exists** → leave it; confirm it's wired.
- **No import present** → add the founder-agnostic block below (append after a blank line if the file
  has content; write it as the whole file if empty/absent).
- **A malformed/commented variant** (`@/docs/...`, `@./docs/...`, commented-out) → fix it in place
  with `Edit` to the exact `@docs/founder-profile.md` form rather than adding a second line.

Never create a duplicate import or a second top-level `#` heading — the block leads with an `##`
heading so it nests cleanly under any existing `CLAUDE.md` content. Never `@import` the dossier and
never write founder facts into `CLAUDE.md`.

Founder-agnostic block to ensure is present:

```markdown
## Soriza Startup Layer — founder profile

This project runs the Soriza Startup Layer — an Idea Stage taking a founder from many raw ideas
to a validated solution concept and a lightweight PoC, as a founder-gated pipeline of skills:
/generate-ideas → /sharpen-hypothesis → /disconfirm → /market-map → /customer-discovery-design →
[human interviews] → /customer-discovery-synthesis → /solution-design → /idea-stage-exit → /build-poc
(run /idea-stage anytime to see where each idea sits).

The founder's context lives in two tiers: the lean summary imported below (loaded every session)
and a complete docs/founder-dossier.md (read on demand for depth). In all startup-layer work,
tailor advice to the founder's background, skills, constraints, and stated interaction preferences,
preferring facts already in the profile over re-asking them. Keep this file and the idea-stage skills
founder-agnostic: the skills hold the general standard and read the founder's specifics from the
profile as data — founder facts never belong in CLAUDE.md or in a skill. If no profile is imported
(the file below is missing or empty), suggest running /create-founder-profile before the idea-stage
skills.

@docs/founder-profile.md
```

Then in chat (not in any file): `Profile + dossier saved and wired. Next: run /generate-ideas to
expand a thesis (or your list) into a slate, pick one, and start validating — or /idea-stage to see the map.`

## Output constraints

- **Paths:** `docs/founder-dossier.md` (complete record) and `docs/founder-profile.md` (summary) —
  exact, no variations.
- **Dossier:** structure and the 16 sections per `references/dossier-schema.md`. Depth over padding;
  honest one-liners and `(pending)` are valid; never invent filler.
- **Summary length:** ≤450 words; omit sections the founder skipped rather than padding.
- **Summary structure:** a `# Founder Profile: <name>` title (the name lives only in this title — no
  `## Name` section), a first line `Full dossier: docs/founder-dossier.md`, then `##` sections using
  these **exact short headings** in this order — Background & domain expertise / Skills & unfair
  advantage / Interests / Location & serviceable geography / Risk & regulatory appetite / Capital &
  runway / Time commitment / Founding-team status / Prior startup experience / Goals & ambition /
  Interaction preferences. Weave skill **levels** into Skills & unfair advantage (e.g. "senior
  fullstack (7 yrs, shipped X at scale)"). **Capital & runway** and **Goals & ambition** are required
  because /generate-ideas' recommendation and seed-generator read them. **Interaction preferences is optional:**
  if the founder skipped all three, omit the section; otherwise include `- Tone:` / `- Answer style:`
  / `- Preferred formats:` bullets, dropping any single one skipped. The summary-heading →
  dossier-section mapping (with the fan-ins) is in `references/dossier-schema.md` → Deriving the
  summary — follow it so the derivation is reproducible. No YAML frontmatter, no "next step" line
  inside the file.
- **CLAUDE.md:** founder-agnostic only — the generic `##` block + the `@docs/founder-profile.md`
  import line, nested under any existing content. Never founder-specific facts, never the dossier
  imported, never a second top-level `#` heading.

## Scope

- In: building the dossier + deriving the summary, level-rating skills against the rubric, ingesting
  provided material, wiring/verifying the `CLAUDE.md` `@import`.
- Out: **per-idea constraints** (a specific idea's budget, B2B-vs-consumer, target geography, stage) —
  those stay captured ad-hoc inside the idea-stage skills (`/generate-ideas`, `/sharpen-hypothesis`).
- Out: idea generation, hypothesis sharpening, market/demand detection, disconfirmation — the
  downstream idea-stage skills. This skill only creates the record and wiring.
- Note: the idea-stage skills consume the summary by reading it as **data** against their own
  founder-agnostic standard. This skill writes the profile; the de-biasing lives in those skills (they
  read the profile as data), not here.
