# Re-Verification Report — Idea Funnel Build (FOLLOW-UP)

**Date:** 2026-06-04 (re-verify)
**Build under audit:** idea-funnel (`/home/ringo/soriza-startup-layer-idea-funnel`)
**Predecessor:** `verification-report-idea-funnel.md` (2026-06-04)
**Audit type:** STATIC logic / design-fidelity re-audit. The funnel was NOT run live; every status below was reproduced by reading the source files (engine, agents, skill docs, references, ADRs).
**Purpose:** Confirm the 7 fixes for the prior findings **W1, W2, W3, W4, W5, M1, M2**, and sweep the touched seams for new regressions.

---

## Overall verdict: PASS WITH WARNINGS

All **7 prior findings are RESOLVED** (5 warning + 2 minor, now closed). The core invariants the original audit cared about — resurrect/appeal re-entry at the kill gate, full-record reconstruction of absent resurrect ids, compound idea-type→lens routing, the "strongest unrebutted objection" kill bar, and the `objection_ledger` / `coverage_gap` contracts — are now actually coded and mutually consistent across engine, agents, and references.

However, the regression sweep confirmed **4 new findings on the same seams the fixes touched: 0 critical, 1 warning, 3 minor.** None crashes the run, drops/nulls a candidate, or corrupts the ledger. The single warning is a **latent contract gap** the resurrect fix load-bearingly depends on but does not lock down (a Gate-2 resurrect can silently re-judge against an empty hypothesis if the writer mirrors the documented schema). The three minors are documentation / defense-in-depth drift adjacent to the M1 fix and a pre-existing ADR filename stale-reference.

Because all 7 are resolved but a new **warning** remains on the resurrect seam, the build is **PASS WITH WARNINGS**, not a clean PASS.

---

## Status of the 7 prior findings

| ID | Dimension | Status | Note |
|----|-----------|--------|------|
| **W1** | resurrect-seam | **RESOLVED** | Engine derives `resumeFrom` from `killed_at` via `STAGE_INDEX={gate-0:0,gate-1:1,gate-2:2}` (lines 48,135) and stamps it on every resurrected candidate. gate0 skip-guard `resumeFrom > 0` (l.159), gate1 `resumeFrom > 1` (l.170): killed@gate-0 re-runs 0/1/2, @gate-1 skips 0 re-runs 1/2, @gate-2 skips 0+1 re-runs 2 — matches the "re-enters at the gate that killed it" contract; earlier gates not re-paid. |
| **W2** | resurrect-seam | **RESOLVED** | Engine reconstructs resurrect ids absent from current seeds. Loop (l.133–150) pushes a fully-built candidate into `candidates` when `byId` lacks the id; a pure appeal with no matching seed is no longer a silent no-op. Unresolved ids (in neither seeds nor prior ledger) are logged (l.151–153). |
| **W3** | resurrect-seam | **RESOLVED** | `ledger-reader` now returns full prior records — `READER_SCHEMA.resurrected` items carry `{id,title,seed,idea_type,killed_at,gates}` (engine l.65); `ledger-reader.md` Output schema (l.31) + Process step 4 match. Engine consumes `killed_at` (resumeFrom) and `gates` (restored l.138 / rebuilt l.146). Docs and code agree (CONTEXT.md, ledger-schema.md, SKILL.md). |
| **W4** | lens-vocab | **RESOLVED** | `LENS_MAP` (l.19–34) has DIRECT keys for every compound `idea_type`: `trading/fintech`→[taleb,munger,musk], `content/community`→[bezos,naval,garry-tan], `services/gig`→[eisenmann,bezos,horowitz] — matching the non-default rows in `expert-lens-map.md`. `lensesFor` (l.38–43) tries exact key → split-token fallback → default; `lensTypeKnown` mirrors it so only genuinely-unknown types trigger the gate2 coverage-gap warning (l.184). All 9 perspective slugs confirmed to have skill dirs. |
| **W5** | judge-agent | **RESOLVED** | Agent kill bar (l.41–44) now reads: kill if the strongest standing (unrebutted) objection is unanswered by evidence, OR market read fails, OR score < 50 — "No severity floor." Matches gate-rubrics.md (l.47–48), CONTEXT.md (l.69,77), and the engine delegation prompt (l.197). Line 33 uses severity only as a tiebreaker to pick *which* objection is strongest, not as a floor — no contradiction. |
| **M1** | judge-agent | **RESOLVED** | `objection_ledger` present and shape-consistent in all three required artifacts: JUDGE_SCHEMA (engine l.69, array of `{expert,status}`), ledger-schema.md Gate-2 block (l.46), and the agent output contract (disconfirmation-judge.md l.47). |
| **M2** | judge-agent | **RESOLVED** | Agent now GENERATES `coverage_gap` rather than only carrying it. Process step 5 (disconfirmation-judge.md l.36–39) instructs judging — from `idea_type` + lenses that fired — whether a more decisive roster lens was missing; name it or set `null`. Inputs (l.24–25) and edge-case note (l.56–57) reinforce self-assessment; `expert-lens-map.md` exists, so the instruction is actionable. |

