---
name: customer-discovery-synthesis
description: |
  Step 5b of the Idea Stage: score a founder's REAL interview evidence against the G4-LOCKED kill-criteria, extract grade-1/2 ledger entries from the notes, and write a bias-checked customer-discovery.md Discovery Read (every claim cites a grade ≤2 entry; never softens a threshold after data; can't send email). Use for "synthesize/score my interviews", "I did N interviews", "Mom Test scoring".
when_to_use: |
  Gate: current_step 5 — kill-criteria.json (locked at G4) + interview notes exist but no customer-discovery.md yet -> here; signing G5 advances to step 6 (/pressure-test --beta). Not designing the pack (/customer-discovery-design), editing the hypothesis (/sharpen-hypothesis), sizing (/market-sizing), the expert panel (/pressure-test), or sending outreach (Cowork, gated).
argument-hint: "[slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob, Agent, Task, WebSearch, WebFetch
effort: high
---

# Customer Discovery — Synthesis (Step 5b)

The **SYNTHESIS** half of step 5 in the **Idea Stage**. The interview **DESIGN** half (target profile,
reachability, warm list, interview guide, sealed run-pack) is produced upstream by
**`/customer-discovery-design`** (step 5a) — this skill no longer designs discovery. It picks up after the
founder has run that pack with real humans, and scores what those humans actually said against the
**kill-criteria locked before any data, at G4, by `/pressure-test` α**. Source method: *The Founder's
Playbook: Building an AI-Native Startup* — "Plan and design customer discovery."

- **Inputs:** `ideas/<slug>/customer-discovery/kill-criteria.json` (the **G4-locked** thresholds) + the
  founder's interview notes under `customer-discovery/interviews/` + `pressure-report-alpha.md` (the OPEN
  assumptions the criteria came from) + `hypothesis.md` (+ `kill-scan.md` demand-scan for segment context,
  if present) + `docs/founder-profile.md`.
- **Outputs:** `ideas/<slug>/customer-discovery.md` (the Discovery Read) + grade-1/2 entries appended to
  `evidence-ledger.jsonl` + provenance under `customer-discovery/`. Then `advance_gate.py --gate g5`.
- **Workers:** `customer-discovery-bias-check` subagent (`.claude/agents/`), read at runtime.
- **Off-surface:** Cowork + Gmail/Calendar/Drive MCP executes the run-pack `/customer-discovery-design`
  emits. This skill never sends.

## The seam — design + send upstream, synthesize here

This skill is a **synthesis engine**, not a design or outreach bot. `/customer-discovery-design` designs
the discovery pack and Cowork runs the outreach; this skill scores the evidence that comes back:

| Claude Code (`/customer-discovery-design`, 5a) | Cowork + Gmail/Calendar/Drive MCP | This skill (5b, SYNTHESIS) |
|---|---|---|
| target profile, reachability map, warm list, interview guide; **emits** sealed `cowork-runpack.md` (drafts, NOT sent) | builds/enriches the prospect list, personalized outreach, scheduling, day-7 follow-up cadence, live tracking sheet | scores real interview evidence against the G4-LOCKED kill criteria; extracts grade-1/2 ledger entries; bias-check; writes the Discovery Read; signs G5 |

The seam in one line: **Cowork tracks *that* you talked to someone (status, schedule); the repo holds
*what they said* (transcripts, the ledger, synthesis, kill-criteria verdicts).** Ops data vs. reasoning data.

## When this skill applies

- `current_step: 5` with a locked `kill-criteria.json` (from G4) + interview notes at
  `ideas/<slug>/customer-discovery/`, the founder has run the pack with real people, and asks "what's next"
  or "synthesize my interviews".
- "Synthesize my interviews" / "I did 5 interviews — what do they say" / "score my interviews against my
  kill criteria".

Out of scope: **designing the discovery pack** — target profile, reachability, warm list, interview guide,
the Cowork run-pack (that is `/customer-discovery-design`); **locking the kill-criteria** (that happens at
G4, in `/pressure-test` α — this skill only consumes them); sending any email (Cowork's job, structurally —
see Gotchas); editing `hypothesis.md` (`/sharpen-hypothesis`); the adversarial expert panel
(`/pressure-test`); market sizing / demand detection (`/market-sizing` and `/kill-scan`); solution-concept
design (`/startup-brief`, downstream) and MVP/build work (after it).

## Gotchas

