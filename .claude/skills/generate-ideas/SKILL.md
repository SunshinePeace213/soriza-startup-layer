---
name: generate-ideas
description: |
  First stage of the Idea Stage: expand a thesis (or normalize a supplied list) into a WIDE slate of
  10 thin startup-idea seeds, recommend which one to take next (weighing demand + founder-fit + moat +
  distribution), and let the FOUNDER pick — then scaffold the chosen idea's workspace. The recommendation
  is advisory; you decide (no auto-pick, no ranking that chooses for you). Use for "generate startup
  ideas", "brainstorm ideas from my thesis", "expand this thesis into ideas", "give me a slate of ideas",
  "which idea should I pursue", or to start the Idea Stage.
when_to_use: |
  Trigger on "generate / brainstorm startup ideas", "expand my thesis into ideas", "give me a slate",
  "ideas for a theme", "which idea should I pursue / start with", or any kickoff of the Idea Stage when
  no idea folder exists yet. Not for sharpening one chosen idea (that's /sharpen-hypothesis).
argument-hint: "[thesis | 'seed list']"
allowed-tools: Read, Glob, Write, WebSearch, WebFetch, Agent, AskUserQuestion
effort: high
---

# Generate Ideas — the slate

Expand a thesis (or a supplied list) into a **wide slate of 10** thin seeds, recommend one, and let
**you** pick. This is a brainstorming aid, not a ranker that decides for you — the recommendation is
advisory; the founder chooses.

## When this applies

- "Generate / brainstorm startup ideas", "expand `<thesis>` into ideas", "give me a slate", "which idea
  should I pursue?" — the kickoff of the Idea Stage, when no `ideas/<slug>/` exists yet.

Out of scope: sharpening one chosen idea (`/sharpen-hypothesis`); deep market work (`/market-map`).

## What it does (goal + constraints)

Goal: one `ideas/_exploration/<thesis-slug>/slate.md` (10 cards + a Recommendation header), then scaffold
the picked idea into `ideas/<slug>/`.

- **Two labelled tracks.** (a) A **blind-wide** track driven by the thesis + real demand — founder-BLIND,
  do **not** bend seeds toward the founder's market/skills/goals (this is the anti-bias guard). (b) A
  **founder-reachable-workflow** track grounded in workflows the founder can actually get inside (read
  `docs/founder-profile.md`). Label each seed's track.
- **Ground it.** Dispatch `startup-idea-researcher` for a grounding sweep (trends / demand / existing
  solutions → `ideas/_exploration/<thesis>/grounding.md`); dispatch `seed-generator` for the blind-wide
  seeds. Tag each seed with an accurate `idea_type` (drives the disconfirm specialist).
- **Apply the doctrine.** Read `forward-deployed-founder` + `lean-startup`. **Flag any undifferentiated-
  SaaS seed** with *"what's your moat in the AI era?"*
- **Recommend (advisory).** Name the suggested pick + reasoning, weighing demand signal + founder-fit +
  moat + **distribution as a first-class factor** (distribution is the founder's #1 documented risk —
  foreground it).
- **Founder picks.** `AskUserQuestion` with the slate + recommendation; the founder chooses or overrides.
- **Scaffold.** On pick, create `ideas/<slug>/` and write the chosen card as `ideas/<slug>/seed.md`
  (the input to sharpening). The other 9 stay in `slate.md` as a **dormant backlog** — no ledger; re-run
  `/sharpen-hypothesis` on any of them later.

## Gotchas

- No auto-pick, no K-cap, no portfolio/resurrect ledger — those were the v2 VC-funnel framing. The founder
  picks; `slate.md` *is* the lightweight backlog.
- Keep generation **wide** — don't quietly narrow to the founder's comfort zone. The reachable-workflow
  track is additive and labelled, never a replacement for the blind track.

## Output

`ideas/_exploration/<thesis>/slate.md` (`assets/slate-template.md`) + `grounding.md`. Next:
`/sharpen-hypothesis` on the picked idea.

## Workers & references

- Workers: `startup-idea-researcher` (grounding), `seed-generator` (blind-wide seeds).
- `assets/slate-template.md` — the slate structure.
