# Design contract — Founder Profile v2 (VC-grade, neutral)

Status: APPROVED (grilled via /grill-me, 2026-06-04). Next: build via /prompt-architect.

Upgrades `/create-founder-profile` from a thin ≤400-word profile into a comprehensive,
VC-due-diligence-grade founder record — AND fixes a neutrality flaw discovered during the grill:
the funnel's "general" rubrics had the founder's specific case baked in.

## Problem this solves

1. **Calibration gap** — agents can't gauge the founder's *level* (seniority, skill depth, track
   record) from the current thin profile, so advice/idea-fit scoring is calibrated to a generic
   solo founder, not the real one.
2. **Coverage gap** — the profile skips whole categories a VC/background-check probes (education,
   detailed employment, finances/runway, track record, network, ambition).
3. **Neutrality flaw (discovered during grill)** — the supposedly-general gate rubrics encode the
   founder's *specific case* as the universal standard, violating the layer's own founder-agnostic
   reusability rule. Evidence:
   - `gate-rubrics.md:24` — Capacity factor: "Cannot be moved at all **part-time**" → founder's
     part-time constraint hard-coded as the universal bar.
   - `gate-rubrics.md:25` — Skill factor: "no **agentic-coding** edge" → the founder's specific
     unfair advantage written into the general skill criterion.
   - `fmf-screen.md:25,27` — "**part-time** capacity" baked into the scoring instruction.
   - `scoring-rubric.md:17` (`/generate-ideas`, related path) — a guarded "thumb on the scale for
     favorites". Left as-is by decision (different path, has an anti-laundering guard); flagged.

## How the profile is consumed today (grounding)

- `docs/founder-profile.md` is `@import`ed into `CLAUDE.md` → loads into **every session's context**
  (length has a real token cost).
- Only machine-scored by **`fmf-screen` (Gate 0)** on 5 fit dimensions: geography/market · risk &
  regulatory · capital · capacity · skill/unfair-advantage, with **hard-fails**.
- `seed-generator` biases idea generation toward the founder's market/skills/interests.
- The funnel's **merit gates are already founder-blind** (verified: sharpen-gate, disconfirmation-judge,
  objection-lens, market-researcher, competitor-steelman all read 0 founder-profile refs). Founder
  influence is isolated to: cap-K (capacity), seed generation, and the Gate 0 *kill-filter*.

## Locked decisions

| # | Decision | Resolution |
|---|---|---|
| 1 | **Architecture** | **Tiered.** `docs/founder-profile.md` = lean summary (`@import`ed, Gate-0-scored). `docs/founder-dossier.md` = complete canonical record (read on demand, NOT `@import`ed). Summary **generated from** the dossier so they never drift. |
| 2 | **Dossier content** | Sections **A–P** (below). Cut 4 theater items (identity-doc verification, third-party reference contact lists, "reason for leaving" each job, credit score). "References" reframed as **H. network & reachable communities** (feeds customer-discovery reachability). |
| 3 | **Level calibration** | Every skill: **level (junior/mid/senior/expert) + required evidence anchor**; intake **Socratically probes** unbacked ratings (reference-check posture). |
| 4 | **Neutrality / de-bias** | **Separate the general standard (rubric) from founder data (profile).** Rewrite `gate-rubrics.md` + `fmf-screen.md` so each factor is a general guideline that **pulls the founder's specifics from the profile**; strip baked-in "part-time" / "agentic-coding". |
| 5 | **Intake flow** | **Ingest-then-probe, resumable.** (a) Optionally ingest raw material the founder provides (CV/LinkedIn/GitHub/freeform dump) and auto-structure it; (b) probe only gaps + challenge unbacked level ratings; (c) tier by importance — Round 1 captures the summary-critical core so the funnel can run, deeper sections are optional follow-ups; (d) resumable — save a partial dossier with `(pending)` markers, stop/continue across sessions. |

### Dossier sections (A–P) and their downstream consumer

