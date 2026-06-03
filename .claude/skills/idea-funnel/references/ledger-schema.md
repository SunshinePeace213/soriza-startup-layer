# Funnel ledger — schema & run layout

The ledger is the funnel's scoreboard AND its cross-run memory (stateful, keyed by Candidate ID).
See [CONTEXT.md](../../../../CONTEXT.md) → "Funnel ledger" and
[ADR-0004](../../../../docs/adr/0004-gate2-uses-a-closed-expert-roster-gaps-are-logged.md) (coverage-gap field).

## Run-folder layout

```
docs/ideas-stages/
  _funnel-runs/
    <run-label>/                 ← run-label = <thesis-slug>-NN (NN = next integer; agents derive it by Glob, never a timestamp)
      ledger.md                  ← the board (human-readable table)
      ledger.json               ← machine state (the source of truth re-runs read)
      shortlist.md              ← the ≤K survivors presented for approval
  <candidate-slug>/             ← one per ADVANCING candidate (the existing per-idea namespace)
      hypothesis.md             ← written by sharpen-gate for Gate-1 survivors
      market-research.md        ← written by the Gate-2 evidence sweep for survivors
      customer-discovery/
        cowork-runpack.md       ← written by cd-design-gate for Shortlist survivors
```

## Candidate ID

`cand-<short-slug>` — stable across runs, derived from the seed title (lower-kebab, deduped with a
numeric suffix on collision). The ID is what makes the ledger stateful: a re-run matches by ID.

## ledger.json (the source of truth)

```json
{
  "run_label": "ai-native-services-apac-03",
  "founder_profile_capacity": { "time": "part-time", "team": "solo", "k_default": 1 },
  "k": 1,
  "candidates": [
    {
      "id": "cand-cross-border-escrow",
      "title": "...",
      "seed": { "problem": "...", "who": "...", "why_now": "..." },
      "status": "killed | advancing | shortlisted | resurrected",
      "killed_at": "gate-2 | null",
      "rank": 3,
      "gates": {
        "gate0_fmf":   { "verdict": "advance", "score": 78, "reason": "..." },
        "gate1_sharpen": { "verdict": "advance", "score": 71, "reason": "...", "hypothesis": { "who": "...", "how_often": "...", "how_severe": "...", "status_quo": "...", "sentence": "..." }, "hypothesis_path": "docs/ideas-stages/.../hypothesis.md" },
        "gate2_disconfirmation": { "verdict": "kill", "score": 38, "reason": "Taleb ruin objection unrebutted", "strongest_unrebutted": "...", "objection_ledger": [{ "expert": "nassim-taleb-perspective", "status": "standing" }], "coverage_gap": "no payments-regulatory lens" },
        "gate3_cd_design": null
      }
    }
  ]
}
```

`status` values:
- **killed** — failed a gate's bar; stays killed on re-run unless resurrected.
- **advancing** — passed all gates run so far, still in flight.
- **shortlisted** — cleared all desk gates and is within the top-K cap.
- **resurrected** — founder flipped a killed candidate; re-enters at `killed_at` on the next run.

## ledger.md (the board)

A markdown table, one row per Candidate, columns: `ID · Title · G0 · G1 · G2 · G3 · Status · Rank ·
Kill reason · Coverage gap`. Each gate cell = `✅ score` / `❌ score`. Sorted: shortlisted first, then
advancing, then killed by score desc. A header block reports the funnel counts (in → per-gate
survivors → shortlist) and the cap K with its profile justification.

## Re-run / resurrect contract

- A re-run reads the latest `_funnel-runs/*/ledger.json` via the **ledger-reader** agent. Candidates
  whose `status = killed` are skipped (their gates are not re-run) UNLESS their ID is in `args.resurrect`.
- A resurrected Candidate re-enters at `killed_at` and runs forward from there.
- New seeds (not present in the prior ledger) run from Gate 0.
- The cap is applied fresh each run over all currently-advancing Candidates.
