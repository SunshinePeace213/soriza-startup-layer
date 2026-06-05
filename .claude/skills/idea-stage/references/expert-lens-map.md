# Expert lens map — the `disconfirm` persona panel (v3)

`disconfirm` convenes a **bounded advisory board**, not the full 12-persona roster. The panel fires sharp
disconfirming objections; **each objection becomes a falsifiable assumption + a Mom-Test interview
question** for the Disconfirmation Brief. **Nothing here kills** — real users validate subjective merit.

## The panel (what always fires + one rotating seat)

- **Fixed core-3** (always), covering the three universal disconfirming axes with zero overlap:
  - `peter-thiel-perspective` — **edge / monopoly**: "monopoly or red ocean? what secret? run the Seven
    Questions + the Distribution test."
  - `charlie-munger-perspective` — **inversion / failure**: "invert — how does this fail? are the
    incentives broken? is it in your circle of competence?"
  - `jeff-bezos-perspective` — **customer / demand**: "work backwards — who is the obsessed customer? is
    this Day 1? who feels this acutely?"
- **competitor-steelman** (always) — "why does the strongest incumbent WIN and you lose?"
- **The doctrine angles** (always, from the knowledge skills, not personas):
  - `forward-deployed-founder` — "**no distribution / commoditized software**: what's your moat in the AI
    era; can a user just have AI rebuild this?"
  - `lean-startup` — "**the riskiest assumption**: what single belief, if false, collapses this?"
- **≤1 idea-type specialist** (auto-suggested; the founder may swap any seat):

| Idea-type | Specialist |
|---|---|
| Trading / fintech / markets / risk | `nassim-taleb-perspective` (tail risk, fragility) |
| Services / ops-heavy / marketplace-of-services | `tom-eisenmann-perspective` (which of the six failure patterns; RAWI) |
| Content / media / community / creator | `naval-ravikant-perspective` (specific knowledge, leverage) |
| Hardware-adjacent / deep / regulated | `elon-musk-perspective` (first-principles unit economics) |
| Marketplace / two-sided platform | `peter-thiel-perspective` already core → add `garry-tan-perspective` (revealed pull) |
| Product / consumer / design-led | `steve-jobs-perspective` (feature vs product; what gets subtracted) |
| Default / unclear | none — the core-3 + doctrine angles suffice |

## Rules

- **One sharpest objection per lens** → 1 falsifiable assumption + 1 past-behaviour interview question.
  The judge dedupes + risk-ranks into ~5–8 OPEN assumptions. The cap is a feature: a *testable* brief,
  not a 30-item wall.
- **Founder-blind, no verdict.** Subjective objections (demand, WTP, moat, behaviour) stay **OPEN →
  interview question**; only a hard checkable fact (legality, feasibility) closes one. A lens may *flag* a
  fatal-flaw-class issue to the judge, never act on it.
- **The Eisenmann lens** also reads `tom-eisenmann-perspective/references/failure-patterns.md` (the six
  patterns, English) to name which death pattern the idea resembles.
- **Curation between runs only.** When a logged `coverage_gap` recurs, mint a new specialist with
  `/nuwa-skill <name>` and add a row above. The roster grows slowly and on purpose — never mid-run.

## Workers

`disconfirm` dispatches `objection-lens` (once per panel seat, in parallel, channelling the named
`*-perspective` SKILL.md), `competitor-steelman`, and `disconfirmation-judge` (compiles the Brief).
