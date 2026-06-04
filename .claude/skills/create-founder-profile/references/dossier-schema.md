# Founder dossier schema — the complete record

`docs/founder-dossier.md` is the **canonical, complete founder record** — the VC-due-diligence-grade
detail. It is NOT `@import`ed (so it never costs every session's context); skills `Read` it on demand.
The lean `docs/founder-profile.md` summary is **generated from this file**, so the dossier is the
source of truth — write it first, derive the summary second.

## File shape

A `# Founder Dossier: <name>` title, then the 16 `##` sections below **in this order**, each with the
exact heading shown. Capture depth, not padding — a section the founder genuinely has nothing for gets
a single honest line (e.g. `No prior ventures.`), never invented filler. A section the founder hasn't
reached yet in a resumable intake gets a literal `(pending)` line so a re-run knows to return to it.

## The 16 sections

Each row: the heading, what it captures, and the downstream consumer it calibrates (so every section
earns its place — drop nothing that has a consumer, pad nothing that doesn't).

| Heading | Captures | Calibrates |
|---|---|---|
| `## Identity & logistics` | base location, work authorization/visa, languages **with fluency level** (native/fluent/working/basic) | Gate 0 geography fit |
| `## Education` | degrees, institutions, years, field; certifications; significant self-directed learning | Level |
| `## Professional experience` | per role: company, dates, title/**seniority**, what was shipped, tech stack, scale (users/team/revenue touched), key achievements | Level + FMF skill |
| `## Skill inventory & proficiency` | technical (languages/frameworks/infra/design) **and** non-technical (product, GTM, sales, design), **each level-rated + evidence-anchored** per `level-rubric.md` | FMF skill / unfair-advantage |
| `## Track record & evidence` | shipped projects, side projects, launches, GitHub/portfolio links, any revenue ever earned, OSS, hackathons | Evidence of execution |
| `## Domain expertise & insider knowledge` | where the founder has *earned*, non-obvious knowledge (not mere interest) | FMF + wedge |
| `## Unfair advantages` | distribution access, audience, network, proprietary insight, build speed | "Why you" |
| `## Network & reachable communities` | communities/audiences the founder can actually reach; potential advisors/co-founders | Customer-discovery reachability + team |
| `## Financial situation & runway` | investable capital, income floor, monthly burn, dependents, months of runway, bootstrap-vs-raise appetite — as **bands**, with a decline path (see below) | Gate 0 capital factor |
| `## Goals & ambition` | venture-scale vs lifestyle, target outcome + timeline, what success looks like, core motivation | Steers funnel toward right idea *shapes* |
| `## Motivation, grit & prior attempts` | why now, evidence of persistence, prior ventures/failures + what was learned | Coaching calibration, Eisenmann lens |
| `## Risk & regulatory appetite` | tolerance for regulated spaces, deep-tech timelines, capital risk; specific no-go zones | Gate 0 risk factor |
| `## Time & commitment` | hours/week, schedule constraints, full-time trigger, runway-to-quit | Feasibility |
| `## Founding-team status` | solo vs co-founders, who's technical, gaps to fill, hiring/contracting appetite | Pressure-test team lens |
| `## Interests` | domains and problems the founder is drawn to | Seed bias |
| `## Interaction preferences` | tone, answer style, preferred formats | Every reply (also lives in the summary) |

## Deliberately excluded (theater for a solo founder)

A literal background check / VC dossier also includes document/identity verification, third-party
reference contact lists, "reason for leaving" each role, and a credit score. These verify a stranger;
they change no agent's output here, so they're **out**. The genuinely useful part of "references" is
captured as `## Network & reachable communities` instead.

## Sensitive fields — financials

Money is the one section founders most often won't share, and a silent blank must never *flatter* the
founder (a hidden weak runway shouldn't read as "no constraint"). So:

- Always offer a **"prefer not to say"** path.
- Capture **bands**, not exact figures, unless the founder volunteers exact numbers:
  - Runway: `<3 mo` / `3–6 mo` / `6–12 mo` / `12+ mo`
  - Investable capital: `none` / `<$5k` / `$5–50k` / `$50k+`
- If declined, write `Runway: (declined)` — Gate 0 then scores the capital factor **conservatively**
  (treats it as tight), so an unknown errs toward caution rather than a free pass.

## Level ratings

Every entry in `## Skill inventory & proficiency` (and the seniority in `## Professional experience`)
is rated against the founder-agnostic scale in `level-rubric.md` — a level **plus** the evidence that
justifies it. A bare rating with no evidence behind it is challenged during intake, not recorded.

## Deriving the summary (`founder-profile.md`)

The lean summary is regenerated from this dossier, never authored separately. Each summary heading
draws from the dossier section(s) below — note the **fan-in**: some summary headings combine several
dossier sections, so this is the checkable spec that keeps two runs deriving the same summary.

| Summary heading | Drawn from dossier section(s) |
|---|---|
| Background & domain expertise | Education + Professional experience + Domain expertise & insider knowledge |
| Skills & unfair advantage | Skill inventory & proficiency (carry the levels) + Unfair advantages |
| Interests | Interests |
| Location & serviceable geography | Identity & logistics |
| Risk & regulatory appetite | Risk & regulatory appetite |
| Capital & runway | Financial situation & runway |
| Time commitment | Time & commitment |
| Founding-team status | Founding-team status |
| Prior startup experience | Motivation, grit & prior attempts (+ any prior launch from Track record & evidence) |
| Goals & ambition | Goals & ambition |
| Interaction preferences | Interaction preferences |

`## Network & reachable communities` and the detail of `## Track record & evidence` are intentionally
**dossier-only** (read on demand by skills such as customer-discovery) — the summary cites only
headline evidence inline, keeping it lean.
