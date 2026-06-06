# Demand / Pain Validation — Findings

## Key findings

- **Shadow IT has surged: 60% of custom internal tool builds in 2025 happened outside IT oversight**, up from ~15% in 2022. The trigger is rigid SaaS: 25% of shadow builders cite "existing SaaS was insufficient," and 31% say building was faster than waiting for IT to approve a tool that still wouldn't fit their workflow. This is mass workaround behavior at enterprise scale, not a fringe signal. (Source: Retool Build vs. Buy Report 2026)

- **Obsidian's plugin ecosystem has crossed 120 million total downloads across 4,456 community-built plugins** (as of mid-2026). Top plugins — Excalidraw (6.3M), Templater (4.5M), Dataview (4.3M) — are not decorative; they are load-bearing rewrites of how users structure, query, and view their notes. Users aren't satisfied with what ships: they rebuild the interface themselves, and millions follow. (Source: obsidianstats.com most-downloaded page)

- **Notion template economy: Thomas Frank's team made $1M in template sales in 2022 alone; Easlo crossed $239K in the same year at ~$20K/month.** These are workflow configurations sold as products — concrete evidence that people pay real money to get software that fits their shape rather than the default. The market has matured (competition is higher now), but the underlying demand is structural: Notion has ~100M users and the default interface fits none of them perfectly. (Sources: Thomas Frank Typefully post; Kajabi/Easlo coverage)

- **Microsoft Power Platform has 56 million monthly active users** doing low-code automation — citizen developers bypassing software rigidity without writing real code. This is the largest revealed-demand proxy: tens of millions of people are hacking workflows because off-the-shelf software doesn't do what they need. 89% of developers have used a low-code platform in the past 12 months. (Source: Microsoft Power Platform stats; Adalo no-code adoption stats)

- **Retool hit $138.6M ARR in 2024 ($90M at end of 2024, $120M by Oct 2025 after AppGen/Agents launch).** The entire business is predicated on the pain: internal ops teams can't get engineers to build tools fast enough, so they build their own. 35% of enterprises have already replaced at least one SaaS tool with a custom build; 78% plan to build more in 2026. CRMs and workflow automations top the replacement list. This is a $138M+ annual signal that rigid SaaS is leaving money on the table. (Sources: Retool/Sacra; BusinessWire Retool 2026 report)

- **Hacker News has at least four distinct threads on "malleable software" (2020, 2024, June 2025, Aug 2025)**, with recurring named examples: Excel/VBA as accidental programming that non-developers actually use, "load-bearing spreadsheets with incomprehensible macros," and a direct HN comment: "I once built a CRM in Google Sheets fully mirroring the data model of Salesforce." The doctor EMR burnout angle is also surfaced — inflexible EHR systems are documented as a driver of professional burnout, with one HN commenter noting ICD code fields that persist from a paper form designed 50+ years ago. These are not abstract complaints; they are named, specific failure modes of rigid software. (Sources: HN threads 44237881, 40188435, 45036754, 47107637)

- **Tampermonkey has 10 million+ users; Greasy Fork hosts thousands of scripts with installs ranging into the hundreds of thousands per script.** These are people writing or installing code just to make existing web software behave differently — Gmail label management scripts, Jira autofill scripts, Reddit Enhancement Suite. The behavior is revealed demand: if the software worked the way users wanted, the scripts wouldn't exist. (Sources: Tampermonkey GitHub; Greasy Fork listing)

- **Neurodivergent users (ADHD, autism) represent an acutely underserved segment.** Most PM tools "were built by neurotypical teams for neurotypical users" — they assume easy prioritization, context-switching, and abstract deadline motivation. Tools like Leantime (open-source) were explicitly built because no off-the-shelf tool fit. This segment actively modifies or abandons tools at higher rates and is vocal about it. It's loud-but-niche — not the mass market — but it's a beachhead with outsized willingness to pay for fit. (Source: Leantime blog; aidigitalspace.com neurodivergent AI tools)

