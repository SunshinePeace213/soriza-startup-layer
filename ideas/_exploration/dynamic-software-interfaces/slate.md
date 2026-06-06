---
stage: generate-ideas
thesis: "Dynamic / Malleable Software Interfaces — companies ship primitives, users (via AI coding agents) reshape the final interface"
recommended_pick: "chat-interface-layer"
generated: 10
tracks: { blind-wide: 7, reachable-workflow: 3 }
---

# Idea Slate — Dynamic Software Interfaces

Grounding: `grounding.md` (+ `research/`). 10 thin seeds across two labelled tracks — a **blind-wide** track
(driven only by the thesis + real demand, founder-blind, the anti-bias guard) and a **reachable-workflow**
track (grounded in workflows the founder can actually get inside). The recommendation is **advisory — you
pick.**

## Recommendation (advisory — you decide)

**Take next: #1 — Malleable Chat/Agent Interface Layer for Multi-Client Chatbot Agencies** (`chat-interface-layer`).

This is the one seed where you can *find the customer first and already understand their workflow better
than they can articulate it* — the FDE doctrine's whole game. You built a **multi-client Chatbot Management
System** in production; the per-client "every client wants the widget + admin dashboard to look and behave
differently, and we hand-customize each one" cost is a workflow you've personally lived. **Demand** is
adjacent-proven (Retool $138M on "incumbents won't customize fast enough"; userscript/Tampermonkey 10M; the
Arc Boosts grave shows per-surface personalization demand is real and now *unserved*), and the thesis is
sharpest on conversational/agent surfaces — generative UI + MCP "Apps" (official Jan 2026) make the chat
surface itself reshapeable per client/end-user. **Moat:** workflow depth + owning the per-client config/
schema layer (the toll-road pattern — Salesforce earns $1 per $5.80 of partner revenue by owning the
locked-in layer). **Distribution — your #1 documented risk:** a *nameable, reachable* niche (chatbot
agencies + SMBs in HK / Greater China), plus a trilingual edge English-first tools don't have — **not**
"everyone." **AI-buildable solo:** it sits dead-center on your Next.js/Node/MySQL + LLM-integration + agentic
stack, so the cheapest PoC is days, not months.

The honest catch (test it *before* building): your GTM is weak and you'd need to re-open agency/SMB
relationships. **Whether you can reach 5 chatbot-agency operators in two weeks is the riskiest assumption —
test that first, not the build.** If you can't, the build is wasted motion.

Runner-up: **#5 — Curated AI-Maintained Userscript Marketplace** — the strongest *directly-cited* standalone
demand (Tampermonkey 10M+, Arc Boosts proved-then-orphaned), and AI auto-maintenance against changing DOMs
is a genuine "why now" unlock. Held back as the pick by two-sided cold-start + the trust/security of running
arbitrary code, and no founder workflow depth. If you'd rather a pure distribution-first *blind* pick:
**#4 — ADHD/Autistic-Tuned PM Interface** (acute niche, proven willingness-to-pay, dense reachable
communities).

> The other 9 stay below as a dormant backlog. Re-run `/sharpen-hypothesis` on any of them later — no ledger,
> no resurrect machinery.

## Cards

