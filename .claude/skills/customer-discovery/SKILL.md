---
name: customer-discovery
description: |
  SYNTHESIS step in the Idea Stage of Soriza Startup Layer — takes ONE idea that came through
  the /idea-funnel (which produced its hypothesis.md, market-research.md, disconfirmation-brief.md,
  and a sealed Phase A run-pack) and scores the REAL interview evidence the founder gathered against
  the LOCKED kill-criteria thresholds, writing a bias-checked customer-discovery.md Discovery Read.
  The interview-DESIGN phase is superseded by the funnel's Phase A — for a target profile,
  reachability map, warm list, and interview guide, run /idea-funnel. This skill is synthesis-only:
  it locks kill criteria from the Disconfirmation Brief's OPEN assumptions + interview questions,
  scores behaviour against them, and never softens a threshold after data. Structurally cannot send
  email — sending lives in Cowork, gated per batch. Reads disconfirmation-brief.md + hypothesis.md
  (+ market-research.md); writes customer-discovery.md.
when_to_use: |
  Use when the founder says "synthesize my interviews", "I did N interviews — what do they say",
  "score my interviews", "customer discovery synthesis", or "what's next" WHEN a
  disconfirmation-brief.md + hypothesis.md exist but customer-discovery.md does NOT yet, in the
  idea's docs/ideas-stages folder (precedence: disconfirmation-brief.md → here; customer-discovery.md
  → /solution-design). Also trigger on "Mom Test scoring", "score against my kill criteria". Do NOT
  trigger to edit hypothesis.md, size the market, run the expert debate, or DESIGN the interview
  guide / outreach (all of that is /idea-funnel now), nor to SEND outreach / schedule calls (Cowork
  sends, gated). Once customer-discovery.md exists, a bare "what's next" hands off to /solution-design
  (explicit "synthesize my interviews" still runs another round here).
argument-hint: "[slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob, Agent, Task, WebSearch, WebFetch
effort: high
---

# Customer Discovery (Synthesis)

The **SYNTHESIS** step in the **Idea Stage** of the Soriza Startup Layer. The interview **DESIGN** phase
(target profile, reachability, warm list, interview guide, sealed run-pack) is now produced upstream by
the **`/idea-funnel`** workflow's **Phase A** — this skill no longer designs discovery. It picks up after
the founder has run that pack with real humans, and scores what those humans actually said against the
thresholds the founder pre-registered *before* collecting data. Source method: *The Founder's Playbook:
Building an AI-Native Startup* — "Plan and design customer discovery."

For DESIGN (a precise target profile + reachability map + warm list + Mom-Test interview guide), run
**`/idea-funnel`** — it builds and seals the Phase A pack per idea.

- **Input:** `docs/ideas-stages/<slug>/disconfirmation-brief.md` (required floor — its OPEN assumptions + interview questions are the kill-criteria source) + `hypothesis.md` (required) + `market-research.md` (folded if present) + `docs/founder-profile.md` + the founder's interview notes under `customer-discovery/interviews/`.
- **Output:** `docs/ideas-stages/<slug>/customer-discovery.md` (the Discovery Read) + provenance under `customer-discovery/`.
- **Workers:** `customer-discovery-bias-check` subagent (`.claude/agents/`), read at runtime.
- **Off-surface:** Cowork + Gmail/Calendar/Drive MCP executes the Phase A run-pack `/idea-funnel` emits. This skill never sends.

## The seam — design + send upstream, synthesize here

This skill is a **synthesis engine**, not a design or outreach bot. The funnel designs the discovery pack
(Phase A) and Cowork runs the outreach; this skill scores the evidence that comes back:

| Claude Code (`/idea-funnel` Phase A) | Cowork + Gmail/Calendar/Drive MCP | This skill (SYNTHESIS) |
|---|---|---|
| target profile, reachability map, warm list, interview guide; **emits** sealed `cowork-runpack.md` (drafts, NOT sent) | builds/enriches the prospect list, personalized outreach, scheduling, day-7 follow-up cadence, live tracking sheet | scores real interview evidence against the LOCKED kill criteria; bias-check; writes the Discovery Read |

