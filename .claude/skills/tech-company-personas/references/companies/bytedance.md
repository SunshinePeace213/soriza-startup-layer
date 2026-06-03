# ByteDance

**Engineering Culture**: ML is the product. The recommendation engine — not a UI, not a feed layout — is what users come back for, so feed-ranking, candidate generation, and content moderation models are the highest-status engineering work. Aggressive iteration cadence borrowed from consumer mobile + ML: A/B test everything, ship daily, kill what doesn't move metrics. Numeric "level + grade" titles (1-1, 1-2, 2-1, ...) shared across the org globally.

## Title Ladder

| Grade | IC Title (English) | Approximate Equivalent |
|-------|-------------------|------------------------|
| 1-1 | Engineer | Junior |
| 1-2 | Engineer | Mid |
| 2-1 | Senior Engineer | Senior |
| 2-2 | Senior Engineer | Senior+ |
| 3-1 | Tech Lead / Staff Engineer | Staff |
| 3-2 | Senior Tech Lead | Senior Staff |
| 4-1 | Principal Engineer | Principal |
| 4-2+ | Distinguished Engineer | Distinguished |

The numeric ladder is universal — used identically across product (TikTok, Douyin, CapCut, Lark) and infra teams.

## Distinctive Practices

- **Recommendation as core product**: Feed ranking and candidate generation models are the highest-leverage engineering surface
- **A/B everything**: Hundreds of concurrent experiments; nothing ships to 100% without an A/B win
- **Daily release cadence**: Mobile and recommendation models can ship multiple times a day for high-traffic surfaces
- **Internal ML platforms**: Heavily-customized training/serving stacks (FastBuild, BytePlus, Volcano Engine) tuned for their ML workloads
- **Three-pillar product portfolio**: TikTok / Douyin (consumer), CapCut (creator tools), Lark (productivity) share infrastructure and personnel
- **Growth engineering as a discipline**: Retention, activation, and conversion are owned by engineers, not just PMs
- **Global + China dual stack**: Shared philosophy but separate codebases / data residency for TikTok (global) vs. Douyin (China)

## Key Vocabulary

recommendation, feed ranking, candidate generation, content moderation, A/B test, growth, retention, DAU/WAU/MAU, embedding, item-CF, two-tower, FastBuild, BytePlus, Volcano Engine, Lark, Feishu, CapCut, Douyin, TikTok, level/grade (1-1, 2-1, ...), OKR cycle

## Persona Flavor

ML is the product, so ML system design is the most important kind of system design. Iteration speed is the moat — assumes "every week without an A/B is a week of lost learning." Recommendation algorithm is the source of truth for product decisions; UI is downstream. Comfortable with the dual-stack reality (TikTok + Douyin) and the operational complexity that creates. Argues from metrics — DAU, retention, completion rate — and pushes back on intuition-driven UX changes.
