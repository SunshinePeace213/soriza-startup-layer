---
name: pressure-test
description: |
  Idea-Stage pressure-test panel — step 4 (α) / step 6 (β). A founder-blind expert panel fires the
  sharpest disconfirming objections at a committed idea and turns each into an OPEN falsifiable
  assumption + a Mom-Test interview question. Use for "pressure-test", "run the panel", "stress-test the idea".
when_to_use: |
  Gate: α runs at current_step 4 (after kill-scan); β needs --beta at current_step 6 (after
  customer-discovery-synthesis). The desk never kills — p_success is calibration, subjective merit
  dies to real users + the founder's signature. Not sharpening the claim (/sharpen-hypothesis) or sizing it (/market-sizing).
argument-hint: "[slug] [--beta]"
disable-model-invocation: true
allowed-tools: Read, Glob, Write, Bash, Agent, AskUserQuestion
effort: high
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          if: "Write(*pressure-report-beta.md)"
          command: "uv run .claude/hooks/citation_density_check.py"
---

# Pressure-test — the calibrated expert panel

Convene a founder-blind advisory board, fire the strongest disconfirming objections, and convert each
into a **falsifiable assumption + a Mom-Test interview question** — wrapped in a calibrated `p_success`
prediction. **The desk never kills.** α (step 4) hands the founder the right risks to go trip-or-clear
with real people and locks the kill-criteria discovery scores against; β (step 6) re-runs the panel over
the Discovery Read, recommends go/pivot/kill, and resolves α's predictions. Subjective merit (moat,
demand, WTP, behaviour) is settled by real users and the founder's signature — never here.

This is the disconfirm machinery upgraded: same panel + steelman + judge, now with a JSON verdict
contract, a cross-examination round, locked predictions, and a founder-blind brief.

## When this applies

- **α (default):** `current_step: 4` (kill-scan passed). Triggers: "pressure-test", "run the panel",
  "stress-test the idea", "what's next" after kill-scan.
- **β (`--beta`):** `current_step: 6` (a `customer-discovery.md` Discovery Read exists).
- **Entry guards:** no `kill-scan.md` / step < 4 → point to `/kill-scan`. `--beta` without a Discovery
  Read → point to `/customer-discovery-synthesis`.

## Gotchas

- **The desk never kills; the panel recommends, the founder decides.** A weak-looking idea *advances*
  with sharper interview questions. "No moat / crowded / they won't pay" are OPEN assumptions, not
  deaths. Only a hard checkable fact (legality, technical feasibility) closes an objection; the judge may
  *flag* a fatal-flaw-class issue with cited evidence, but it is surfaced for the founder to weigh, never
  acted on.
- **Founder-blind panel.** Every seat reads ONLY `neutral-brief.md` + `evidence-ledger.jsonl` — never
  `hypothesis.md`, never the founder profile. Identity or enthusiasm cues in the brief poison the
  calibration. If `scripts/make_brief.py` is absent, **stop and report it** — do not hand-write a brief
  or pass `hypothesis.md` straight to the panel.
- **The independent round is sacred.** Spawn every seat in ONE message as parallel `Agent` calls so
  their contexts stay isolated; no seat may see a sibling's verdict before the cross-examination round.
  (4.8 under-fires a vague "spawn N personas" — issue one explicit `Agent` call per seat in a single
  turn, or you silently get fewer.)
- **`p_success` is a calibration prediction, never a verdict.** Lock every one into `predictions.jsonl`
  with `resolution_criteria` + `resolve_by`; the validator rejects a prediction missing either.
- **Append-only ledgers.** `predictions.jsonl` grows; never modify a locked line. β resolution is an
  appended supplement line carrying the same `id`.
- **Lock-ahead is enforced.** `advance_gate.py` refuses G4 unless `gates/criteria-g5.yaml` is locked and
  the G5 kill-criteria (derived from the OPEN assumptions) exist — pre-registration walks ahead of data.
- **β citation tooth.** Every β claim cites a ledger `E-xxx` (interview claims grade ≤2). The
  `test_pressure_beta` validator is shipped and **always-on** via `schema_on_write` — it checks the
  report's shape (recommendation enum, required sections) and that the report and its recommendation
  rationale are citation-grounded. The stricter, β-only `citation_density_check` hook — every
  evidence-table claim row carries an `E-xxx`, and every cited `E-xxx` exists in the ledger — is shipped,
  tested (`tests/hooks/`), and **wired into this skill's frontmatter** (the `hooks:` block above): a
  founder opt-in, since it auto-executes a command (self-modification of agent config).
- **Cost.** ≥5 seats × 2 rounds + steelman + judge runs several× a single thread — note a token estimate
  per run.

## Workflow — α (step 4)

**Goal:** `ideas/<slug>/pressure-report-alpha.md` + locked p_success predictions + a locked G5
kill-criteria set → the founder reads every `change_my_mind` and signs proceed/pivot at G4.

Order is load-bearing (the independent round must precede cross-examination), so run these in sequence;
within each round, fan out in parallel.

1. **Confirm state + build the brief.** Read `ideas/<slug>/STATE.md` (`current_step: 4`). Run
   `uv run scripts/make_brief.py --slug <slug>` to produce the de-identified `neutral-brief.md` (the
   validator gates banned tokens). This is the only description of the idea the panel gets.