**Roll-up:** 7 / 7 RESOLVED. The original 5-warning / 2-minor surface is fully closed.

---

## New confirmed regressions (sweep of the touched seams)

All four were re-verified against the real files; all citations hold.

### Critical (0)
None.

### Warning (1)

**N1 — Gate-2 resurrect depends on the writer persisting the full `gate1_sharpen.hypothesis` OBJECT, which `ledger-schema.md` only documents as `hypothesis_path`**
**File:** `/home/ringo/soriza-startup-layer-idea-funnel/.claude/skills/idea-funnel/references/ledger-schema.md` (also `idea-funnel-engine.js` l.185–197; `ledger-writer.md`)
**Detail:** When a gate-2-killed candidate is resurrected, gate2 re-runs and feeds the objection lenses and judge from `c.gates.gate1_sharpen.hypothesis` (engine l.185, used l.187,193,197). That object only survives the round-trip if the ledger-writer persisted the full `SHARPEN_SCHEMA` verdict (which includes the `hypothesis` object) and `ledger-reader` returns it via the unconstrained `gates:{type:'object'}` (engine l.65). But the `ledger-schema.md` gate1_sharpen example (l.45) shows only `{verdict, score, reason, hypothesis_path}` — the `hypothesis` object is absent, with no qualifier marking the field list as partial. `ledger-writer.md` is told both "write exactly what you're given" (preserves it) AND "Follow references/ledger-schema.md exactly" (whose example drops it) — a genuine instruction conflict on a haiku-class writer. If the writer mirrors the documented example, `c.gates.gate1_sharpen.hypothesis` is `undefined` on resurrect and gate2 runs with `hypothesis=null` — a silently degraded (not crashed) disconfirmation judgment on exactly the appeal path W1–W3 were meant to make first-class. There is no engine fallback to read `${ns}hypothesis.md` from disk. Verified: there is no deterministic crash — realization depends on the LLM's interpretation — hence warning, not critical.
**Fix:** Add the `hypothesis` object to the gate1_sharpen example in `ledger-schema.md` (l.45) so the persisted shape is explicit, AND/OR have the engine defensively fall back to reading `${ns}hypothesis.md` at l.185 when `c.gates.gate1_sharpen.hypothesis` is missing. Lock the resurrect→gate2 path so it cannot silently lose the hypothesis.

### Minor (3)

**N2 — `gate-rubrics.md` Gate-2 Output line omits `objection_ledger` (doc drift left by the M1 fix)**
**File:** `/home/ringo/soriza-startup-layer-idea-funnel/.claude/skills/idea-funnel/references/gate-rubrics.md` (l.56)
**Detail:** The M1 fix added `objection_ledger` to three places (JUDGE_SCHEMA at engine l.69, the ledger-schema.md Gate-2 block l.46, and the agent output contract at disconfirmation-judge.md l.47) but NOT to the Gate-2 rubric's own Output spec. Line 56 still reads `Output: { verdict, score, reason, strongest_unrebutted, market, coverage_gap }` — `objection_ledger` absent. This is the canonical per-gate output contract the agent body cites as authoritative ("matching the rubric"), so the four artifacts no longer agree on the judge's output shape. Not a runtime break — JUDGE_SCHEMA does not mark `objection_ledger` required, so a missing field passes validation — but it is exactly the contract drift M1 was meant to eliminate.
**Fix:** Update gate-rubrics.md l.56 to `Output: { verdict, score, reason, strongest_unrebutted, objection_ledger, market, coverage_gap }` so all four artifacts list the same fields.