The seam in one line: **Cowork tracks *that* you talked to someone (status, schedule); the repo holds
*what they said* (transcripts, synthesis, kill-criteria verdicts).** Ops data vs. reasoning data.

## When this skill applies

- Founder has a `disconfirmation-brief.md` + `hypothesis.md` at `docs/ideas-stages/<slug>/`, has run the funnel's Phase A pack with real people, and asks "what's next" or "synthesize my interviews"
- "Synthesize my interviews" / "I did 5 interviews — what do they say" / "score my interviews against my kill criteria"

Out of scope: **designing the discovery pack** — target profile, reachability, warm list, interview guide,
the Cowork run-pack (that is `/idea-funnel` Phase A now); sending any email (Cowork's job, structurally —
see Gotchas); editing `hypothesis.md` or running a pivot/resurrect (`/idea-funnel`); the adversarial expert
debate (`/idea-funnel`'s Disconfirmation Brief); market sizing / demand detection (`/idea-funnel`'s
market-research); solution-concept design (`/solution-design`, the next stage) and MVP/build work (after it).

## Gotchas

- **The skill structurally cannot send email — and that is the design, not a limitation.** `allowed-tools` excludes every send-capable MCP tool. Cold outreach is irreversible, outward-facing, and reputation-/jurisdiction-sensitive. Outreach drafts live in the funnel's sealed Phase A run-pack; *Cowork* sends, gated per batch. Never reach for a Gmail-send tool to "be helpful" — there is no such tool in your hands here, and adding one breaks the safety guarantee.
- **Kill-criteria thresholds are LOCKED — never relitigate them after seeing data.** Their source is the funnel's `disconfirmation-brief.md`: each OPEN assumption + its interview question becomes a kill criterion, pre-registered *before* interviews as an anti-self-deception device. On first synthesis, encode them once into `customer-discovery/kill-criteria.json` (write-once); reuse that file every round. If interview data comes back ugly, you do not soften a threshold to keep the idea alive — you score it honestly and let the founder override *on the record*. This founder's documented failure mode is "concede the diagnosis, keep the prescription"; this rule exists to stop exactly that.
- **The bias-check MUST run in a separate context from the agent that wrote the Discovery Read.** An agent grading its own synthesis rationalizes it. Dispatch `customer-discovery-bias-check` as an independent subagent given the notes + the draft read + the coverage snapshot, prompted to *refute*. Do not "self-check" the read inline.
- **Don't try to design discovery here — the funnel already did.** No target profile, reachability map, warm list, or interview guide is built in this skill; all of that is `/idea-funnel` Phase A, sealed into `customer-discovery/cowork-runpack.md`. If the founder asks for a guide or outreach, point them at `/idea-funnel`. This skill only consumes the interview notes that pack produced.
- **Phase is implicit — this skill is synthesis-only.** Discovery DESIGN is superseded by the funnel's Phase A; there is no DESIGN phase to detect. Run a SYNTHESIS round whenever `interviews/*.md` hold notes newer than the latest `synthesis/round-*.md` (or no round exists yet). If no interview notes exist at all, say so and point the founder to run the funnel's Phase A pack first.
- **Create subdirectories before writing.** This skill Writes to fixed paths (`customer-discovery/`, `customer-discovery/synthesis/`); if the parent doesn't exist the Write fails. Create them before scoring.
- **A high-risk Disconfirmation Brief makes synthesis *more* pointed, not pointless.** The funnel never kills on subjective merit — it ranks risk and hands you OPEN assumptions to test. If the brief's top-ranked risks are severe (high `risk_score`, load-bearing assumptions), surface that loudly and frame synthesis as "go trip-or-clear these with real people — the desk deliberately left them OPEN for users to settle."
- **This skill needs a real subagent-spawn tool for the bias-check.** If neither `Agent` nor `Task` is available, degrade gracefully (run the bias-check as a deliberately adversarial *second pass* in a fresh framing) — but tell the founder the bias-check is weaker without context isolation, because a same-context self-critique is structurally compromised.

