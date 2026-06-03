# Idea-Stage Skill Verification Report

**Date:** 2026-06-04
**Scope:** `generate-ideas`, `sharpen-hypothesis`, `pressure-test`, `market-research`, `customer-discovery`, `solution-design`
**Method:** Dynamic multi-agent workflow (`verify-startup-skills`, run `wf_0527f92d-fa6`) — 23 agents, ~466s. Per-skill audit on an 8-dimension rubric grounded in this repo's own prompt-architect doctrine (`anti-patterns.md`, `4-8-principles.md`, `thariq-principles.md`, `skill-template.md`), each finding re-opened and adversarially verified by an independent skeptic, plus 3 cross-cutting integration lenses (subagent-reference integrity, pipeline-routing consistency, skill/command references). Only **confirmed** findings appear below — false positives were dropped during verification.

---

## Overall verdict: HIGH QUALITY — minor fixes

Yes — these are genuinely high-quality, 4.8-tuned skills: clean anti-pattern hygiene, frontmatter within the 1,536-char budget with real founder phrasings, effort-as-the-lever throughout, and production-grounded Gotchas. The cross-over is **structurally sound** — all 6 registered subagents resolve with no orphans or dangling dispatches, all 11 panel personas exist on disk, and the file-contract chain (`ideas.md → hypothesis.md → pressure-test.md → market-research.md → customer-discovery.md → solution-design.md`) is coherent end-to-end.

It does **not** ship perfectly clean: two confirmed bugs misfire at runtime (CD-1 scorer wrong-path exit-2; PT-1 anti-thesis slug silently inverts the central pass rule) and a recurring effort-pin contradiction (SRI-1/SRI-2) would downgrade the two heaviest stages if followed literally. **Fix those four and it ships.**

---

## Per-skill scorecard

| Skill | Score | Verdict | One-liner |
|---|---|---|---|
| `solution-design` | 4.8 | ✅ ship | Strongest skill: tight triggering, two verified stdlib scripts, blind separate-context red-team with matching tools/paths + Glob fallback. Flaws: effort-pin misstatement (SD-1) and a scorecard parser that drops INCONCLUSIVE/MANUAL/ERROR (SD-3). |
| `generate-ideas` | 4.6 | ✅ ship | Model-citizen on-ramp: clean parallel dispatch of `startup-idea-researcher`, schema/path match the agent verbatim, correct `idea-exploration` boundary, only correct effort-pin handling in the suite. One minor contradiction (GI-1). |
| `pressure-test` | 4.6 | minor-fixes | Strong orchestration: all 11 personas resolve via glob, `compute_verdict.py` faithfully implements the truth table, refuse-rather-than-degrade is correct. Major: scorer trusts `--anti-thesis` blindly (PT-1). |
| `market-research` | 4.6 | minor-fixes | Well-architected four-workstream fan-out, correct contracts, uniquely-resolving Glob fallback. Bugs: misstates worker effort as `high` (agents pin `xhigh`) (MR-1/SRI-1); passes a `<RISKS>` input nothing sources (MR-2). |
| `customer-discovery` | 4.6 | minor-fixes | Doctrine-compliant two-phase design, locked thresholds, independent bias-check; both workers match specs. Major: Step S3 calls the scorer with repo-relative paths the CWD won't resolve (CD-1). Dead Skill grant (CD-2). |
| `sharpen-hypothesis` | 4.4 | minor-fixes | Solid single-file entry point, intact refusal path. Output folder is `<project-name>` in prose but `<slug>` in operative steps (SH-1); missing outbound boundary clause (SH-2) and recommended-effort note (SH-3). |

---

## Cross-over integrity (subagents / commands / skills)

**Structurally sound, with one recurring defect class.**

