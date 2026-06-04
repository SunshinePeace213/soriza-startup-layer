# Market Research — hk-sme-accounting-interface-morphing

> Desk research synthesizing public evidence (competitor sites, reviews, market data, trend
> signals) — not customer validation. A favorable read means the public evidence supports the
> idea; it is not proof customers will pay. This doc bundles all four workstreams (W1 landscape,
> W2 review-synthesis, W3 sizing, W4 trends) because the sweep was delegated as one pass.
> Load-bearing claims in W2/W3 are tagged [verified ≥2 src] or [single-source].

**Idea in one line:** per-user, admin-free interface "morphing" (rearrange dashboards, hide
columns, surface job-critical views) layered on Xero/QuickBooks for HK/Greater-China SME finance
teams of 2–8, sold against the pain of admin-locked role views.

---

## W1 — Competitive Landscape

### Direct (same job, same buyer)
| Player | What they do | Who they serve | Pricing (HK) | Where they fall short for this segment |
|---|---|---|---|---|
| **Xero** | Cloud accounting; most-recommended by HK accounting firms; HSBC/Hang Seng/StanChart bank feeds; unlimited users all plans | HK SMEs via accountant channel | ~HK$155 Starter → ~HK$400 Premium /mo (USD-billed: $29/$50/$75) | No per-user layout customization; roles are admin-set (Admin/Standard/Advisor/Read-only), can't split AP/AR; "limited customization" cited 142× in G2 reviews; reports formatted AU/UK not HKFRS |
| **QuickBooks Online** | World's largest SME accounting platform by share; active in HK | HK SMEs, freelancers | ~HK$152 → HK$259 /mo | New interface widely hated ("can't hide menu items I don't use"; "5 clicks where it took 1"); partial Traditional-Chinese support; US Trustpilot 1.1★ |
| **Giga Accounting (凌峰會計)** | Locally-built; bilingual EN/TC/SC UI + reports, HKFRS statements, MPF/IR56 hooks, cheque printing, multi-company | HK SMEs wanting full Chinese + local compliance | One-off desktop licence or cloud (10GB) | Desktop-era UX; not a per-user-morphing play, but owns the localization wedge this idea would need |
| **Info-Tech / ABSS / Flexaccount** | Local HK packages (accounting + payroll + HRMS, HKFRS, MPF) | HK SMEs, compliance-first | Info-Tech ~HK$1,800/yr unlimited users | Older interfaces; customization not the selling point — but they own HK install base |

### Indirect (different approach to the same job)
| Player | Approach to the same job | Why a customer settles for it | Where it fails |
|---|---|---|---|
| **Excel / CSV export** | Export from Xero/QBO, hide columns + rearrange in a spreadsheet | Free, already known, total layout control | Manual, error-prone, breaks audit trail — this is the exact workaround the hypothesis names |
| **Xero/QBO native role permissions** | Admin sets Standard vs Read-only vs Advisor | Built-in, no extra cost | Permission ≠ layout; can't surface job-critical *views*, only gate access |
| **Fathom / Spotlight Reporting (Xero add-ons)** | Bolt-on dashboards/KPI/reporting layers | Richer reporting than native | From ~US$44/mo per company — priced/positioned for advisors & reporting, not per-clerk layout morphing |

### Potential acquirers
- **Xero / Intuit** — would buy or (more likely) build a layout-personalization feature to close a churn gap; for a solo bootstrapper this means a feature, not a company, gets acquired — i.e. acqui-hire at best, more likely cloned.
- **Local HK players (Giga, Info-Tech)** — could buy a modern UX layer to refresh dated products, but these are small firms with little M&A budget.

### Adjacent (could move in)
- **Xero/QBO themselves via their app marketplaces + AI roadmap** — they already expose the API surface; "adaptive UI" is on every 2026 SaaS roadmap (see W4). Fast — quarters, not years.
- **Mid-market suites (Sage Intacct, NetSuite, DualEntry)** — already ship role-based, drag-and-drop, fully-customizable dashboards upmarket. The capability exists; it just hasn't been pushed down into the Xero/QBO SME price tier. They could move down-market with a lite SKU.

