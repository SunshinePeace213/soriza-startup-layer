# Funnel Board: Dynamic Software Interfaces (AI + Agentic Coding)
## Run: dynamic-software-interfaces-ai-coding-ag-01

### Funnel Summary
- **In:** 10 candidates
- **After Gate 0 (founder-market fit):** 6 advancing
- **After Gate 1 (hypothesis sharpening):** 6 advancing
- **After Gate 2 (disconfirmation):** 0 advancing
- **Shortlist (K=1):** 0 candidates

### Capacity & Selection
**K = 1** (target shortlist size)

Justification: Solo founder (Ringo Ma) with 15–25 hrs/week available, 1–2 month runway, and zero day-one team. Running 2 campaigns in parallel would split attention across idea validation and burn runway faster with less converged signal. K=1 enforces **depth over breadth**: one high-conviction campaign to validate before pivoting or scaling toward profitability.

---

## Candidate Status Table

| ID | Title | G0 | G1 | G2 | G3 | Status | Rank | Kill Reason | Coverage Gap |
|:---|:------|:---|:---|:---|:---|:-------|:-----|:------------|:------------|
| cand-freelance-crm-morphing-workspace | Freelance CRM That Morphs Into Each Contractor's Workflow View | ❌ 48 | — | — | — | killed | — | Capacity: 8–12 weeks build time vs 1–2 months runway | — |
| cand-student-notes-to-study-interface | Student Note-Taking App That Renders Course Material as the Study Mode Each Student Learns Best | ✅ 83 | ✅ 82 | ❌ 22 | — | killed | — | Strongest objection (Thiel, sev 82): no moat — RemNote, Quizlet+Coconote, Notion Agent already shipped the exact multi-view-on-one-data-source mechanism | ben-horowitz-perspective: execution/distribution is the binding constraint, not just desire |
| cand-ecommerce-ops-dashboard-per-role | E-Commerce Back-Office Where Each Team Member Gets Their Own AI-Generated Operations Dashboard | ✅ 86 | ✅ 72 | ❌ 22 | — | killed | — | Strongest objection (Thiel, sev 82): feature not company, zero-priced into platform — Shopify ships role-based views free (Saved Views + custom roles + Sidekick) | jeff-bezos-perspective: no clear, acute customer — pain premise unverified |
| cand-chatbot-platform-white-label-per-client-ui | White-Label Chatbot Platform Where Each Client's End-Users Self-Configure Their Chat Interface | ❌ 52 | — | — | — | killed | — | Capacity hard fail: B2B SaaS platform MVP requires 200–300 eng. hours over 8–12 weeks; founder's 80–160 hrs insufficient before runway expires | — |
| cand-legal-doc-review-interface-per-lawyer | Legal Document Review Tool Where Each Lawyer Renders the Case File in Their Own Preferred Layout | ✅ 55 | ✅ 68 | ❌ 24 | — | killed | — | Strongest objection (Musk, sev 82): core value (parse contract → checklist/calendar) is a prompt + commodity API (Claude $20 gets 80% of it); no non-substitution evidence | tom-eisenmann-perspective: regulated-adjacent, weak founder-market fit on GTM, building inside a feature the platform will ship by default |
| cand-startup-ops-primitive-solo-founder-dashboard | Solo-Founder Operations Primitive — One Shared Data Model, Infinite Personal Dashboard Configs | ✅ 79 | ✅ 75 | ❌ 22 | — | killed | — | Strongest objection (Thiel, sev 82): no moat — Notion shipped the exact NL-driven self-reshaping unified ops view (Dashboard Views Mar 2026; Workers DB-sync May 2026) | steve-jobs-perspective: textbook feature-not-product case |
| cand-hk-sme-accounting-interface-morphing | SME Accounting Back-Office Where Each Staff Role Sees Only the Financial View They Need | ✅ 72 | ✅ 72 | ❌ 16 | — | killed | — | Strongest objection (Thiel, sev 82): UI shim with no moat — Xero already ships per-user customisable widgets + QBO custom dashboards; adaptive UI collapsing the wedge | nassim-taleb-perspective: platform fragility/tail risk — founder builds on Anthropic stack while Anthropic itself ships the exact mechanism via MCP |
| cand-dev-tool-ui-sdk-malleable-saas-builders | SDK for SaaS Builders to Ship Per-User Malleable Interfaces Without Building the Plumbing | ✅ 83 | ✅ 75 | ❌ 22 | — | killed | — | Strongest objection (Thiel, sev 82): thin middleware, no moat — CopilotKit (owns AG-UI protocol, $27M raised) already shipped persisted-generative-UI/shared-state layer (May 2026) | steve-jobs-perspective: feature, not product — thin bolt-on subsumed by protocol owner's whole stack |
| cand-corp-trainer-lms-per-learner-interface | Corporate Training Platform Where Each Employee Self-Configures Their Learning Interface | ✅ 60 | ✅ 68 | ❌ 22 | — | killed | — | All three objections stand: core mechanism (15–25% dropout from interface disengagement) has NO source support; contradicted by evidence (dropout = relevance/time/length) | charlie-munger-perspective: regulated-adjacent, solo dev with 1–2 month runway cannot underwrite outcome-based completion guarantees |
| cand-hk-property-agent-deal-tracking-interface | Property Agent Deal Tracker Where Each Agent Renders Their Pipeline in Their Own Workflow View | ✅ 82 | ✅ 75 | ❌ 22 | — | killed | — | All three severity-72 objections stand: no exclusive portal data moat; no proven outcome-pricing unit economics (UNVERIFIED); no revealed demand — agents stay on free spreadsheets by choice | tom-eisenmann-perspective: false-start / no-validated-demand failure pattern; weak founder-market fit on GTM |

