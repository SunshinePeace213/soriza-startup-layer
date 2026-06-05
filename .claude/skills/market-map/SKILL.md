---
name: market-map
description: |
  Fourth stage of the Idea Stage: map the market for a hypothesis via a parallel fan-out of focused
  research agents — competitor tiers, review-complaint mining (problem-solution-fit signal) + user
  language, TAM/SAM/SOM (pressure-tested for inflation) + buyer landscape + market maturity, and 3 named
  trends (tailwind/headwind) + analogous markets — plus the moat/distribution read. It is CONTEXT, never
  a gate: size NEVER kills. Use for "market research", "map the competitive landscape", "size the
  market", "who are the competitors", "is the timing right", "TAM SAM SOM", "what are the trends".
when_to_use: |
  Gate: a hypothesis.md exists for the idea. Not arguing against the idea (/disconfirm) or building the interview pack (/customer-discovery-design).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Agent, WebSearch, WebFetch
effort: high
---

# Market Map

Map the market for the idea — competitors, demand, sizing, trends, distribution — as **context** for the
interview brief and the founder's judgment. **Never a gate: size never kills.** A tiny-but-real niche is a
pass (niche + real demand = a market). Competitor presence, unproven demand, and "looks small" are
interview questions and rank inputs, not deaths.

## When this applies

- `hypothesis.md` exists; "market research", "map competitors", "size the market", "is the timing right",
  "TAM/SAM/SOM", "what trends affect this".
- **Entry guard:** no `hypothesis.md` → point to `/sharpen-hypothesis`.

## What it does (parallel fan-out, then synthesize)

Goal: `ideas/<slug>/market-research.md`. Spawn **~3–4 focused research subagents in parallel** (each keeps
its web-fetch noise OUT of this context); the skill synthesizes their distilled findings. Runs once, for
the committed idea — depth > saving agents.

1. **Competitor tiers** — direct / indirect / acquirers / adjacent.
2. **Review-complaint mining → PSF signal** — mine competitor *reviews* for the top **unresolved**
   complaints; flag whether the hypothesis addresses them (a problem-solution-fit signal); capture **user
   language** (feeds the interview guide + outreach).
3. **Sizing + buyer landscape** — TAM/SAM/SOM **pressure-tested for inflation**; market maturity
   (expanding / consolidating / mature); **who holds budget · who influences · are they the same person**.
4. **Trends + analogues** — **3 named external trends** (regulatory / technological / demographic), each
   scored **tailwind / headwind**; **analogous markets** where a similar problem was solved (what worked /
   didn't).

Plus read `forward-deployed-founder` for the **moat / distribution read** (can the founder reach + own
these customers — the #1 risk).

## Gotchas

- **Size never kills, and TAM is pressure-tested, not celebrated** — the article's warning is that AI will
  find the number that makes a TAM look fundable; surface the inflation, don't launder it.
- This is **context, not a verdict**. Everything here becomes a rank input or an interview question.

## Output

`ideas/<slug>/market-research.md` (`assets/market-research-template.md`) + `market-research/` per-facet
provenance. Next: `/customer-discovery-design`.

## Workers & references

- Workers: `market-researcher` + facet researchers (parallel fan-out).
- `assets/market-research-template.md` — the market-map structure.