---

## W2 — Review Synthesis

### Top unresolved complaints (ranked)
1. **Interface is cluttered / overwhelming / "not made for non-accountants"** — high frequency, both platforms; QBO "all of the information might be overwhelming… added clutter," "not really made with non-accountants in mind"; Xero "clunky," "outdated." sources [2][6][8][9] — **[verified ≥2 src]**
2. **Limited customization / forced to use external tools (Excel) as a workaround** — Xero "limited customization" = 142 review mentions on G2; "requires workarounds using external tools"; users export to Excel to hide columns. sources [1][3][6] — **[verified ≥2 src]**
3. **Forced interface changes with no opt-out / can't hide menu items you don't use** — QBO "Classic View let me hide menu items I don't use, now I can't," "can rearrange order but that's about it," no revert option. sources [2][7] — **[verified ≥2 src]**
4. **Partial/poor Traditional-Chinese & HKFRS support (HK-specific)** — QBO TC "partial rather than first-class"; Xero "limited TC support, reports formatted AU/UK not HKFRS"; bilingual invoicing friction at audit. sources [5][10][13] — **[verified ≥2 src]**
5. **Granular per-role permissions weak (can't split AP/AR; clerk sees outgoings)** — Xero "difficult to split permissions for accounts payable and accounts receivable." source [4] — **[single-source]** (community/guide, not corroborated)
6. **The *specific* "let each user customize their own layout / hide columns in-app" request** — exists but demand is THIN: the canonical Xero feature request has only **20 votes**, submitted 2023, no Xero response. sources [11] — **[single-source / weak demand signal]**

### Does this idea address them?
- #1 cluttered/overwhelming → **Partially.** Per-user morphing could declutter a clerk's view — but the deeper complaint is "designed for accountants," which is product philosophy, not layout.
- #2 limited customization / Excel workaround → **Yes (direct).** This is the closest fit; the export-to-Excel-to-hide-columns workaround is exactly the named status-quo.
- #3 forced changes / can't hide items → **Yes (direct).** Per-user hide/rearrange addresses this head-on.
- #4 TC/HKFRS localization → **No.** The hypothesis is layout morphing, not language/compliance — yet this is one of the best-attested HK-specific pains.
- #5 granular permissions → **No.** Hypothesis explicitly scopes *out* role-permission redesign; this complaint is about permissions, not layout.
- #6 in-app per-user layout → **Yes** — but only 20 people asked, so it's a real-but-tiny demand signal.

### Problem–Solution-Fit signal
**weak.** The idea cleanly addresses complaints #2/#3 (customization & forced-change friction), which are genuinely unresolved — but the *intensity* of demand for the specific "per-user layout morphing" mechanism is thin (20-vote feature request), and the loudest HK-specific pains (#1 "not for non-accountants," #4 TC/HKFRS) are not what this idea solves. The strongest-attested pain is localization, not interface morphing.

---

## W3 — Market Sizing + Buyer Map

### TAM / SAM / SOM
| Layer | Range | Key assumptions (tagged with source) |
|---|---|---|
| **TAM** (HK SMEs on cloud accounting) | ~HK$300M–600M/yr software spend | ~360,000 HK SMEs, >98% of enterprises [12, SUCCESS/TID] **[verified ≥2 src vs C&SD]**; assume 30–50% on paid cloud accounting × ~HK$2,000–4,000/yr each |
| **SAM** (2–8-person finance *teams* on Xero/QBO, HK + Greater China English-serviceable) | **Small.** ~10,000–30,000 HK firms | ~90% of HK SMEs have <10 employees total [census, verified] — so a *2–8-person finance team* implies a firm of ~20+ staff, a minority of the base. Xero/QBO together a slice of the cloud segment |
| **SOM** (realistic 3-yr reachable, bootstrapped solo) | **~HK$0.3M–1.5M ARR** (≈300–1,500 paying seats/orgs) | reachable orgs × price × conversion, below |

### Bottom-up SOM
- **Reachable orgs:** a solo HK bootstrapper with weak GTM realistically reaches low-thousands of Xero/QBO HK orgs via app-marketplace listing + accountant referrals over 3 yrs. Take ~1,000–3,000 as the reachable funnel.
- **Price:** anchor to existing Xero add-ons — Fathom from ~US$44/mo/company [Fathom pricing]. A per-user *layout* utility commands far less than a reporting suite; realistic ~US$5–15/mo per org. Call it ~HK$50–120/mo.
- **Conversion:** marketplace utility apps convert in the low single-digit %; 10–30% of a *referred* warm funnel at best. Blended ~10–20% of reachable.
- **Result:** ~150–600 paying orgs × ~HK$600–1,400/yr ≈ **HK$0.1M–0.8M ARR**, optimistic case ~HK$1.5M. Order-of-magnitude only.

### Buyer landscape
- **Budget holder:** the SME **owner** (pays the Xero/QBO subscription and any add-ons).
- **Influencer:** the **clerk/accountant** who feels the daily friction — but they don't hold budget.
- **Decider:** owner, often on the **external accountant's** recommendation (Xero adoption is accountant-channel-driven).
- **Same person?** No — pain-feeler ≠ payer. The clerk hurts; the owner pays; the accountant gates. A solo founder weak on GTM must sell to the owner *through* the accountant channel, the hardest path.

### Market maturity
**Mature/consolidating** core accounting (Xero/QBO/Intuit are entrenched, accountant network effects, Xero 70%+ in NZ) — but the **personalization/adaptive-UI layer is expanding** (2026 = "year of agentic AI" per Deloitte; adaptive UX "becoming the default"). Classifying signal: incumbents and mid-market suites are actively shipping the exact capability (role-based customizable dashboards already in Sage Intacct/NetSuite/DualEntry).

### Sensitivity
The answer hinges most on **whether per-user layout morphing is a paid wedge or a free feature incumbents ship.** If Xero/QBO add layout personalization to their AI roadmap (highly plausible — W4), SOM → near zero. Even holding that aside, the SAM is structurally small because ~90% of HK SMEs are <10 staff total, so the "2–8-person finance team" sub-segment is a minority — if that's wrong by 2×, SOM still tops out low-single-digit-million HK$.

---

## W4 — Trends

### Three trends
| Trend | Type | Tailwind / Headwind | Mechanism for THIS idea | Source |
|---|---|---|---|---|
| Adaptive/personalized UI becoming the SaaS default; "interface adapts to the individual user… based on responsibilities and prior actions" | tech | **Headwind (net)** | Validates the concept — but means Xero/QBO will build per-user adaptive dashboards natively, collapsing the wedge. A standalone morphing layer competes with the platform's own roadmap. | [14] |
| 2026 = "year of agentic AI"; agents "dynamically adapt workflows," surface insights | tech | **Mixed** | Could reframe the idea as an *agent* that arranges each user's view — but incumbents (BlackLine, Intuit) are best-placed to ship this on their own data. | [14, Deloitte] |
| HK eMPF mandatory by end-2025 / 2026; HKFRS + bilingual compliance pressure; e-invoicing still *voluntary* (no B2B mandate) | reg | **Tailwind for localization, neutral for morphing** | Regulatory push favors HK-localized tools (Giga, Flexaccount) — strengthens the *localization* pivot, not the interface-morphing thesis. No e-invoicing mandate = no forced digitalization wave to ride. | [5][10] |

### Community language (exact phrases)
- "all of the information might be overwhelming… the added clutter" (QBO user) — QuickBooks Community
- "not really made with non-accountants in mind, but it's sold as user friendly" — coachingwithkaylee / QBO reviews
- "the old Classic View let me hide menu items I don't use, now I can't" — QuickBooks Community
- "I currently export to excel and hide the 'calculation' columns" — Xero Product Ideas
- "limited customization… requires workarounds using external tools" — G2 Xero reviews
- "navigate a global helpdesk queue" / wanting "someone who understands Hong Kong's accounting environment" — HK buyer guides

### Analogous markets
| Market | Similar problem | What worked | What didn't | Transplant |
|---|---|---|---|---|
| Mid-market ERP (Sage Intacct, NetSuite, DualEntry) | Role-specific dashboard needs | Native role-based drag-and-drop customizable dashboards | Stayed upmarket; SME tier never got it | Proves the feature is *expected* upmarket — but proves it's a *feature*, not a standalone product |
| Browser extensions / "skins" over SaaS (e.g. Gmail/Salesforce UI tweakers) | Users want to reshape an app they don't control | Niche power-user utilities exist | Platform UI changes break them; thin, low-WTP businesses; acquisition or obsolescence | Cautionary: layering on a platform you don't own = permanent platform risk + low pricing power |
| Xero/QBO app marketplaces (Fathom, Spotlight) | Add capability the core lacks | Distribution via marketplace, accountant channel | Most apps are reporting/forecasting (high value); pure-utility apps under-monetize | Marketplace is the realistic GTM, but a layout utility sits at the low-WTP end |

---

## Load-bearing claims & verification
- **~360,000 HK SMEs, >98% of enterprises** → SUCCESS/TID [12] + corroborated by C&SD/census references [15] — **verified ≥2 src.**
- **~90% of HK SMEs have <10 employees** → census/LegCo statistical highlights — **verified (single primary lineage, multiple periods);** treat the *implication* (2–8-person finance team is a minority sub-segment) as the load-bearing inference.
- **Xero "limited customization" = 142 G2 mentions; "not for non-accountants" (QBO)** → G2 [1][6] + QBO community/NerdWallet [2][8][9] — **verified ≥2 src.**
- **QBO US Trustpilot 1.1★** → noted on coachingwithkaylee [8] and Trustpilot domain — **verified ≥2 src**, but note the UK QBO domain is 4.5★ over 16k reviews; the 1.1★ is the US .com domain — cite carefully, NOT "QuickBooks is 1.1★" globally.
- **The specific per-user layout / hide-column feature request = only 20 votes, no Xero response** → Xero Product Ideas [11] — **single-source; treat as weak demand signal, the key disconfirming fact for the wedge.**
- **Mid-market tools already ship role-based customizable dashboards** → NetSuite [17] / Sage Intacct / DualEntry [17] — **verified ≥2 src.**
- **Adaptive UI becoming SaaS default / 2026 agentic-AI** → GitNexa/Millipixels/Deloitte [14] — **verified ≥2 src** (analyst commentary, directional not numeric).
- **Fathom add-on from ~US$44/mo** → Fathom/Capterra [16] — **verified ≥2 src** (used only as a price *ceiling* anchor; a layout utility prices well below).

---

## Synthesis — Market Read

**reposition (leaning reconsider).** The friction the hypothesis names is real and unresolved
(complaints #2 limited-customization and #3 can't-hide-items are well-attested), but three things
undercut the *specific* interface-morphing wedge: (1) demand for the exact mechanism is thin — the
canonical Xero feature request has 20 votes; (2) the capability already exists upmarket and
adaptive UI is on every incumbent's 2026 roadmap, so this is a feature Xero/QBO will likely ship
free, not a defensible product; (3) the SAM is structurally small (~90% of HK SMEs are <10 staff,
so a 2–8-person *finance team* is a minority) and you'd build on a platform you don't own, with
the payer (owner) separated from the pain-feeler (clerk) and gated by the accountant channel — the
worst GTM shape for a solo bootstrapper weak on distribution.

**Positioning & Wedge (if pursued):** own the "Excel-export-to-hide-columns workaround" pain —
the one complaint this idea fits cleanly. But the better-attested HK pain is **Traditional-Chinese
/ HKFRS localization** (Giga, Flexaccount already win here), which the current hypothesis does not
address — that is the stronger market signal.

**Strongest Threat:** Xero (and Intuit) themselves — they hold the data, the accountant channel,
and an explicit 2026 adaptive-UI roadmap; any traction invites a free native feature that
collapses the wedge. Survival bar: you must be either (a) impossible-to-clone via something the
platform won't build, or (b) addressing a pain the platform structurally won't (e.g. HK
localization), and reach the owner-buyer without depending on the accountant channel.

**Sizing Reality:** SOM ~HK$0.1M–0.8M ARR realistic (≤HK$1.5M optimistic); price ~US$5–15/mo
per org; budget held by the owner, pain felt by the clerk, gated by the accountant — not the same
person. Marginal at the founder's bootstrap scale, and fragile to platform risk.

**Timing:** **Net headwind.** Adaptive UI is becoming the default — validating but commoditizing —
and there's no HK regulatory forcing function for interface tools (eMPF/HKFRS push favors
*localization* tools, not morphing).

**Problem–Solution-Fit:** **weak.**

**Hypothesis Updates Flagged (route to /sharpen-hypothesis — do NOT edit hypothesis.md):**
- The loud, well-attested HK pain is **Traditional-Chinese / HKFRS localization**, not interface
  morphing. Consider repositioning toward localization if staying in HK SME accounting.
- Demand for the *specific* per-user layout mechanism is thin (20-vote feature request) — the
  hypothesis overstates "1–2 hrs/week lost to navigation friction"; that figure is unsourced and
  should be treated as a disconfirmation target for customer discovery.
- The "2–8-person finance team" segment is structurally small (~90% of HK SMEs <10 total staff) —
  re-examine whether the target sub-segment is large enough at the founder's scale.
- "Layered on a platform you don't own" is a permanent platform-risk and pricing-power constraint —
  surface it explicitly in the hypothesis's defensibility section.

---

## Sources
1. https://blog.coupler.io/xero-reports/ — Xero report/dashboard customization limits
2. https://quickbooks.intuit.com/learn-support/en-uk/account-management/new-interface-is-terrible-and-not-an-improvement-stop-messing/00/1561013 — QBO can't-hide-menu-items complaint
3. https://productideas.xero.com/forums/939198-for-small-businesses/suggestions/44960344 — Xero dashboard graph/report customization request
4. https://jacrox.co/user-permissions-xero/ — Xero AP/AR permission split limitation (single-source)
5. https://www.xero.com/hk/ + https://aspireapp.com/hk/blog/xero-tutorial — Xero HK features, bank feeds, TC limitation
6. https://www.g2.com/products/xero/reviews — Xero "limited customization" 142 mentions, UI clunky
7. https://quickbooks.intuit.com/learn-support/en-us/other-questions/how-do-i-change-the-dashboard-to-the-old-style-before-this/00/1579656 — QBO no-revert / can't hide items
8. https://www.coachingwithkaylee.com/is-quickbooks-online-really-that-bad/ — QBO "not for non-accountants," Trustpilot 1.1★ (US)
9. https://www.nerdwallet.com/business/software/reviews/quickbooks-online — QBO overwhelming/clutter for new users
10. https://linfungaccounting.com/en/best-accounting-software-in-hong-kong-for-smes-2026 — TC/HKFRS localization pain; Giga/Flexaccount
11. https://productideas.xero.com/forums/939198-for-small-businesses/suggestions/46006927-custom-report-ability-to-hide-unhide-columns — hide-column request, 20 votes, no Xero response (key disconfirming signal)
12. https://www.success.tid.gov.hk/english/aboutus/what_are_sme.html — ~360,000 HK SMEs, >98% of enterprises (Dec 2025)
13. https://statrys.com/hk/guides/accounting-standards/best-accounting-software — HK accounting software comparison, local options, pricing
14. https://www.gitnexa.com/blogs/ui-ux-trends-in-saas-products + https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/saas-ai-agents.html — adaptive UI default / 2026 agentic AI
15. https://www.censtatd.gov.hk/en/web_table.html?id=660-78001 — HK enterprise operating characteristics (size distribution corroboration)
16. https://apps.xero.com/us/app/fathom + https://www.capterra.com/p/136476/Fathom/ — Fathom add-on pricing (~US$44/mo) as price ceiling anchor
17. https://www.netsuite.com/portal/resource/articles/accounting/accounts-payable-AP-dashboard.shtml + https://www.dualentry.com/scale/accounting-dashboards — mid-market role-based customizable dashboards already exist
18. https://www.xero.com/hk/pricing-plans/ — Xero HK pricing tiers