### 1. Malleable Chat/Agent Interface Layer for Multi-Client Chatbot Agencies  ·  track: `reachable-workflow`  ·  idea_type: `ai-agent`  ·  slug: `chat-interface-layer`
- **Problem:** Chatbot/agent agencies and CMS operators ship one canonical chat widget + admin dashboard and then **hand-customize per client** (branding, flows, the fields an agent sees, the way a conversation renders) — a recurring, manual, margin-eating cost. There's no layer that ships chat/agent *primitives* and lets each client (or the operator) reshape the interface to their workflow, with the modification persisted, shareable, and permissioned.
- **Who:** Multi-client chatbot/automation agencies and SMBs running customer-facing bots — the exact operators behind a multi-client Chatbot Management System. Reachable in HK / Greater China / English markets.
- **Why now:** Generative UI is tractable (Vercel AI SDK 20M dl/mo; users preferred AI-gen UI 83% of the time) and **MCP "Apps" (official Jan 2026)** make tools return interactive UI inside the conversation — the chat surface itself becomes per-context reshapeable. Build-cost collapse (6–13×) makes a bespoke per-client interface finally viable.
- **Demand signal:** Adjacent-proven — Retool $138M ARR on "incumbents won't customize fast enough"; 35% of enterprises already replaced a SaaS with a custom build; Tampermonkey 10M+; Arc Boosts proved per-surface personalization demand then died (now unserved). (Chatbot-agency-specific demand is inferred from founder's lived workflow — to be tested in discovery.)
- **Moat / distribution read:** Workflow depth (founder has earned, non-obvious knowledge of exactly this) + owning the per-client config/schema layer = toll-road switching cost. Distribution: a nameable niche + trilingual channel English-first tools ignore. ⚠ Distribution is the load-bearing risk — *test reachability before building*.
- **Recommend?:** **PICK.** Best intersection of workflow depth + AI-buildability + a reachable, ownable niche — and on-thesis where the thesis is sharpest (agent surfaces).

### 2. Malleable EMR Interface Layer for Clinicians  ·  track: `blind-wide`  ·  idea_type: `regulated-adjacent`
- **Problem:** EMRs (Epic/Cerner) force one rigid, cluttered interface on every clinician regardless of specialty/role — a documented driver of burnout. Vendors won't fix it: they sell an IT-owned canonical interface.
- **Who:** Individual clinicians (MDs/NPs/RNs) inside health systems, already hacking SmartPhrases/macros/layout workarounds to survive a shift.
- **Why now:** AI drops the cost of per-user interface configs to ~zero; the Ink & Switch unsolved stack (persistence/sharing/auth) is now tractable; clinician burnout is a policy-level crisis accelerating procurement of cognitive-load relievers.
- **Demand signal:** EMR rigidity named as a burnout driver (HN threads); existing macro/SmartPhrase workaround economies inside health systems.
- **Moat / distribution read:** Deep if you embed in one specialty's workflow; durable via clinical trust. ⚠ Heavy regulation (HIPAA, hospital procurement, integration with locked EMRs) — collides with founder's stated avoid-heavy-regulation + bootstrap/runway constraints. Distribution into health systems is brutal for a solo founder.
- **Recommend?:** No for this founder (regulatory + procurement + access barriers), but a real opportunity for a team with clinical access.

### 3. Shadow-IT Legitimizer: Primitive-First Internal-Tool Builder for Ops Teams  ·  track: `blind-wide`  ·  idea_type: `default`
- **Problem:** 60% of custom internal tools in 2025 were built outside IT — brittle, unshared, discarded when the builder leaves. No product turns shadow-IT output into a persistent, team-shareable, IT-blessable interface layer.
- **Who:** Non-engineer ops/RevOps/finance builders at 10–200-person firms, and the small IT teams who inherit their tools.
- **Why now:** Shadow IT 15%→60% (2022→2025); AI lets a non-engineer describe and get a working exportable interface config, closing the last skill gap.
- **Demand signal:** Retool $138M ARR; 35% already replaced a SaaS, 78% plan more in 2026; shadow-IT at scale.
- **Moat / distribution read:** ⚠ **"What's your moat in the AI era?"** — head-on with Retool/Airtable/Notion (well-funded, entrenched), and a horizontal internal-tool builder is exactly the undifferentiated-platform trap unless it picks a sharp niche wedge. B2B distribution is hard for a solo bootstrapper with weak GTM.
- **Recommend?:** No as a horizontal play; only viable as a narrow vertical wedge. Demand is real but the category is a knife fight.

### 4. ADHD/Autistic-Tuned Task & Project-Management Interface  ·  track: `blind-wide`  ·  idea_type: `default`
- **Problem:** Neurotypical-designed PM tools (Notion/Linear/Asana) assume a task-hierarchy, notification cadence, and visual density that ADHD/autistic users bounce off — driving constant tool-switching and elaborate personal workarounds.
- **Who:** ADHD/autistic knowledge workers, students, indie devs/writers already spending on Notion templates, Obsidian plugins, or ADHD coaching to compensate.
- **Why now:** Obsidian 120M+ plugin downloads + Notion $1M-template-sellers prove people invest to reshape generic tools; AI removes the technical barrier to a *personal* interface config.
- **Demand signal:** Acute niche with proven willingness-to-pay (Leantime); dense, reachable communities (Reddit/Discord/newsletters) — directly answers the distribution warning.
- **Moat / distribution read:** Moat = depth of fit for one cognition + community trust; distribution = dense niche channels you can post into (ownable-ish). Risk: competes with users' own Obsidian/Notion setups; "fit" is hard to defend long-term.
- **Recommend?:** Strong *distribution-first blind pick* — the best alternative if you want a niche with already-acted-on demand and reachable channels but outside your domain.

### 5. Curated, AI-Maintained Userscript Marketplace for Existing Web Apps  ·  track: `blind-wide`  ·  idea_type: `marketplace`
- **Problem:** 10M+ people use Tampermonkey/Greasy Fork to reshape Gmail/Jira/Notion/Linear, but scripts go stale on every app update, distribution is fragmented, and running arbitrary code is a trust/security barrier. No curated, auto-maintained, trustworthy marketplace exists.
- **Who:** Power users of web SaaS (PMs, devs, ops analysts) who already use or hunt for userscripts/extensions to fix specific interface annoyances in tools they can't replace.
- **Why now:** AI can regenerate + retest a script against a changed DOM in minutes (the maintenance problem, finally solvable); Arc Boosts proved the demand and left it orphaned.
- **Demand signal:** Tampermonkey 10M+, Greasy Fork install counts in the hundreds of thousands per script; Arc Boosts proved-then-killed.
- **Moat / distribution read:** Moat = auto-maintenance engine + a curated/verified (certified) tier that holds margin where open marketplaces commoditize; channel = power-user communities (postable, not owned). ⚠ Two-sided cold-start + arbitrary-code trust/security are the real risks; horizontal "any web app" scope risks the Arc Boosts grave — needs an anchor app.
- **Recommend?:** **Runner-up.** Strongest directly-cited standalone demand; held back by cold-start + trust + no founder workflow depth.

### 6. Living, Adaptive Configuration Economy for Notion & Obsidian Power Users  ·  track: `blind-wide`  ·  idea_type: `marketplace`
- **Problem:** Today's Notion templates / Obsidian setups are *static* — a buyer gets a frozen export that fit the seller's workflow months ago and never adapts to the buyer's data, habits, or team. No way to ship a *living*, AI-adaptive configuration.
- **Who:** Notion/Obsidian power users who already buy templates/plugins (solopreneurs, students, researchers) + the template sellers who want recurring revenue over one-time exports.
- **Why now:** Geoffrey Litt (Malleable Software co-author) now at Notion signals the platform is moving toward user-malleable interfaces; runtime-gen UI (Thesys/Tambo/AI SDK) makes adaptive views from a shared schema tractable; Claude Artifacts normalized forking/personalizing an AI app.
- **Demand signal:** Notion templates $1M/yr single sellers; Obsidian 120M+ plugin downloads — a paying configuration economy already exists.
- **Moat / distribution read:** Moat = own the adaptive-config schema + take a cut (toll road, exact Notion-template analogue); sellers do vertical GTM for free. Risk: **platform-dependency** — Notion itself (with Litt) may build this; you'd be building on a platform that could absorb you.
- **Recommend?:** Maybe — real economy and clear monetization, but high platform/absorption risk.

### 7. MCP Interactive-UI Server Runtime for AI Assistants  ·  track: `blind-wide`  ·  idea_type: `ai-agent`
- **Problem:** MCP "Apps" lets tools return interactive UI in the conversation, but there's no standardized runtime to publish, version, persist, and permission a set of interactive MCP UI components. Every team rebuilds this from scratch; results are ephemeral and unmonitored.
- **Who:** Product/eng teams at early-adopter SaaS + internal-tooling shops already building/evaluating MCP servers.
- **Why now:** MCP Apps official Jan 2026, 97M SDK dl/mo, 10k+ servers; the Ink & Switch unsolved stack (persistence/sharing/sandbox/auth) maps exactly onto MCP-UI needs.
- **Demand signal:** MCP adoption curve; absence of any funded startup closing the infra gap.
- **Moat / distribution read:** ⚠ **"What's your moat in the AI era?"** — dev-infra that Anthropic/Vercel could ship natively; selling infra to devs is a hard, credibility-gated motion for a solo founder with weak GTM. Real risk of being a feature, not a company.
- **Recommend?:** No for this founder (infra-platform + dev-GTM mismatch); a fast-mover-with-distribution play.

### 8. Portable, Open-Schema Interface-Config Layer for Low-Code / Citizen Devs  ·  track: `blind-wide`  ·  idea_type: `default`
- **Problem:** 56M Power Platform users + low-code citizen devs are locked into proprietary schemas they can't export, version, or compose; tools die on pricing changes or a departing builder. No portable, open-schema config layer that travels with the user.
- **Who:** Citizen devs / ops-technical pros (RevOps, finance, ops) on Power Platform/Retool/Airtable/Glide burned by lock-in.
- **Why now:** AI can translate between platform schemas, making "export and reimport elsewhere" mechanically feasible for the first time; lock-in is the named low-code failure mode.
- **Demand signal:** Power Platform 56M MAU; Retool $138M / Airtable $478M ARR confirm willingness-to-pay in the segment.
- **Moat / distribution read:** ⚠ A portability *feature*, not obviously a company — incumbents have every incentive to block export; hard to monetize a "freedom layer." Distribution unclear.
- **Recommend?:** No — thinnest moat on the slate; a feature dressed as a startup.

### 9. Trilingual Greater-China SMB Interface / Internal-Tool Builder  ·  track: `reachable-workflow`  ·  idea_type: `default`
- **Problem:** HK / Greater-China SMBs are underserved by English-first dynamic-UI / low-code tools — language, local payment, and WeChat/WhatsApp-centric workflows don't fit. Owners hack spreadsheets and messaging apps instead of getting an interface over their own data.
- **Who:** Non-technical Cantonese/Mandarin-speaking SMB owners and ops staff in HK / Greater China.
- **Why now:** Build-cost collapse + AI lets an owner describe, *in their language*, the tool/interface they want over existing data; shadow-IT/low-code behaviour is global (56M Power Platform) but localized tooling is thin.
- **Demand signal:** Global shadow-IT/low-code demand (60%, 56M MAU) as a proxy; local-language gap is real but **demand among non-technical SMBs may be the indifferent-median trap** (the counter-signal) — to be tested.
- **Moat / distribution read:** Distribution edge = **language + locality + on-the-ground presence** — a genuinely *ownable* channel English-first tools can't easily contest (the founder's clearest unfair channel). ⚠ But horizontal builder = cold-start + support burden, and moat beyond language is thin.
- **Recommend?:** Maybe — strongest *ownable distribution* on the slate, but the median-SMB demand risk and horizontal scope are real. Best if narrowed to one vertical/one workflow.