2. **Select the panel** from `.claude/skills/idea-stage/references/expert-lens-map.md` — the operative
   roster: fixed core-3 (Thiel / Munger / Bezos) + `competitor-steelman` + the doctrine angles
   (`forward-deployed-founder`, `lean-startup`) + ≤1 idea-type specialist auto-suggested from
   `idea_type`. Offer the founder a seat swap via `AskUserQuestion`; the roster grows only between runs.
3. **Independent round (sacred).** In one message, dispatch `objection-lens` once per panel seat (pass
   the expert slug + the `neutral-brief.md` and `evidence-ledger.jsonl` paths) and `competitor-steelman`
   once (pass the Candidate `{id,title,problem,who,why_now,idea_type}` + its hypothesis, the competitor
   set, the open objections so far, and a doc path under `ideas/<slug>/disconfirmation/`). Each
   `objection-lens` returns the α JSON contract; its `SubagentStop` contract hook validates the JSON
   before you ever see it.
4. **Cross-examination round.** Re-dispatch each `objection-lens` seat with all sibling verdicts. A seat
   may revise its `p_success` only with a `revision_note` — never a silent overwrite.
5. **Judge.** Dispatch `disconfirmation-judge` with the final persona verdicts + the competitor-steelman
   doc + the Candidate + the lens slugs. It dedupes and risk-ranks into **5–8 OPEN assumptions**, each
   with one past-behaviour interview question, and returns `fatal_flaw` (`none` unless objectively
   established with cited evidence) + `risk_score`.
6. **Aggregate + write the report.** You play the aggregator: report the panel's final `p_success`
   distribution and a `p_agg` summary (a calibration prediction, not a verdict). Append one prediction
   line per persona to `predictions.jsonl` (the falsifiable_assumption as `claim`, plus `p`,
   `resolution_criteria`, `resolve_by`). Assemble `pressure-report-alpha.md` from
   `assets/pressure-report-alpha-template.md`: ranked risks, the OPEN-assumptions → interview-questions
   table, every persona's `steelman_for` + `change_my_mind`, the p distribution + `p_agg`, the
   competitor-steelman summary + doc link, any `fatal_flaw` flag with its cited evidence, and the cost
   estimate.
7. **Lock the G5 kill-criteria (lock-ahead).** From the top-ranked OPEN assumptions, derive the
   pre-registered kill-criteria discovery will score against (concrete thresholds + resolution source);
   write `customer-discovery/kill-criteria.json` (write-once) and ensure `gates/criteria-g5.yaml` is
   locked. These are never softened after data — that is the whole point of pre-registration.
8. **Close G4.** The founder reads every `change_my_mind`, then signs. Run
   `uv run scripts/advance_gate.py --slug <slug> --gate g4 --result proceed --p-agg <p_agg> --attest g4-5`
   — it enforces the triple lock (report validator + predictions + lock-ahead) and advances to step 5.
   **α never kills.** If the founder pivots, route to `/sharpen-hypothesis`.

## Workflow — β (step 6, `--beta`)

Same five-stage panel, run over the **Discovery Read** instead of a fresh brief, with two added teeth and
a real recommendation. **Goal:** `ideas/<slug>/pressure-report-beta.md` → the founder's go/pivot/kill at
G6 (the main kill decision).

- **Input:** `customer-discovery.md` + the full `evidence-ledger.jsonl` (pass `neutral-brief.md` too for
  idea context). No new `make_brief` run.
- **Citation tooth.** Every claim in the report cites a ledger `E-xxx`; interview-derived claims cite
  grade ≤2 entries. Enforced deterministically: `test_pressure_beta` (shape + citation-grounded, via
  `schema_on_write`) and the `citation_density_check` hook (per-row density + ledger referential
  integrity). Write the ledger entry first, then cite it — a dangling `E-xxx` bounces for repair.
- **Recommendation tooth.** The judge/aggregation produces a `go | pivot | kill` *recommendation* — the
  panel recommends; the founder's signature decides.
- **Resolve due α predictions.** For each `predictions.jsonl` entry from g4 whose `resolution_criteria`
  the Discovery Read now answers, append a supplement line (same `id`, `resolved` date, `outcome`,
  `brier`, `resolved_by: pressure-beta`).
- **Close G6.** `uv run scripts/advance_gate.py --slug <slug> --gate g6 --result <go|pivot|kill>
  --p-agg <p_agg> --attest <g6 human criterion>`. NO-GO routes per the gate table (pivot → step 2;
  keep-discovering → more interviews; drop → promote another slate idea).

## Workers, references & assets

- **Workers:** `objection-lens` (×panel seat, parallel, both rounds), `competitor-steelman` (one-shot),
  `disconfirmation-judge` (compiles the ranked OPEN assumptions).
- **Panel roster:** `.claude/skills/idea-stage/references/expert-lens-map.md`.
- **Templates:** `assets/pressure-report-alpha-template.md`, `assets/pressure-report-beta-template.md`.
- **Spec:** `docs/loop-engineering-reference-en.md` §2 (steps 4 & 6), §3.5 (predictions protocol).
