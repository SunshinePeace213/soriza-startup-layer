# Grounding Research — Dynamic Software Interfaces / Per-User AI-Malleable UIs

Thesis summary: AI coding agents are now capable enough that end-users become their own
forward-deployed engineers. Software ships as shared primitives (data model + actions +
embedded agent) and each user heavily modifies the UI to fit their workflow. The startup
opportunity is the full delivery stack that makes this safe, easy, and durable — with
strong wedge verticals where per-user interface malleability commands highest WTP.

---

## Trends / Why Now

1. **Lovable hit $400M ARR in February 2026 (from $0 at launch ~14 months prior)** — the fastest
   ARR ramp ever recorded for a consumer dev tool. Bolt.new crossed $40M ARR by March 2025.
   Together they prove that non-engineers building full apps via natural language is already a
   mass behavior, not a niche one. The infrastructure for "user as developer" is proven; the
   next step is making it per-session, per-workflow, per-person inside *existing* software.
   Source: Sacra / Lovable funding data.

2. **Cursor reached $2B ARR in February 2026** — $4M to $2B in 18 months, fastest B2B SaaS
   growth on record. GitHub Copilot has 4.7M paid subscribers with 90% Fortune 100 adoption.
   These numbers confirm that AI-augmented coding is now mainstream developer behavior, not
   bleeding edge — the cultural pre-condition for end-users expecting similar agency over their
   own interfaces is already forming.
   Source: The Next Web / GTM Newsletter.

3. **FDE job postings surged 800%+ Jan–Sep 2025; role count grew 42x from 2023 to 2025.**
   "Forward deployed engineers" are engineers who live at the customer site customizing software
   per-account. The explosive demand signals that generic SaaS can no longer fit diverse
   workflows — enterprises are paying full-time engineering salaries just to adapt UI and
   logic per customer. A product that lets the *user* do this without an FDE is a direct cost
   substitution play.
   Source: Computerworld / AI Daily / Salesforce blog.

