# Idea Stage v3 — Phase 3 Build & Verification Record

Phase 3 = the **9-step loop-engineering canon** (`docs/loop-engineering-reference-en.md` v1) and the
issue-closure pass that followed full verification. Phase 1/2 built the older v3 spine
(disconfirm / market-map / solution-design / idea-stage-exit); Phase 3 migrates that spine to the
9-step pipeline and closes the gaps a full T01–T37 / W1–W12 audit surfaced.

## The 9-step migration (git is the record)

The retired stage order was replaced per the migration table (reference §2.11). Commits:
`new_idea` scaffold + templates (T01) → W1 validators/hooks/advance_gate (T02–T08) →
make_brief (T10) → pressure-test α/β orchestrator (steps 4/6) → market-sizing (step 7) →
startup-brief (step 8, T25–T26) → build-poc (step 9) → kill-scan (step 3) + lock_criteria →
customer-discovery 5a/5b (step 5) → β citation teeth (T27). Old stage skills archived to
`.claude/skills-archive/`; affected worker agents repointed to the 9-step canon.

## Issue-closure pass (post-verification)

A full verification (Steps 1–9, T01–T37, W1–W12) found 14 issues. Closure:

| # | Issue | Disposition |
|---|---|---|
| 2 | α-side validators unshipped (test_pressure / test_predictions / test_neutral_brief) | **Fixed** — shipped with green+red fixtures; G4 now auto-passable (gate-chain commit) |
| 5 | persona-contract SubagentStop hook missing | **Fixed** — `persona_contract_check.py` + wired into `objection-lens` (gate-chain commit) |
| 12 | criteria templates only g2–g6 | **Fixed** — g7/g8 (gate-chain commit) + **g9** template added; `test_criteria_templates` guards every `check:auto` `test:` resolves |
| 4 | `build_delta_ledger.py` skill-local, not `scripts/` | **Fixed** — `git mv` to `scripts/`; startup-brief invocation repointed (canon path) |
| 7 | ledger-audit (T24) absent | **Fixed** — `scripts/ledger_audit.py` (three-way gates↔decision-log↔criteria + ledger/prediction sanity) + 6 tests; first report at `reports/ledger-audit.md` |
| 6 | canary/isolation test (T14) absent | **Fixed** — `tests/schemas/test_canary_isolation.py` guards the config that enforces independent-round isolation (no spawn tool on a seat; sibling-verdict = cross-exam-round-only; contract hook wired) |
| 8 | nightly reports (T29) + Brier (T34) absent | **Fixed** — `render_dashboard.py` (dual-state audit, §3.3 declared-vs-derived drift alarm) + `calibration_review.py` (Brier) → `reports/`; 5 tests |
| 10 | CLAUDE.md W2 §6 / W5 §7 inserts were placeholder comments | **Fixed** — real §6 Two-Round Protocol + §7 Hook Behaviour sections |
| 11 | `soriza-operator-os` orphan (no STATE.md) | **Fixed** — truthful schema-v2 STATE backfilled (`status: blocked`, `gates: {}` — no fabricated passes; founder decides re-enter vs archive) |
| 14 | prompt-architect cited deleted `idea-funnel-engine.js` | **Fixed** — repointed to the live `/artifact-eval` → `artifact-eval.js` exemplar (6 refs) |
| 13 | no Phase-3 build record | **Fixed** — this file |
| 9 | deprecation guard (T35) | **Partial** — `deprecated_redirect.py` hook built + 6 tests; **`.claude/settings.json` `UserPromptExpansion` wiring needs founder approval** (agent self-modification of active hooks is gated) |
| 1 | "T38" | **N/A** — the reference defines T01–**T37** only; there is no T38 |
| 3 | Rule-Zero evidence track (≥5 interviews; Gate-2 external founder) | **Not agent-fixable by design** — §11.4 never-automated; fabricating interviews would violate Rule Zero. Founder-only |

## Verification

- **`uv run pytest -q`: 139 passed** (was 93 pre-migration-fixes, 118 at the inherited gate-chain commit; +21 from this pass: deprecation 6 · ledger-audit 6 · reports 5 · canary 4).
- Every new validator/script ships with a red fixture or a planted-drift test that bites (doc-TDD).
- `ledger_audit --all`, `render_dashboard`, `calibration_review` run clean against the live ideas
  (0 drift, 0 resolved predictions — accurate: no idea is past step 2).

## Known follow-ups (founder / environment, not code gaps)

- **Wire the deprecation guard:** add the `UserPromptExpansion` block (shown in the verification report) to `.claude/settings.json`.
- **Evidence track:** the loop must close through reality — Gate-1 (≥5 interviews) and Gate-2 (external founder) are the founder's to run.
- **Optional (W9 L3):** `WorktreeCreate/Remove` lifecycle hooks for 2-idea parallelism; the harness already provides worktrees.
- **Bezos seat (T33):** available now via the parameterized `objection-lens` (slug), no separate persona file by design.
