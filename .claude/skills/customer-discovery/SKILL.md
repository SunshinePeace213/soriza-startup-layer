---
name: customer-discovery
description: |
  Fourth step in the Idea Stage of Soriza Startup Layer — takes ONE idea that passed
  /market-research into customer discovery with real people. Two phases: DESIGN builds a
  precise target profile + reachability map, per-persona kill-criteria-anchored interview
  guides (Mom-Test audited), and a sealed, paste-and-go Cowork run-pack for
  outreach/scheduling/tracking; SYNTHESIS scores real interview evidence against the LOCKED
  kill-criteria thresholds and writes a bias-checked customer-discovery.md Discovery Read.
  Structurally cannot send email — sending lives in Cowork, gated per batch. Reads
  pressure-test.md + market-research.md; writes customer-discovery.md.
when_to_use: |
  Use when the founder says "customer discovery", "talk to users", "interview customers",
  "build my interview guide", "who should I talk to", "design my outreach", "synthesize my
  interviews", "I did N interviews — what do they say", or "what's next" WHEN a market-research.md
  exists but customer-discovery.md does NOT yet, in the idea's docs/ideas-stages folder
  (precedence: market-research.md → here; customer-discovery.md → /solution-design). Also trigger
  on "Mom Test", "problem interview", "prospect list". Do NOT trigger to edit hypothesis.md
  (/sharpen-hypothesis), size the market (/market-research), or SEND outreach / schedule calls
  (Cowork sends, gated). Once customer-discovery.md exists, a bare "what's next" hands
  off to /solution-design (explicit "synthesize my interviews" still runs another round here).
argument-hint: "[slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob, Agent, Task, WebSearch, WebFetch
effort: high
---

# Customer Discovery

Fourth step in the **Idea Stage** of the Soriza Startup Layer. Turns the upstream `pressure-test.md`
Kill Criteria / Disconfirmation Questions and `market-research.md` buyer map into a customer-discovery
campaign with real humans, then scores what those humans actually said against the thresholds the
founder pre-registered *before* collecting data. Source method: *The Founder's Playbook: Building an
AI-Native Startup* — "Plan and design customer discovery."

- **Input:** `docs/ideas-stages/<slug>/pressure-test.md` (required floor) + `market-research.md`, `hypothesis.md` (folded if present) + `docs/founder-profile.md`.
- **Output:** `docs/ideas-stages/<slug>/customer-discovery.md` (the Discovery Read) + provenance under `customer-discovery/`.
- **Workers:** `customer-discovery-personas-worker` and `customer-discovery-bias-check` subagents (`.claude/agents/`), read at runtime.
- **Off-surface:** Cowork + Gmail/Calendar/Drive MCP executes the run-pack the skill emits. The skill never sends.

## The seam — design here, send in Cowork

This skill is a **design + synthesis engine**, not an outreach bot. It splits the work the way the
Playbook does:

| Claude Code (this skill) | Cowork + Gmail/Calendar/Drive MCP |
|---|---|
| target profile, interview guides, post-interview synthesis, bias-check; **emits** `cowork-runpack.md` (drafts, NOT sent) | builds/enriches the prospect list, personalized outreach, scheduling, day-7 follow-up cadence, live tracking sheet |

The seam in one line: **Cowork tracks *that* you talked to someone (status, schedule); the repo holds
*what they said* (transcripts, synthesis, kill-criteria verdicts).** Ops data vs. reasoning data.

## When this skill applies

- Founder has a `market-research.md` at `docs/ideas-stages/<slug>/` and asks "what's next"
- "Customer discovery", "talk to users", "build my interview guide", "who should I talk to"
- "Design my outreach" / "draft outreach emails" / "prospect list" / "schedule interviews"
- "Synthesize my interviews" / "I did 5 interviews — what do they say" (the synthesis phase)