### 10. Adaptive Storefront / Post-Purchase Interface Layer for Small Consumer & Cosmetics Sellers  ·  track: `reachable-workflow`  ·  idea_type: `e-commerce`
- **Problem:** Small independent consumer/cosmetics sellers want their storefront + post-purchase experience reshaped per campaign or customer-segment without a developer — today they're stuck with rigid themes or expensive agencies.
- **Who:** Small Shopify/independent cosmetics & consumer-goods sellers (the Soriza-adjacent niche the founder built for).
- **Why now:** Headless commerce growing ($1.74B→$7.16B by 2032); generative UI makes per-campaign/per-segment storefront variants tractable; the founder has an e-commerce build (Soriza) and the intended brand.
- **Demand signal:** Headless-commerce growth + the Shopify theme/app economy; sellers already pay agencies for storefront customization.
- **Moat / distribution read:** ⚠ **"What's your moat in the AI era?"** — Shopify themes/apps + Figma Make + a crowded storefront-customization space; founder's weak GTM + thin differentiation make this hard. Some founder affinity (Soriza) but no clear ownable channel.
- **Recommend?:** No as framed — crowded, thin moat, weak distribution. Listed for completeness given founder's e-commerce affinity; would need a sharp wedge (e.g., one vertical's post-purchase workflow).