## Interaction model

Hybrid, like the sibling stages: **autonomous tag→score→read→bias-check → final review**, with founder
decisions routed through `AskUserQuestion` (a `notes` escape hatch on every choice — house style; read
`/solution-design` for sibling voice). One phase only — **SYNTHESIS** — which runs after the founder
returns with interview notes from the funnel's Phase A pack: autonomous tag→score→read→bias-check, one
review gate (with an override gate) before appending the round. Discovery DESIGN is superseded by
`/idea-funnel` Phase A.

Quality scales with reasoning depth — run at `high` effort or above; the subagent carries its own.

## Workflow

Goal: score real interview evidence against the kill criteria locked from the funnel's Disconfirmation
Brief, then write a bias-checked Discovery Read. Steps are ordered where order is real (guard before
locking criteria; lock criteria before scoring; score before the read; read before bias-check); within
each step the bullets are constraints, not a script.

### Step 1 — Resolve slug, entry guard, confirm interviews exist

If invoked with a slug, use it. Otherwise `glob docs/ideas-stages/*/` and fire `AskUserQuestion` with the available slugs.

Read, in order: `disconfirmation-brief.md` (the floor — its OPEN assumptions + interview questions are the kill-criteria source), then `hypothesis.md`, `market-research.md`, and `docs/founder-profile.md` if present.

**Entry guard:** if `disconfirmation-brief.md` **or** `hypothesis.md` is missing, refuse with exactly: *"No Disconfirmation Brief + hypothesis at `docs/ideas-stages/<slug>/`. Run /idea-funnel first — it produces the hypothesis, Disconfirmation Brief, market research, and the sealed Phase A discovery pack that this synthesis scores."* Stop. Write nothing.

- If `market-research.md` is **absent**, do not refuse — say so in chat (*"No market-research.md for this idea — coverage/segment context will be thinner; proceeding."*) and continue.
- The Disconfirmation Brief's `ranked_risks` carry a `risk_score` and per-risk severity. If the top-ranked risks are severe, hold that and surface it loudly at Step S0.

**Confirm interviews exist.** This skill is synthesis-only — it needs real interview notes. Check `docs/ideas-stages/<slug>/customer-discovery/interviews/*.md`:
- notes exist and are newer than the latest `synthesis/round-*.md` (or no round yet) → run a **SYNTHESIS round** (Steps S0–S6).
- no interview notes at all → say so and point the founder at the funnel's sealed Phase A pack: *"No interview notes yet at `customer-discovery/interviews/`. The discovery DESIGN (target profile, warm list, interview guide) is built by /idea-funnel's Phase A — run it (or paste its `cowork-runpack.md` into Cowork), interview real people, drop each conversation's notes into `customer-discovery/interviews/<date>-<prospect>.md`, then come back."* Write nothing.
- all current interviews already synthesized, or genuinely ambiguous → `AskUserQuestion`: *New synthesis round / Skip*.

---

### SYNTHESIS phase

#### Step S0 — Lock the kill criteria (write-once)

If `customer-discovery/kill-criteria.json` does **not** exist, create `docs/ideas-stages/<slug>/customer-discovery/` first, then encode each kill criterion from `disconfirmation-brief.md` into it: each **OPEN assumption** (`open_assumptions[].assumption` — "What would have to be true: …") + its matching **interview question** (`interview_questions[]`) becomes one criterion, with a trip-threshold chosen following the schema and scoring-type guide in `references/kill-criteria-anchoring.md`. Set each criterion's `source` to the brief's open assumption it came from. Use the `ranked_risks` order to prioritize which assumptions matter most. This file pins the thresholds for every future round. If it already exists, read and reuse it unchanged — never edit a threshold after data exists (see Gotchas).