- **Counter-signal — "customization is a vitamin most people never act on":** HN commenters in the malleable software threads note that customization options often go unused because the UX for customization itself is bad (toolbar customization "sucks," cognitive overhead is too high). The WoW modding culture and HyperCard are cited as past peaks that didn't generalize. Outlook has had decades of customization options that remain untouched. This is real: the demand for custom UX is revealed loudest in power-user communities (Obsidian, Notion, HN), not the median user. The opportunity is probably not "everyone customizes everything" — it's "the right abstraction makes customization zero-friction enough that the latent demand activates." AI coding agents could be that abstraction shift.

- **AI-native workaround tools are accelerating the pattern.** n8n (open-source workflow automation) is gaining fast; Make.com and Zapier are growing their AI layers. Deloitte's 2026 tech predictions flag that "SaaS subscriptions and seat-based licensing could give way to usage/outcome-based pricing" as agents replace click-through interfaces. The direction of travel is clear: users want outcomes, not interfaces — and they are already duct-taping toward that future with automation tools. The startup opportunity is to make the duct tape load-bearing by design. (Sources: Deloitte 2026 tech predictions; Bain agentic AI SaaS report 2025)

## Sources

1. https://retool.com/blog/ai-build-vs-buy-report-2026 — Shadow IT growth (15%→60%), 35% replacing SaaS, build triggers
2. https://www.businesswire.com/news/home/20260217548274/en/Retools-2026-Build-vs.-Buy-Report-Reveals-35-of-Enterprises-Have-Already-Replaced-SaaS-With-Custom-Software — Retool 2026 build vs buy headline stats
3. https://sacra.com/c/retool/ — Retool ARR $90M→$120M trajectory
4. https://getlatka.com/companies/retool — Retool $138.6M ARR 2024
5. https://www.obsidianstats.com/most-downloaded — Obsidian plugin download counts (Excalidraw 6.3M, Templater 4.5M, Dataview 4.3M, 120M total)
6. https://obsidian.md/blog/future-of-plugins/ — Obsidian plugin ecosystem overview
7. https://typefully.com/TomFrankly/dollar1-million-in-notion-template-sales-kuFT0iD — Thomas Frank $1M template sales 2022
8. https://www.kajabi.com/blog/best-place-to-sell-notion-templates — Easlo $239K / Notion template economy
9. https://www.microsoft.com/en-us/power-platform — Microsoft Power Platform 56M MAU
10. https://www.adalo.com/posts/traditional-coding-vs-no-code-adoption-statistics — 89% of devs using low-code; citizen developer stats
11. https://news.ycombinator.com/item?id=44237881 — HN "Malleable Software: Restoring User Agency" June 2025; EMR burnout, color customization complaints
12. https://news.ycombinator.com/item?id=40188435 — HN "Malleable Software in the Age of LLMs" May 2024; Excel/VBA accidental programming, Outlook unused customization
13. https://news.ycombinator.com/item?id=45036754 — HN "Malleable Software" Aug 2025; load-bearing Excel macros, SAP clean core, ICD code field fossilization
14. https://news.ycombinator.com/item?id=47107637 — HN comment: "I once built a CRM in Google Sheets fully mirroring Salesforce's data model"
15. https://github.com/Tampermonkey/tampermonkey — Tampermonkey 10M+ users
16. https://greasyfork.org/en — Greasy Fork userscript repository
17. https://leantime.io/open-source-project-management-for-adhd-why-we-built-leantime-for-neurodivergent-productivity/ — Neurodivergent segment / ADHD PM tool failure modes
18. https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/saas-ai-agents.html — Deloitte 2026: SaaS pricing disruption by agents
19. https://www.bain.com/insights/will-agentic-ai-disrupt-saas-technology-report-2025/ — Bain agentic AI SaaS disruption analysis 2025
20. https://zapier.com/blog/ai-sprawl-survey/ — Tool sprawl: 70% of enterprises haven't moved beyond basic integration; 76% experienced negative outcomes from disconnected AI
