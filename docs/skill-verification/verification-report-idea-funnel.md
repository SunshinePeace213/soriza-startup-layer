# Verification Report — Idea Funnel Build

**Date:** 2026-06-04
**Build under audit:** idea-funnel (`/home/ringo/soriza-startup-layer-idea-funnel`)
**Audit type:** STATIC logic / design-fidelity audit — the funnel was NOT run live; all findings were reproduced by reading source files (engine, agents, skill docs, references, ADRs).

---

## Overall verdict: PASS WITH WARNINGS

7 of 8 raw findings were confirmed: **0 critical, 5 warning, 2 minor.**

No confirmed finding crashes the run, drops/nulls candidates, or corrupts the ledger — the keep-all / pass-through control-flow invariants hold for every candidate that enters the pipeline. The defects are broken *documented contracts* and *audit-surface gaps*, concentrated on two seams: (1) the appeal/resurrect path, which does not behave as the docs promise, and (2) a Gate-2 vocabulary/prompt mismatch that silently weakens disconfirmation routing. None is severe enough to fail the build, but the resurrect contract and the idea-type→lens key mismatch should be fixed before the funnel is relied on for real founder appeals. Hence **PASS WITH WARNINGS**, not PASS.

---

## Confirmed findings by severity

### Critical (0)

None.

---

### Warning (5)

**W1 — Resurrected candidates re-run from Gate 0 instead of re-entering at `killed_at`**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/workflows/idea-funnel-engine.js`
Detail: The narrow resurrect filter (line 113) correctly keeps a settled-killed candidate only when its id is in `resurrectSet`, but `mkCandidate` (lines 35-45) hard-codes `status:'advancing', killed_at:null` for every seed and nothing copies the prior `killed_at` onto the rebuilt candidate; gates only short-circuit on `status==='killed'`, so a resurrected candidate is re-judged from Gate 0 forward — re-paying the expensive Gate 2 sweep and contradicting the "re-enters at killed_at" / "cheap re-runs" contract in ledger-schema.md and SKILL.md.
Fix: Build a `priorSettled` Map keyed by `candidate_id`; on the resurrect path carry the prior `killed_at` onto the candidate, and add a `stageIndexOf(c.killed_at) > thisStage` skip guard in gate0/gate1/gate2 so it resumes at its kill gate.

**W2 — Resurrect ids absent from the current seed set silently never re-enter the funnel**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/workflows/idea-funnel-engine.js`
Detail: `candidates` is derived purely from `seeds` (line 113); `resurrectSet` only widens which seed-derived candidates survive the filter — it never re-injects a prior candidate absent from the current seeds. In thesis mode seeds are regenerated each run with slug-derived ids, so a resurrected id may not reappear, and the resurrect becomes a silent no-op (no candidate, no error, no log).
Fix: Reconstruct any resurrect id missing from current seeds from `priorSettled` (the ledger-reader already returns id/status/killed_at) and merge into `candidates` before the pipeline; emit a log line when a requested resurrect id is found in neither seeds nor the prior ledger so a typo isn't silently dropped.

**W3 — Resurrect/appeal does not re-enter a prior-killed candidate at its kill gate (documented stateful re-run contract unimplemented)**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/workflows/idea-funnel-engine.js`
Detail: CONTEXT.md (lines 115-117), ledger-schema.md (lines 67-73), and SKILL.md (lines 80-84) all promise an appealed candidate re-enters "at the gate that killed it" and that settled candidates aren't re-run. For a pure appeal the founder passes `args.resurrect` but not the full `seeds` list, so the candidate is never constructed; the engine reads `killed_at` from the ledger but never consumes it for re-entry (every candidate enters `pipeline(...)` at gate0, line 162). The stateful contract is documented in three places but not coded.
Fix: Either reconstruct resurrected candidates from the prior ledger and gate them from `killed_at`, or narrow the three docs to the behavior actually built ("re-supply seeds + re-run from gate0") so docs and code agree. (Same root cause as W1/W2, viewed as a design-fidelity docs-vs-code disagreement.)

**W4 — Gate-2 lens routing silently breaks for 3 of 9 idea_types (vocabulary key mismatch) — undermines ADR-0004 roster**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/workflows/idea-funnel-engine.js`
Detail: seed-generator.md (lines 31-33) and expert-lens-map.md tag seeds with compound slash tokens (`trading/fintech`, `content/community`, `services/gig`), but the engine's `lensesFor()` map (lines 19-34) is keyed on split single tokens (`trading`, `fintech`, `content`, `community`, `services`). The key sets don't intersect for those three categories, so a compliant `idea_type:"trading/fintech"` falls through to `M.default` (thiel/munger/bezos) instead of the intended Taleb-led roster — silently bypassing the closed idea-type→lens mapping ADR-0004 makes load-bearing, with no coverage_gap necessarily logged.
Fix: Make one vocabulary canonical across all three surfaces (engine map, seed-generator.md, expert-lens-map.md). Add a normalize step in `lensesFor()` that splits on `/`, tries each token, then falls back to default *and logs a coverage_gap* so future drift degrades gracefully.