4. **CHI 2025 research paper ("Generative and Malleable User Interfaces with Generative and
   Evolving Task-Driven Data Model", arXiv 2503.04084)** proposed task-driven data models as
   the stable primitive underlying generative UI — users modify schema and UI spec via natural
   language or direct manipulation, with changes propagating automatically. This is the academic
   proof-of-concept for the exact thesis above; it is now citable, peer-reviewed, and published
   — meaning the idea has crossed from speculation to validated HCI research, one step from
   productization.
   Source: ACM CHI 2025 / arXiv.

5. **CopilotKit raised $27M (May 2026) to standardize the AG-UI protocol** — an open,
   bidirectional agent-to-frontend event stream now adopted by Google, Microsoft, AWS, LangChain,
   Mastra, and Oracle in production. Millions of weekly npm installs. This means the *plumbing*
   for connecting backend agents to live, state-sharing UIs is becoming commoditized
   infrastructure, lowering the build cost for any startup that wants to ship malleable-UI
   products today.
   Source: TechCrunch / CopilotKit blog.

---

## Existing Solutions — Gaps

6. **No-code platforms (Notion, Airtable, Coda, Bubble) stop at team-level configuration.**
   Coda's advanced formula/automation system lets teams build workflows, but the unit of
   customization is the *workspace*, not the *individual user*. Notion hits hard limits with
   large datasets and cannot take in-product action without Zapier. None of these products let
   user A render the same underlying database as a Kanban while user B renders it as a calendar
   and user C renders it as a scripted automation — from the same shared data model. That gap
   is the exact gap the thesis addresses.
   Source: Coda blog / AFFiNE / community comparisons.

7. **Intercom Fin crossed $100M ARR at $0.99/resolution with outcome-based pricing, backed by
   a $1M performance guarantee.** This is the clearest live proof that outcome-based pricing
   (pay per result, not per seat) works at scale in an AI product. Fin resolves >1M
   conversations/week. The model is directly replicable in vertical malleable-UI products:
   charge per workflow completed or time saved, not per "interface view."
   Source: GTM Newsletter / Stripe customer story / Gleap blog.

8. **Vertical AI SaaS commands 2–3x higher WTP than horizontal SaaS in 2026,** with
   regulated industries layering on further premiums: healthcare (HIPAA) +25–40%, legal
   +30–45%. Harvey (legal AI) hit $195M ARR in 2025 at $11B valuation, up 3.9x YoY —
   purely from per-seat licensing to law firms where every lawyer's workflow is different.
   The intersection of "high-stakes vertical" + "per-user interface divergence" = the
   strongest WTP zone for malleable-UI products.
   Source: CNBC / Sacra / L40 insights / buildmvpfast.com.

---

## Demand / Pain

9. **Gartner projected >30% of enterprise SaaS would have outcome-based pricing components
   by 2025 (up from ~15% in 2022).** Traditional SaaS gross margins compressed from ~90% to
   ~60% as AI inference costs hit. This is forcing buyers to demand results, not licenses —
   and forcing sellers toward outcome-tied models. A per-user malleable interface product
   that can credibly say "your workflow runs X% faster or you don't pay" is structurally
   aligned with where enterprise procurement is heading.
   Source: Monetizely / SoftwareSeni / BetterCloud.

10. **Vertical SaaS growing at 18–22% CAGR, 2–3x faster than horizontal SaaS.**
    Micro-niches experienced 340% growth vs broad market platforms (Gartner Q4 2025 SaaS
    report cited in entrepreneurloop.com). The LMS market alone is $28.6B in 2025, projected
    $123.8B by 2033 (20.2% CAGR). Healthcare, legal, edtech, and logistics are all cited as
    sectors with "painful document-heavy workflows" that vertical AI is only beginning to
    address — and where per-person interface divergence is most acute (a nurse's workflow vs
    a billing admin's workflow in the same hospital system look nothing alike).
    Source: Grand View Research / L40 / entrepreneurloop.com.

---

## Adjacent Markets — Wedge Signals

11. **Anthropic launched Claude enterprise agent plugins (Feb 2026)** targeting finance, legal,
    HR, and engineering departments — pre-built agents that companies *modify* to fit unique
    needs. Priced at $0.08/session-hour (consumption model) on top of token costs. This signals
    that the major model provider is explicitly building toward "shared primitive + per-org
    customization" — validating the thesis at the infrastructure layer, and opening a gap at
    the *per-user* (not per-org) layer that Anthropic is not yet addressing.
    Source: TechCrunch / Anthropic blog.

12. **AI-powered personalization in LMS/edtech shown to boost retention by 30%** through
    adaptive layout and content pacing. Cypher Learning and Sana Labs are building agent-native
    LMS platforms in 2025. But none yet ship the *interface itself* as user-malleable — the
    adaptive behavior is system-driven, not user-directed. A student who wants their course
    materials rendered as a Pomodoro scheduler, or a corporate trainer who wants the same
    content deck rendered as a decision tree, cannot do that today.
    Source: Cypher Learning / Unified Infotech / Grand View Research.

---

## Sources

1. https://sacra.com/c/lovable/ — Lovable $400M ARR data and funding rounds
2. https://thenextweb.com/news/cursor-anysphere-2-billion-funding-50-billion-valuation-ai-coding — Cursor $2B ARR milestone
3. https://thegtmnewsletter.substack.com/p/deconstructing-cursor-growth-playbook-4m-to-2b-arr — Cursor GTM and growth speed
4. https://www.computerworld.com/article/4171867/heres-one-career-emerging-from-the-ai-shift-forward-deployed-engineers.html — FDE job growth stats
5. https://www.ai-daily.news/articles/forward-deployed-engineers-ais-key-role-in-2026 — FDE demand 2026 context
6. https://arxiv.org/abs/2503.04084 — CHI 2025 malleable UI / task-driven data model paper
7. https://techcrunch.com/2026/05/05/copilotkit-raises-27m-to-help-devs-deploy-app-native-ai-agents/ — CopilotKit $27M raise and AG-UI adoption
8. https://www.copilotkit.ai/ag-ui — AG-UI protocol details and ecosystem adopters
9. https://thegtmnewsletter.substack.com/p/gtm-178-intercom-ai-agent-outcome-based-pricing-archana-agrawal — Intercom Fin $100M ARR outcome pricing
10. https://www.gleap.io/blog/intercom-fin-ai-pricing-2026 — Fin $0.99/resolution and performance guarantee
11. https://www.cnbc.com/2025/08/04/legal-ai-startup-harvey-revenue.html — Harvey $100M ARR milestone
12. https://sacra.com/c/harvey/ — Harvey $195M ARR and seat-based growth
13. https://www.l40.com/insights/vertical-ai-saas — Vertical SaaS 2–3x WTP premium
14. https://www.buildmvpfast.com/blog/vertical-ai-eating-horizontal-saas-2026 — Vertical AI CAGR vs horizontal
15. https://www.getmonetizely.com/blogs/the-2026-guide-to-saas-ai-and-agentic-pricing-models — Outcome-based pricing shift
16. https://techcrunch.com/2026/02/24/anthropic-launches-new-push-for-enterprise-agents-with-plugins-for-finance-engineering-and-design/ — Anthropic enterprise agent plugins
17. https://www.grandviewresearch.com/industry-analysis/learning-management-systems-market — LMS market $28.6B to $123.8B
18. https://www.cypherlearning.com/blog/business/the-future-of-learning-lms-platforms-with-ai-agents-in-2025 — Cypher Learning agent-native LMS
19. https://affine.pro/blog/notion-alternative-tips — Notion limitation analysis
20. https://entrepreneurloop.com/bootstrapped-saas-niches-solo-founders/ — Micro-niche 340% growth stat
