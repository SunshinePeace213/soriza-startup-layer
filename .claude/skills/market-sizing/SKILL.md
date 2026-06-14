---
name: market-sizing
description: |
  Idea-Stage market sizing — step 7. Parallel facet agents size the market bottom-up (TAM/SAM/SOM
  pressure-tested for inflation), map the buyer landscape (budget-holder vs influencer), score 3 named
  trends tailwind/headwind, and find analogues. Context, never a gate — size never kills. Use for
  "size the market", "TAM SAM SOM", "market sizing", "buyer landscape", "what trends affect this".
when_to_use: |
  Gate: runs at current_step 7 (after pressure-test β / G6). The output is CONTEXT for the founder and
  the startup brief — size never kills, there is no verdict to sign. Not arguing the idea (/pressure-test)
  and not mining competitor complaints (that was step 3, /kill-scan) — demand mining is already done upstream.
argument-hint: "[slug]"
disable-model-invocation: true
allowed-tools: Read, Glob, Write, Bash, Agent
effort: high
---

# Market sizing — the context facet

Map the size and shape of the market — bottom-up TAM/SAM/SOM, the buyer landscape, the trend balance,
and analogues — as **context** for the founder's judgment and the startup brief. **Never a gate: size
never kills.** A tiny-but-real, reachable niche is a pass (niche + real demand = a market). Everything
here is a rank input or an interview question, never a death.

This is the `market-map` skill's sizing / buyer / trends / analogues facets, harvested into step 7. The
complaint-mining facet is **not** here — it ran in step 3 (`/kill-scan`).

## When this applies

- `current_step: 7` — a `pressure-report-beta.md` and a `customer-discovery.md` Discovery Read exist.
  Triggers: "size the market", "TAM/SAM/SOM", "buyer landscape", "what trends affect this", "what's next"
  after pressure-test β.
- **Entry guard:** step < 7 / no Discovery Read → point to `/pressure-test <slug> --beta` (G6 is the
  main kill decision; sizing comes after it).

## Gotchas

- **Size never kills, full stop.** A small-but-real, reachable niche is a pass. Nothing here is a
  verdict; every number is a rank input or an interview question. No "too small → kill" language — that
  would invert the doctrine. G7 is a *completeness* check, not a judgment.
- **TAM is pressure-tested, not celebrated.** AI will happily find the number that makes a TAM look
  fundable — **surface the inflation, don't launder it.** Size **bottom-up** (count real units × a
  defended price), never top-down off a "the $X-trillion market" headline; flag what a top-down model
  would have inflated the figure to. (The validator requires the inflation flag and a bottom-up basis.)
- **Web enters via the ledger only.** The facet agents hold the web tools; the skill does not. Every
  external number is a grade-4 `evidence-ledger.jsonl` entry (URL required) cited as `E-xxx`. **Append
  the ledger line FIRST, then cite it** — never paste a web fact straight into the artifact.
- **The independent fan-out is parallel.** Dispatch every facet agent in ONE message as parallel `Agent`
  calls so their web-fetch noise stays out of this context (4.8 under-fires a vague "spawn N agents" —
  issue one explicit `Agent` call per facet).
- **Complaint mining already happened in step 3.** Don't re-mine competitor reviews here — this is
  sizing / buyer / trends / analogues only.

## Workflow

**Goal:** `ideas/<slug>/market-sizing.md` (passes `test_sizing`) → the founder reads the context. There
is no verdict to sign; G7 is a completeness check.

1. **Confirm state.** Read `ideas/<slug>/STATE.md` (`current_step: 7`). Note the validated baseline from
   the Discovery Read and `hypothesis.md` (+ any `deltas_pending`) — sizing is sized against the problem
   discovery confirmed, not the one assumed going in.
2. **Parallel facet fan-out.** In one message, dispatch `startup-idea-researcher` once per facet (pass
   the facet brief, the hypothesis + Discovery-Read context, and a findings path under
   `ideas/<slug>/market-sizing/`):
   - **Sizing + buyer landscape** — bottom-up TAM/SAM/SOM (unit counts × defended price), pressure-tested
     for inflation; who holds budget · who influences · are they the same person.
   - **Trends + why-now** — 3 named external trends (regulatory / technological / demographic), each to be
     scored tailwind or headwind.
   - **Analogues** — markets where a similar problem was solved; what worked / what didn't.
3. **Ledger first.** For every external fact you will cite, append a grade-4 entry to
   `evidence-ledger.jsonl` (unique ascending id, `url` required); corrections are new lines, never edits.
4. **Synthesize the artifact.** Write `ideas/<slug>/market-sizing.md` from
   `assets/market-sizing-template.md`: bottom-up TAM/SAM/SOM with the inflation flag, the buyer landscape,
   3 trends each scored, analogues, the `forward-deployed-founder` moat/distribution read (can a solo
   founder reach + own this niche — the #1 risk), and "what this means" (rank inputs + new interview
   questions). Cite `E-xxx` for every web fact. `schema_on_write` runs `test_sizing` on save — fix and
   rewrite on any stderr feedback.
5. **Lock-ahead G8 (write-once).** Before G7 can pass, the startup-brief's gate criteria must already be
   locked: `uv run scripts/lock_criteria.py --slug <slug> --gate g8`.
6. **Close G7 (read-only).** `uv run scripts/advance_gate.py --slug <slug> --gate g7` — the `test_sizing`
   completeness check is the gate (lock-ahead now satisfied). The founder reads the context; **there is
   no verdict to sign.** Next: `/startup-brief <slug>`.

## Workers, references & assets

- **Workers:** `startup-idea-researcher` (×facet, parallel) + `market-researcher` for demand/niche
  context if needed; `forward-deployed-founder` for the moat/distribution read.
- **Template:** `assets/market-sizing-template.md`.
- **Validator:** `tests/schemas/test_sizing.py` (the G7 completeness gate; size never kills).
- **Spec:** `.claude/skills/idea-stage/references/stage-pipeline.md` (step 7).