**W5 — disconfirmation-judge kill bar weakens the rubric: "high-severity" instead of "strongest" objection**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/agents/disconfirmation-judge.md`
Detail: The rubric (gate-rubrics.md line 49), CONTEXT.md (lines 68/77), and the engine delegation prompt (idea-funnel-engine.js line 154) all define the kill condition as "kill if the STRONGEST objection stands unrebutted" with no severity floor. The agent Bar (line 36) instead says "kill if a HIGH-SEVERITY objection stands unrebutted" — an undefined, strictly narrower bar that flips a should-kill to advance when the strongest standing objection is only moderate (and the agent even contradicts its own line 6/31). This makes the gate less harsh, the opposite of its harsh-by-design intent.
Fix: Change the Bar to "kill if the STRONGEST standing (unrebutted) objection has not been answered by evidence, OR the market read fails, OR score < 50" — drop the undefined "high-severity" qualifier.

---

### Minor (2)

**M1 — `objection_ledger` declared in the judge contract but neither schema-validated nor persisted**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/agents/disconfirmation-judge.md`
Detail: The judge's output contract (line 40) declares `objection_ledger: [{expert, status}]` — the per-objection rebutted/standing audit trail. But the engine `JUDGE_SCHEMA` (idea-funnel-engine.js line 55), the gate2 ledger block (ledger-schema.md line 46), and gate-rubrics.md (line 56) all omit it, so the field is validated-away and never persisted. The kill decision is unaffected (driven by `strongest_unrebutted`); this is an audit-surface fidelity gap, not a kill-logic bug.
Fix: Either add `objection_ledger` to `JUDGE_SCHEMA` and the gate2 ledger-schema block (and gate-rubrics.md) so it is validated and persisted, or drop it from the judge contract so all surfaces agree.

**M2 — disconfirmation-judge told to "carry through" a coverage_gap it is never given — it must GENERATE it**
File: `/home/ringo/soriza-startup-layer-idea-funnel/.claude/agents/disconfirmation-judge.md`
Detail: There is no lens-selector agent at runtime (selection is the deterministic `lensesFor()` JS), so the engine delegates coverage-gap *identification* to the judge (line 154). But the agent body frames coverage_gap as a pass-through it receives — Inputs line 24 "carry it through", Edge case line 49 "always pass through" — with no Process step to generate it. A judge following its body literally emits `coverage_gap:null`, which the schema accepts, silently dropping the gap ADR-0004 requires to be logged ("never a silent miss").
Fix: Rewrite Inputs/Edge-case wording and add a Process step instructing the judge to assess, from `idea_type` and the lenses that actually fired, whether a more decisive roster lens (expert-lens-map.md) was missing; name it in coverage_gap or null — never silently omit it (ADR-0004). Keep "carry through" only as a fallback; make generation the default.

---

## Prioritized fix list

1. **Fix the resurrect/appeal seam (W1 + W2 + W3 — one coordinated change).** Build a `priorSettled` Map by `candidate_id`; reconstruct resurrected ids missing from current seeds; carry over `killed_at`; add stage-skip guards in gate0/gate1/gate2 so resurrected candidates resume at their kill gate; log unresolved resurrect ids. This restores the stateful re-run contract documented in three places and the "cheap re-runs" promise. (If reconstruction is out of scope, instead narrow CONTEXT.md / ledger-schema.md / SKILL.md to match the built behavior.)
2. **Fix the Gate-2 vocabulary mismatch (W4).** Align the engine map, seed-generator.md, and expert-lens-map.md on one canonical idea_type vocabulary, and add a normalize-and-log fallback in `lensesFor()`. Restores ADR-0004 routing for 3 of 9 categories.
3. **Tighten the judge kill bar (W5).** Replace "high-severity" with "strongest standing (unrebutted)" so the agent matches rubric/CONTEXT/engine and the gate stays harsh-by-design.
4. **Make coverage_gap generation explicit (M2).** Rewrite the judge's coverage_gap instructions to identify, not carry through — closes the no-silent-gaps guarantee.
5. **Reconcile the objection_ledger contract (M1).** Add it to schema + ledger, or drop it from the judge contract, so all four surfaces agree.

---

## Scope note

This was a **STATIC logic / design-fidelity audit**: findings were reproduced by reading the engine, agents, skill docs, references, and ADRs. The funnel was **not executed live**, so no runtime/integration behavior, token cost, or agent-output realism was empirically measured.