#### Step S1 — Gather

Read all `customer-discovery/interviews/*.md` not yet covered by a synthesis round. Read `customer-discovery/kill-criteria.json` (the locked thresholds) and the latest `customer-discovery/prospects-*.csv` snapshot if present (for coverage). If fewer than ~5 new interviews exist, say so and ask whether to synthesize anyway (small-n caveat) or wait.

#### Step S2 — Tag the interviews

For each interview, extract the per-criterion signal each kill criterion needs (e.g. for "willingness-to-pay against free": did this person ever actually pay for a comparable product?), following `references/kill-criteria-anchoring.md`. This is reasoning — read the transcript, judge the behavior, not the stated intention. Assemble the scoring JSON (shape in `references/kill-criteria-anchoring.md`) and write it to `customer-discovery/synthesis/round-<N>-scoring.json` (create `synthesis/` first).

#### Step S3 — Score against the locked thresholds (bundled script)

Run the bundled scorer rather than tallying by eye — so a mis-count or a soft-pedaled threshold can't quietly flip a criterion:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/score_criteria.py" \
  docs/ideas-stages/<slug>/customer-discovery/kill-criteria.json \
  docs/ideas-stages/<slug>/customer-discovery/synthesis/round-<N>-scoring.json
```
(Pass full `docs/ideas-stages/<slug>/…` paths — the script runs from the repo root, so repo-relative paths under `customer-discovery/` won't resolve and it exits 2.)
It prints JSON: per-criterion `TRIPPED` / `CLEARED` / `INCONCLUSIVE` (with `n` and a small-sample flag), a `coverage` breakdown by persona (interview-only — it does not read the prospects CSV), and any `MANUAL` (qualitative) criteria the script can't auto-score — those you judge in prose and mark explicitly. An `ERROR` status means `kill-criteria.json` is malformed for that criterion (missing/typo'd threshold) — fix the JSON and re-run; do not hand-grade around it.

#### Step S4 — Draft the Discovery Read

Read `references/discovery-read-template.md`. Compose `customer-discovery.md` (draft in chat first): the **Kill-Criteria Scorecard** (from the script, verbatim statuses), the **two-list evidence** (supports / challenges), the **coverage & skew** read (does the sample's persona mix bias any number — e.g. "18% willingness-to-pay is founders only"?), and a **non-binding overall call** (CONTINUE / PIVOT / KILL / KEEP-DISCOVERING) tied to the evidence.

#### Step S5 — Independent bias-check (separate context)

Dispatch `customer-discovery-bias-check` (one subagent, high effort) with: the raw interview notes, your draft Discovery Read, and the coverage breakdown. It returns where the read pattern-matches to what the founder hoped rather than what the data says. Fold its challenge into the read's **Bias-check** section — do not soften the script's scorecard to accommodate it; surface the tension.

#### Step S6 — Review, override gate, and write (append round)

Print the full draft Read in chat. Fire `AskUserQuestion`:
- **Ship it** → write `customer-discovery.md` and `customer-discovery/synthesis/round-<N>.md`.
- **Proceed past a TRIPPED criterion** *(only offered when a criterion is TRIPPED and the overall call is CONTINUE/PIVOT)* → write the file, and stamp the override line: `<call> | Override: founder proceeded past TRIPPED <criterion> on <ISO-date>`.
- **Refine** → founder names what to redo in `notes`; return to the relevant step.
- **Abort** → write nothing; provenance interviews stay on disk.

#### Step S7 — Exit message

- If any criterion is **TRIPPED** and no override: *"Discovery Read written. Criterion `<x>` tripped at n=<N> — the kill criterion you pre-registered fired. See customer-discovery.md. To proceed anyway, re-run and choose the override."*
- If **CONTINUE / PIVOT / KEEP-DISCOVERING**: *"Discovery Read written. Next: keep interviewing toward ~10–15 (use the funnel's sealed Phase A pack via Cowork); re-run synthesis every ~5. When the call is a confident CONTINUE or a PIVOT, run /solution-design <slug> — it crystallizes the wedge + validated profile into a challenged final solution concept (a PIVOT just means the drift audit centers the pivot; this is the stage before MVP)."*
- If the call is **PIVOT** (sharper/different problem, or right problem wrong segment): *"This is a PIVOT — the problem the interviews revealed differs from the hypothesis. Re-enter /idea-funnel to redesign the hypothesis (and a fresh Disconfirmation Brief + Phase A pack) for the sharpened problem, or take it straight to /solution-design if the pivot is small enough to design around."*
- If **hypothesis updates flagged**: *"The interviews flagged hypothesis updates — re-enter /idea-funnel to apply them (it re-sharpens the hypothesis and re-runs the Disconfirmation Brief) before you build."*

## Subagent dispatch templates

Literal templates. Substitute `<UPPER_PLACEHOLDERS>` at dispatch. Dispatch at high effort; the agent's frontmatter pins Opus + `high`.

### customer-discovery-bias-check (Step S5)

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

- `references/kill-criteria-anchoring.md` — how to turn a Disconfirmation Brief OPEN assumption + its interview question into a trip-threshold, the `kill-criteria.json` schema, and the per-interview scoring-JSON shape. Read in Steps S0, S2.
- `references/discovery-read-template.md` — the `customer-discovery.md` Discovery Read structure. Read in Step S4.
- `references/mom-test-audit.md`, `references/run-pack-template.md` — design-phase references, **superseded** by `/idea-funnel` Phase A; this synthesis-only skill no longer reads them (kept for the funnel's design logic / portability).

## Bundled scripts

- `scripts/score_criteria.py` — deterministic Step-S3 scoring. Reads the locked `kill-criteria.json` + the per-interview scoring JSON, applies each threshold (proportion / count / majority), and prints per-criterion `TRIPPED` / `CLEARED` / `INCONCLUSIVE` + `n` + small-sample flag + a per-persona coverage breakdown, surfacing qualitative criteria as `manual`. Bundled so the thresholds are applied mechanically and can't be soft-pedaled by eye. Stdlib-only; runs under `python3` or self-executes via `uv run --script`.

## Composition

- **Upstream:** `/idea-funnel` — it produces `hypothesis.md`, `disconfirmation-brief.md` (the kill-criteria source: OPEN assumptions + interview questions), `market-research.md`, and the **sealed Phase A discovery pack** (`customer-discovery/cowork-runpack.md`) the founder runs. Floor guard = `disconfirmation-brief.md` + `hypothesis.md`.
- **Downstream:** `/solution-design` consumes `customer-discovery.md` — the validated profile, the wedge, and the Discovery Read verdict — to crystallize and challenge the final solution concept; the MVP stage (not yet built) follows it. Pivots and hypothesis updates route back through `/idea-funnel`.
- **Off-surface:** Cowork (+ Gmail/Calendar/Drive MCP) executes the funnel's `cowork-runpack.md`. Not a versioned artifact — regenerated per run.
- **Workers:** `customer-discovery-bias-check` under `.claude/agents/`, dispatched at runtime.

## Scope

- **In:** locking kill criteria from the Disconfirmation Brief's OPEN assumptions + interview questions, scoring real interview evidence against those locked thresholds, the bias-checked Discovery Read + provenance.
- **Out:** designing the discovery pack — target profile, reachability, warm list, interview guide, the Cowork run-pack (all `/idea-funnel` Phase A). Sending any email (Cowork's job, structurally). Editing `hypothesis.md` or pivot/resurrect (`/idea-funnel`). Market sizing / competitor mapping / demand detection (`/idea-funnel`). The expert debate (`/idea-funnel`'s Disconfirmation Brief). Solution-concept design (`/solution-design`) and MVP/build work (later stages). Inventing persona skills (`/nuwa-skill`).
