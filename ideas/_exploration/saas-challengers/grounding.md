# Grounding — SaaS Challengers (AI-native software replacing legacy SaaS)

Synthesis of four research facets (`research/trends-why-now.md`, `existing-solutions.md`, `demand-pain.md`,
`adjacent-markets.md`). This is the evidence base the blind-wide seed generator reads. Founder-blind: it
describes the *opportunity space*, not who should build it.

## The thesis, grounded

YC / Jared Friedman's **Summer 2026 "SaaS Challengers" RFS is live and explicit** — it names chip design
(EDA), ERPs, industrial control (ICS/SCADA/MES), and supply chain (SCM/TMS/WMS) as priority targets, with
the framing "the next generation will be built by replacing legacy SaaS with AI-native software." Four
named Friedman playbooks: (1) clone at 1/10th price, (2) AI-native rebuild that rethinks the workflow,
(3) bundle 10 point-solutions into a suite, (4) open-source replacement monetized via services. [trends]

**The cost-collapse is empirically real and dated.** Anthropic's 2026 Agentic Coding Trends Report: 78%
of Claude Code sessions now multi-file (was 34% in Q1 2025), ~20 autonomous actions per run (doubled in 6
months), one Rakuten feature shipped across a 12.5M-line codebase in a 7-hour unattended run. A solo
founder can now sustain velocity that needed a 5–10-person team. [trends]

**Demand-side pull is flipping, not just supply-side capability.** 55% of US IT execs expect to replace
some commercial software with AI-generated tools (Recognize, Nov 2025); Gartner projects 35% of
point-product SaaS replaced/absorbed by agents; 47% of top-500 US enterprises migrated ≥1 business
process from SaaS to a vertical AI agent in 2024–25 (was 11% in 2023, Stanford HAI). Enterprise vertical-AI
spend tripled to $3.5B in 2025 (Bessemer). The buyer is now *looking*. Window: 2025–2027 before the next
AI-native incumbents lock their own moats. [trends]

## Proof the wedge works against "invulnerable" incumbents

- **Campfire** — 12-person team, $100M raised in <1yr (Accel A + B), customers "ripping out NetSuite"
  in 9 months; cut one close from 15→3 days. [trends]
- **Rillet** — $100M in <1yr (Sequoia→a16z/ICONIQ), 200+ customers, mid-market SaaS that outgrew
  QuickBooks but won't endure a 12-month NetSuite install. [trends]
- **DualEntry** — $90M Series A, "NextDay Migration" (live in 24h vs months), pitch: 90% of manual
  accounting automatable, legacy ERP "impossible to customize." [demand]
- **EDA challengers** — ChipAgents ($50M A1, 6,377% H1-2025 usage growth, 10x on RTL), Cognichip ($60M A,
  30+ customers), Normal Computing ($50M, Samsung). LLMs crossed the threshold for HDL/RTL. [trends]
- **Adjacent proof** — Legal: Harvey/Legora each ~$100M ARR by attacking ONE document workflow; EvenUp
  narrower still (PI demand letters). Healthcare RCM: 12 fast-rising AI startups, services-led labor
  replacement. Zamp: AI+human "managed OS" beating Avalara in sales tax. MaintainX: $150M D displacing
  IBM Maximo in mid-market CMMS. Tekion: $4B+ cracking the CDK/Reynolds DMS oligopoly. [adjacent]

## The incumbent-vulnerability map (where "invulnerable" is real vs soft)