| # | Section | Calibrates |
|---|---|---|
| A | Identity & logistics — base, work authorization, languages + fluency *levels* | Gate 0 geography fit |
| B | Education — degrees, institutions, years, field, certs, self-directed learning | Level calibration |
| C | Professional experience — per role: company, dates, seniority, what shipped, stack, scale, achievements | Level + FMF skill |
| D | Skill inventory + proficiency — tech + non-tech (product/GTM/design), each *level-rated* | FMF skill/unfair-advantage |
| E | Track record / evidence — shipped projects, side projects, launches, GitHub/portfolio, any revenue ever | Evidence of execution |
| F | Domain expertise & insider knowledge — where the founder has *earned*, non-obvious knowledge | FMF + wedge |
| G | Unfair advantages — distribution, audience, network, proprietary insight, speed | "Why you" |
| H | Network & reachable communities — communities/audiences reachable; potential advisors/co-founders | Customer-discovery reachability + team |
| I | Financial situation & runway — investable capital, income floor, burn, dependents, months of runway, bootstrap-vs-raise | Gate 0 capital hard-fail |
| J | Goals & ambition — venture-scale vs lifestyle, target outcome/timeline, motivation/why | Steers funnel toward right idea *shapes* |
| K | Motivation, grit & prior attempts — why now, persistence evidence, prior ventures/failures + learnings | Coaching calibration, Eisenmann lens |
| L | Risk & regulatory appetite *(deepened)* — specific no-go zones, capital-risk tolerance | Gate 0 risk hard-fail |
| M | Time & commitment *(deepened)* — hours/week, schedule, full-time trigger | Feasibility |
| N | Founding-team status *(deepened)* — solo/co-founders, gaps, hiring appetite | Pressure-test team lens |
| O | Interests | Seed bias |
| P | Interaction preferences — tone, answer style, formats *(also in summary)* | Every reply |

## Open items — resolved by recommendation (approved)

- **R1 · Summary schema** — keep the 9 headings consumers depend on; **add** a concise
  `Capital & runway` line and a `Goals & ambition` line (the de-biased rubric now reads runway +
  ambition); weave skill *levels* into `Skills & unfair advantage`; top the file with a
  `Full dossier: docs/founder-dossier.md` pointer. Cap ≤450 words.
- **R4 · Level rubric** — new file `.claude/skills/create-founder-profile/references/level-rubric.md`.
  Scale **junior / mid / senior / expert**, anchored on 5 axes: **years · scope · scale · autonomy ·
  recency**. One general table reused for technical *and* non-technical skills; the evidence anchor
  must justify the level. Founder-agnostic (a general standard).
- **R3 · Migration** — on run, detect the existing thin `founder-profile.md`, **promote** its content
  into the dossier (map old sections → A–P), grill only gaps + run the level-probe on existing
  claims, regenerate the summary. Idempotent (same resume pattern as today).
- **R5 · Sensitive fields** — always offer a "prefer not to say" path; capture finances as **bands**
  (runway <3 / 3–6 / 6–12 / 12+ mo; investable capital none / <$5k / $5–50k / $50k+), not exact
  figures unless volunteered. The de-biased capital factor treats "declined" **conservatively** so a
  blank never silently flatters.
- **R6 · CLAUDE.md wiring** — stays founder-agnostic; update the block to (a) mention the dossier
  exists alongside the profile, (b) state the *general-standard-vs-founder-data* principle so future
  skills honor it. Never `@import` the dossier; never founder facts in `CLAUDE.md`.
- **R7 · Verification** — after build, run the funnel fixtures (should-advance / should-kill) + a
  **reusability check** (would a *different* hypothetical founder now be scored neutrally?) to confirm
  no regression in the verified funnel.

## Build deliverables (for /prompt-architect)

1. Upgraded `.claude/skills/create-founder-profile/SKILL.md` — tiered output, A–P dossier intake,
   ingest-then-probe + resumable flow, level+evidence+probe, migration, ≤450-word summary schema,
   updated CLAUDE.md wiring instructions.
2. New `.claude/skills/create-founder-profile/references/level-rubric.md` — objective level scale.
3. De-biased `.claude/skills/idea-funnel/references/gate-rubrics.md` (Gate 0 factors → general
   guidelines pulling founder data) and `.claude/agents/fmf-screen.md` (strip "part-time"/"agentic-coding").
4. Verification pass per R7.
