# Expert lens map — Gate 2 objection lenses

Gate 2 draws a **closed roster** of distilled `*-perspective` experts. The selector picks 3–4 whose
lens best fits a Candidate's idea-type, plus the competitor-steelman, and each fires ONE
evidence-checked objection. When the ideal lens isn't in the roster, the selector still picks the best
available AND logs the missing one as a `coverage_gap` (ADR-0004) — it never auto-mints.

## Lens cards (the roster)

Each card = the one question the expert asks + what it kills. `objection-lens` uses the card by default
and reads the full `.claude/skills/<slug>/SKILL.md` only when it needs to channel deeper.

| Expert (slug) | The one question | Kills Candidates that… |
|---|---|---|
| `peter-thiel-perspective` | Monopoly or red ocean? What truth do few agree with you on? | are me-too, no moat, compete on price |
| `jeff-bezos-perspective` | Work backwards — who is the obsessed customer? Is this Day 1? | have no clear, acute customer |
| `charlie-munger-perspective` | Invert: how does this fail? Are the incentives broken? Circle of competence? | sit outside the founder's competence / are mis-incentivized |
| `nassim-taleb-perspective` | Fragile? Tail risk? Mediocristan or Extremistan? | carry ruin / blow-up exposure |
| `elon-musk-perspective` | First principles — do the unit economics / physics actually work? | have broken economics or idiot-index problems |
| `tom-eisenmann-perspective` | Which of the six failure patterns? RAWI? founder-market fit? | match a known startup death pattern |
| `ben-horowitz-perspective` | Is there a wartime path? Lead bullets, not silver? Can it be run? | have no hard path through execution reality |
| `naval-ravikant-perspective` | Specific knowledge? Permissionless leverage? Long-term game? | lack leverage / aren't a game worth playing repeatedly |
| `steve-jobs-perspective` | Is this insanely great? Whole widget? What gets subtracted? | are feature-not-product, undifferentiated |
| `vilfredo-pareto-perspective` | Strip the derivation — what's the residue? Who's lion, who's fox? Where's the 80/20? | rest on rationalization, not the vital few |
| `garry-tan-perspective` | Make something people want? Earnest? Ambitious enough? Process power? | nobody actually wants / aren't ambitious enough |
| `competitor-steelman` (agent) | Why does the competitor WIN and you lose? | have no defensible edge vs incumbents |

## Idea-type → default lenses

The selector matches the Candidate's dominant shape to a row; ties broken by the founder profile's
interests. Always include `competitor-steelman`.

| Idea-type | Default 3–4 lenses (+ steelman) |
|---|---|
| Marketplace / two-sided platform | thiel, bezos, munger |
| E-commerce / DTC / retail | bezos, munger, garry-tan |
| Trading / fintech / markets | taleb, munger, musk |
| AI agent / dev-tool / SaaS | thiel, musk, garry-tan |
| Content / media / community | bezos, naval, garry-tan |
| Marketplace-of-services / gig | eisenmann, bezos, horowitz |
| Hardware-adjacent / ops-heavy | musk, taleb, eisenmann |
| Regulated-adjacent (flag for FMF too) | taleb, munger, eisenmann |
| Default / unclear | thiel, munger, bezos |

## Adding an expert (curation, between runs)

1. `/nuwa-skill <name>` → mints `.claude/skills/<name>-perspective/`.
2. Add a lens card row above + slot the expert into the relevant idea-type row(s).
3. Next run picks it up automatically — no workflow change (ADR-0004).