| Category | Hard moat (avoid head-on) | Soft underbelly / open wedge |
|---|---|---|
| **EDA** | Foundry certification (TSMC mandates "Calibre-clean" at tape-out); PDK co-dev 24mo out; 95%+ retention. **Regulatory/cert moat — wrong beachhead for a bootstrap solo.** | PCB layout (Quilter already funded here), schematic capture, BOM/DFM checks for SMB electronics shops — sit *beside*, never replace the signoff flow. |
| **ERP** | F500 lock-in: custom code in vendor formats, data gravity, multi-year ELAs, $2.5M+ switching. GL/finance is now **crowded** (Rillet/Campfire/DualEntry/Doss, >$500M VC/18mo). | **Mid-market ops layer** (inventory/procurement/order-routing) for manufacturing/CPG; **non-English markets**; vertical-specific ERP (HK/China trading cos with fapiao/VAT/multi-entity). |
| **ICS/SCADA/MES** | Safety certification (IEC 61511, ISA/IEC 62443), OT protocol lock-in, 40-yr hardware cycles — replacing a DCS needs years of re-cert. | **MES layer** (scheduling/quality/traceability, softer lock-in; Tulip funded the enterprise tier); SCADA per-tag pricing revolt (Wonderware $80–150K vs Ignition $15–25K); predictive-maintenance/OEE for sub-200-emp brownfield plants. |
| **SCM/TMS/WMS** | o9 ($3.7B), Blue Yonder/Kinaxis (no public pricing, 12–24mo installs, enterprise-only). | **"Intelligence layer above ERP/TMS/WMS"** (newest, least-crowded, June 2026); SMB shippers/3PLs/brokers run on email+Excel; demand-planning for Asian importers/exporters. |

## Where the real, voiced pain is (revealed demand)

- **ERP failure is the base case**: 68% implementation failure (73% in discrete manufacturing), 189–215%
  cost overruns, ~$450K avg mid-market cost. **SAP ECC support ends Dec 2027** → ~20,000 mid-market SAP
  customers forced to move, migration not keeping pace → alternatives spike 2026–27. [demand]
- **The consultant layer IS the revealed willingness-to-pay**: NetSuite year-one $100K–300K, ~30% partner
  shortage, $150–1,000/hr; reviews: "nine months of false promises… not up and running." [demand]
- **Spreadsheets are the de-facto incumbent**: 54% of plants still run MES on pen-and-paper/Excel; 67% of
  supply-chain managers manage on Excel; TMS/WMS integration "often equals or exceeds software cost." The
  workaround *is* the product gap. [demand]
- **SMB MES** (sub-50-emp job shops, food/contract mfrs on whiteboards) is the clearest reachable niche —
  standard modules miss the shop-floor tribal workflow that "lives on clipboards." Communities:
  r/manufacturing, r/PLC, r/supplychain, FreightWaves/DAT, LinkedIn industry groups. [demand]
- **EDA pain is strong but the buyer is unreachable** for a non-domain founder ($400K/seat, fabless
  startups, deep-credibility-gated). [demand]

## The repeatable wedge playbook (Bessemer Vertical-AI book, Jan 2026)

1. Start with a **standardized, repetitive sub-workflow with a measurable output** — not a judgment-heavy
   core process. 2. Automate it with an **"undeniable miracle" 10x demo**, earn trust, expand into core.
3. Become the **system of record for the data that sub-workflow generates** — the data layer is the moat,
not the model. Durability = workflow-integration depth + proprietary compounding data + ROI tied to
**labor-budget displacement** (not IT spend). **Thin AI features bolted onto old data are not durable**
("feature, not a company": Moveworks→ServiceNow $2.85B, Vanti→Tray). [adjacent, existing]

## Geography angle (real but thin signal)

- **China/HK ERP is structurally distinct**: SAP/Oracle ~40% at the high end; Kingdee/Yonyou own SME tier
  but have **not shipped an AI-native rebuild**; Huawei MetaERP displacing foreign vendors at SOEs (data
  sovereignty). Open gap: mid-tier manufacturer/trader that outgrew Kingdee, can't afford SAP, needs
  China-specific compliance (Golden Tax, VAT fapiao, HK+mainland multi-entity) — no funded AI-native
  player there. GBA manufacturing cluster generates AI-embedded production data at scale. [existing, adjacent]

## Traps to flag

- **GL/finance ERP is crowded** — entering there now is a knife fight with >$500M of funded competitors.
- **EDA core flow + safety-critical ICS** are certification-moated — wrong beachhead for a bootstrap solo.
- **Augmentation/copilot layers atop SAP/NetSuite** (e.g. "shadow GL") are the most acquirable, least
  durable position — own the data or be acqui-hired.
- **Horizontal "AI for X" with no proprietary data flywheel** = feature, not company.