- **Subagent contracts:** all six registered agents resolve and are dispatched (no orphans, no dangling references). Doc-path handoffs match end-to-end: `market-researcher`/`competitor-steelman` write the `workstream-briefs`-mapped provenance docs; `customer-discovery-personas-worker` writes `persona-<slug>.md`; `customer-discovery-bias-check` is prose-only with `tools: Read` and no Write exactly as the skill states; `solution-red-team` writes `solution-design/red-team.md` as its frontmatter expects. All `parallel` / `one-per-X` / `blind` / `separate-context` claims match how each agent is built.
- **Pipeline routing:** the reads-X / writes-Y file chain is coherent; every skill's precedence and "what's next" gating agrees with its neighbours; the `docs/idea-exploration/<theme-slug>` vs `docs/ideas-stages/<slug>` namespace split is intentional and consistently guarded; the `idea-to-hypothesis` orchestrator reads exactly the headings `generate-ideas` writes without touching `docs/ideas-stages`.
- **`/name` and Skill references:** every slash-name across the 6 skills, 6 agents, and 2 workflows resolves. `pressure-test` deliberately dispatches isolated subagents that **Read** each `*-perspective/SKILL.md` rather than calling them through the Skill tool (Skill correctly absent from its allowed-tools, with a documented isolation rationale) — a **sound deviation**, not a defect, because inline role-play would collapse the personas into one averaged voice.
- **The one systemic problem:** `market-research:145` and `solution-design:187` both assert their workers pin `high` and instruct "dispatch at high effort," but `market-researcher`, `competitor-steelman`, and `solution-red-team` all pin `effort: xhigh`. A misstatement *plus* a re-set instruction that would downgrade the heaviest, most reasoning-sensitive stages if an operator followed it literally.

---

## Prioritized fix list (confirmed findings only)

### Blocking — fix before relying on the affected stage (the "fix these four")

| # | Sev | Where | Problem → Fix |
|---|---|---|---|
| 1 | major | `customer-discovery/SKILL.md:164-167` + `references/kill-criteria-anchoring.md:98-99` | **CD-1** Scorer invoked with repo-relative JSON args (`customer-discovery/kill-criteria.json`, …) but files live at `docs/ideas-stages/<slug>/customer-discovery/…`; default CWD is repo root → `is_file()` fails → exits 2 "not a file". Synthesis phase can't score. **Fix:** prefix both args with `docs/ideas-stages/<slug>/` (both sibling scorer skills already do). |
| 2 | major | `pressure-test/scripts/compute_verdict.py:130,155` + `SKILL.md:89,150` | **PT-1** Script tags the anti-thesis only via exact `slug == args.anti_thesis` and never verifies the slug matched a rebuttal file. On a typo/slug-vs-name mismatch, no seat is tagged, `per_expert.get(...)` returns `None`, and the anti-thesis's RESTATE-HARDER counts in `restate_non_anti` — **silently inverting the central pass rule, with no warning**. **Fix:** if `anti_thesis not in per_expert`, emit `anti_thesis_warning` and exit non-zero unless `--allow-malformed`; document the exact-slug requirement in Step 8. |
| 3 | major | `market-research/SKILL.md:145` (and `:106`) vs `agents/market-researcher.md:12`, `competitor-steelman.md:12` | **SRI-1/MR-1** Says workers pin `high` and instructs "dispatch at high effort," but both agents pin `xhigh`. A literal follow downgrades the heaviest research stage. **Fix:** mirror `generate-ideas` — "Do not set model/effort on the dispatch — the frontmatter pins Opus + `xhigh`." |
| 4 | major | `solution-design/SKILL.md:187` vs `agents/solution-red-team.md:13` | **SRI-2/SD-1** Same class, single agent. Says "pins Opus + `high`" but `solution-red-team.md:13` pins `xhigh`. The blind red-team is the load-bearing adversary. **Fix:** "Do not set model/effort — frontmatter pins Opus + `xhigh`." |

### Polish — quality/consistency, non-blocking