- **The skill structurally cannot send email — and that is the design, not a limitation.** `allowed-tools`
  excludes every send-capable MCP tool. Cold outreach is irreversible, outward-facing, and
  reputation-/jurisdiction-sensitive. Outreach drafts live in the sealed `/customer-discovery-design`
  run-pack; *Cowork* sends, gated per batch. Never reach for a Gmail-send tool to "be helpful" — there is
  no such tool in your hands here, and adding one breaks the safety guarantee.
- **Kill-criteria thresholds are LOCKED at G4 — never relitigate them, and never re-lock them here.** Their
  source is `/pressure-test` α's `pressure-report-alpha.md`: each OPEN assumption + its interview question
  became a kill criterion, locked by `/pressure-test` α into `customer-discovery/kill-criteria.json`
  *before* interviews (the lock-ahead / anti-self-deception device). **Read it; never write it.** If it is
  missing, that is an upstream error — route back to `/pressure-test` α; do not lock it here. If interview
  data comes back ugly, you do not soften a threshold to keep the idea alive — you score it honestly and
  let the founder override *on the record*. This founder's documented failure mode is "concede the
  diagnosis, keep the prescription"; this rule exists to stop exactly that.
- **Extract the ledger BEFORE you cite it.** Every claim in the Discovery Read cites a grade ≤2
  `evidence-ledger.jsonl` entry (`E-xxx`). Those entries come from the interview notes — commitments
  (money/time/intro) = **grade 1**, quotes = **grade 2** — and you append them first (append-only, unique
  ascending ids), then cite them. A claim with no ledger entry behind it does not belong in the Read.
- **The bias-check MUST run in a separate context from the agent that wrote the Discovery Read.** An agent
  grading its own synthesis rationalizes it. Dispatch `customer-discovery-bias-check` as an independent
  subagent given the notes + the draft read + the coverage snapshot, prompted to *refute*. Do not
  "self-check" the read inline.
- **Don't try to design discovery here — `/customer-discovery-design` already did.** No target profile,
  reachability map, warm list, or interview guide is built in this skill. If the founder asks for a guide
  or outreach, point them at `/customer-discovery-design`. This skill only consumes the interview notes
  that pack produced.
- **Create subdirectories before writing.** This skill Writes to fixed paths (`customer-discovery/`,
  `customer-discovery/synthesis/`); if the parent doesn't exist the Write fails. Create them before scoring.
- **A high-risk α report makes synthesis *more* pointed, not pointless.** The desk never kills on
  subjective merit — it ranks risk and hands you OPEN assumptions to test. If the α report's top-ranked
  risks are severe, surface that loudly and frame synthesis as "go trip-or-clear these with real people —
  the panel deliberately left them OPEN for users to settle."
- **This skill needs a real subagent-spawn tool for the bias-check.** If neither `Agent` nor `Task` is
  available, degrade gracefully (run the bias-check as a deliberately adversarial *second pass* in a fresh
  framing) — but tell the founder the bias-check is weaker without context isolation.

## Interaction model

Hybrid: **autonomous extract→tag→score→read→bias-check → final review**, with founder decisions routed
through `AskUserQuestion` (a `notes` escape hatch on every choice — house style). One phase only —
**SYNTHESIS** — which runs after the founder returns with interview notes from the
`/customer-discovery-design` pack, then ends by signing G5. Discovery DESIGN is `/customer-discovery-design`.

Quality scales with reasoning depth — run at `high` effort or above; the subagent carries its own.

## Workflow

Goal: score real interview evidence against the G4-locked kill criteria, extract the grade-1/2 ledger, and
write a bias-checked Discovery Read with every claim cited — then sign G5. Steps are ordered where order is
real (guard before reading criteria; extract the ledger before citing it; score before the read; read
before bias-check; bias-check before the gate); within each step the bullets are constraints, not a script.

### Step 1 — Resolve slug, entry guard, confirm interviews exist

If invoked with a slug, use it. Otherwise `glob ideas/*/` and fire `AskUserQuestion` with the available slugs.

Read, in order: `pressure-report-alpha.md` (the OPEN assumptions the criteria came from), then
`hypothesis.md`, `kill-scan.md` (demand-scan, for segment context), and `docs/founder-profile.md` if present.

**Entry guard:** if `pressure-report-alpha.md` **or** `hypothesis.md` **or**
`customer-discovery/kill-criteria.json` is missing, refuse with exactly: *"No α report + hypothesis +
locked kill-criteria at `ideas/<slug>/`. Run /sharpen-hypothesis → /kill-scan → /pressure-test →
/customer-discovery-design first — they produce the hypothesis, the α pressure-report, the G4-locked
kill-criteria, and the sealed discovery pack this synthesis scores."* Stop. Write nothing.

