---
stage: generate-ideas / grounding
thesis: "Dynamic / Malleable Software Interfaces — software companies ship primitives, users (via AI coding agents) heavily modify the final interface"
facets: [trends-why-now, existing-solutions, demand-pain, adjacent-markets]
generated: 2026-06-06
---

# Grounding — Dynamic Software Interfaces

Synthesis of four parallel research facets (full findings + citations in `research/`). This doc feeds the
blind-wide seed generator and the recommendation. Every claim traces to a facet file.

## The one-line landscape

AI made building software ~6–13× cheaper and the app-store glut proves it (557K Apple submissions in
2025, +24% YoY). The tooling layer that does this is already a real business — **Cursor $2B ARR, Lovable
$400M ARR / ~8M users / ~100k apps a day, v0 4M users**. But **every one of those tools serves app
*creators* and emits a *greenfield, developer-owned app*.** None of them serves the **end user who wants
to reshape an app they already use** into the shape of their own workflow. That asymmetry is the whole
opening.

## Why now (the enabling shifts)

- **Primitive infrastructure is the accepted standard, not a bet.** shadcn/ui (75–100k+ stars; used by
  Vercel/Linear/Supabase) + Radix (130M+ npm downloads/mo) made "components as owned source you restyle &
  extend" the React default. A "ship primitives → users compose" model inherits an adopted standard. (trends, existing-solutions)
- **Generative / runtime-assembled UI is now tractable, not research.** Vercel AI SDK (20M downloads/mo)
  codified generative UI; a Google study found users preferred AI-generated UI over markdown 83% of the
  time ("emergent capability"). Thesys (C1, 300+ teams) and Tambo (OSS) are early runtime-gen-UI SDKs. (trends, existing-solutions)
- **MCP "Apps" (official Jan 2026): tools return interactive UI rendered in the conversation.** 97M SDK
  downloads/mo, 10k+ servers — a protocol backbone for "ship a server/primitives, AI assembles the UI per
  user's context." (trends)
- **Claude Artifacts proved a forkable, shareable AI-app runtime to consumers** — build inside Claude,
  share, recipient gets their own modifiable copy, billed to their own subscription (≈free distribution
  for the creator). First mainstream "software you fork like a document." (trends)
- **The intellectual anchor exists:** Ink & Switch's *Malleable Software* essay (Jun 2025, co-authored by
  Geoffrey Litt, now at Notion) — shared-data workspaces users reshape with LLM help "in minutes." (trends)

## Revealed demand (people already bend rigid software — at scale)

- **Shadow IT: ~60% of custom internal-tool builds in 2025 happened outside IT** (up from ~15% in 2022);
  25% cite "SaaS was insufficient," 31% "faster than waiting for IT." Mass workaround behaviour. (demand)
- **Retool ~$138M ARR**; 35% of enterprises already replaced ≥1 SaaS with a custom build, 78% plan more
  in 2026 — CRMs & workflows top the list. (demand)
- **Obsidian: 120M+ plugin downloads across 4,456 community plugins** (Dataview 4.3M, Templater 4.5M) —
  load-bearing rewrites of how the tool looks & works, not decoration. (demand)
- **Notion template economy: $1M/yr (Thomas Frank), $239K/yr (Easlo)** selling *workflow configurations
  as products* on ~100M generic-primitive users. People pay for software that fits their shape. (demand, adjacent)
- **Power Platform 56M MAU; 89% of devs touched low-code in the last 12 mo.** Citizen devs bypassing
  rigidity at scale. (demand)
- **Tampermonkey 10M+ users; Greasy Fork userscripts** — people writing/installing code purely to make
  *existing* web apps behave their way (Gmail, Jira, Reddit). If the software fit, the scripts wouldn't
  exist. (demand)
- **Acute niches:** neurodivergent (ADHD/autism) users abandon/modify neurotypical-built PM tools at high
  rates and pay for fit (Leantime); EMR/EHR rigidity is a documented driver of clinician burnout. (demand)

## The named, unsolved stack (the gap)

Ink & Switch names exactly what's missing and **no funded startup has closed it**: persistence of user
modifications, sharing them, sandboxing/security, auth/permissions, and a **sustainable business model**
for tools-vs-apps hybrids. The most-cited projects (Potluck, Patchwork, Cambria, Pushpin) remain research
artefacts. (existing-solutions, demand)

**The dead canary:** Arc Boosts (per-user CSS/JS to reshape any website) proved real prosumer demand for
interface personalisation — then **The Browser Company stopped Arc (May 2025) and sold to Atlassian for
$610M**, pivoting to enterprise. "Personalise any web surface" is now effectively **unserved**. Demand was
real; the business model wasn't. (existing-solutions)

**Incumbents won't fix it:** Retool/Airtable Interfaces/Notion all assume one canonical interface built by
admins/IT, consumed passively — personalised per-user interfaces would *erode* the control they sell. (existing-solutions)

## What the analogous markets teach (monetization + failure modes)

- **Value accrues to whoever owns identity + billing + distribution + the config/schema layer.** Roblox
  keeps ~70%; Salesforce earns $1 for every $5.80 partners earn by owning the locked-in data layer; Notion
  takes 10% and gets vertical GTM done for free by template sellers. **The toll-road wins, not the modder.** (adjacent)
- **Open marketplaces commoditize within ~18 months; curated/certified tiers hold margin.** WordPress
  plugins ($2.4B) — value concentrates at the top, long tail → zero. Minecraft ran a *certified* Bedrock
  Marketplace ($500M+ payouts) alongside the free mod scene: open layer = discovery, certified = revenue. (adjacent)
- **Excel's lesson (750M users, the most successful end-user-programming runtime ever): it must feel like
  *configuration/arranging*, not *coding*.** The moment users feel they're "programming," adoption
  collapses to the developer segment. AI's job is to hide the runtime. (adjacent)
- **Low-code stalled by missing both segments** (too high a floor for power users, too low for non-tech)
  and by lock-in. An open-schema (exportable JSON config) dynamic-UI layer can position *against* lock-in
  while still charging for runtime/hosting. (adjacent)
- **Living proof primitives-as-platform scales without being a dev tool:** Airtable ($478M ARR, +57%) and
  Notion ($500M ARR) — one primitive reshaped into radically different workflows; both now adding AI/agent
  config layers. The thesis is on the right timing curve. (adjacent)

## The honest counter-signal (read before betting)

Customization is, for the median user, **a vitamin they never act on** — toolbar customization "sucks,"
Outlook's decades of options sit untouched, HyperCard/WoW-modding peaks didn't generalize. Demand is
**loud-but-niche** (Obsidian/Notion/HN power users, shadow-IT ops people, acute segments), not broad-and-
shallow. The only bet that flips this: **AI lowers the friction of customization to ~zero, activating the
latent demand.** A winning seed should target a segment where the pain is already *acted on* (workarounds
already exist) — not bet on converting the indifferent median. (demand)

## Distribution reality check (the founder's #1 documented risk)

Most of this space's demand lives in **communities you can post into** (Obsidian/Notion/Reddit/HN power
users, indie hackers, shadow-IT ops) and in **specific verticals with no good tool** — both reachable
channels. The losing version is a horizontal "customize anything" platform with no owned channel and no
niche (the Arc Boosts grave). The winning version picks one reachable niche whose workaround behaviour is
already visible, and owns that channel.