| # | Sev | Where | Problem → Fix |
|---|---|---|---|
| 5 | minor | `sharpen-hypothesis/SKILL.md` (`:15,:186` `<project-name>` vs `:61,67,180,181` `<slug>`) | **SH-1** Output folder named two ways; operative write steps correctly use `<slug>`, only prose/recap use `<project-name>`. Documentation inconsistency (verifier downgraded major→minor). **Fix:** replace `<project-name>`→`<slug>` for the folder; rename the human-readable title token to `<idea-name>` + one clarifying line. |
| 6 | minor | `market-research/SKILL.md:178` vs Steps 1 & 3 | **MR-2** Steelman template passes `<RISKS or "none">` but the workflow never extracts open risks / anti-thesis flag from `pressure-test.md`. **Fix:** in Step 1, also pull the open-risks / anti-thesis section and hold it for the steelman dispatch. |
| 7 | minor | `market-research/SKILL.md:110` (deep-mode W2/W3 write paths) | **SRI-3** Deep-mode branch hardcodes non-dated `market-research/review-synthesis.md` / `market-sizing.md` while Step 4 parameterizes `<PROVENANCE_DIR> = market-research/<ISO-date>/`. Append-round + deep-mode could clobber prior round. **Fix:** substitute `<PROVENANCE_DIR>` in both deep-mode paths. |
| 8 | minor | `pressure-test/SKILL.md:153` vs `compute_verdict.py:133-139` | **PT-2** Step 8 prose claims the script always prints `per_expert`/`tally`, but the malformed branch prints only `{verdict:null, malformed, message}`. **Fix:** scope the key list to the success case and document the malformed shape. |
| 9 | minor | `solution-design/scripts/build_delta_ledger.py:124-152` vs `customer-discovery/references/discovery-read-template.md:27` | **SD-3** Scorecard parser buckets only `TRIPPED`/`CLEARED`, silently dropping `INCONCLUSIVE`/`MANUAL`/`ERROR` rows — a criterion left INCONCLUSIVE never surfaces in the delta ledger. **Fix:** capture non-{tripped,cleared} statuses in the JSON, or note in `drift-audit.md` to read those rows directly from `customer-discovery.md`. |
| 10 | minor | `customer-discovery/SKILL.md:23` (allowed-tools) | **CD-2** `Skill` granted but never invoked (handoffs are prose). Dead surface area. **Fix:** drop `Skill` from allowed-tools, or add a documented call site. |
| 11 | minor | `sharpen-hypothesis/SKILL.md:4-9` (when_to_use) | **SH-2** Entry point has positive triggers only — no outbound "Do NOT use" clause; a bare "what's next" after `hypothesis.md` exists isn't deferred to `/pressure-test` from this side. **Fix:** add a closing boundary sentence (budget is healthy, 845/1536). |
| 12 | minor | `sharpen-hypothesis/SKILL.md` Interaction model | **SH-3** No recommended-effort note despite reasoning-sensitive grilling; both siblings carry one. **Fix:** add "run at high effort or above." |
| 13 | minor | `market-research/SKILL.md:77` (Step 1) | **MR-3** "Read the `## Verdict` line" is looser than reality (value is on the line *under* the heading). **Fix:** match the sibling's precise wording. |
| 14 | minor | `create-founder-profile/SKILL.md:3,9` | **PRC-2** Claims it auto-loads into "every idea-stage skill" but enumerates only three; downstream skills also Read the profile. **Fix:** drop the parenthetical list or extend to all six. |
| 15 | minor | Step ordinals across 5 skills | **PRC-1** Skills self-number First, Second, (no Third), Fourth, Fifth, Sixth — phantom missing stage. Routing is correct; only human-facing labels. **Fix:** renumber downstream skills down by one. |
| 16 | minor | `customer-discovery/scripts/score_criteria.py:101-103` | **CD-3** Non-dict branch's ERROR return omits `label`/`source` keys. Cosmetic (main() reads only status). **Fix:** add the two keys for uniform shape. |
| 17 | minor | `generate-ideas/SKILL.md:53` vs `:91,136` | **GI-1** Line 53 says "set effort:high on the spawn call"; authoritative line 91 says "you don't set those on the spawn" (agent already pins it). **Fix:** drop the spawn-call clause at line 53. |
| 18 | minor | `customer-discovery/SKILL.md:3-21` | **CD-4** description+when_to_use is 1521/1536 — only 15 chars headroom; future additions risk truncating the tail `/solution-design` routing clause. **Fix:** tighten ~30-40 chars of redundancy now. |

---

## What's genuinely well-built

