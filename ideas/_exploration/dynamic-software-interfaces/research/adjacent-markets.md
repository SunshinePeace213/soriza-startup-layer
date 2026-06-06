# Adjacent / Analogous Markets — Findings

## Key findings

- **WordPress plugin market at ~$2.4B (2025), but value accumulates at the top — not spread across the ecosystem.** WooCommerce (~$28M ARR), Elementor, Yoast, and Gravity Forms dominate; thousands of commodity plugins race to zero. The platform (Automattic) captures hosting/brand; a handful of vertical specialists capture the premium plugin tier; the long tail earns almost nothing. Lesson for a dynamic-UI startup: being the "primitives layer" is good, but running a curated ecosystem of verified UI-configuration providers (not an open free-for-all) is where margin lives. The failure mode is open-listing a marketplace and watching it commoditize within 18 months.
  - Source: https://colorlib.com/wp/wordpress-statistics/ | https://zetamatic.com/blog/2025/01/how-much-revenue-does-wordpress-generate/

- **Salesforce AppExchange: the "ecosystem multiplier" model — $5.80 earned by partners for every $1 Salesforce earns (2024), projected $6.19 by 2026.** Salesforce provides the data model + identity + distribution (AppExchange); ISVs build vertical workflow apps on top. Key mechanism: Salesforce locks in the org-wide CRM data layer, making switching catastrophically expensive — ISVs then rent that captive audience. Lesson: a dynamic-interface platform that owns the schema / config layer (the "data model of how a user shaped their app") creates the same switching cost. The platform's job is to own the layer ISVs cannot afford to recreate.
  - Source: https://foundationinc.co/lab/salesforce-21b-b2b-ecosystem/ | https://www.salesforce.com/news/press-releases/2019/10/25/new-research-finds-the-salesforce-economy-will-create-more-than-1-trillion-in-new-business-revenues-and-4-2-million-jobs-between-2019-and-2024/

- **Excel: 750M regular users vs. ~11M JavaScript developers — spreadsheets are the most successful "end-user programming" runtime ever built, and they succeeded by hiding the runtime.** Two decisions made it work: (1) GUI-first launch (Mac-only, lowered the abstraction floor) and (2) incremental recalculation (made feedback instant). Nobody calls Excel a coding environment — users feel like they are arranging data. Lesson for AI-driven dynamic UI: the interface must feel like configuration or customization, not coding. The moment users feel they are "programming," adoption collapses to the developer segment only.
  - Source: https://www.notboring.co/p/excel-never-dies

