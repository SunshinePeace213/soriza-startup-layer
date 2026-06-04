# Hypothesis: HK Property Agent Deal Tracking

**Candidate ID:** cand-hk-property-agent-deal-tracking-interface

**Sharpened Hypothesis (provisional, to-be-tested):**

Independent property agents in Hong Kong (solo or 2–5 person boutique agencies) managing 15–40 active deals per year per agent lose an average of HKD 50–150k in annual commission (3–5 deals/year) due to fragmented deal tracking across WhatsApp, spreadsheets, and US-centric CRM tools that don't reflect their custom workflow logic. An outcome-based pricing model (commission-percentage-based pricing) will reduce those losses to below HKD 25k/year by consolidating deal state and aligning incentives.

---

## Four Dimensions (Provisional)

| Dimension | Definition | Status |
|---|---|---|
| **WHO** | Independent property agents (licensed, handling residential/commercial deals, HKD 2M–10M+ transactions) operating solo or in 2–5 person boutique agencies in Hong Kong. Cantonese-speaking, relationship-driven, systematically underserved by US-centric CRM tools. Directly reachable via local networks. | Specific ✓ |
| **HOW OFTEN** | Daily — each agent spends 2–5 hours per day managing active listings, scheduling viewings, tracking negotiations, and recording commissions. Equivalent to 15–40 active deals per agent per year. | Specific ✓ |
| **HOW SEVERE** | Commission leakage: 3–5 lost deals per agent per year due to tracking gaps, missed follow-ups, and delayed offer tracking. Estimated annual impact: HKD 50–150k in lost commission per agent (at typical HK property commission rates of 2–5% on deals valued HKD 2M–5M). | Specific ✓ |
| **STATUS QUO** | Fragmented tooling: WhatsApp for client communication, Excel/Google Sheets for custom deal tracking (organized per agent's logic: by district + price band, by buyer-readiness stage, or by monthly commission expected), and optional generic Kanban CRM (Salesforce, HubSpot, local alternative) forced into a standardized pipeline. No unified audit trail; high context-switching overhead. | Specific ✓ |

---

## Testability & Falsifiability

**Is the hypothesis falsifiable?**
- YES — measurable against: (1) actual commission loss before/after adoption, (2) deal-closure latency improvements, (3) adoption + churn rates under outcome-based pricing vs. per-seat.

**How would it be disproven?**
- If agents still lose ≥ HKD 50k/year with the product in use.
- If outcome-pricing adoption stalls because agents fear variable cost or prefer fixed-fee models.
- If deal-closure latency does not improve after product adoption.
- If agents report that the product enforces a standard pipeline view, failing to accommodate their custom workflow logic.

---

## Next Steps (for Customer Discovery)

1. **Validate commission-loss estimate** — interview 5–8 agents on current deal leakage and time spent switching tools.
2. **Test outcome-pricing willingness** — probe pricing model preference: per-seat vs. per-deal vs. % of commission closed.
3. **Explore custom-view feasibility** — understand exactly how each agent organizes deals (by district, buyer stage, commission timeline) and whether a configurable UI can accommodate 80%+ of agent workflows.
4. **Benchmark status quo tooling** — verify which platforms agents actually use (WhatsApp, specific spreadsheet patterns, which CRM brands locally).

---

**Gate:** Gate 1 (Testability)  
**Score:** 75 / 100  
**Verdict:** ADVANCE
