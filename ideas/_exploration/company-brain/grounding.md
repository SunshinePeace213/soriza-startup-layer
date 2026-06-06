# Company Brain — Grounding Findings
*Facets: Why-now / Trends · Demand & Pain · Existing Solutions & Gaps · Niche/Wedge Angles*

---

## Why-now

- **YC Summer 2026 RFS explicitly names "Company Brain" as a wanted category.** Tom Blomfield (YC GP, Monzo founder) wrote one of the 15 RFS items verbatim: "a system that pulls knowledge out of every fragmented source, structures it, keeps it current, and turns it into an executable skills file for AI… not a search tool, not a chatbot over documents… a living map of how a company actually works." A second RFS item by Diana Hu ("AI Operating System for Companies") covers the same layer from an agent-orchestration angle. Two of fifteen YC slots targeting the identical infrastructure gap is a strong institutional signal. Source: [YC RFS](https://www.ycombinator.com/rfs), [VC Corner breakdown](https://www.thevccorner.com/p/yc-summer-2026-requests-for-startups-ideas)

- **MCP (Model Context Protocol) hit 97M monthly SDK downloads and 10,000+ public servers by end-2025, becoming the de facto agent-tool integration standard.** 41% of software organizations surveyed by Stacklok are in limited or broad production with MCP servers. MCP makes a "company knowledge layer" technically deliverable as a standards-compliant server rather than a bespoke integration, opening a clean wedge for a new infrastructure product. Source: [MCP Adoption Stats 2026](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol), [Splunk AI Trends 2025](https://www.splunk.com/en_us/blog/artificial-intelligence/top-10-ai-trends-2025-how-agentic-ai-and-mcp-changed-it.html)

- **Gartner projects 40% of enterprise software applications will embed task-specific AI agents by end of 2026, up from <5% in 2025.** This step-change in agent deployment creates an immediate structural need for the knowledge substrate those agents will consume. The infrastructure demand arrives before the infrastructure exists. Source: [Sterlites Enterprise Agentic AI 2026](https://sterlites.com/blog/2026-enterprise-agentic-ai-architecture)

- **Enterprise RAG is being reframed from "search tool" to "agent data foundation."** RAGFlow's 2025 year-end review documents the field's own conclusion: pure vector retrieval is insufficient for agents; the direction is toward context graphs, entity relationships, and multi-modal representations. Microsoft's GraphRAG (open-sourced 2024) introduced knowledge-graph-backed retrieval; this shift validates the "structured living map" framing over "chatbot over docs." Source: [RAGFlow 2025 Year-End Review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context), [RAG Enterprise Guide 2025](https://datanucleus.dev/rag-and-agentic-ai/what-is-rag-enterprise-guide-2025)

- **SKILL.md / agent-skills open standard announced by Anthropic December 2025, adopted by 26+ tools** (Claude, OpenAI Codex, GitHub Copilot, Cursor, VS Code, Atlassian, Figma, Stripe, Notion, Zapier). The standard formalizes the exact "executable skills file" concept in Blomfield's RFS — giving any company-brain product a concrete delivery format that plugs into every major agent runtime. Source: [Agent Skills Guide 2026](https://serenitiesai.com/articles/agent-skills-guide-2026), [SKILL.md Standard](https://medium.com/@loccarrre/the-agent-skills-standard-how-a-simple-skill-md-file-turns-ai-agents-into-on-demand-specialists-172af1d9737d)

---

## Demand & Pain

- **Workers spend 20–30% of their workweek searching for information.** 54% of organizations use 5+ platforms for documenting and sharing information; 31% don't know how many KM tools they have. Source: [KM Statistics 2025](https://cake.com/blog/knowledge-management-statistics/), [LiveAgent KM Challenges](https://www.liveagent.com/blog/knowledge-management-challenges/)

- **"About 70% of operational decisions have never been formally documented."** — Fabian Jakobi, CEO Interloom (validated at Commerzbank, Volkswagen, Zurich Insurance deployments). This is the direct causal link between tribal knowledge and AI agent failure. Source: [Fortune / Interloom](https://fortune.com/2026/03/23/interloom-ai-agents-raises-16-million-venture-funding/)

- **Verbatim pain from Hyper's HN launch:** "There's a lot of business and domain knowledge trapped in random places and mostly aggregated in employees' heads" — jameslk. And: "installing things onto my system without being transparent isn't great" — jpathm (showing sensitivity to data-ownership and privacy in this category). These comments also surface vendor lock-in fear: "open source and that data could live on my own servers" as an explicit demand. Source: [HN Launch Thread: Hyper YC P26](https://news.ycombinator.com/item?id=48387095)

- **Guru G2 reviews show 575 mentions of search/findability complaints**: slow results with scale, unrelated results, and organization challenges. Guru requires a 10-seat minimum at $25/seat — a 6-person team pays $250/month minimum. This price floor + poor search-at-scale is a real SMB frustration. Source: [Guru Pricing & Reviews 2026](https://www.featurebase.app/blog/guru-pricing), [Glitter AI Guru Alternatives](https://www.glitter.io/blog/knowledge-sharing/best-guru-alternatives)

- **Microsoft Copilot's accuracy NPS dropped to -24.1 by September 2025; nearly half of lapsed users cited distrust of its answers as the primary reason they stopped.** This is enterprise-scale evidence that generic AI over org data fails when it lacks structured, verified company context. Source: [Atlassian vs Copilot Comparison](https://www.automation-consultants.com/atlassian-rovo-vs-microsoft-copilot-how-do-these-ai-tools-compare/)

- **SMB AI investment rose from 42% (2024) to 57% (2025).** SMBs are now buying AI tools, but most enterprise knowledge-layer solutions (Glean: $60K/yr minimum; Guru: 10-seat min; Dust: €29/user/mo enterprise tier) are priced above SMB reach or require enterprise sales. Source: [SMB AI Outlook 2026](https://www.business.com/articles/ai-usage-smb-workplace-study/)

---

## Existing Solutions & Gaps

| Player | What it does | Who buys it | Key gap vs "company brain" |
|---|---|---|---|
| **Glean** | Indexes 100+ apps, enterprise search | Mid-market/enterprise 500+ employees; $60K/yr minimum ACV | Search, not structured executable context. Index-heavy (PII/compliance risk). No skills output. $7.2B valuation, heavy enterprise sales. |
| **Guru** | Verified wiki + AI search; verification workflows | Support/sales teams | Knowledge stale without human verification; 575 findability complaints on G2; SMB price floor $250/mo. No agent skills output. |
| **Notion AI** | Embedded AI in Notion workspace | Notion-centric teams | Ecosystem-locked; passive (answers questions), doesn't synthesize cross-source or output agent-runnable skills. |
| **Dust.tt** | Multiplayer AI workspace; 100+ connectors; MCP support | 3,000+ orgs, >300K agents deployed; €29/user/mo | Primarily a platform/runtime for agents, not the knowledge ingestion/structuring layer. $40M Series B (May 2026, Sequoia). Focuses on human-agent co-working. |
| **Atlassian Rovo** | AI search over Jira/Confluence ecosystem | Atlassian shops | Deeply Atlassian-locked; cross-tool knowledge ingestion is API-dependent and limited; cannot synthesize skills files from outside the ecosystem. |
| **Microsoft 365 Copilot** | AI assistant over M365 suite | Enterprise M365 customers | NPS -24.1 by Sep 2025; treats Jira/external data as second-class; no structured skills output; accuracy trust collapse. |
| **Interloom** | Context graph from operational records (tickets, emails, transcripts) → AI agent memory | Large European enterprises (Commerzbank, VW, Zurich Insurance) | Enterprise-only, European market focus, $16.5M seed (Mar 2026). Narrow on operational/support workflows; not a general company brain. |
| **Cognee** | Self-improving memory graph for AI agents; ECL pipeline; MCP integration | Developers + 70+ companies including Bayer | Developer-first infrastructure layer, not a product for non-technical teams. €7.5M seed (early 2026). Requires integration work. |
| **Hyper (YC P26)** | Silent company brain that learns from all tools, pushes context to AI tools | AI-first dev teams | Early-stage YC company; HN comments flag opacity concerns; no clear pricing/go-to-market for non-eng teams. |
| **Onyx (open-source)** | Self-hosted enterprise search + agentic RAG | Tech teams wanting self-hosting | Self-hosted = requires DevOps; not managed; $20/user/mo for cloud; pure search/RAG, not skills-file output. |
| **GoSearch** | Hybrid enterprise search, real-time + indexed | Mid-market; Glean alternative | Search tool, not a structured knowledge layer. Positioned as a cheaper Glean. |

**The consistent gap across all players:** None produces an *executable, agent-consumable skills file* from raw scattered company knowledge. Most are retrieval tools (find information), not synthesis tools (extract, structure, and output agent-runnable context). Interloom and Cognee come closest on architecture but target large enterprise with significant integration burden.

---

## Niche / Wedge Angles

- **Support teams, SMB tier — sharpest unmet pain, most reachable.** Support knowledge is highest-velocity (tickets, Slack threads, SOPs constantly change), most visibly broken (agents give wrong answers, Copilot NPS -24.1), and support teams at SMBs (10–200 employees) are priced out of Glean/Guru. A bootstrapped founder can sign 5–20 companies at $99–$299/mo without enterprise sales. The wedge: "build your support team's company brain, plug into your helpdesk in one afternoon."

- **Engineering/dev teams — highest AI-agent adoption, strongest SKILL.md / AGENTS.md pull.** The SKILL.md and AGENTS.md standards are already adopted by dev tooling. Engineers already run Claude Code, Cursor, Copilot. A "company brain that outputs SKILL.md / AGENTS.md for your codebase and engineering runbooks" maps directly to an existing workflow. Reachable by a founder with a dev-tools background; can start PLG/free tier.

- **Ops/compliance for regulated SMBs (fintech, insurance, healthcare-adjacent).** Interloom's Commerzbank/Zurich Insurance pattern shows the pattern works in regulated contexts. But Interloom is enterprise-only. An affordable, self-hostable company brain targeting fintech compliance ops or insurance underwriting SOPs — priced for Series A startups, not Fortune 500 — has no incumbent.

- **MCP server as the delivery mechanism.** Building a company-brain product that exposes its output as an enterprise MCP server is the right technical wedge: every major agent runtime already consumes MCP. This makes the product agent-runtime-agnostic and future-proof against model/tool churn.

- **Segments requiring enterprise sales (avoid for bootstrapped):** Glean, Dust, Interloom, and Microsoft Copilot all target 500+ employee orgs with 6–18 month sales cycles and $100K+ deals. A solo bootstrapped founder cannot compete here. The open lane is 10–200 employee companies (SMBs, scale-ups) willing to self-serve or do a brief product demo.

---

## Honest Risks (Saturation & GTM)

- **This is now an explicitly named YC category.** The RFS guarantees 5–15 funded teams will attempt this in the next batch. Hyper (YC P26) already launched. The window for being "first" is closed; the window for being "best-fit for a specific segment" is open for ~12–18 months before the well-funded players land there.

- **The enterprise tier is saturated and requires unfeasible GTM for a solo bootstrapper.** Glean ($7.2B, $300M ARR), Dust ($40M Series B), Atlassian Rovo (Atlassian-scale), and Microsoft Copilot are all pursuing the same enterprise layer with sales armies. Do not compete here without funding.

- **Knowledge freshness / quality is a hard, ongoing problem** — not just a build problem. Guru's G2 complaints center on staleness even with human verification workflows. Any company-brain product that cannot guarantee freshness will face the same NPS collapse as Copilot. This is an ongoing operational cost, not a one-time build.

- **Privacy and data-ownership concerns are a real buying blocker at SMBs.** HN launch of Hyper surfaced "open source / data lives on my servers" as an explicit demand, and vendor lock-in anxiety as a barrier. A self-hostable or local-first architecture is a competitive differentiator in this market, not a luxury.

- **"Company brain" is not yet a commoditized space** — it is a genuinely open layer at the SMB/mid-market end, but it is rapidly filling from the venture-backed top. The honest window for a bootstrapped founder is narrow: a specific vertical or department wedge, self-serve/PLG motion, and a fast (3–6 month) ship-to-revenue timeline.

---

## Sources

1. [YC Requests for Startups — Summer 2026](https://www.ycombinator.com/rfs) — Tom Blomfield's "Company Brain" and Diana Hu's "AI OS for Companies" RFS items
2. [VC Corner: YC Summer 2026 RFS breakdown](https://www.thevccorner.com/p/yc-summer-2026-requests-for-startups-ideas) — Detailed breakdown of both RFS items
3. [VC Cafe: YC Summer 2026 RFS edition](https://www.vccafe.com/2026/04/28/requests-for-startups-summer-2026-edition/) — "The missing layer is no longer model capability, but company context"
4. [Alex Lockey: Company Brain — Four Builders, One Architecture](https://www.alexlockey.com/writing/the-company-brain-four-builders-one-architecture/) — Karpathy, Garry Tan (GBrain/GStack), Hannah Stulberg (DoorDash), Ramp (Glass/Dojo) case studies; shared architecture elements; RESOLVER.md pattern
5. [HN Launch: Hyper (YC P26)](https://news.ycombinator.com/item?id=48387095) — Verbatim demand/concern signals from community; "domain knowledge trapped in employees' heads"; lock-in and transparency concerns
6. [Fortune / Interloom $16.5M seed](https://fortune.com/2026/03/23/interloom-ai-agents-raises-16-million-venture-funding/) — "70% of operational decisions never formally documented"; Commerzbank/VW/Zurich Insurance deployments; context graph architecture
7. [EU-Startups: Interloom €14.2M seed](https://www.eu-startups.com/2026/03/german-startup-interloom-lands-e14-2-million-seed-funding-for-ai-agent-knowledge-infrastructure/) — Interloom framing and funding details
8. [EU-Startups: Cognee €7.5M seed](https://www.eu-startups.com/2026/02/german-ai-infrastructure-startup-cognee-lands-e7-5-million-to-scale-enterprise-grade-memory-technology/) — ECL pipeline; 500x pipeline growth in 2025; Bayer deployment
9. [Dust $40M Series B (May 2026)](https://dust.tt/blog/series-b-multiplayer-ai) — 3,000+ orgs, 300K agents, zero churn 2025; Sequoia/Abstract; multiplayer AI framing
10. [SiliconAngle: Dust Series B](https://siliconangle.com/2026/05/18/multiplayer-ai-startup-dust-swipes-40m-funding-help-enterprises-move-beyond-isolated-ai-assistants/) — 100+ enterprise data platform connectors; human-agent co-working
11. [MCP Adoption Statistics 2026](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol) — 97M monthly SDK downloads; 10,000+ public servers; 41% of software orgs in production
12. [CData: 2026 Year for Enterprise-Ready MCP](https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption) — MCP becoming de facto enterprise agent standard
13. [Splunk: Top 10 AI Trends 2025](https://www.splunk.com/en_us/blog/artificial-intelligence/top-10-ai-trends-2025-how-agentic-ai-and-mcp-changed-it.html) — How MCP changed IT in 2025
14. [Sterlites: Enterprise Agentic AI 2026](https://sterlites.com/blog/2026-enterprise-agentic-ai-architecture) — Gartner: 40% of enterprise apps will embed agents by end-2026 (from <5% in 2025)
15. [RAGFlow: RAG 2025 Year-End Review](https://ragflow.io/blog/rag-review-2025-from-rag-to-context) — RAG → context engine shift; validation of structured-context-over-search direction
16. [SKILL.md Agent Skills Standard](https://medium.com/@loccarrre/the-agent-skills-standard-how-a-simple-skill-md-file-turns-ai-agents-into-on-demand-specialists-172af1d9737d) — SKILL.md format; 26+ platform adoption; Anthropic Dec 2025 announcement
17. [Agent Skills Guide 2026](https://serenitiesai.com/articles/agent-skills-guide-2026) — Skills standard across 16+ tools including Atlassian, Figma, Stripe, Notion, Zapier
18. [Glean Pricing Explained 2026](https://www.gosearch.ai/blog/glean-pricing-explained/) — $60K/yr minimum ACV; $50+/user/month; 100-seat enterprise minimum
19. [Sacra: Glean revenue & valuation](https://sacra.com/c/glean/) — $300M ARR May 2026; $7.2B valuation Series F Jun 2025
20. [Guru Pricing 2026](https://www.featurebase.app/blog/guru-pricing) — 10-seat minimum at $25/seat; G2 575 findability complaints
21. [Glitter AI: Guru Alternatives 2026](https://www.glitter.io/blog/knowledge-sharing/best-guru-alternatives) — Search quality degrades at scale; SMB pricing pain
22. [Atlassian Rovo vs Microsoft Copilot](https://www.automation-consultants.com/atlassian-rovo-vs-microsoft-copilot-how-do-these-ai-tools-compare/) — Copilot accuracy NPS -24.1 Sep 2025; nearly half of lapsed users cite distrust
23. [KM Statistics 2025](https://cake.com/blog/knowledge-management-statistics/) — 20–30% of workweek lost to information search; 54% use 5+ platforms
24. [LiveAgent KM Challenges](https://www.liveagent.com/blog/knowledge-management-challenges/) — Fragmented systems, trust erosion, tribal knowledge persistence
25. [SMB AI Outlook 2026](https://www.business.com/articles/ai-usage-smb-workplace-study/) — SMB AI investment: 57% in 2025 vs 42% in 2024
26. [Hyper YC — Y Combinator company page](https://www.ycombinator.com/companies/hyper-4) — "Self-Driving Company Brain" description; YC P26 batch