- **Minecraft Bedrock Marketplace: $500M+ cumulative payout to creators (70/30 split in creators' favor), $146M in Q1 2025 alone — a "ship primitives + certified store" model that outperformed the uncontrolled free-mod ecosystem.** The open Java modding scene is thriving but unmonetized; Microsoft built a controlled Bedrock Marketplace alongside it. Controlled marketplace = quality signal, payment rail, and trust, driving spending. Lesson: running a permissioned tier of "certified UI configurations / adapters" alongside an open layer is a proven dual-track model. The open layer handles discovery; the certified layer handles revenue.
  - Source: https://screenrant.com/minecraft-marketplace-350-million-profit-modders/ | https://oasisaiminecraft.com/statistics/minecraft-economic-marketplace-analytics/

- **Roblox: $923M creator payouts in 2024, $1.5B+ in 2025, $4B+ cumulative — but creators earn ~30% of each sale and the platform keeps ~70%.** Roblox ships engine primitives (physics, rendering, scripting API) and lets creators build actual experiences. The platform's outsized cut holds because it owns identity, wallet, and distribution; creators accept it because there is no alternative runtime for that audience. Lesson: in a dynamic-UI platform, whoever controls user identity + billing + distribution captures the majority of value even when creators do all the building. This is the toll-road model — build the road, take the toll on every transaction.
  - Source: https://endsights.com/roblox-creator-economy | https://www.sec.gov/Archives/edgar/data/0001315098/000131509824000163/rblx-20240801xexhibit991.htm

- **Notion template economy: individual creators earning $239K–$1M+ per year; Notion charges only 10% + $0.40 per transaction.** Notion's primitives (blocks, databases, pages) are deliberately generic. The template layer converts generic primitives into vertical use-case software — "second brain for students," "CRM for freelancers." Notion hit ~$500M ARR with ~100M users. Lesson: when primitives are flexible enough, creators do your vertical GTM for free. The platform's job is making primitives expressive enough that templates feel like different products, not just re-skins.
  - Source: https://foundationinc.co/lab/notion-project-templates/ | https://sacra.com/c/notion/ | https://www.notion.com/help/selling-on-marketplace

- **Chrome Web Store: 111,933 extensions, 1.69B installs, but 86.3% of extensions under 1,000 users; Google deprecated its own payment system.** Result: fragmented payment rails, no platform-level subscription lock-in, and a long tail of abandoned extensions that become security liabilities. Outliers (GMass: $130K/month, Speechify: ~$14M ARR) succeed by owning their own billing and audience. Lesson: a dynamic-UI platform that offloads billing loses leverage and creates a fragmented user experience. Owning the subscription layer is what converts a distribution platform into a sustainable business.
  - Source: https://www.extensionradar.com/blog/how-to-monetize-chrome-extension | https://ful.io/blog/5-chrome-extensions-with-the-highest-revenue-in-2024

- **Headless / API-first commerce (Shopify Hydrogen): global headless commerce market $1.74B in 2025, projected $7.16B by 2032 at 22.4% CAGR — the "unbundled frontend" model created an entirely new integrator layer.** Shopify ships commerce primitives (catalog, cart, checkout APIs); Hydrogen is the opinionated React framework for consuming them; agencies and brands build the storefront. Value split: Shopify captures recurring SaaS fees on the backend; agencies capture project/retainer revenue. Failure mode: complexity creep — headless requires developer expertise, pricing out smaller merchants and fragmenting the support surface.
  - Source: https://www.swell.is/content/headless-commerce-trends-statistics | https://www.digitalapplied.com/blog/headless-commerce-trends-2025-shopify-plus

- **Low-code / no-code: 86.3% of professional developers never used a low-code platform in 2024; vendor lock-in is the primary exit barrier.** Low-code stalled on the same axis the dynamic-UI thesis must navigate — abstraction floors that are too high for power users and too low for non-technical users, missing both segments. Once users invest deeply, migration is near-impossible (proprietary schema, proprietary runtime). This creates an opening: a dynamic-UI layer built on open schemas (JSON configs exportable to standard formats) can position against lock-in as a differentiator while still capturing subscription revenue through runtime/hosting.
  - Source: https://thebrightbyte.com/playbook/expertise/why-low-code-became-a-trap-2025 | https://www.appbuilder.dev/blog/vendor-lock-in/

- **Airtable ($478M ARR, 57% YoY growth in 2025) and Notion ($500M ARR) as current living proof that primitives-as-platform scales to hundreds of millions without being a developer tool.** Both reached this scale by letting users reshape the same underlying primitives into radically different workflows — Airtable as CRM, PM tool, inventory system — from one relational-database primitive. The AI transition is already underway: Airtable added AI field types in 2025; Notion added autonomous scheduling agents. This signals "users configure with natural language / agents" is the next layer, not a distant possibility — the dynamic-interface thesis is on the right timing curve to catch this shift.
  - Source: https://sacra.com/c/notion/ | https://tech-insider.org/airtable-vs-notion-2026/

## Sources
1. https://colorlib.com/wp/wordpress-statistics/ — WordPress plugin market scale, dominant players
2. https://zetamatic.com/blog/2025/01/how-much-revenue-does-wordpress-generate/ — WordPress ecosystem $2.4B plugin market, WooCommerce revenue
3. https://foundationinc.co/lab/salesforce-21b-b2b-ecosystem/ — Salesforce AppExchange ecosystem multiplier, ISV value capture
4. https://www.salesforce.com/news/press-releases/2019/10/25/new-research-finds-the-salesforce-economy-will-create-more-than-1-trillion-in-new-business-revenues-and-4-2-million-jobs-between-2019-and-2024/ — $5.80 ecosystem multiplier, IDC research
5. https://www.notboring.co/p/excel-never-dies — Excel 750M users, GUI-first strategy, incremental recalculation, end-user programming mechanics
6. https://screenrant.com/minecraft-marketplace-350-million-profit-modders/ — Minecraft Marketplace $500M+ creator earnings
7. https://oasisaiminecraft.com/statistics/minecraft-economic-marketplace-analytics/ — $146M Q1 2025 Minecraft Marketplace, 70/30 split
8. https://endsights.com/roblox-creator-economy — Roblox creator monetization mechanics, 30% creator share
9. https://www.sec.gov/Archives/edgar/data/0001315098/000131509824000163/rblx-20240801xexhibit991.htm — Roblox 2024 financial filings, creator payout figures
10. https://foundationinc.co/lab/notion-project-templates/ — Notion template creator revenues ($239K–$1M+)
11. https://sacra.com/c/notion/ — Notion $500M ARR (Sept 2025), AI agents rollout
12. https://www.notion.com/help/selling-on-marketplace — Notion Marketplace fee structure (10% + $0.40)
13. https://www.extensionradar.com/blog/how-to-monetize-chrome-extension — Chrome Web Store ecosystem, monetization fragmentation
14. https://ful.io/blog/5-chrome-extensions-with-the-highest-revenue-in-2024 — Top Chrome extension revenue figures (GMass, Speechify)
15. https://www.swell.is/content/headless-commerce-trends-statistics — Headless commerce market $1.74B to $7.16B
16. https://www.digitalapplied.com/blog/headless-commerce-trends-2025-shopify-plus — Shopify Hydrogen, headless primitives model and failure modes
17. https://thebrightbyte.com/playbook/expertise/why-low-code-became-a-trap-2025 — Low-code failure modes, developer adoption gap 2025/2026
18. https://www.appbuilder.dev/blog/vendor-lock-in/ — Vendor lock-in as primary low-code exit barrier
19. https://tech-insider.org/airtable-vs-notion-2026/ — Airtable $478M ARR (2025), AI field types; Notion AI agents
