# Demand / Pain Validation — Findings

## Key findings

- **ERP implementation failure rate is 68% industry-wide, 73% in discrete manufacturing, with average cost overruns of 189–215%** — the pain is not subtle or rare; most buyers fail on first attempt. Panorama Consulting puts average mid-market ERP implementation cost at ~$450K, meaning a failed project costs real money even for a 50-person shop. The strongest opportunity signal: failure is the base case, not the edge case. (Source 1, 2)

- **SAP ECC mainstream support ends December 2027, creating a hard forcing function for ~20,000+ mid-market SAP customers** — Gartner notes migration acceleration is not happening fast enough to meet the deadline, so demand for alternatives (not just S/4HANA) will spike in 2026–2027. Consulting day rates for S/4HANA specialists are already up 30–50% vs 2022 levels, and 49% of migrated customers report costs exceeded budget (up 17% YoY from 2023). Mid-market companies feeling cost-squeezed are the reachable segment here. (Source 3, 4)

- **NetSuite mid-market implementations: $100K–$300K year-one cost; consultant shortage confirmed at ~30% of NetSuite partners reporting difficulty finding skilled resources** — boutique firms bill $150–$300/hr, Big Four up to $1,000/hr. TrustRadius and G2 reviewers repeatedly quote: "after nine months of false promises… not up and running"; "regular updates ruin customized features"; "hired a consulting firm that performed poorly, paid for a whole year before going live." The consultant layer is the workaround — it is the revealed willingness to pay, and it is large. (Source 5, 6, 7)

- **54% of plants globally (2024, IoT Analytics 163-page MES report) still use pen-and-paper or spreadsheets as their de-facto MES** — work-order management, production scheduling, downtime tracking, and OEE are the four workflows most commonly handled manually. IoT Analytics explicitly flags spreadsheets as "not reliable sources of data for AI integration." This is 300+ vendors chasing an enormous un-digitized base; the mid-market/SMB manufacturer running on clipboards is the most reachable segment and least well-served by $500K enterprise MES deployments. (Source 8)

- **67% of supply chain managers still use Excel as a management tool; TMS/WMS integration cost "often equals or exceeds the software itself" for mid-market shippers** — supply chain planners explicitly reach for spreadsheets when enterprise tools are too rigid for fast scenario modeling, creating a "shadow system… invisible to governance." Voiced frustration: "trying to manage that network with spreadsheets, emails, and phone calls is inefficient at best and operationally risky at worst." The workaround IS the product gap. (Source 9, 10)

- **SCADA/HMI per-tag pricing is a documented mid-market squeeze: Wonderware (AVEVA) charges $80K–$150K for a 10,000-tag system vs Ignition's $15K–$25K for the same scale** — Ignition is taking share from Wonderware specifically in mid-market food-and-beverage, water-and-wastewater, and discrete manufacturing. This pricing bifurcation shows the segment is already defecting — they are reachable and price-sensitive, and an AI-native challenger in this space would land in a segment already mid-flight from legacy vendors. (Source 11)

- **EDA tools: >60% of chip design startups face significant barriers from EDA licensing costs; licenses can reach $400K per seat per year; Cadence/Synopsys/Siemens control ~75% of the market** — fabless startups at 5nm report $80K–$150K per engineer annually in tools alone. Cloud EDA (pay-per-use) cuts costs ~40% and is the only affordable path for small teams. EDA pain is real but the segment (fabless chip startups) is small, technically deep, and largely VC-funded — not a bootstrap-reachable niche for an SMB-focused founder. Signal is strong but the buyer is not reachable without deep domain credibility. (Source 12, 13)

- **AI-native ERP challenger DualEntry raised $90M Series A (Oct 2025, Lightspeed + Khosla) specifically targeting mid-market finance automation with "NextDay Migration" (live in 24 hrs vs months for NetSuite)** — their explicit pitch is that 90% of manual accounting tasks can be automated and that legacy ERP is "clunky, slow, and impossible to customize." $90M raised in 18 months from stealth = institutional validation that mid-market ERP replacement is a real, NOW opportunity. Also: Doss raised $55M (March 2026) for AI inventory management that plugs into existing ERPs — signaling that point-solution AI layers on top of legacy ERP are also fundable. (Source 14, 15)

