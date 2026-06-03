# Output Template — `solution-design.md`

The top-level deliverable: a Solution Design action card that crystallizes the concept the validated
evidence supports and challenges it from every angle the Playbook names. It carries a **non-binding**
Concept Read (a recommendation, not a pass/fail gate — only proceeding past a KILL Discovery Read is
stamped as an override). For a redesign re-run, append a `## Round <N> (<date>)` section rather than
overwriting, so the founder watches the concept evolve.

```markdown
# Solution Design: <slug>

> Crystallizes & challenges the concept the validated evidence supports. The design must serve the
> problem DISCOVERY revealed — not the one the hypothesis ASSUMED. n is small; read the caveats.

## Concept Read
**<build | narrow | redesign | reconsider>** — 1 line + 1–2 sentences of rationale tied to the evidence
below. Non-binding. If proceeding past a KILL Discovery Read, see the Override line.

## The Solution Concept
- **Wedge** — the narrowest first version that delivers value (one sentence).
- **Validated who** — the persona discovery actually validated (narrowed from the hypothesis's wider net).
- **Core job / workflow it owns** — the one job it does end-to-end.
- **The whole-product sketch** — what the end-to-end experience is (2–4 lines).
- **What it deliberately does NOT do** — focus = subtraction; name the tempting scope you're cutting.
- **Why it wins** — the unfair-advantage / moat thesis, tied to the founder's agentic-coding edge + any
  defensible signal discovery surfaced.

## Drift Audit — assumed → validated
*(Baseline = original hypothesis + accumulated flagged deltas from pressure-test / market-research /
customer-discovery, applied or not — see `solution-design/validated-baseline.md`. Measured against the
reconstruction, never the stale hypothesis.md.)*

| Originally assumed (hypothesis.md) | What validation revealed (reconstructed baseline) | Does the concept serve the VALIDATED version? |
|---|---|---|
| <assumed dimension> | <what discovery/research showed> | ✅ serves it / ⚠️ drifting / ❌ still solving the old problem |

Any `❌` or accumulation of `⚠️` pushes the Concept Read toward `redesign`. State it; do not launder it.

## Three Load-Bearing Assumptions
*(Top 3 of all material assumptions, ranked by leverage × uncertainty — statuses verbatim from
`scripts/rank_assumptions.py`. Assumptions the blind solution-red-team raised that the draft missed are
flagged. The rest of the ranked list goes below the table.)*

| # | Assumption | Why load-bearing (what collapses if false) | What would have to be true | Current evidence (cited) | Cheapest test → MVP RAT |
|---|---|---|---|---|---|
| 1 | <statement> | <what breaks> | <condition> | <supports / contradicts, cited> | <the riskiest-assumption-test> |

## Alternatives Considered
The other concepts/approaches that could serve the validated problem, and why this wedge wins — or,
honestly, where one of them might beat it. (The Playbook's "what alternatives exist?")

## Scale Conditions
What must hold for this to work at scale: distribution (how the 1000th user arrives), unit economics,
defensibility, and the agentic-leverage assumption. (The Playbook's "what would have to be true at scale?")

## Challenge (independent blind solution-red-team)
<the red-team's challenge, folded in: where the concept is weakest, the scale-failure modes, and the
single most likely self-deception — each tied to evidence. Plus the **reconciliation gaps**: assumptions
or drift the adversary found that the draft missed. Do NOT soften this to protect the concept.>

## MVP Brief (forward contract → MVP stage)
Self-contained handoff for the not-yet-built MVP stage:
- **Wedge** — <the narrowest first version, restated>
- **Prioritized riskiest-assumption-tests** — <the top-3 assumptions' cheapest tests, in rank order>
- **Validated profile** — <who to build for, from discovery>
- **Non-goals** — <what the MVP must NOT include>

## Hypothesis Updates Flagged
Evidence the design surfaced that should sharpen or correct the hypothesis. Route to
`/sharpen-hypothesis` — do NOT edit hypothesis.md here.
- <update> — what the design exposed

## Override (only if proceeding past a KILL Discovery Read)
*(Only when the Discovery Read was KILL and the founder proceeds anyway. CONTINUE / PIVOT /
KEEP-DISCOVERING never carry an override line.)*
<Read> | Override: founder proceeded past KILL Discovery Read on <ISO-date> — concept narrowed to <wedge>

---

## Provenance
- `solution-design/delta-ledger.md` — every flagged delta + Discovery verdict + tripped criteria, verbatim (script output)
- `solution-design/validated-baseline.md` — the reconstructed problem the drift audit measures against
- `solution-design/assumptions.json` — per-assumption leverage/uncertainty scores (ranker input)
- `solution-design/red-team.md` — the blind solution-red-team's raw challenge
- `solution-design/reconciliation.md` — draft vs blind adversary; gaps surfaced
- `solution-design/rounds/round-<N>.md` — per-round provenance when the concept is redesigned + re-run
```

Honesty rule (mirrors `/market-research` and `/customer-discovery`): never present a `⚠️`/`❌` drift row
or an unsupported top-3 assumption as if the concept were build-ready. The Concept Read must follow the
evidence — a concept that still serves the assumed problem is a `redesign`, not a `build` with caveats.
