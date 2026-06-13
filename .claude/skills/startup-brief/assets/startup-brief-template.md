# Output Template — `startup-brief.md`

The top-level deliverable of step 8: a Startup Brief that crystallizes the concept the validated
evidence supports, challenges it from every angle the Playbook names, runs the premortem, and stamps a
**GO / NO-GO**. It merges what used to be `solution-design` (concept + drift audit + blind red-team +
ranked assumptions) and `idea-stage-exit` (the deliberate exit decision). The GO/NO-GO is **binding** —
this is the main build/no-build stamp; proceeding past a tripped/overridden kill-criterion is an
explicit, stamped override. For a redesign re-run, append a `## Round <N> (<date>)` section rather than
overwriting, so the founder watches the concept evolve.

Every `##` heading below is required by the validator (`test_startup_brief`). Keep them.

```markdown
# Startup Brief: <slug>

> Crystallizes, challenges, and stamps GO/NO-GO on the concept the validated evidence supports. The
> design must serve the problem DISCOVERY revealed — not the one the hypothesis ASSUMED. n is small;
> read the caveats.

## Decision
**<GO | NO-GO>** — 1 line + 1–2 sentences of rationale tied to the evidence below. This is the binding
build/no-build stamp. If proceeding past a tripped/overridden kill-criterion, see the Override section.

## The Validated Problem
The problem discovery actually revealed (not the one the hypothesis assumed). Cite grade ≤2 evidence.
- **Who** — the persona discovery validated (narrowed from the hypothesis's wider net). <E-xxx>
- **How often** — <frequency, with a number> <E-xxx>
- **How severe** — <the real severity / the fear that drives action> <E-xxx>
- **Status quo** — <what they do now; a grade-1 time/money commitment is the strongest signal> <E-xxx>

## The Solution Concept
- **Wedge** — the narrowest first version that delivers value (one sentence).
- **Validated who** — the persona discovery validated.
- **Core job / workflow it owns** — the one job it does end-to-end.
- **What it deliberately does NOT do** — focus = subtraction; name the tempting scope you're cutting.
- **Why it wins** — the unfair-advantage / moat thesis, tied to the founder's stated edge (from the
  profile) + any defensible signal discovery surfaced.

## Drift Audit — assumed → validated
*(Baseline = original hypothesis + accumulated flagged deltas from kill-scan / pressure-report-alpha /
customer-discovery / pressure-report-beta / market-sizing, applied or not — see
`startup-brief/validated-baseline.md`. Measured against the reconstruction, never the stale hypothesis.md.)*

| Originally assumed (hypothesis.md) | What validation revealed (reconstructed baseline) | Serves the VALIDATED problem? |
|---|---|---|
| <assumed dimension> | <what discovery/research showed, cited> | ✅ serves it / ⚠️ drifting / ❌ still solving the old problem |

Any `❌` or accumulation of `⚠️` pushes the Decision toward NO-GO / redesign. State it; do not launder it.

## Three Load-Bearing Assumptions
*(Top 3 of all material assumptions, ranked by leverage × uncertainty — statuses verbatim from
`scripts/rank_assumptions.py`. Assumptions the blind solution-red-team raised that the draft missed are
flagged. The rest of the ranked list goes below the table.)*

| # | Assumption | Why load-bearing (what collapses if false) | What would have to be true | Current evidence (cited) | Cheapest test → PoC RAT |
|---|---|---|---|---|---|
| 1 | <statement> | <what breaks> | <condition> | <supports / contradicts, cited> | <the riskiest-assumption-test> |

## Alternatives Considered
The other concepts/approaches that could serve the validated problem, and why this wedge wins — or,
honestly, where one of them might beat it. (The Playbook's "what alternatives exist?")

## Scale Conditions
What must hold for this to work at scale: distribution (how the 1000th user arrives), unit economics,
defensibility, and whether the founder's stated edge is durable. (The Playbook's "what at scale?")

## Challenge (independent blind solution-red-team)
<the red-team's challenge, folded in: where the concept is weakest, the scale-failure modes, and the
single most likely self-deception — each tied to evidence. Plus the **reconciliation gaps**: assumptions
or drift the adversary found that the draft missed. Do NOT soften this to protect the concept.>

## Premortem (Eisenmann six-pattern checklist)
It's 18 months later and this failed. Which pattern killed it? Assess all six (see `references/premortem.md`).
1. **Good Idea, Bad Bedfellows** — <applies / mitigated / live, + why>
2. **False Starts** — <…>
3. **False Positives** — <…>
4. **Speed Trap** — <…>
5. **Help Wanted** — <…>
6. **Cascading Miracles** — <multiply the independent miracles; state the combined odds>

## Exit-Criteria Check (the three)
1. **Is the problem real & specific?** — <yes/no + the evidence: exactly who, how often, how severe,
   what they do now>
2. **Does the solution address the VALIDATED problem?** — <per the drift audit; serves the discovered
   problem, not the assumed one>
3. **Is there enough signal to justify building?** — <a reasoned bet, not certainty — and not an act of
   faith; summarize the kill-criteria status>

## PoC Kill-Criteria (locked → G9)
The pre-registered criteria the PoC is scored against. Locked write-once in `gates/criteria-g9.yaml`
(lock-ahead — locked BEFORE this G8 stamp). Never softened after the PoC runs. Each ties to a top
load-bearing assumption.
- **g9-1** — <concrete threshold, e.g. ≥3 of 5 PoC users do X> (tests assumption #N)
- **g9-2** — <concrete threshold>
- **g9-3** — <concrete threshold>
- **g9-4** — all open α/β predictions resolved

## PoC Brief (forward contract → step 9 /build-poc)
Self-contained handoff for `/build-poc`:
- **Wedge** — <the narrowest first version, restated>
- **Prioritized riskiest-assumption-tests** — <the top-3 assumptions' cheapest tests, in rank order>
- **Validated profile** — <who to build for, from discovery>
- **Non-goals** — <what the PoC must NOT include>
- **Archetype hint** — <video / concierge / Wizard-of-Oz / functional — the cheapest that tests g9-1/2>

## Hypothesis Updates Flagged
Evidence the design surfaced that should sharpen or correct the hypothesis. Route to
`/sharpen-hypothesis` — do NOT edit hypothesis.md here.
- <update> — what the design exposed

## Override
*(Only when a kill-criterion tripped and the founder proceeds anyway — e.g. a KILL Discovery Read
overridden at G6. A clean GO carries "None".)*
<None> | Override: founder proceeded past TRIPPED <criterion> on <ISO-date> — <reason / narrowed wedge>

---

## Provenance
- `startup-brief/delta-ledger.md` — every flagged delta + Discovery verdict + tripped/cleared/unsettled criteria + overrides, verbatim (script output)
- `startup-brief/validated-baseline.md` — the reconstructed problem the drift audit measures against
- `startup-brief/assumptions.json` — per-assumption leverage/uncertainty scores (ranker input)
- `startup-brief/red-team.md` — the blind solution-red-team's raw challenge
- `startup-brief/reconciliation.md` — draft vs blind adversary; gaps surfaced
- `startup-brief/rounds/round-<N>.md` — per-round provenance when the concept is redesigned + re-run
```

Honesty rule (mirrors the funnel's market research and `/customer-discovery`): never present a `⚠️`/`❌`
drift row, an unsupported top-3 assumption, or a live early-stage premortem pattern as if the concept
were build-ready. The Decision must follow the evidence — a concept that still serves the assumed
problem is a NO-GO/redesign, not a GO with caveats.
