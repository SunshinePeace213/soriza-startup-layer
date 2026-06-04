# Expert lens map — disconfirmation angle generators

The disconfirmation stage draws a **closed roster** of distilled `*-perspective` experts. The selector
picks 3–4 whose lens best fits a Candidate's idea-type, plus the competitor-steelman, and each fires
ONE sharp objection.

**Lenses are ANGLE generators, not prosecutors. No objection kills.** Each objection is converted into
a **falsifiable assumption + an interview question** for the Disconfirmation Brief — never a verdict.
The lenses exist because their angles are valuable for *surfacing the right risks to test with real
users*, not for screening ideas out at the desk.

- **Nothing the lenses raise can eliminate an idea.** "No moat / incumbent exists / market small / they
  might not pay / not ambitious enough" all become **open assumptions + interview questions and a rank
  input**, not deaths. Real users are the only validator of subjective merit. The only desk kills live
  at the checkpoint (the 3 fatal flaws) — never here.
- **The AI does not debate-rebut.** An objection is marked **closed only when a hard, checkable FACT
  settles it** (legality, technical feasibility). **Everything subjective** (demand, willingness to pay,
  behaviour, defensibility) **stays OPEN → interview question.**
- A lens may *surface* a candidate fatal flaw (illegal/impossible, demand provably negative, no
  reachable audience). It does not act on it — it flags it for the checkpoint to weigh against research.

When the ideal lens isn't in the roster, the selector still picks the best available AND logs the
missing one as a `coverage_gap` — it never auto-mints.

## Lens cards (the roster)

Each card = the one question the expert asks + the **assumption + interview angle** it surfaces.
`objection-lens` uses the card by default and reads the full `.claude/skills/<slug>/SKILL.md` only when
it needs to channel deeper. Read the "surfaces" column as *"this becomes a falsifiable assumption to
test with users"* — not *"this kills."*

| Expert (slug) | The one question | Assumption + interview angle it surfaces |
|---|---|---|
| `peter-thiel-perspective` | Monopoly or red ocean? What truth do few agree with you on? | whether it's me-too / has any edge → test what would make a user switch from what exists |
| `jeff-bezos-perspective` | Work backwards — who is the obsessed customer? Is this Day 1? | whether a clear, acute customer exists → test who feels this acutely and why |
| `charlie-munger-perspective` | Invert: how does this fail? Are the incentives broken? Circle of competence? | the most likely failure mode + whether incentives align → test the assumption that would break it |
| `nassim-taleb-perspective` | Fragile? Tail risk? Mediocristan or Extremistan? | hidden ruin / blow-up exposure → test for the tail risk a user would actually hit |
| `elon-musk-perspective` | First principles — do the unit economics / physics actually work? | whether the economics close → test the load-bearing cost/value assumption |
| `tom-eisenmann-perspective` | Which of the six failure patterns? RAWI? founder-market fit? | which known death pattern it resembles → test the assumption that pattern hinges on |
| `ben-horowitz-perspective` | Is there a wartime path? Lead bullets, not silver? Can it be run? | whether there's a hard, executable path → test the operational reality a user/buyer imposes |
| `naval-ravikant-perspective` | Specific knowledge? Permissionless leverage? Long-term game? | whether there's leverage / a repeatable game → test whether demand recurs |
| `steve-jobs-perspective` | Is this insanely great? Whole widget? What gets subtracted? | whether it's a product vs a feature → test what users would call indispensable |
| `vilfredo-pareto-perspective` | Strip the derivation — what's the residue? Who's lion, who's fox? Where's the 80/20? | the real (vs rationalized) driver of demand → test the vital-few users/use-cases |
| `garry-tan-perspective` | Make something people want? Earnest? Ambitious enough? Process power? | whether anyone actually wants it → test revealed pull, not stated interest |
| `competitor-steelman` (agent) | Why does the competitor WIN and you lose? | the strongest incumbent threat → test what makes users leave the incumbent |

## Idea-type → default lenses

The selector matches the Candidate's dominant shape to a row; ties broken by the founder profile's
interests. Always include `competitor-steelman`. (Routing only — it selects *angles*, not kills.)

| Idea-type | Default 3–4 lenses (+ steelman) |
|---|---|
| Marketplace / two-sided platform | thiel, bezos, munger |
| E-commerce / DTC / retail | bezos, munger, garry-tan |
| Trading / fintech / markets | taleb, munger, musk |
| AI agent / dev-tool / SaaS | thiel, musk, garry-tan |
| Content / media / community | bezos, naval, garry-tan |
| Marketplace-of-services / gig | eisenmann, bezos, horowitz |
| Hardware-adjacent / ops-heavy | musk, taleb, eisenmann |
| Regulated-adjacent (flag for fit-screen too) | taleb, munger, eisenmann |
| Default / unclear | thiel, munger, bezos |

## Adding an expert (curation, between runs)

1. `/nuwa-skill <name>` → mints `.claude/skills/<name>-perspective/`.
2. Add a lens card row above + slot the expert into the relevant idea-type row(s).
3. Next run picks it up automatically — no workflow change.
