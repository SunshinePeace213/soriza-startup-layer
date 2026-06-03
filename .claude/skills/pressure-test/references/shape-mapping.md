# Shape Mapping — Panel Curation Rules

Read during Step 3 of the workflow. Goal: produce a panel of 4–6 `(persona_name, persona_slug, role)` tuples with exactly one tagged `anti-thesis: true`. Inputs are the content of `hypothesis.md`. Output is the curated panel.

This is **fuzzy text matching against hypothesis content** — apply judgment. Don't try to regex-classify. Read the Who/How Often/How Severely/Status Quo sections and pick the experts whose lenses are most likely to surface load-bearing objections.

## Selection algorithm

1. Start the panel with the **default base** (always 2 seats).
2. Add **specialists** for each hypothesis attribute that matches. Each specialist consumes one seat.
3. Pick the **anti-thesis** slot last — it consumes one seat. Avoid duplicating an expert already on the panel as anti-thesis; if the natural anti-thesis is already on the panel, demote them to anti-thesis (their tag changes; no extra seat needed).
4. If the panel has **fewer than 4 seats**, fill to 4 in priority order: `Eisenmann → Munger → Thiel` (skipping any already on).
5. If the panel has **more than 6 seats**, drop the lowest-priority specialist additions until 6 (priority list below).
6. Verify exactly one seat is tagged `anti-thesis: true`. If somehow zero or two are tagged, re-do step 3.

## Default base (always include)

| persona_name | persona_slug | Role on panel |
|---|---|---|
| Tom Eisenmann | tom-eisenmann | Failure-pattern scholar (RAWI, six failure patterns). Asks: is this a false start, false positive, speed trap, cascading miracle, bad bedfellows, help-wanted? |
| Jeff Bezos | jeff-bezos | Customer obsession lens. Asks: working backwards from the customer, is the severity claim real, would the customer pay to escape? |

These two are always-on because they cover the two most common failure modes in problem-hypothesis stage: structural failure patterns (Eisenmann) and customer-obsession gaps (Bezos).

## Specialist additions (conditional)

Apply one row per matching attribute. A hypothesis can match multiple rows; each match adds one seat (subject to the 6-cap in the algorithm).

| If hypothesis content suggests… | Add | persona_slug | Why this expert |
|---|---|---|---|
| B2B SaaS / mid-market software / vertical SaaS | Garry Tan | garry-tan | YC operator lens; pattern-matches founder-market fit and the YC failure modes for SaaS |
| Consumer / network effects / network goods / community / social | Garry Tan | garry-tan | Consumer + network-effect lens (already covered if SaaS matched too) |
| Hardware / atoms / physical product / robotics / energy / space | Elon Musk | elon-musk | First-principles physics lens; "the idiot index"; capex realism |
| Deep-tech / contrarian thesis / claims a monopoly possibility / "10x better" framing | Peter Thiel | peter-thiel | Monopoly lens; mimetic competition detection; definite vs. indefinite optimism |
| Regulated industry / compliance risk / financial services / healthcare / legal-tech | Charlie Munger | charlie-munger | Incentives + circle of competence + invert; spots regulatory and incentive failure modes |
| Fat-tail risk surface (irreversible decisions, financial blow-ups, health/safety, model risk) | Nassim Taleb | nassim-taleb | Fragility / antifragility; ruin-risk; barbell logic; Mediocristan vs. Extremistan |
| Wealth/leverage framing / solo-founder / creator economy / "permissionless" framing | Naval Ravikant | naval-ravikant | Leverage lens; specific knowledge; play long-term games |
| Aesthetic / consumer design / "whole widget" / brand-defining product | Steve Jobs | steve-jobs | Integrated stack; taste as a moral category; focus is saying no |
| Sociological / political / elite dynamics / status-driven / behavioral | Vilfredo Pareto | vilfredo-pareto | Residues and derivations; circulation of elites; strips ideological derivations |
| Operator-heavy / scaling team / wartime-or-peacetime framing / org design | Ben Horowitz | ben-horowitz | Wartime/peacetime; the Struggle; lead bullets vs. silver bullets |

Multiple specialists can match. Examples:

- "AI legal-tech SaaS for in-house counsel" → +Tan (B2B SaaS) + Munger (regulated industry, legal compliance) — 4 seats with base
- "Hardware sensor for retail analytics" → +Musk (hardware) + Tan (B2B SaaS) — 4 seats with base
- "Crypto lending platform" → +Munger (regulated finance) + Taleb (fat-tail ruin risk) + Thiel (contrarian monopoly thesis if claimed) — 5 seats with base

## Anti-thesis selection

The anti-thesis seat is filled by the persona most temperamentally disposed to disagree with the hypothesis's *dominant temperamental shape* — not just its domain. The point is to seat someone who will find something to object to even when the other experts are aligned.

Match the hypothesis tone/framing against this table:

| If the hypothesis reads as… | Anti-thesis | persona_slug | Why |
|---|---|---|---|
| Optimistic moonshot / "this changes everything" / 10x framing | Nassim Taleb | nassim-taleb | Fragility lens cuts against optimism without ruin-risk accounting |
| Solid SaaS with large clear TAM / ROI confident | Peter Thiel | peter-thiel | "Big TAM" usually means mimetic competition — no monopoly path |
| Hardware / capex-heavy / physical | Charlie Munger | charlie-munger | Capital intensity + circle of competence — atoms have unforgiving margins |
| Consumer / virality / network effects assumed | Peter Thiel | peter-thiel | Mimetic competition collapses most viral consumer plays |
| Founder-friendly framing / "we'll figure out distribution later" | Tom Eisenmann | tom-eisenmann | Help-wanted pattern; cascading-miracles pattern |
| Status quo is "no organized workaround" / greenfield | Tom Eisenmann | tom-eisenmann | False-positive pattern — no workaround often means no real pain |
| Crypto / DeFi / financial services with leverage | Nassim Taleb | nassim-taleb | Built-in ruin risk; Talebian Extremistan domain |
| Aesthetic / lifestyle / "delight the user" framing | Charlie Munger | charlie-munger | Lollapalooza warning; incentives matter more than delight |
| Anything else | Tom Eisenmann | tom-eisenmann | Default skeptic; always finds a failure pattern that applies |

## Specialist priority (for the 6-cap)

When the panel exceeds 6 seats, drop in this order (lowest priority first):

1. Vilfredo Pareto (specialized lens; usually adds least to problem-stage hypothesis review)
2. Naval Ravikant (most useful for leverage/distribution; weakest on problem validation)
3. Ben Horowitz (operator lens; most useful at scaling stage, not problem stage)
4. Steve Jobs (taste lens; weakest on customer-discovery hypotheses)
5. Garry Tan (preserve if B2B SaaS or consumer — the most common shapes)
6. Charlie Munger (preserve for regulated/financial)
7. Elon Musk (preserve for hardware/atoms)
8. Nassim Taleb (preserve when fat-tail risk is present)
9. Peter Thiel (preserve when monopoly thesis is claimed)
10. Default base (Bezos, Eisenmann) — never drop

## Worked examples

### Example 1 — "Contract redline tool for in-house legal teams at mid-market SaaS"

Base: Eisenmann, Bezos (2)
Specialists: +Tan (B2B SaaS), +Munger (regulated — legal compliance) (4 total)
Anti-thesis selection: Hypothesis reads as "solid SaaS with clear ROI" → Thiel
Anti-thesis is not already on panel → add as 5th seat tagged anti-thesis.
**Final panel: Eisenmann, Bezos, Tan, Munger, Thiel (anti-thesis). 5 seats.**

### Example 2 — "Crypto-collateralized consumer lending"

Base: Eisenmann, Bezos (2)
Specialists: +Munger (financial services regulated), +Taleb (fat-tail ruin risk), +Thiel (claims contrarian monopoly thesis) (5 total)
Anti-thesis selection: "Crypto + financial services" → Taleb. Already on panel → demote Taleb's role to anti-thesis (no extra seat).
**Final panel: Eisenmann, Bezos, Munger, Thiel, Taleb (anti-thesis). 5 seats.**

### Example 3 — "Open-source dev tool for solo developers"

Base: Eisenmann, Bezos (2)
Specialists: +Naval (solo-founder / permissionless framing) (3 total)
Fill to 4: priority order Eisenmann → Munger → Thiel; Eisenmann is on; add Munger (4 total)
Anti-thesis selection: Reads as "founder-friendly, will figure out distribution later" → Eisenmann. Already on panel → demote to anti-thesis.
**Final panel: Eisenmann (anti-thesis), Bezos, Naval, Munger. 4 seats.**

### Example 4 — "Vertical AI agent for HVAC contractors in Texas"

Base: Eisenmann, Bezos (2)
Specialists: +Tan (B2B SaaS, but vertical) (3 total)
Fill to 4: Eisenmann on, add Munger (4 total)
Anti-thesis selection: Status quo is "manual workaround / phone calls" → reads as solid B2B SaaS → Thiel.
**Final panel: Eisenmann, Bezos, Tan, Munger, Thiel (anti-thesis). 5 seats.**

## Edge case — fewer perspective skills than needed

If `glob .claude/skills/*-perspective/` finds fewer skills than the algorithm needs (e.g., a fresh install with only 4 personas available), use what exists. Always keep the anti-thesis tag on the persona whose temperament most disagrees with the hypothesis shape — even if the panel is smaller than ideal.

## Edge case — new personas added to the pool

When a new `*-perspective` skill appears, add a row to the Specialist Additions table mapping a hypothesis-attribute trigger to that persona. Until the table is updated, new personas only enter the panel via the fill-to-4 priority list (which is currently Eisenmann/Munger/Thiel — unaffected).