1. **4.8 anti-pattern hygiene is clean across all six** — no fake incentives, no competitive framing, no "think harder" filler, no forced progress cadence, heading depth ≤3, every capitalized MUST carries a why-clause.
2. **Effort treated as the dominant lever** — frontmatter `effort: high` + user-facing notes, and parallel fan-out explicitly steered against 4.8's under-firing (`generate-ideas` is the model citizen).
3. **Subagent wiring is structurally airtight** — all 6 agents resolve and are dispatched; doc-path handoffs match end-to-end; blind/separate-context/parallel claims match how each agent is built; `bias-check` is correctly prose-only.
4. **Pipeline routing is coherent end-to-end** — the full file-contract chain holds; precedence gating agrees between neighbours; the namespace split is intentional and consistently guarded.
5. **Bundled deterministic scripts pull real weight** and were verified runnable — `compute_verdict.py` implements the documented truth table; `build_delta_ledger.py` + `rank_assumptions.py` handle latest-round scoping, scorecard isolation, adversary-in-top-3 flagging, and out-of-range clamping (Thariq Tip 8 done right).
6. **Progressive disclosure is well-executed** — lean SKILL.md bodies, detail in `references/` read at named steps, genuine production-grounded Gotchas sections.
7. **Frontmatter triggering is strong** — descriptions written for the model with real founder phrasings, within budget, non-colliding precedence.
8. **`pressure-test`'s deviation from the brief is the right call** — isolated per-persona subagents preserve the context isolation inline role-play would collapse.

---

## Remediation applied (2026-06-04)

All **18 confirmed findings were fixed** (the founder opted to apply everything), plus one bonus fix surfaced during verification. Changes verified: all three edited scripts compile, all 7 edited skills pass `quick_validate`, and a functional smoke suite (10 PT-1 cases + CD-3 + SD-3) passes green.

| Finding | File(s) | What changed |
|---|---|---|
| CD-1 | customer-discovery `SKILL.md` S3, `kill-criteria-anchoring.md` | scorer now invoked with full `docs/ideas-stages/<slug>/…` paths + a why-note |
| PT-1 | `compute_verdict.py` + pressure-test `SKILL.md` Step 3/8 | anti-thesis slug guarded: warns + exits 2 (unless `--allow-malformed`) when it matches no rebuttal; docstring + skill text document the exact-slug rule |
| SRI-1 | market-research `SKILL.md` :106/:145 | dispatch text corrected to "don't set model/effort — frontmatter pins Opus + `xhigh`" |
| SRI-2 | solution-design `SKILL.md` :187 | same effort-pin correction to `xhigh` |
| SH-1 | sharpen-hypothesis `SKILL.md` | `<project-name>` → `<slug>` for the folder; title token → `<idea-name>` + clarifier |
| MR-2 | market-research `SKILL.md` Step 1 | Step 1 now pulls open-risks / anti-thesis flag to fill the steelman's `<RISKS>` slot |
| SRI-3 | market-research `SKILL.md` :110 | deep-mode W2/W3 write paths now use `<PROVENANCE_DIR>` (no append-round clobber) |
| PT-2 | pressure-test `SKILL.md` :153 | output-shape wording scoped to success vs malformed vs anti-thesis-warning exits |
| SD-3 | `build_delta_ledger.py` + `drift-audit.md` | new `unsettled_criteria` bucket captures INCONCLUSIVE/MANUAL/ERROR; drift-audit tells the model to use it |
| CD-2 | customer-discovery `SKILL.md` :23 | dead `Skill` grant removed from allowed-tools |
| SH-2 | sharpen-hypothesis `when_to_use` | outbound "Do NOT use" boundary clause added |
| SH-3 | sharpen-hypothesis Interaction model | recommended-effort note added |
| MR-3 | market-research `SKILL.md` :77 | verdict-line read made precise (value under the heading) |
| PRC-2 | create-founder-profile `SKILL.md` :3/:9 | "every idea-stage skill" enumeration de-contradicted |
| PRC-1 | 3 downstream skills | step ordinals renumbered → First/Second/Third/Fourth/Fifth (phantom gap closed) |
| CD-3 | `score_criteria.py` :101 | non-dict ERROR entry given uniform `label`/`source` keys |
| GI-1 | generate-ideas `SKILL.md` :53 | spawn-call effort clause dropped (line 91 is the single source of truth) |
| CD-4 | customer-discovery `description`+`when_to_use` | ~50 chars of redundancy trimmed (headroom 15 → ~65) |
| **bonus** | create-founder-profile `description` | `Re-runnable: reads` → `Re-runnable — reads` (a `: ` was breaking strict-YAML frontmatter validation) |

Verdict after remediation: the four blocking issues are closed, so the suite now meets the **high-quality-ship** bar.