- **MES for SMB manufacturers is the clearest reachable niche: sub-50-employee job shops, food manufacturers, and contract manufacturers run on whiteboards and Excel; entry-point MES tools (MRPeasy, MachineMetrics Manual Stations) show the segment IS willing to pay for lightweight digitization** — the voiced pain: "the MES handles work orders, scheduling, and OEE. But the workflows specific to their operation — the ones that live on whiteboards and clipboards and tribal knowledge — those never quite make it [into the system]." This gap between standard modules and actual shop-floor workflow is where an AI-configurable, agentic MES could wedge in. Communities: r/manufacturing, r/msp, LinkedIn manufacturing groups, and industry-specific Facebook groups for job shops. (Source 8, 16)

- **3PL and freight broker segment: small/mid brokerages explicitly manage loads via email threads and spreadsheets; voiced pain appears in sales copy ("gone are Frankenstein systems") suggesting the problem is well-known and unsolved at the sub-100-employee brokerage level** — TMS for brokers is fragmented; mid-market TMS integration cost "often equals or exceeds software cost." This is a bootstrappable entry: brokers are reachable via FreightWaves community, DAT forums, and LinkedIn logistics groups, and a narrow AI-powered load-management/quoting tool could find early adopters fast. Signal is moderate — not as loud as ERP complaints, but community is accessible. (Source 17)

## Sources

1. https://godlan.com/erp-implementation-failure-statistics/ — ERP failure rate 68% industry / 73% discrete manufacturing; cost overrun 189–215%
2. https://www.netsuite.com/portal/resource/articles/erp/erp-statistics.shtml — Panorama $450K average mid-market ERP cost; Gartner 70% projection
3. https://ignitesap.com/the-s-4hana-deadline/ — SAP ECC support end-2027 deadline detail
4. https://19523792.fs1.hubspotusercontent-na1.net/hubfs/19523792/2025%20Research%20Report/SAPinsider%20-%202025-02%20SAP%20S4HANA%20Migration%20-%20Executive%20Summary.pdf — SAPinsider 2025: 49% over budget, consulting rates up 30–50%
5. https://www.houseblend.io/articles/netsuite-consultant-hourly-rates-2026 — NetSuite consultant rate ranges; 30% partner shortage
6. https://www.g2.com/products/netsuite/reviews — G2 NetSuite reviews: learning curve, consultant dependency, slow performance
7. https://www.trustradius.com/products/netsuite-erp/reviews — TrustRadius: "nine months of false promises"; "$100K implementation cost"; "updates ruin customized features"
8. https://iot-analytics.com/mes-vendors-replace-pen-paper-spreadsheets/ — IoT Analytics MES Market 2025–2031: 54% of plants use pen/paper or spreadsheets
9. https://flox.is/blog/hitting-an-excel-spreadsheet-wall — 67% of supply chain managers use Excel; spreadsheet as shadow system
10. https://blog.shipperguide.com/tms-for-3pl — TMS/WMS integration cost equals or exceeds software cost for mid-market
11. https://industrialmonitordirect.com/blogs/knowledgebase/indusoft-vs-ignition-vs-wonderware-scada-software-comparison-guide — Wonderware $80–150K vs Ignition $15–25K for 10,000-tag system
12. https://richardtoad.substack.com/p/moat-goat-eda-software — Cadence/Synopsys/Siemens 75% EDA market share; $400K/seat licensing
13. https://semiengineering.com/eda-startups-at-dac-2025/ — EDA startups DAC 2025; ChipAgents agentic AI chip design
14. https://www.dualentry.com/funding-announcement — DualEntry $90M Series A Oct 2025; NextDay Migration; mid-market target
15. https://techcrunch.com/2026/03/24/doss-raises-55m-for-ai-inventory-management-that-plugs-into-erp/ — Doss $55M AI inventory management plug-in for ERP
16. https://www.machinemetrics.com/blog/downsides-of-mes — MES gap: standard modules miss shop-floor tribal workflow
17. https://www.denim.com/blog/best-tms-software-for-brokers — 3PL/freight broker TMS fragmentation; email/spreadsheet workarounds