**N3 — Engine Gate-2 delegation prompt never instructs the judge to emit `objection_ledger`**
**File:** `/home/ringo/soriza-startup-layer-idea-funnel/.claude/workflows/idea-funnel-engine.js` (l.197)
**Detail:** The judge delegation prompt tells the judge to kill on the unrebutted-objection / market-read bar and to name `coverage_gap`, but never asks for `objection_ledger`. The field is produced only because the agent body (disconfirmation-judge.md l.47) lists it in its own output schema. Because JUDGE_SCHEMA marks only `candidate_id/verdict/score/reason` required (l.69), `objection_ledger` is optional at the validation layer — so if a run leans on the prompt over the agent's static contract, the per-objection ledger the writer/board expect (ledger-schema.md l.46) could come back empty/absent with no error. Low likelihood given the agent body instructs it (Process step 1 makes rebutted/standing load-bearing), so not currently reproducible — a missing-backstop / defense-in-depth gap, not an active bug.
**Fix:** Add `objection_ledger` (and `strongest_unrebutted`) to `JUDGE_SCHEMA.required` (stronger guard), or extend the l.197 prompt to explicitly request "an `objection_ledger` entry `{expert, status}` for every objection you adjudicated."

**N4 — ADR-0002 still names the workflow `idea-funnel.js`; the actual file and SKILL.md launcher are `idea-funnel-engine.js`**
**File:** `/home/ringo/soriza-startup-layer-idea-funnel/docs/adr/0002-validator-runtime-is-a-dynamic-workflow.md` (l.12)
**Detail:** ADR-0002's live "Decision" statement describes the runtime as "(`.claude/workflows/idea-funnel.js`, invoked as `/idea-funnel`)". The real file is `.claude/workflows/idea-funnel-engine.js` and SKILL.md Step 2 (l.58) correctly points the Workflow tool at `idea-funnel-engine.js`. No `idea-funnel.js` file exists anywhere in the repo. The rename is documented as intentional in `docs/skill-designs/idea-funnel.md` (As-built deviation #1) to avoid a `/command` name collision, but ADR-0002 l.12 was not updated. Pre-existing doc/code drift — not introduced by these fixes and outside the W1–W3 seam — but a genuine doc/code disagreement adjacent to the W3 "docs and code now agree" check. No runtime impact: the engine is launched by path from SKILL.md, not from the ADR.
**Fix:** Update ADR-0002 l.12 to reference `.claude/workflows/idea-funnel-engine.js` so all surfaces name the same file.

---

## Prioritized follow-up fix list

1. **Lock the resurrect→gate2 hypothesis path (N1, warning).** Add the `hypothesis` object to the gate1_sharpen example in ledger-schema.md AND/OR add an engine disk-fallback to `${ns}hypothesis.md` at l.185. This is the only new finding on a live behavioral path and protects the appeal path W1–W3 made first-class.
2. **Finish the M1 contract sweep (N2, minor).** Add `objection_ledger` to gate-rubrics.md l.56 so all four output-contract surfaces agree.
3. **Add an `objection_ledger` backstop (N3, minor).** Put it in `JUDGE_SCHEMA.required` or name it in the l.197 delegation prompt.
4. **Refresh the stale ADR filename (N4, minor).** Point ADR-0002 l.12 at `idea-funnel-engine.js`.

---

## Scope note

This was a **STATIC** re-audit: every status and finding was reproduced by reading the engine, agents, skill docs, references, and ADRs. The funnel was **not executed live**, so no runtime/integration behavior, token cost, or agent-output realism was empirically measured. N1 and N3 in particular are *latent / non-deterministic* contract gaps whose realization depends on LLM (writer/judge) interpretation, not on a deterministic code path — they are correctly rated as latent, not as guaranteed failures.