- If `kill-scan.md` is **absent**, do not refuse — say so in chat (*"No kill-scan.md for this idea —
  segment/demand context will be thinner; proceeding."*) and continue.
- The α report's `ranked_risks` carry a `risk_score`. If the top-ranked risks are severe, hold that and
  surface it loudly at Step S0.

**Confirm interviews exist.** This skill is synthesis-only — it needs real interview notes. Check
`ideas/<slug>/customer-discovery/interviews/*.md`:
- notes exist and are newer than the latest `synthesis/round-*.md` (or no round yet) → run a **SYNTHESIS
  round** (Steps S0–S8).
- no interview notes at all → say so and point the founder at the sealed `/customer-discovery-design` pack:
  *"No interview notes yet at `customer-discovery/interviews/`. The discovery DESIGN is built by
  /customer-discovery-design — run it (or paste its `cowork-runpack.md` into Cowork), interview real
  people, drop each conversation's notes into `customer-discovery/interviews/<date>-<prospect>.md`, then
  come back."* Write nothing.
- all current interviews already synthesized, or genuinely ambiguous → `AskUserQuestion`: *New synthesis
  round / Skip*.

---

### SYNTHESIS phase

#### Step S0 — Read the locked kill-criteria (read-only; never re-lock)

Read `customer-discovery/kill-criteria.json` — the thresholds **locked at G4** by `/pressure-test` α from
the OPEN assumptions (schema + scoring-type guide in `references/kill-criteria-anchoring.md`). You
**consume** them; you never edit a threshold or re-lock the file. If it is absent, do **not** create it —
stop and route back to `/pressure-test` α (the entry guard should have caught this). This file pins the
thresholds for every round.

#### Step S1 — Gather

Read all `customer-discovery/interviews/*.md` not yet covered by a synthesis round. Read the locked
`customer-discovery/kill-criteria.json` and the latest `customer-discovery/prospects-*.csv` snapshot if
present (for coverage). If fewer than ~5 new interviews exist, say so and ask whether to synthesize anyway
(small-n caveat) or wait — note that **G5 needs ≥5**, so a <5 round is a progress read, not a gate close.

#### Step S2 — Extract the ledger (grade 1 / grade 2, append-only)

For each interview note, append `evidence-ledger.jsonl` entries (see `tests/schemas/test_ledger.py`
+ `tests/fixtures/ledger.sample.jsonl` for the line shape) — **first-party commitments** (the prospect put money / booked time / made an
intro) as **grade 1**, **verbatim quotes** as **grade 2**. Unique ascending ids (`E-xxx`); each line names
its `source` (the interview file) and `added_by: agent`. Append only — never modify a prior line; a
correction is a new line carrying `"corrects":"E-xxx"`. These entries are what the Discovery Read cites and
what `/pressure-test` β resolves against, so extract them before you draft.

The interview notes follow the emoji legend in `/customer-discovery-design`'s `assets/interview-note-template.md`
— read these emoji as extraction cues: **🤝 = commitment given (currency: time / reputation / cash) → a
grade-1 ledger entry** (the strongest evidence; "would pay" is *not* 🤝 — only a real currency given up
counts); **⚡ / 💰 = verbatim pain / price-anchor quotes → grade-2**; **➡️ = a booked next step
(advancement)**; **🔥 = earlyvangelist** (surface these by name in the Read — they're the candidate first
customers). A founder's note may not use the emoji — extract the same signals from the prose regardless.

- **Landing-page signups are NOT evidence.** If a note or tracking sheet reports landing-page/waitlist
  signups, treat them as a *lead source for conversations*, never validation — a signup count is a vanity
  metric with no ledger grade. Do not append it to the ledger or cite it in the Read; only behaviour in the
  actual conversations counts.

#### Step S3 — Tag the interviews

For each interview, extract the per-criterion signal each kill criterion needs (e.g. for "willingness-to-pay
against free": did this person ever actually pay for a comparable product?), following
`references/kill-criteria-anchoring.md`. This is reasoning — read the transcript, judge the behaviour, not
the stated intention. Assemble the scoring JSON (shape in `references/kill-criteria-anchoring.md`) and write
it to `customer-discovery/synthesis/round-<N>-scoring.json` (create `synthesis/` first).

#### Step S4 — Score against the locked thresholds (bundled script)

Run the bundled scorer rather than tallying by eye — so a mis-count or a soft-pedaled threshold can't
quietly flip a criterion:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/score_criteria.py" \
  ideas/<slug>/customer-discovery/kill-criteria.json \
  ideas/<slug>/customer-discovery/synthesis/round-<N>-scoring.json
```
(Pass full `ideas/<slug>/…` paths — the script runs from the repo root, so repo-relative paths under
`customer-discovery/` won't resolve and it exits 2.)
It prints JSON: per-criterion `TRIPPED` / `CLEARED` / `INCONCLUSIVE` (with `n` and a small-sample flag), a
`coverage` breakdown by persona (interview-only — it does not read the prospects CSV), and any `MANUAL`
(qualitative) criteria the script can't auto-score — those you judge in prose and mark explicitly. An
`ERROR` status means `kill-criteria.json` is malformed for that criterion (missing/typo'd threshold) — that
is an **upstream** lock error; surface it, do not hand-grade around it.

#### Step S5 — Draft the Discovery Read

Read `assets/discovery-read-template.md`. Compose `customer-discovery.md` (draft in chat first): the
**Kill-Criteria Scorecard** (from the script, verbatim statuses), the **two-list evidence** (supports /
challenges) **with every line citing a grade ≤2 `E-xxx`** from Step S2, the **coverage & skew** read (does
the sample's persona mix bias any number — e.g. "18% willingness-to-pay is founders only"?), and a
**non-binding overall call** (CONTINUE / PIVOT / KILL / KEEP-DISCOVERING) tied to the cited evidence. A
claim with no `E-xxx` behind it does not go in.

#### Step S6 — Independent bias-check (separate context)

Dispatch `customer-discovery-bias-check` (one subagent, high effort) with: the raw interview notes, your
draft Discovery Read, and the coverage breakdown. It returns where the read pattern-matches to what the
founder hoped rather than what the data says. Fold its challenge into the read's **Bias-check** section — do
not soften the script's scorecard to accommodate it; surface the tension.

#### Step S7 — Review, override gate, and write (append round)

Print the full draft Read in chat. Fire `AskUserQuestion`:
- **Ship it** → write `customer-discovery.md` and `customer-discovery/synthesis/round-<N>.md`. (The
  schema_on_write hook runs `test_synthesis` on the Read — verdict + scorecard + two lists + Bias-check +
  `E-xxx` citations; fix and rewrite on any stderr feedback.)
- **Proceed past a TRIPPED criterion** *(only offered when a criterion is TRIPPED and the overall call is
  CONTINUE/PIVOT)* → write the file, and stamp the override line: `<call> | Override: founder proceeded past
  TRIPPED <criterion> on <ISO-date>`.
- **Refine** → founder names what to redo in `notes`; return to the relevant step.
- **Abort** → write nothing; provenance interviews stay on disk.

#### Step S8 — Close G5 (lock-ahead, then advance) and exit

Only once the Read is written and the founder is ready to sign:
1. **Lock-ahead G6 (write-once).** Before G5 can pass, β's gate criteria must already be locked:
   `uv run scripts/lock_criteria.py --slug <slug> --gate g6` (write-once; `--force` only to re-register; the
   schema_on_write hook runs `test_criteria` on the result). Pre-registration walks ahead of data —
   `/pressure-test` β's gate is locked before discovery closes.
2. **STATE.** Flip this step's `owner: agent` checklist items to `done: true` and set `next_action` to
   *"run /pressure-test --beta for step 6"*. Do not touch `gates:`, `owner`, or `interview_budget`
   (agent-writable fields are `status / next_action / step_checklist / deltas_pending` only).
3. **Advance.** The founder confirms ≥5 interviews, interview_budget intact (an overrun is a stamped
   override), and that they have read the Read (every TRIPPED criterion + the bias-check). Then:
   ```bash
   uv run scripts/advance_gate.py --slug <slug> --gate g5 --attest g5-2 --attest g5-3 --attest g5-4
   ```
   It runs `test_synthesis` (auto), records the human attestations, enforces the G6 lock-ahead, and advances
   to step 6. **G5 is the founder's signature** — the desk never closes it.

Exit message:
- If any criterion is **TRIPPED** and no override: *"Discovery Read written. Criterion `<x>` tripped at
  n=<N> — the kill criterion pre-registered at G4 fired. See customer-discovery.md. To proceed anyway,
  re-run and choose the override."*
- If **CONTINUE** (clean): *"Discovery Read written and G5 signed. Next: run /pressure-test --beta <slug> —
  the β panel re-runs over this Read, enforces ledger citations, recommends go/pivot/kill, and resolves the
  α predictions at G6 (the main kill decision)."*
- If the call is **PIVOT** (sharper/different problem, or right problem wrong segment): *"This is a PIVOT —
  the problem the interviews revealed differs from the hypothesis. Re-enter /sharpen-hypothesis to redesign
  the hypothesis (then /kill-scan + /pressure-test + /customer-discovery-design for fresh criteria + pack),
  or, if the pivot is small, take the Read straight to /pressure-test --beta."*
- If **hypothesis updates flagged**: *"The interviews flagged hypothesis updates — re-enter
  /sharpen-hypothesis to fold them (it is the only place hypothesis.md is edited) before you build."*

## Subagent dispatch templates

Literal templates. Substitute `<UPPER_PLACEHOLDERS>` at dispatch. Dispatch at high effort; the agent's
frontmatter pins Opus + `high`.

### customer-discovery-bias-check (Step S6)

```
You are an independent skeptic. You did NOT write the synthesis you are about to read — your job is to refute it. Founders pattern-match interview data to what they hoped to find; you are the correction. A both-sides take is a failure of this task.

Critique this Discovery Read: find every place it reads the evidence more favorably than the evidence supports — over-weighted positive quotes, kill criteria scored as INCONCLUSIVE that the data actually TRIPS, coverage skew used to flatter a number, "they said they'd pay" treated as willingness-to-pay, a PIVOT dressed up as a CONTINUE.

Context:
- Raw interview notes: <INTERVIEW_NOTES_OR_PATHS>
- The draft Discovery Read: <DRAFT_READ>
- Coverage breakdown (who was actually interviewed, by persona): <COVERAGE>

Be specific and cite the interview. Close with the single most likely way this founder is fooling themselves here. Do not soften the conclusion to be fair — fairness is the main conversation's job.

Return your challenge as prose (no file write needed) — the main conversation folds it into the Read's Bias-check section.
```

## Reference files

- `references/kill-criteria-anchoring.md` — how the OPEN assumptions in `pressure-report-alpha.md` became
  trip-thresholds, the `kill-criteria.json` schema, and the per-interview scoring-JSON shape. Read in Steps
  S0, S3.
- `assets/discovery-read-template.md` — the `customer-discovery.md` Discovery Read structure (incl. the
  ledger-citation requirement). Read in Step S5.
- Design-phase references (target profile, reachability, warm list, the Mom-Test interview guide) live in
  `/customer-discovery-design`, not here.

## Bundled scripts

- `scripts/score_criteria.py` — deterministic Step-S4 scoring. Reads the locked `kill-criteria.json` + the
  per-interview scoring JSON, applies each threshold (proportion / count / majority), and prints per-criterion
  `TRIPPED` / `CLEARED` / `INCONCLUSIVE` + `n` + small-sample flag + a per-persona coverage breakdown,
  surfacing qualitative criteria as `manual`. Bundled so the thresholds are applied mechanically and can't be
  soft-pedaled by eye. Stdlib-only; runs under `python3` or self-executes via `uv run --script`.

## Composition

- **Upstream:** `/sharpen-hypothesis` (`hypothesis.md`), `/kill-scan` (`kill-scan.md` demand-scan +
  grade-4 ledger), `/pressure-test` α (`pressure-report-alpha.md` — the OPEN assumptions, and the
  **G4-locked** `kill-criteria.json`), and `/customer-discovery-design` (the **sealed discovery pack**
  `customer-discovery/cowork-runpack.md`) the founder runs. Floor guard = α report + hypothesis + locked
  `kill-criteria.json` + interview notes.
- **Downstream:** `/pressure-test --beta` (step 6) re-runs the panel over `customer-discovery.md`, enforces
  ledger citations, recommends go/pivot/kill, and resolves the α predictions at G6 — the main kill decision.
  Pivots and hypothesis updates route back through `/sharpen-hypothesis`.
- **Off-surface:** Cowork (+ Gmail/Calendar/Drive MCP) executes the `/customer-discovery-design`
  `cowork-runpack.md`. Not a versioned artifact — regenerated per run.
- **Workers:** `customer-discovery-bias-check` under `.claude/agents/`, dispatched at runtime.

## Scope

- **In:** reading the G4-locked kill criteria, extracting grade-1/2 ledger entries from the interview notes,
  scoring real interview evidence against those locked thresholds, the bias-checked + ledger-cited Discovery
  Read + provenance, and signing G5.
- **Out:** designing the discovery pack — target profile, reachability, warm list, interview guide, the
  Cowork run-pack (`/customer-discovery-design`). **Locking** the kill-criteria (that is G4, in
  `/pressure-test` α). Sending any email (Cowork's job, structurally). Editing `hypothesis.md`
  (`/sharpen-hypothesis`). Market sizing / demand detection (`/market-sizing`, `/kill-scan`). The expert
  panel (`/pressure-test`). Solution-concept design (`/startup-brief`) and MVP/build work (later steps).