---

## Dispatch Notes

**Gate 0 Kills (Capacity Hard Fails):** 2 candidates
- **cand-freelance-crm-morphing-workspace** (48/100): 8–12-week timeline incompatible with 1–2-month runway at 15–25 hrs/week
- **cand-chatbot-platform-white-label-per-client-ui** (52/100): B2B SaaS platform MVP beyond founder's available engineering hours before runway expires

**Gate 1 Survivors → Gate 2:** 6 candidates advanced through sharpening with testable hypotheses. All were well-defined on WHO, HOW_OFTEN, HOW_SEVERE, and STATUS_QUO.

**Gate 2 Kills (Disconfirmation):** 6 candidates
- **cand-student-notes-to-study-interface** (22/100): Feature already shipped by RemNote, Quizlet+Coconote, Notion Agent with no defensible moat
- **cand-ecommerce-ops-dashboard-per-role** (22/100): Shopify's native Saved Views + custom roles + Sidekick eliminate the wedge; Retool free-to-5-users kills pricing
- **cand-legal-doc-review-interface-per-lawyer** (24/100): Contract parsing is a commodity LLM prompt; Microsoft Word Legal Agent ships to the buyer by default at $30/mo
- **cand-startup-ops-primitive-solo-founder-dashboard** (22/100): Notion's Dashboard Views (Mar 2026) + Workers DB-sync (May 2026) ship the exact product inside the ICP's existing tool
- **cand-hk-sme-accounting-interface-morphing** (16/100): Xero's per-user customisable widgets + QBO's custom dashboards; adaptive UI from Anthropic/JAX commoditizes the mechanism
- **cand-dev-tool-ui-sdk-malleable-saas-builders** (22/100): CopilotKit's Enterprise Intelligence Platform (May 2026) already shipped the persisted-generative-UI/shared-state layer
- **cand-corp-trainer-lms-per-learner-interface** (22/100): Core pain (interface disengagement as dropout cause) UNVERIFIED and contradicted by evidence; market consolidation (Workday–Sana $1.1B closed Nov 2025) ship the wedge natively
- **cand-hk-property-agent-deal-tracking-interface** (22/100): Commission-leakage premise (HKD 50–150k/yr) is single-source/unverified; portals own listing supply and can bundle tracker at zero CAC

**Shortlist (K=1):** Empty. No candidates cleared all gates. The dynamic-software-interfaces thesis ran into a consistent pattern: every idea targets a personalized-UI/multi-view-on-shared-data gap that has been **commoditized by platform incumbents or AI infrastructure owners** in the 12–18 months since thesis conception. The founder's technical strength in agentic coding remains high, but execution windows have narrowed from "build in 8 weeks" to "shipped by the platform owner in a product release 2–6 months ago."

---

## Thesis Reflection

The **dynamic-software-interfaces-ai-coding-ag** thesis was built on a legitimate insight: users have heterogeneous interaction preferences, and modern AI-driven UI generation (AG-UI) could let each user describe their preferred interface from shared data. However, the thesis underestimated:

1. **Incumbent velocity:** Notion, Shopify, Xero, QuickBooks, CopilotKit, and platform owners move faster than a solo bootstrapper. The "personalized UI as a feature" is now a commodity roadmap item, not a structural gap.
2. **Commoditization timing:** CopilotKit's AG-UI protocol, Claude's $20 API cost, Anthropic's MCP with generative-per-context UI, and Lovable's $400M ARR have all collapsed the "build a working UI agent from scratch" time to <1 week. The defensibility of that layer is gone.
3. **CAC + retention unknown:** None of these ideas had validated that users would pay a recurring fee for a feature that flows naturally from the platform's own roadmap. SOM estimates collapsed when realistic conversion rates (<2%) were applied.

**Recommendation:** Pause the dynamic-software-interfaces thesis. Pivot toward either (a) a **domain-specific AI coding tool** where the founder's agentic-coding skill + domain knowledge (fintech, e-commerce, chatbots) creates defensibility, or (b) a **high-conviction indie SaaS product** in the founder's existing circle (e.g., optimizing his own workflows as the first user). The founder's unfair advantage is agentic build velocity, not UI morphing.