Out of scope: sending any email (that is Cowork's job, structurally — see Gotchas); editing `hypothesis.md`
(that's `/sharpen-hypothesis`); the adversarial persona panel (`/pressure-test`); market sizing
(`/market-research`); solution-concept design (`/solution-design`, the next stage) and MVP/build work (after it).

## Gotchas

- **The skill structurally cannot send email — and that is the design, not a limitation.** `allowed-tools` excludes every send-capable MCP tool. Cold outreach is irreversible, outward-facing, and reputation-/jurisdiction-sensitive; the founder's risk appetite is low. The skill writes drafts + a run-pack; *Cowork* sends, gated per batch. Never reach for a Gmail-send tool to "be helpful" — there is no such tool in your hands here, and adding one breaks the safety guarantee.
- **Kill-criteria thresholds are LOCKED — never relitigate them after seeing data.** They are pre-registered in `pressure-test.md` *before* interviews, as an anti-self-deception device. On first synthesis, encode them once into `customer-discovery/kill-criteria.json` (write-once); reuse that file every round. If interview data comes back ugly, you do not soften a threshold to keep the idea alive — you score it honestly and let the founder override *on the record*. This founder's documented failure mode is "concede the diagnosis, keep the prescription"; this rule exists to stop exactly that.
- **The bias-check MUST run in a separate context from the agent that wrote the Discovery Read.** An agent grading its own synthesis rationalizes it. Dispatch `customer-discovery-bias-check` as an independent subagent given the notes + the draft read + the coverage snapshot, prompted to *refute*. Do not "self-check" the read inline.
- **Headless Cowork cannot see this repo.** The run-pack must be *sealed* — every input Cowork needs (target-profile excerpt, templates, send protocol, schedule windows, tracking schema) inlined. Do not write a run-pack that says "read `target-profile.md`"; that file does not exist from Cowork's vantage point.
- **Phase is detected from folder state, not asked blindly.** No `customer-discovery/target-profile.md` → run the DESIGN phase. `interviews/` holds notes newer than the latest `synthesis/round-*.md` → run a SYNTHESIS round. When genuinely ambiguous (both done, founder re-running), fire one `AskUserQuestion`.
- **Create subdirectories before dispatching writers.** Workers Write to fixed paths (`customer-discovery/`, `customer-discovery/interviews/`, `synthesis/`); if the parent doesn't exist the Write fails and the fan-out aborts. (Mirrors `/pressure-test` and `/market-research`.)
- **A `kill-suggested` pressure-test verdict makes discovery *more* pointed, not pointless.** If `pressure-test.md`'s verdict is `kill-suggested`, surface it loudly at scope-lock and reframe discovery as "go trip-or-clear these kill criteria with real people — resurrect with evidence the panel lacked, or bury it honestly." Do not silently proceed as if the panel had passed it.
- **This skill needs a real subagent-spawn tool for its two fan-outs.** If neither `Agent` nor `Task` is available, degrade gracefully (run the per-persona design inline, and run the bias-check as a deliberately adversarial *second pass* in a fresh framing) — but tell the founder the bias-check is weaker without context isolation, because a same-context self-critique is structurally compromised.

## Interaction model

Hybrid, like the sibling stages: **scope-lock checkpoint → autonomous fan-out → final review**, with
founder decisions routed through `AskUserQuestion` (a `notes` escape hatch on every choice — house
style; read `/market-research` or `/pressure-test` for voice). Two phases, auto-detected:

- **DESIGN** — one scope-lock gate up front, autonomous per-persona generation, one review gate before writing the run-pack.
- **SYNTHESIS** — runs after the founder returns with interview notes; autonomous tag→score→read→bias-check, one review gate before appending the round.

Quality scales with reasoning depth — run at `high` effort or above; the subagents carry their own.

## Workflow

Goal: in DESIGN, produce a target profile + per-persona kill-anchored guides + a sealed Cowork run-pack;
in SYNTHESIS, score real evidence against locked thresholds and write a bias-checked Discovery Read.
Steps are ordered where order is real (guard before scope-lock; lock criteria before scoring; score
before the read; read before bias-check); within each step the bullets are constraints, not a script.

### Step 1 — Resolve slug, entry guard, detect phase

If invoked with a slug, use it. Otherwise `glob docs/ideas-stages/*/` and fire `AskUserQuestion` with the available slugs.

Read, in order: `pressure-test.md` (the floor), then `market-research.md`, `hypothesis.md`, and `docs/founder-profile.md` if present.

**Entry guard:** if `pressure-test.md` is missing, refuse with exactly: *"No pressure-test at `docs/ideas-stages/<slug>/pressure-test.md`. Run /pressure-test first — customer discovery tests the Kill Criteria it produces."* Stop. Write nothing.

- If `market-research.md` is **absent**, do not refuse — say so in chat and make proceeding an explicit choice (*"No market-research.md yet — the target profile will be less sharp on segment/geography/willingness-to-pay. Proceed with discovery now, or run /market-research first?"*).
- Read the verdict value on the line **under** the `## Verdict` heading of `pressure-test.md` (the value follows the heading, e.g. `**kill-suggested** — …`, not on the heading line itself). If it is `kill-suggested` / `refine-hypothesis` / override, hold it and surface it loudly at Step D1.

**Detect phase** from `docs/ideas-stages/<slug>/customer-discovery/`:
- folder or `target-profile.md` missing → **DESIGN phase** (Steps D1–D6)
- `interviews/*.md` exist and are newer than the latest `synthesis/round-*.md` (or no synthesis round yet) → **SYNTHESIS phase** (Steps S1–S6)
- both design complete and interviews already synthesized, or genuinely ambiguous → `AskUserQuestion`: *Re-run design / New synthesis round / Skip*.

---

### DESIGN phase

#### Step D1 — Scope-lock checkpoint

Extract, don't ask blank. From `hypothesis.md`/`market-research.md`: the **personas** (the distinct user types in `Who` + the buyer map — e.g. PM / marketer / dev / founder), the **target-profile seed** (titles, company types, seniority), candidate **reachability channels** (communities, Slack, LinkedIn groups, events), and from `pressure-test.md` the **Disconfirmation Questions + Kill Criteria** (these become the spine of every interview guide). From `founder-profile.md`: the founder's **interview availability** and geography, to compute scheduling overlap windows.

Fire one `AskUserQuestion` that shows what you extracted and lets the founder confirm/correct in `notes`:
- The persona list (each persona gets its own guide + question set — the Playbook: *"a single interview framework will flatten that distinction"*).
- The founder's availability windows + target geographies (so the run-pack only proposes both-sides-sane interview slots — see `references/run-pack-template.md` for the overlap-window logic).
- If the verdict was `kill-suggested`, state it plainly and make proceeding the explicit choice.

#### Step D2 — Lock the kill criteria (write-once)

If `customer-discovery/kill-criteria.json` does **not** exist, encode each Kill Criterion / Disconfirmation Question from `pressure-test.md` into it, following the schema and scoring-type guide in `references/kill-criteria-anchoring.md`. This file pins the thresholds for every future round. If it already exists, read and reuse it unchanged — never edit a threshold after data exists (see Gotchas).

#### Step D3 — Fan out per-persona design workers (parallel)

Create the output directory first: `docs/ideas-stages/<slug>/customer-discovery/`.

Dispatch one `customer-discovery-personas-worker` per persona in a single assistant message (parallel), at high effort. Each worker produces, for its persona: the precise sub-profile + reachability ranking, a kill-criteria-anchored + Mom-Test-audited interview guide, and per-channel outreach-email drafts. Use the dispatch template below; the worker reads `references/kill-criteria-anchoring.md` and `references/mom-test-audit.md`.

**Degrade:** if no spawn tool exists, generate the per-persona guides inline using the same two references, and tell the founder it ran inline (no parallel isolation).

When workers report, Read each persona doc and assemble `customer-discovery/target-profile.md` (the merged profile + reachability + prioritization across personas). Offer to **audit any questions the founder drafts** against `references/mom-test-audit.md` (the Playbook exercise).

#### Step D4 — Compose the sealed run-pack

Read `references/run-pack-template.md`. Compose `customer-discovery/cowork-runpack.md` — fully self-contained (Gotchas: headless Cowork can't see the repo). It inlines: mission, target-profile excerpt, sourcing rules, per-persona outreach templates, the **send-gate protocol** (per-batch founder approval, ~5–10/day ramp, opt-out line, auto-stop on bounces/complaints, channel-norm respect), the **overlap-window scheduling rules**, the day-7 follow-up cadence, the **tracking-sheet schema**, the MCP-setup reminder, and the report-back contract.

**Output path:** by default write the run-pack to `customer-discovery/cowork-runpack.md`. When a Cowork shared folder is configured (`/mnt/c/dev/soriza-cowork/`, per ADR-0003), also write it there so Cowork reads it natively and drops interview notes back into the repo; otherwise the founder pastes the sealed run-pack into Cowork. The `/idea-funnel` workflow passes this path to its `cd-design-gate` for Shortlist survivors.

Surface a **pre-flight note** to the founder in chat (not legal advice): a one-paragraph jurisdiction caution (HK PDPO / EU GDPR / US CAN-SPAM for B2B cold outreach) and a nudge to prefer warm/community channels where the target congregates.

#### Step D5 — Review and write

Print the target profile + one sample persona guide + the run-pack's send-protocol section in chat. Fire `AskUserQuestion`: **Ship it** (write the files) / **Refine** (founder names what to redo in `notes`) / **Abort** (write nothing).

#### Step D6 — Exit message

*"Design written. Next: in Cowork, connect Gmail/Calendar/Drive (MCP), paste `customer-discovery/cowork-runpack.md`, and approve the first outreach batch (~5–10). Run interviews in your overlap windows; drop each conversation's notes into `customer-discovery/interviews/<date>-<prospect>.md`. Come back after ~5 interviews and I'll synthesize."*

---

### SYNTHESIS phase

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
- If **CONTINUE / PIVOT / KEEP-DISCOVERING**: *"Discovery Read written. Next: keep interviewing in your overlap windows toward ~10–15; re-run synthesis every ~5. When the call is a confident CONTINUE or a PIVOT, run /solution-design <slug> — it crystallizes the wedge + validated profile into a challenged final solution concept (a PIVOT just means the drift audit centers the pivot; this is the stage before MVP)."*
- If **hypothesis updates flagged**: *"The interviews flagged hypothesis updates — run /sharpen-hypothesis <slug> to apply them, then re-run /pressure-test before you build."*

## Subagent dispatch templates

Literal templates. Substitute `<UPPER_PLACEHOLDERS>` at dispatch. **Resolve `${CLAUDE_SKILL_DIR}` to this skill's absolute path** when composing — the subagent runs in its own context and won't expand it. Dispatch at high effort; the agents' frontmatter pins Opus + `high`.

### customer-discovery-personas-worker (Step D3, one per persona)

```
You are the customer-discovery-personas-worker for a committed startup idea that has passed sharpen-hypothesis, pressure-test, and market-research. Design the customer-discovery materials for ONE persona — reason hard about how THIS persona experiences the problem, and tie every interview question to a kill criterion.

First: Read ${CLAUDE_SKILL_DIR}/references/kill-criteria-anchoring.md and ${CLAUDE_SKILL_DIR}/references/mom-test-audit.md and follow both.

Persona to design for: <PERSONA_NAME> (<PERSONA_ONE_LINER>)

Context:
- Hypothesis (full): <HYPOTHESIS_FULL_CONTENT>
- Kill Criteria + Disconfirmation Questions (from pressure-test.md): <KILL_CRITERIA_AND_QUESTIONS>
- Locked thresholds (the canonical customer-discovery/kill-criteria.json): <KILL_CRITERIA_JSON> — anchor each question's trip-threshold to these verbatim; do not re-derive or alter them.
- Buyer/segment/geography/WTP (from market-research.md, if any): <MARKET_CONTEXT or "none">
- Founder reachability/geography constraints: <FOUNDER_CONSTRAINTS>

Produce, for THIS persona only:
1. Precise sub-profile (titles, company type, seniority, team structure) + where they congregate (communities, Slack, LinkedIn groups, events) + a proximity-to-pain ranking for who to reach first.
2. A kill-criteria-anchored interview guide: every question traces to a specific criterion with its trip-threshold, framed as PAST BEHAVIOUR ("tell me about the last time…"), never future-hypothetical ("would you…"). Then run the Mom-Test audit on your own questions and rewrite any that are leading / future-facing / too broad / socially-desirable. Add 2–3 deflection probes.
3. Per-channel outreach-email drafts (personalized, with an opt-out line) — DRAFTS ONLY; you do not send.

Write to: docs/ideas-stages/<SLUG>/customer-discovery/persona-<PERSONA_SLUG>.md
Return one line naming the persona + the doc path — not the contents.
```

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

- `references/kill-criteria-anchoring.md` — how to turn a Kill Criterion into a past-behaviour question + trip-threshold, the `kill-criteria.json` schema, and the per-interview scoring-JSON shape. Read in Steps D2, D3, S2.
- `references/mom-test-audit.md` — the audit checklist (leading / future-facing / too-broad / socially-desirable) + deflection-probe design. Read in Step D3 (and when auditing founder-drafted questions).
- `references/run-pack-template.md` — the sealed Cowork run-pack structure + overlap-window scheduling logic. Read in Step D4.
- `references/discovery-read-template.md` — the `customer-discovery.md` Discovery Read structure. Read in Step S4.

## Bundled scripts

- `scripts/score_criteria.py` — deterministic Step-S3 scoring. Reads the locked `kill-criteria.json` + the per-interview scoring JSON, applies each threshold (proportion / count / majority), and prints per-criterion `TRIPPED` / `CLEARED` / `INCONCLUSIVE` + `n` + small-sample flag + a per-persona coverage breakdown, surfacing qualitative criteria as `manual`. Bundled so the thresholds are applied mechanically and can't be soft-pedaled by eye (mirrors `/pressure-test`'s `compute_verdict.py`). Stdlib-only; runs under `python3` or self-executes via `uv run --script`.

## Composition

- **Upstream:** `/market-research` (and `/pressure-test` for the Kill Criteria + Disconfirmation Questions). Floor guard = `pressure-test.md`.
- **Downstream:** `/solution-design` consumes `customer-discovery.md` — the validated profile, the wedge, and the Discovery Read verdict — to crystallize and challenge the final solution concept; the MVP stage (not yet built) follows it. Hypothesis updates route back through `/sharpen-hypothesis`.
- **Off-surface:** Cowork (+ Gmail/Calendar/Drive MCP) executes the generated `cowork-runpack.md`. Not a versioned artifact — regenerated per run.
- **Workers:** `customer-discovery-personas-worker`, `customer-discovery-bias-check` under `.claude/agents/`, dispatched at runtime.

## Scope

- **In:** target profile + reachability, per-persona kill-anchored interview guides, the sealed Cowork run-pack, scoring real evidence against locked thresholds, the bias-checked Discovery Read + provenance.
- **Out:** sending any email (Cowork's job, structurally). Editing `hypothesis.md` (`/sharpen-hypothesis`). Market sizing / competitor mapping (`/market-research`). The persona panel (`/pressure-test`). Solution-concept design (`/solution-design`) and MVP/build work (later stages). Inventing persona skills (`/nuwa-skill`).
