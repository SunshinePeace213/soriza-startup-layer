# Funnel ledger — schema & run layout

The ledger is the funnel's scoreboard AND its cross-run memory (stateful, keyed by Candidate ID).
**This file is self-contained** — it is the single source of truth for the ledger at runtime. No agent
reads CONTEXT.md or the ADRs to write or read the ledger; the schema below is authoritative.

Two things the ledger must make true (v2):

1. **Demand-strength and founder-fit are SEPARATE, unfused columns.** The idea-axis demand signal
   (founder-BLIND) and the fit-axis fit score (founder-AWARE) are recorded and displayed side by side.
   They are **never blended into one hidden number.** Demand is the primary rank key; fit is shown
   alongside and used only as a tiebreaker.
2. **The board is never silently empty.** Every Candidate is persisted with its outcome. Sub-cap
   survivors are kept **alive and resurrectable** (`queued-alive`), not killed. The desk kills only on
   objective, checkable criteria (see "What may kill" below).

## Run-folder layout

```
docs/ideas-stages/
  _funnel-runs/
    <run-label>/                 ← run-label = <thesis-slug>-NN (NN = next integer; agents derive it by Glob, never a timestamp)
      ledger.md                  ← the board (human-readable table)
      ledger.json               ← machine state (the source of truth re-runs read)
      shortlist.md              ← the ≤K survivors presented for approval
  <candidate-slug>/             ← one per ADVANCING candidate (the existing per-idea namespace)
      hypothesis.md             ← written by the hypothesis (testability) stage for survivors
      market-research.md        ← written by the demand-detection sweep for survivors
      disconfirmation-brief.md  ← open assumptions + interview questions (NOT a verdict)
      customer-discovery/
        cowork-runpack.md       ← sealed Phase A run-pack, written for the top-K survivor(s)
```

All paths are resolved against the **repo root**, never the caller's CWD. (A v1 bug let a polluted CWD
send every write nowhere and killed ideas by-default on "missing" files — agents must anchor at the
repo root regardless of who invoked them.)

## Candidate ID

`cand-<short-slug>` — **stable across runs**, derived from the seed title (lower-kebab, deduped with a
numeric suffix on collision). The ID is what makes the ledger stateful: a re-run matches by ID, so a
Candidate carries its history (and its resurrect eligibility) forward between runs.

## The two axes (never fuse them)

| Axis | Source | Founder-aware? | Where it lives |
|---|---|---|---|
| **demand-strength** | demand-detection stage (reachable niche showing real demand — who pays / complains / hacks a workaround) | **BLIND** — judged on the idea's own merits | `demand` field + its own board column; **primary rank key** |
| **founder-fit** | fit-screen stage (durable capability/legal/geo/language; money/time/runway ignored) | **AWARE** — reads the profile as data | `fit` field + its own board column; **tiebreaker only** |

Record both. Display both. **Do not compute a single combined score.** A re-run or an appeal must be
able to read each axis independently.

## What may kill (the only desk eliminations)

The desk **almost never kills.** Weak-but-not-fatal ideas **rank low and stay `queued-alive`** — "no
moat / incumbent exists / market small / they might not pay" are interview questions and a rank, never
deaths. The complete list of `killed_at` values:

