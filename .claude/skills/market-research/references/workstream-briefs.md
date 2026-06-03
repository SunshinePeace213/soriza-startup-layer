# Workstream Briefs

The per-workstream instructions and output shapes for `/market-research`'s subagent fan-out. The four W-briefs are read by the `market-researcher` agent; the last by `competitor-steelman`. Each writes one provenance doc under `docs/ideas-stages/<slug>/market-research/`.

Shared rules for all workstreams: distill, don't dump. Every load-bearing claim cites a source URL. Prefer recent, primary sources and named players over generic market commentary. Tie each finding to *this* idea, not the category in general.

---

## W1 — Competitive landscape → `competitive-landscape.md`

Map the players around this idea into four tiers. Start from the scope-locked competitor set and expand it via search — the founder's list is a seed, not the ceiling.

- **Direct** — same job, same buyer (the obvious competitors)
- **Indirect** — a different approach to the same job (e.g. a manual workaround tool, a generalist that covers the need)
- **Potential acquirers** — who would plausibly buy a winner in this space, and why
- **Adjacent** — players one step away who could move in (platform owners, upstream tools)

For each named player: what they do, who they serve, pricing if public, and the one place they fall short for this segment.

Output shape:

    # Competitive Landscape — <slug>

    ## Direct
    | Player | What they do | Who they serve | Pricing | Where they fall short |
    |---|---|---|---|---|

    ## Indirect
    | Player | Approach to the same job | Why a customer settles for it | Where it fails |
    |---|---|---|---|

    ## Potential acquirers
    - <player> — why they'd buy this space; what it implies for the founder

    ## Adjacent (could move in)
    - <player> — the capability that lets them enter; how fast

    ## Sources
    1. <URL> — what it supports

---

## W2 — Customer-review synthesis → `review-synthesis.md`

Mine public complaints about the named incumbents and distill the **top unresolved** ones — the things existing solutions have NOT fixed. Then judge whether this idea addresses them.

Search G2, Capterra, Trustpilot, Reddit, app-store reviews, YouTube comments, niche forums. Use targeted site queries; community pain surfaces poorly in plain web search.

**Adversarial verify:** every "users complain about X" claim must trace to ≥2 independent sources. Flag single-source or unverified complaints explicitly — do not present them as established.

Output shape:

    # Review Synthesis — <slug>

    ## Top unresolved complaints (ranked)
    1. <complaint> — frequency/intensity signal — sources [n][m] — [verified / single-source]
    2. ...

    ## Does this idea address them?
    For each top complaint: Addressed / Partially / Not — one line of why.

    ## Problem–Solution-Fit signal
    strong | weak | none — one sentence tying the hypothesis to the unresolved complaints it would (or wouldn't) solve.

    ## Sources
    1. <URL> — what it supports

---

## W3 — Market sizing + buyer map → `market-sizing.md`

Lean, SOM-weighted, and sourced — the founder is bootstrapping, not raising. Order-of-magnitude ranges with cited assumptions beat false precision.

- **TAM / SAM / SOM** as ranges. Tag every assumption with its source. Weight effort toward the **bottom-up SOM**: reachable users × realistic price × plausible conversion.
- **Buyer landscape** — who holds the budget, who influences, who decides; note whether they're the same person.
- **Market maturity** — expanding / consolidating / mature, with the signal that classifies it (funding flow, entrant/exit rate, consolidation).
- **Sensitivity note** — the single assumption the SOM hinges on most.

**Adversarial verify** the load-bearing figures against ≥2 sources; flag the unverifiable.

Output shape:

    # Market Sizing — <slug>

    ## TAM / SAM / SOM
    | Layer | Range | Key assumptions (tagged with source) |
    |---|---|---|

    ## Bottom-up SOM
    reachable users × price × conversion = <range>, with each factor sourced/justified.

    ## Buyer landscape
    - Budget holder: <who> · Influencer: <who> · Decider: <who> · Same person? <y/n>

    ## Market maturity
    expanding | consolidating | mature — the classifying signal.

    ## Sensitivity
    The answer hinges most on: <assumption>. If it's wrong by <x>, SOM moves to <y>.

    ## Sources
    1. <URL> — what it supports

---

## W4 — Trend analysis → `trends.md`

Three external trends and whether each is a tailwind or headwind **for this specific hypothesis** — plus the language users use and what analogous markets teach.

- **Three trends**, one each from regulatory / technological / demographic where possible. For each: the trend, tailwind or headwind, and the *mechanism* by which it helps or hurts *this* idea (not the category).
- **Community language** — the exact words/phrases the target users reach for when describing this problem (from subreddits, LinkedIn, forums). Useful for positioning and copy.
- **Analogous markets** — where a similar problem was solved elsewhere: what worked, what didn't, what transplants here.

Output shape:

    # Trends — <slug>

    ## Three trends
    | Trend | Type (reg/tech/demo) | Tailwind or headwind | Mechanism for THIS idea | Source |
    |---|---|---|---|---|

    ## Community language
    - "<exact phrase users use>" — where seen

    ## Analogous markets
    | Market | Similar problem | What worked | What didn't | Transplant |
    |---|---|---|---|---|

    ## Sources
    1. <URL> — what it supports

---

## Competitor-steelman → `competitor-steelman.md`

(Read by the `competitor-steelman` agent — adversarial, not balanced. Full voice rules are in the agent's own system prompt.)

Make the strongest case the incumbent wins. Per-tier threat, then the single most dangerous competitor in full, then the survival bar.

Output shape:

    # Competitor Steelman — <slug>

    ## Per-tier threat
    - Direct: why they crush the founder
    - Indirect: why "good enough" wins
    - Potential acquirer: why the space gets bought out from under the founder
    - Adjacent: why a bigger player absorbs this

    ## The one that kills you
    <named competitor>. Why their approach is better, why customers choose them, and why each of the founder's claimed differentiators is not defensible.

    ## Survival bar
    For the founder to survive this, the following must be true: <conditions> — stated as the bar to clear, not reassurance.

    ## Sources
    1. <URL> — what it supports