| `killed_at` stage | Kills ONLY on (objective, checkable) |
|---|---|
| `fit-screen` | **durable-impossible** founder mismatch — can't legally / linguistically / geographically serve it, or needs hardware / heavy-regulated licensing. **Money / time / runway ignored.** |
| `hypothesis` | cannot be made into a **testable** hypothesis (who / how-often / how-severe / status-quo) after one sharpening pass |
| `checkpoint` | one of the **3 fatal flaws**: ① illegal/impossible · ② demand **provably negative** (graveyard of unused identical free tools, documented failed clones, review-mining shows the pain isn't felt) · ③ **no reachable audience** at all |

`disconfirmation` and `demand-detection` **never kill** — disconfirmation emits a Brief (open
assumptions → interview questions), demand-detection emits a signal. A fatal flaw they *surface* is
applied at the `checkpoint`, with the evidence cited.

## ledger.json (the source of truth)

```json
{
  "run_label": "ai-native-services-apac-03",
  "founder_profile_capacity": { "time": "part-time", "team": "solo", "k_default": 1 },
  "n": 10,
  "k": 1,
  "candidates": [
    {
      "id": "cand-cross-border-escrow",
      "title": "...",
      "idea_type": "fintech",
      "seed": { "problem": "...", "who": "...", "why_now": "..." },
      "status": "queued-alive",
      "killed_at": null,
      "rank": 3,
      "demand": { "strength": 64, "reachable_niche": "...", "where_they_congregate": "...", "unsolved_complaints": ["..."], "signals": ["pays", "complains", "workaround"] },
      "fit":    { "score": 71, "reasons": "...", "hard_fail": null },
      "stages": {
        "fit_screen":       { "verdict": "keep", "fit_score": 71, "reason": "...", "hard_fail": null },
        "hypothesis":       { "verdict": "advance", "score": 68, "testable": true, "hypothesis": { "who": "...", "how_often": "...", "how_severe": "...", "status_quo": "...", "sentence": "..." }, "hypothesis_path": "docs/ideas-stages/cand-cross-border-escrow/hypothesis.md" },
        "disconfirmation":  { "verdict": "brief", "open_assumptions": [{ "expert": "nassim-taleb-perspective", "assumption": "...", "interview_question": "...", "status": "open" }, { "expert": "...", "assumption": "...", "status": "closed-by-fact", "fact": "legality confirmed" }], "coverage_gap": "no payments-regulatory lens", "brief_path": "docs/ideas-stages/cand-cross-border-escrow/disconfirmation-brief.md" },
        "demand_detection": { "verdict": "signal", "strength": 64, "reachable_niche": "...", "unsolved_complaints": ["..."], "market_path": "docs/ideas-stages/cand-cross-border-escrow/market-research.md" },
        "checkpoint":       { "verdict": "queued-alive", "fatal_flaw": null, "rank": 3, "reason": "below the K=1 cap; alive for resurrect" },
        "phase_a":          null
      }
    }
  ]
}
```

Notes on the record:
- `demand` and `fit` are **promoted to top-level** (in addition to living inside their stage) precisely
  so they read as two independent axes, not a blend.
- `disconfirmation.open_assumptions` is a Brief, not a verdict. An objection is `closed-by-fact` **only
  when a hard, checkable fact settles it** (legality, technical feasibility); everything subjective
  (demand, willingness to pay, behavior) stays `open` and becomes an interview question.
- `phase_a` is non-null only for top-K survivors; it carries `{ verdict, reachable, runpack_path,
  reason }`. Phase A produces **sealed drafts only** — nothing is ever sent.
- `coverage_gap` records an ideal-but-missing objection lens (the selector logs it, never auto-mints).

## `status` values

- **shortlisted** — cleared every desk stage AND is within the top-K cap. Gets a sealed Phase A pack.
- **queued-alive** — a **sub-cap survivor**: cleared the desk (no fatal flaw) but ranked below K. Stays
  alive in the ledger and is **resurrectable** — on a re-run it is the first to be promoted when a
  shortlisted Candidate resolves or K is raised. Never treated as a kill.
- **advancing** — still in flight (passed the stages run so far; the run hasn't reached the checkpoint).
- **killed** — failed one of the objective desk eliminations above. Stays killed on re-run **unless**
  resurrected. Persisted with its `killed_at` stage and one-line reason — the ledger is the appeal
  surface; no silent kills.
- **resurrected** — the founder flipped a `killed` (or re-promoted a `queued-alive`) Candidate; it
  re-enters at its `killed_at` stage on the next run and runs forward from there.

## ledger.md (the board)

A markdown table, one row per Candidate. Columns:

`ID · Title · Fit-screen · Hypothesis · Disconfirmation · Demand-detection · Phase A · **Demand-strength** · **Founder-fit** · Status · Rank · Kill reason · Coverage gap`

- **Demand-strength** and **Founder-fit** are **two distinct columns**, side by side, never merged —
  this is the load-bearing visual contract of v2 (idea axis vs founder axis, unfused).
- Each per-stage cell = `✅ score` / `❌ score` for the gating stages (Fit-screen, Hypothesis,
  Checkpoint); for the no-kill stages it shows the artifact state — Disconfirmation = `brief (k open)`,
  Demand-detection = the demand signal, Phase A = `sealed` / `—`.
- **Sort:** shortlisted first, then `queued-alive` and `advancing` by **demand-strength** desc (fit
  breaks ties), then `killed` by demand-strength desc.
- A **header block** reports the funnel counts (entered → per-stage survivors → `queued-alive` →
  shortlisted) and the cap **K** with its profile justification, plus **n** (seeds generated).
- The board is **never empty** unless literally every seed hit a fatal flaw; sub-cap survivors always
  appear as `queued-alive`.

## Params

- **n = 10** seeds default (overridable). **K = 1** Phase-A pack default (overridable; derived from the
  founder profile's capacity).
- The **cap K** is applied fresh each run over all currently-advancing Candidates; everything below the
  cap that cleared the desk becomes `queued-alive` (not killed).

## Re-run / resurrect contract

- A re-run reads the latest `_funnel-runs/*/ledger.json` via the **ledger-reader** agent. Candidates
  whose `status = killed` are skipped (their stages are not re-run) UNLESS their ID is in
  `args.resurrect`. `queued-alive` Candidates are carried forward and re-considered against the cap.
- A resurrected Candidate re-enters at its `killed_at` stage and runs forward from there.
- New seeds (not present in the prior ledger) run from the start (fit-screen).
- The cap is applied fresh each run over all currently-advancing Candidates; when a shortlisted
  Candidate resolves, the top-ranked `queued-alive` is promoted into the freed cap slot.

---

> **Human background only (not read at runtime):** the rationale for the stateful ledger, the
> coverage-gap field, and the closed expert roster lives in `CONTEXT.md` ("Funnel ledger") and the ADRs
> (`docs/adr/`). Those documents are **optional context for humans** — no agent reads them to operate
> the ledger. This file is the runtime source of truth, so the skill folder stays portable when copied
> to another repo.
