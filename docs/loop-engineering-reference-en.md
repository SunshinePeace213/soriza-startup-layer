# Soriza Idea Stage — Loop Engineering Implementation Reference (EN) v1

Date: 2026-06-12 ｜ Canonical English repo doc. Consolidates the v2 playbook (operational sections), the files-and-samples handbook, and three founder revisions: (1) CLAUDE.md written to the house schema, (2) hook placement incl. skill/agent-scoped hooks, (3) the automation map of Claude Code built-ins. The Chinese v2 doc remains the review/decision record; where they differ, this doc wins.

Mechanics in §7 and §11 verified against the official hooks reference (code.claude.com/docs/en/hooks, fetched 2026-06-12). Re-verify field names with `claude --debug` when implementing.

-----

## 1. Principles

### 1.1 Rule Zero (unchanged, verbatim in spirit)

**The loop must close through reality, not just through the repo.** When infra work competes with interview/evidence work for time, evidence wins. Infra DoD may slip a week; Gate 1 (5 real interviews) and Gate 2 (an external founder walks the pipeline) may not. This rule exists because the pleasure of building systems disguises itself as progress — and this backlog itself can become a procrastination toy. Each week, the evidence-track row gets done before any build task opens.

### 1.2 Three file classes, three disciplines

|Class|Nature|Who writes|Frequency|Discipline|
|---|---|---|---|---|
|**Rule files**|CLAUDE.md ×2, gate criteria YAML, validators, hooks, persona agents, scripts|**Human**|Low|Edits need a reason; personas/rubric tuned ONLY after a calibration-review; locked criteria are NEVER edited|
|**State files**|STATE.md, ideas/ACTIVE, kill-criteria.json|Script + agent (per-field)|Once per step|Structure enforced by validators; `gates:` block writable by script only|
|**Ledger files**|evidence-ledger, predictions, decision-log, run-log, learning-log|Agent / hook / script|High, append|**Append-only, never modify old lines**; corrections are new lines referencing the old ID|

One-line mnemonic: **humans write rules, machines manage state, ledgers only grow.** Agents have zero write authority over rule files; humans never hand-edit ledgers.

### 1.3 Hard Rules (stacked on the master plan's four)

1. **Evidence first** — when budget blows, cut build tasks, never the evidence track
2. **Validator first** — no artifact's skill is "done" before its validator is green
3. **The independent round is sacred** — no persona touches a sibling's output before the cross-examination round; guaranteed by isolated subagent contexts + the canary test, not by prompts
4. **Web content enters artifacts ONLY via the evidence ledger**; the research agent is the single web ingress
5. **Personas start at 3**; add more only after token cost proves worth it
6. **Gates are written ONLY by `scripts/advance_gate.py`** — hand-editing `gates:` is a violation
7. **Lock-ahead** — before passing G(n), G(n+1)'s criteria must already be locked; pre-registration always walks ahead of data
8. **Subjective merit is killed only by real users + the founder's signature** — the desk (personas/agents) kills only on hard checkable facts (kill-scan); `p_success` is a calibration prediction, never a verdict
9. **Delta discipline** — no stage edits `hypothesis.md` directly; stages emit a "Hypothesis Updates Flagged" block; folding is `sharpen-hypothesis`'s exclusive right

-----

## 2. Pipeline Canon — 9 Steps

Gate number = step number; the gate sits at the step's end. Each card: Input → Process (who) → Output → Gate → **Founder control point**.

### Step 1 — Generate (skill: `generate-ideas`, kept + scaffold upgrade)

- **Input**: thesis or seed list; `docs/founder-profile.md`
- **Process**: dual-track slate of 10 (blind-wide + founder-reachable, as today) → advisory recommendation → **founder picks** → scaffold. Upgrade: scaffold also writes `STATE.md` (schema v2), locks `gates/criteria-g2.yaml`, sets `ideas/ACTIVE`
- **Output**: `slate.md`, `ideas/<slug>/{seed.md, STATE.md}`, locked g2 criteria
- **G1**: pick made + scaffold complete + rationale in decision-log
- **Control**: the pick (advisory, never auto-pick)

### Step 2 — Hypothesis (skill: `sharpen-hypothesis`, retrofitted)

- **Input**: seed.md + grounding.md + founder domain knowledge (interactive)
- **Process**: agent drafts WHO / HOW OFTEN / HOW SEVERE / STATUS QUO + value/growth hypotheses, all marked provisional; founder injects specifics; web stays banned (sharpen, don't prove). Retrofit: reads/writes STATE; finishes by calling `advance_gate.py --gate g2`
- **Output**: `hypothesis.md` (validator: 5 sections, ≤300 words, each dimension one falsifiable claim)
- **G2**: validator green + founder signs
- **Control**: dimension content is the founder's testimony; the agent only forces specificity

### Step 3 — Kill-scan + Demand-scan (skill: `kill-scan`, new; harvests disconfirm's fatal-flaw logic + market-map's complaint-mining facet)

- **Input**: hypothesis.md
- **Process**: research agent (sole web-tool holder, **writes to ledger only**) runs two legs: (a) disqualifiers — regulatory walls, technical impossibility, platform single-point risk, graveyard cases; (b) demand-scan — unresolved competitor-review complaints, user language, named people who publicly complained (grade-4 entries feeding 5a's warm list). Main agent writes `kill-scan.md`, every verdict citing entry IDs
- **Output**: `kill-scan.md` + ledger entries
- **G3**: no disqualifier tripped; proceeding past one = stamped founder override in decision-log
- **Control**: the override — **the only legitimate desk-kill in the pipeline** (hard, checkable facts only)

### Step 4 — Pressure-test α (skill: `pressure-test` = disconfirm upgraded, not rebuilt)

- **Input**: `neutral-brief.md` (de-identified by `scripts/make_brief.py`; validator checks banned tokens) + ledger
- **Process**: ① independent round — spawn personas ×3 in parallel (Thiel/Eisenmann/Munger, isolated contexts, read brief+ledger only), each returns JSON `{p_success, base_rate_ref, risk_patterns, sharpest_objection→falsifiable_assumption + past-behaviour interview question, steelman_for, change_my_mind}`; + competitor-steelman ② cross-examination round — all verdicts fed back; p revisions require `revision_note` ③ judge (the existing disconfirmation-judge) dedupes and risk-ranks into **5–8 OPEN assumptions** ④ aggregator applies the rubric; every `p_success` locked into predictions.jsonl with resolution criteria
- **Output**: `pressure-report-alpha.md` + prediction entries
- **G4 (triple lock)**: report passes validator + predictions locked + **G5 kill-criteria locked from the OPEN assumptions** (the existing write-once `kill-criteria.json` mechanism) + founder signs proceed/pivot
- **Control**: read every `change_my_mind`, then sign. **α does not kill**: `p_success` is for calibration; subjective merit dies only to real users (steps 5–6) or the founder
- **Cost note**: personas start at 3; judge/aggregator/QC on a cheap model; subagent-heavy flows can cost several × single-thread tokens — log an estimate per α run

### Step 5 — Customer Discovery (5a design / human interviews / 5b synthesis; both existing skills kept)

- **5a (`customer-discovery-design`, rewired inputs)**: consumes α's OPEN assumptions (was: disconfirmation-brief) and step-3 demand-scan entries (was: market-research). Produces the sealed run-pack (target profile, warm★ list, Mom-Test guide, cold drafts, tracker). **Structurally cannot send** (as today): founder posts warm replies; Cowork sends cold, per-batch approved
- **Interviews (human only)**: founder runs them; notes go to `customer-discovery/interviews/<date>-<prospect>.md`; the agent then extracts ledger entries — commitments (money/time/intro) = grade 1, quotes = grade 2
- **5b (`customer-discovery-synthesis`, kept + wired to STATE/ledger)**: scores against **LOCKED** criteria line by line (never softened, as today) + bias-check worker; every claim in the Discovery Read cites a grade ≤2 entry
- **Output**: run-pack, interviews/, `customer-discovery.md`, ledger entries
- **G5**: ≥5 interviews + scoring done + interview_budget intact (overrun needs an override) + founder signs
- **Control**: interviews, commitments, and final send approval — all three human

### Step 6 — Pressure-test β (same panel, citation-enforced mode)

- **Input**: Discovery Read + full ledger
- **Process**: α's flow plus two teeth: **every claim must cite a ledger entry ID** (validator-enforced); verdict recommends go/pivot/kill; resolves due α predictions (appends outcome lines)
- **Output**: `pressure-report-beta.md`
- **G6**: founder signs — **the main kill decision point**. Proceeding past a tripped criterion = stamped override (the absorbed idea-stage-exit discipline)
- **Control**: go/pivot/kill is the founder's signature; the panel only recommends

### Step 7 — Market Sizing (skill: `market-sizing` = market-map's sizing/buyer/trends facets; complaint mining already done in step 3)

- **Input**: Discovery Read + hypothesis (+ pending deltas)
- **Process**: parallel facet agents (existing workers): bottom-up TAM/SAM/SOM pressure-tested for inflation, budget-holder vs influencer, 3 named trends scored tail/headwind, analogues
- **Output**: `market-sizing.md` ｜ **G7**: completeness check — **size never kills** (as today); context only
- **Control**: read; no verdict to sign

### Step 8 — Startup Brief (skill: `startup-brief` = solution-design + idea-stage-exit, merged and absorbed)

- **Input**: everything upstream + the validated baseline reconstructed by the existing `scripts/build_delta_ledger.py`
- **Process**: ① crystallize the final solution concept (founder confirms — they own the design) ② **drift audit** against the problem discovery revealed, not the one assumed going in; a `❌ still solving the old problem` row is a finding, not a nuisance ③ red-team (existing solution-red-team worker) ④ premortem (Eisenmann six-pattern checklist) ⑤ **lock G9 PoC kill-criteria** ⑥ the three exit criteria + GO/NO-GO stamp
- **Output**: `startup-brief.md` (validator: drift-audit table + premortem + PoC criteria + upstream citations)
- **G8**: founder stamps GO / NO-GO (NO-GO routes as today: PIVOT → step 2; KEEP-DISCOVERING → more interviews; DROP → promote another slate idea)
- **Control**: the stamp + reading every ❌ drift row

### Step 9 — PoC (skill: `build-poc`, kept + wired to STATE)

- **Input**: brief + LOCKED PoC criteria
- **Process**: as today — scope (archetype ladder video/concierge/WoZ/functional + IN/OUT list) → build (functional only; own worktree + session) → synthesize 5 target-user reactions. **The 5 conversations are the deliverable, not the code**
- **Output**: `poc/{poc-brief.md, reactions.md, mvp-input.md}` + result scored against locked criteria
- **G9**: keep-building (→ MVP layer; worktree merge to main = graduation) / pivot / kill. All open predictions resolved
- **Control**: the pretotype, the 5 conversations, the direction call

### 2.10 Gate signature table

|Gate|Founder's hands-on act|
|---|---|
|G1|Pick the idea|
|G2|Hypothesis content + sign|
|G3|Disqualifier override authority|
|G4|Read change_my_mind list → sign proceed/pivot; confirm G5 criteria locked|
|G5|Interviews, commitments, outreach approval|
|G6|**Main kill decision** — go/pivot/kill stamp|
|G7|Read only|
|G8|GO/NO-GO stamp + drift-audit ❌ rows|
|G9|Pretotype + 5 conversations + direction|

### 2.11 Legacy-asset migration table

|Existing asset|Disposition|Destination / action|
|---|---|---|
|generate-ideas|**Keep + upgrade**|Step 1; scaffold adds STATE + g2 lock + ACTIVE|
|sharpen-hypothesis|**Keep + retrofit**|Step 2; STATE wiring; output constraints → validator|
|disconfirm|**Upgrade → pressure-test**|Panel/steelman/judge machinery kept; add JSON contract, cross-exam round, predictions; fatal-flaw logic split out to kill-scan. Old name deprecated|
|market-map|**Harvest in parts**|Complaint-mining facet → step 3; sizing/buyer/trends facets → step 7; "size never kills" kept. Old name deprecated|
|customer-discovery-design|**Keep + rewire**|Step 5a; the kill-criteria lock mechanism is **generalized into the pipeline-wide gate-criteria system** — the single most important mechanism inherited|
|customer-discovery-synthesis|**Keep + wire**|Step 5b; STATE + ledger citations|
|solution-design|**Absorb**|Drift audit + delta script + red-team → startup-brief. Old name deprecated|
|idea-stage-exit|**Absorb**|Exit criteria + GO/NO-GO + override stamping → G8 / advance_gate. Old name deprecated|
|build-poc|**Keep + wire**|Step 9; criteria check against locked G9 file|
|idea-stage (router)|**Keep + retrofit**|Human-readable dashboard; its derive-stage-from-artifacts logic becomes the state-audit (§3.3); pipeline map updated to the 9 steps **in W1**|
|Workers (objection-lens, competitor-steelman, disconfirmation-judge, bias-check, solution-red-team, researchers, seed-generator)|**All kept**|objection-lens gains the JSON contract; rest used as-is|
|Perspective skills (thiel / eisenmann / munger / bezos / …)|**Keep, dual-use**|Unchanged as conversational skills; **converted** into persona-subagent system prompts (no re-distillation via Nuwa)|
|lean-startup, solo-founder, forward-deployed-founder, grill-*, nuwa-skill, create-founder-profile|**Keep**|Cross-cutting tools, outside the pipeline; nuwa reserved for Rumelt (W3, optional)|

**Deprecation (W11)**: move retired skills to `.claude/skills-archive/` or rename `zz-deprecated-<name>` with a one-line redirect description; update `stage-pipeline.md`; add the UserPromptExpansion deprecation guard (§7.6).

-----

## 3. State Layer

### 3.1 Directory (stays under `ideas/` — no relocation)

```
ideas/
  ACTIVE                      # one line: the current slug (hook pointer; W9 worktree mode derives from branch instead)
  _exploration/<thesis>/      # slate + grounding (as today)
  <slug>/
    STATE.md                  # machine-readable state (schema v2)
    seed.md / hypothesis.md / kill-scan.md
    pressure-report-alpha.md / pressure-report-beta.md
    customer-discovery/{cowork-runpack.md, kill-criteria.json, interviews/*.md}
    customer-discovery.md     # the Discovery Read (name kept)
    market-sizing.md / startup-brief.md
    poc/{poc-brief.md, reactions.md, mvp-input.md}
    gates/criteria-g{2..9}.yaml   # pre-registered gate criteria (write-once)
    evidence-ledger.jsonl / predictions.jsonl
    decision-log.md           # append-only
    learning-log.md           # BML + pivot history (kept; runway = pivots left)
logs/run-log.jsonl            # repo-level, one line per tool call, slug field included
```

### 3.2 STATE.md schema v2 (full sample, mid-W5 typical state)

```yaml
---
slug: hk-broker-recon
schema_version: 2
current_step: 5
step_name: customer_discovery
status: in_progress        # pending | in_progress | blocked | done | killed
owner: human               # who holds the NEXT action: human | agent
interview_budget: {total: 10, used: 4}
step_checklist:
  - {item: "Interviews 5 and 6 done, notes in interviews/", owner: human, done: false}
  - {item: "Extract ledger entries (grade 1-2) from each note", owner: agent, done: false}
  - {item: "Synthesis scores every LOCKED criterion", owner: agent, done: false}
  - {item: "Bias-check worker signs off", owner: agent, done: false}
deltas_pending: [kill-scan]   # stages with unfolded "Hypothesis Updates Flagged" blocks
gates:
  g1: {result: pass, date: 2026-06-16, criteria: gates/criteria-g1.yaml, decision: DL-001}
  g2: {result: pass, date: 2026-06-17, criteria: gates/criteria-g2.yaml, decision: DL-003}
  g3: {result: pass, date: 2026-06-28, criteria: gates/criteria-g3.yaml, decision: DL-005}
  g4: {result: proceed, p_agg: 0.35, date: 2026-07-01, criteria: gates/criteria-g4.yaml, decision: DL-009}
next_action: "Finish interviews 5-6, then run customer-discovery-synthesis"
blocking: null
updated: 2026-07-08T21:40+08:00
---
(Below the frontmatter: optional one-line human summary; machines read the frontmatter only.)
```

**Who writes which field**: `gates:` = advance_gate.py only ｜ everything else = the active step's skill at step close ｜ any hand edit still passes the validator (hook), so format mistakes bounce immediately.

### 3.3 Dual-state audit (reconciling two philosophies)

- **Declared layer**: STATE.md (machine-readable; hooks, gates, dashboard need it)
- **Derived layer**: the router's existing "derive stage from which artifacts exist" logic (`stage-pipeline.md`, updated to the 9 steps in W1)
- **state-audit**: every dashboard render computes both; **derived ≠ declared = a drift alarm** (red row). STATE gets machine-readability without losing the original "no status file can silently rot" insurance

### 3.4 Gate-write enforcement

1. The `gates:` block is written ONLY by `scripts/advance_gate.py`. Script duties: artifact validator green → criteria YAML checked line by line → criteria lock timestamp earlier than evidence file mtimes → **lock-ahead** (criteria-g(n+1) exists and is locked; g9 exempt) → append decision-log → write STATE → self-check via test_state
2. Hook `gates_guard` (PreToolUse on Write|Edit): diff touches `gates:` → deny with "use scripts/advance_gate.py" (the script writes via plain Python file IO under Bash, so it never trips the file-tool hook — that asymmetry IS the enforcement mechanism)
3. Residual risk (agent sed-bypasses via Bash) is caught by ledger-audit's three-way reconciliation: every gate entry must have a matching decision-log entry and criteria file

### 3.5 predictions.jsonl resolution protocol

```json
{"id":"p-003","slug":"hk-broker-recon","gate":"g4","date":"2026-07-01","persona":"munger","claim":">=3 of 10 interviewed brokers spent >=2h on manual reconciliation in the last 30 days","p":0.55,"resolution_criteria":"customer-discovery.md severity table","resolve_by":"2026-07-12","resolved":null,"outcome":null,"brier":null}
{"id":"p-003","resolved":"2026-07-11","outcome":true,"brier":0.2025,"resolved_by":"pressure-beta"}
```

Rules: once locked, claim/p never change; resolution is an **appended supplement line** with the same id (ledger discipline) — β resolves due predictions, the W10 calibration-review clears the rest; validator rejects any prediction missing `resolution_criteria` or `resolve_by`.

-----

## 4. Master File Table — when to create, when to edit, who writes

|File|Create (task/moment)|Edit afterwards|Write authority|Git|
|---|---|---|---|---|
|`~/.claude/CLAUDE.md` (global)|exists|**Add NO project rules** — global holds personal cross-project conventions only (uv, bun, .env layering, safe delete)|human|—|
|`CLAUDE.md` (repo root)|W1 T01, same day|Only when rules change: W2 add two-round protocol line; W5 add hook-behaviour section; W11 update pipeline table after deprecation|human|✓|
|`ideas/CLAUDE.md`|W1 T01|Essentially frozen once written|human|✓|
|`ideas/ACTIVE`|W1 T01|Script changes it on idea switch; retired after W9 (branch-derived)|script|✓|
|`ideas/<slug>/STATE.md`|at scaffold (T01 script / generate-ideas)|`status/next_action/step_checklist/deltas_pending`: the step's skill; **`gates:`: advance_gate.py only**|script + agent, per-field|✓|
|`gates/criteria-g2.yaml`|at scaffold, locked immediately|Never after lock|human drafts → script locks|✓|
|`gates/criteria-g(n+1).yaml`|**before passing G(n)** (lock-ahead forces it)|Never after lock; changing one = reopen the idea or a loudly-stamped decision-log exception|same|✓|
|`customer-discovery/kill-criteria.json`|locked at G4 (the concrete form of criteria-g5; existing schema kept)|Write-once, as today|script|✓|
|`evidence-ledger.jsonl`|empty at scaffold|Append-only: research agent (g4), post-interview extraction (g1–2), ledger-add|agent|✓|
|`predictions.jsonl`|empty at scaffold|Append at G4 (claim/p locked); resolution lines by β / W10|script|✓|
|`decision-log.md`|at scaffold (DL-001 = why this idea)|Append-only: advance_gate automatically + founder override notes|script + human|✓|
|`learning-log.md`|existing, kept|Append on confirmed pivot / validated learning (router flow, as today)|agent (founder confirms)|✓|
|`logs/run-log.jsonl`|auto on first hook fire|**Never hand-edited**|hook|optional|
|`.claude/settings.json` (hooks)|W1 T05; W5 T22/T23 additions|Only when adding hooks|human|✓|
|`.claude/hooks/*.py`|#1/#1b/#3 → T05; #2 → T22; #4/#5 → T23|Bug fixes; behaviour changes rerun their test case|human|✓|
|`scripts/new_idea.py / advance_gate.py / make_brief.py`|T01 / T06 / T10|Logic changes must pass pytest|human|✓|
|`tests/schemas/*.py` + `tests/fixtures/`|**always before the matching skill** (validator-first rule)|Schema change → bump STATE `schema_version` + migration note in the validator|human|✓|
|`.claude/agents/persona-*.md`|T09 (W2 ×3; W7 +Bezos; W3 Rumelt optional)|**Only after a calibration-review** (quarterly from W10) — mid-cycle tuning poisons the calibration data|human|✓|
|`.claude/agents/` (research/judge/aggregator/qc)|T11/T15|Low-frequency, same discipline|human|✓|
|`reports/` (dashboard/Brier)|W7 T29 nightly|Machine-rebuilt; never hand-edited|headless|optional|
|`stage-pipeline.md` (router reference)|exists|**Updated to the 9-step map in W1** (T02's state-audit depends on it); W11 clears legacy names only|human|✓|

**Create-timing rule of thumb**: rule files are born before the thing that uses them (validator before skill, criteria before evidence — lock-ahead); state and ledger files are born empty at scaffold and filled only by the flow. **If you ever feel the need to hand-create a file inside `ideas/`, the scaffold or a skill is missing something — fix the source, don't patch the hole.**

-----

## 5. CLAUDE.md — House Schema + Samples

### 5.1 The house schema (how every CLAUDE.md in this system is written)

Derived from the founder's global file; every layer follows the same shape:

1. **Numbered sections** — `## N. Title`. Numbers are stable anchors other docs and hook messages can cite ("see CLAUDE.md §2")
2. **One rule per bullet** — `- **Keyword**: imperative rule`. The bold keyword is the lookup key; the rule is a command, not a description
3. **ALWAYS / NEVER in caps for absolutes — and every NEVER ships its replacement** (the safe-delete pattern: "NEVER `rm -rf` → use `mv <target> ~/.Trash/`"). A ban without an alternative trains workarounds
4. **Pointer pattern** — `See \`<skill>\` skill for standard.` CLAUDE.md names the law; the skill holds the procedure. Keeps the file short; procedure detail loads on demand
5. **Rules, not data** — anything dynamic (current step, next action) lives in STATE.md. CLAUDE.md is loaded every session: every line is a recurring token cost
6. **Layering, no repetition** — global = personal cross-project tooling; repo = domain constitution; subdirectory = operating protocol. A child layer references a parent rule, never restates it
7. **Mark hook-backed rules** — append "(hook-enforced)" where a hook polices the rule. The doc is the law; the hook is the police; a rule with police gets the badge

### 5.2 Global `~/.claude/CLAUDE.md` — disposition

Unchanged. Your existing schema (e.g., `## 6. Tooling & Runtime`: **Python** always `uv` never raw python/pip; **JavaScript/TypeScript** always `bun` never npm/npx; layered `.env`; full-width rich panels; **Safe delete** NEVER `rm -rf`, `mv` to `~/.Trash/`) stays exactly as is. Add nothing project-specific — pollution here leaks into every other repo. Optional alignment: the official hooks doc's worked example is precisely a `block-rm.sh` PreToolUse guard; your safe-delete rule can graduate from instruction to enforcement in global *settings* (not global CLAUDE.md) if you want a police for it.

### 5.3 Repo `CLAUDE.md` — full sample (W1 version; W2/W5/W11 insertion points marked)

```markdown
# Soriza Startup Layer -- Pipeline Constitution

## 1. Pipeline Canon
- **Stages**: Idea Stage = 9 steps: generate -> hypothesis -> kill-scan -> pressure-a ->
  discovery (design / human interviews / synthesis) -> pressure-b -> sizing -> startup-brief -> PoC
- **Spec**: step cards in `docs/loop-engineering-reference-en.md` SS2. The legacy stage order
  (disconfirm / market-map / solution-design / idea-stage-exit as standalone stages) is RETIRED --
  see the migration table SS2.11

## 2. Write Rules (hook-enforced)
- **Write path**: ONLY write inside `ideas/<ACTIVE>/` and `ideas/_exploration/`;
  ACTIVE = contents of `ideas/ACTIVE` (hook-enforced)
- **Gates**: NEVER edit the `gates:` block of STATE.md -> run
  `uv run scripts/advance_gate.py` instead (hook-enforced)
- **Agent-writable STATE fields**: `status`, `next_action`, `step_checklist`, `deltas_pending` only
- **Hypothesis**: NEVER edit `hypothesis.md` outside `sharpen-hypothesis` -> emit a
  "Hypothesis Updates Flagged" block; folding is that skill's exclusive right
- **Validation feedback**: every artifact write is schema-checked (hook-enforced); on stderr
  feedback, fix and rewrite -- do not argue, do not bypass

## 3. Evidence Rules
- **Web ingress**: web content enters artifacts ONLY via `evidence-ledger.jsonl`; the research
  agent is the single web entry point
- **Grading**: 1=first-party commitment (money/time/intro) | 2=interview quote |
  3=persona opinion | 4=web source (URL required) | 5=founder belief
- **Citations**: ALWAYS cite external facts as `E-xxx`; interview claims cite grade <=2 only

## 4. Kill Authority
- **Desk kills**: hard, checkable facts ONLY (kill-scan: legality / technical impossibility).
  Subjective merit dies only to real users + the founder's signature
- **p_success**: a calibration prediction, NEVER a verdict

## 5. Tooling & Runtime
- **Python**: Always `uv` (`uv run scripts/...`, `uv run pytest`) -- inherits global CLAUDE.md;
  never restated here beyond this pointer
- **Paths**: schemas `tests/schemas/` | gate script `scripts/advance_gate.py` |
  agents `.claude/agents/` | reference `docs/loop-engineering-reference-en.md`

<!-- W2 insert: ## 6. Two-Round Protocol -- independent round blind; cross-exam p-changes need revision_note (ref SS6.3) -->
<!-- W5 insert: ## 7. Hook Behaviour -- Stop blocks until agent-owned checklist items clear; schema failures arrive as stderr -->
<!-- W11: update SS1 pipeline table; remove legacy names -->
```

### 5.4 `ideas/CLAUDE.md` — full sample (written once in W1, then frozen)

```markdown
# ideas/ -- Operating Protocol

## 1. Session Start (read in this order)
- **ACTIVE**: read `ideas/ACTIVE` for the slug
- **STATE**: read `ideas/<slug>/STATE.md` -- current_step / owner / next_action / step_checklist
- **Ownership**: if `owner: human`, NEVER perform the step for the founder -> prepare drafts,
  organize material, remind. Nothing more

## 2. Doing Work
- **Checklist scope**: only items with `owner: agent`
- **On completion**: flip the item to `done: true` immediately; when the step clears, update
  `next_action` and run `uv run scripts/advance_gate.py --slug <slug> --gate gN ...`
- **Citations**: append the ledger entry FIRST, then cite `E-xxx` in the artifact

## 3. Never (each has its lawful alternative)
- **Gates / locked criteria**: never edit -> `advance_gate.py` / reopen via decision-log
- **hypothesis.md**: never edit (unless you ARE sharpen-hypothesis) -> emit a flagged-delta block
- **Ledger history**: never modify old lines -> append a correction line referencing the old ID
- **New file types**: never invent files this protocol does not name -> report it; the scaffold
  gets fixed instead

## 4. Resume
- **SessionStart(resume|compact) hook** injects the ACTIVE STATE summary; if absent, run SS1 manually
```

-----

## 6. Data File Samples

### 6.1 `ideas/ACTIVE`

```
hk-broker-recon
```

### 6.2 `gates/criteria-g4.yaml` (lock-ahead: must be locked before passing G3)

```yaml
gate: g4
slug: hk-broker-recon
locked: true
locked_at: 2026-06-27T22:10+08:00     # must predate the alpha evidence files' mtime; script checks
criteria:
  - {id: g4-1, desc: "pressure-report-alpha.md passes its validator", check: auto, test: test_pressure}
  - {id: g4-2, desc: "5-8 OPEN assumptions, each with a past-behaviour interview question", check: auto}
  - {id: g4-3, desc: "Every persona prediction in predictions.jsonl with resolution_criteria", check: auto}
  - {id: g4-4, desc: "G5 kill-criteria.json locked (lock-ahead)", check: auto}
  - {id: g4-5, desc: "Founder has read all change_my_mind items and signs proceed/pivot", check: human}
```

`check: auto` items are judged by the script against pytest / file existence; `check: human` items require `--attest g4-5` on the advance_gate call (= your signature, recorded in the decision-log).

### 6.3 `evidence-ledger.jsonl` — one line per grade

```json
{"id":"E-001","grade":5,"type":"founder_belief","claim":"Small brokerages reconcile manually in Excel","source":"founder","date":"2026-06-16","added_by":"human"}
{"id":"E-007","grade":4,"type":"web","claim":"Competitor X's top three unresolved G2 review complaints all concern reconciliation errors","url":"https://...","source":"demand-scan","date":"2026-06-27","added_by":"research-agent"}
{"id":"E-012","grade":3,"type":"persona_opinion","claim":"Eisenmann: pattern-matches False Start -- tooling built before WTP validated","source":"pressure-report-alpha.md#eisenmann","date":"2026-06-30","added_by":"judge"}
{"id":"E-019","grade":2,"type":"interview_quote","claim":"Respondent spends 6-8h per month-end on manual reconciliation","quote":"those last two days of the month, I basically do nothing else","source":"interviews/2026-07-03-brokerA.md","date":"2026-07-03","added_by":"agent"}
{"id":"E-023","grade":1,"type":"commitment","claim":"Broker A agrees to a two-week concierge pilot at HK$500","source":"interviews/2026-07-03-brokerA.md","date":"2026-07-03","added_by":"human"}
```

Rules: unique ascending ids; grade ≤4 requires source/url; **corrections are new lines** (`"corrects":"E-007"`), never edits.

### 6.4 `decision-log.md` entry format (append-only)

```markdown
## DL-009 | 2026-07-01 | g4 -> proceed
- Source: scripts/advance_gate.py (criteria-g4.yaml 5/5; g4-5 founder-attested)
- Verdict: proceed (p_agg 0.35)
- Rationale: all three change_my_mind items resolvable by interviews; kill-scan clean
- Signed: Ringo
```

### 6.5 `logs/run-log.jsonl` (hook-written; humans never touch)

```json
{"ts":"2026-07-08T21:32:11+08:00","session":"abc123","slug":"hk-broker-recon","tool":"Write","detail":"ideas/hk-broker-recon/customer-discovery/interviews/2026-07-08-brokerC.md"}
```

-----

## 7. Hooks — Placement, Configuration, Scripts

### 7.1 Where a hook can live (verified, official hooks reference)

|Location|Scope|Shareable|
|---|---|---|
|`~/.claude/settings.json`|All your projects|No (local machine)|
|`.claude/settings.json`|Single project|Yes — committed to the repo|
|`.claude/settings.local.json`|Single project|No (gitignored)|
|Managed policy settings|Organization-wide|Admin-controlled|
|Plugin `hooks/hooks.json`|While the plugin is enabled|Bundled with the plugin|
|**Skill or agent frontmatter**|**While that component is active**|Yes — defined in the component file|

Skill/agent frontmatter hooks use the same configuration format, support all events, and are cleaned up when the component finishes. **For subagents, a `Stop` hook is automatically converted to `SubagentStop`.**

### 7.2 Placement doctrine for this pipeline (the layering decision)

The founder's tip is right that nothing belongs in *global* settings — and this plan never used global; it uses **project** `.claude/settings.json` (committed). The finer split:

|Hook|Placement|Why|
|---|---|---|
|write_path_guard, gates_guard, run_log, stop_guard, resume_inject|**Project settings** (committed)|These are **invariants** — they must hold no matter which skill is active, or when no skill is active at all (a stray agent action is exactly the threat model). A skill-scoped guard only runs while its skill runs: that is a hole, not a guard|
|schema_on_write|**Project-level** (one hook, FILEMAP routes by filename)|Coverage: artifacts get validated even when written outside their "home" skill. Skills MAY additionally carry stricter checks in their own frontmatter (e.g., pressure-test adds a citation-density check) — additive, never a replacement|
|Persona output-contract check|**Persona agent frontmatter** (`Stop` → auto-`SubagentStop`)|Lives and dies with the component; ships inside the agent file; validates the JSON contract the moment the persona finishes, before the orchestrator ever sees a malformed verdict|
|Per-skill workflow checks|**Skill frontmatter**|e.g., kill-scan's hook asserting every verdict line carries an `E-xxx` before the skill may stop|
|Deprecation guard (W11)|Project settings, `UserPromptExpansion` matcher on legacy command names|Blocks `/disconfirm` etc. with a redirect message to the new skill|

Rule of thumb: **invariants in project settings; component-specific contracts ride inside the component.** Frontmatter hooks are also the distribution story — when the layer ships as a plugin or to the Gate-2 founder, component-scoped hooks travel with their components for free.

### 7.3 Project `.claude/settings.json` hooks block (W1 version + W5 additions marked)

```json
{
  "hooks": {
    "PreToolUse": [
      {"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "uv run .claude/hooks/write_path_guard.py"},
        {"type": "command", "if": "Edit(*STATE.md)|Write(*STATE.md)",
         "command": "uv run .claude/hooks/gates_guard.py"}
      ]}
    ],
    "PostToolUse": [
      {"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "uv run .claude/hooks/schema_on_write.py"}
      ]},
      {"matcher": "Write|Edit|Bash|Task", "hooks": [
        {"type": "command", "command": "uv run .claude/hooks/run_log.py"}
      ]}
    ],
    "Stop": [
      {"hooks": [{"type": "command", "command": "uv run .claude/hooks/stop_guard.py"}]}
    ],
    "SessionStart": [
      {"matcher": "resume|compact", "hooks": [
        {"type": "command", "command": "uv run .claude/hooks/resume_inject.py"}
      ]}
    ]
  }
}
```

Notes: the optional `if` field uses permission-rule syntax to narrow spawns at config level (saves process overhead); the `resume|compact` matcher means the STATE summary is re-injected **after context compaction too** — pipeline position survives compaction. Exit-code protocol: 0 = pass (stdout context-injected only for SessionStart/UserPromptSubmit), 2 = block with stderr fed back to Claude; richer JSON decisions (`permissionDecision: deny/allow/ask`) are available if you outgrow exit codes.

### 7.4 Hook scripts

**#1 `write_path_guard.py` (complete, drop-in)**

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
import json, sys
from pathlib import Path

data = json.load(sys.stdin)
fp = (data.get("tool_input") or {}).get("file_path", "")
if not fp:
    sys.exit(0)
root = Path(data["cwd"]).resolve()
target = (Path(fp) if Path(fp).is_absolute() else root / fp).resolve()
ideas = root / "ideas"
try:
    rel = target.relative_to(ideas)
except ValueError:
    sys.exit(0)   # outside ideas/: not this hook's jurisdiction (type-safety hooks still apply)
active = (ideas / "ACTIVE").read_text().strip() if (ideas / "ACTIVE").exists() else ""
top = rel.parts[0] if rel.parts else ""
if top in {"_exploration", "ACTIVE", "CLAUDE.md"} or top == active:
    sys.exit(0)
print(f"[write-path] Only ideas/{active}/ and ideas/_exploration/ are writable; "
      f"you tried {fp}. Switch ideas via the script that updates ideas/ACTIVE.", file=sys.stderr)
sys.exit(2)
```

**#1b `gates_guard.py` (skeleton + decisive branches)**

```python
data = json.load(sys.stdin)
ti = data.get("tool_input") or {}
fp = ti.get("file_path", "")
if not fp.endswith("STATE.md"):
    sys.exit(0)

def gates_block(text: str) -> str:
    """Extract the raw gates: block from frontmatter (empty string if absent)."""
    ...

if data["tool_name"] == "Edit":
    if "gates" in ti.get("old_str", "") + ti.get("new_str", ""):
        deny("Edit touches gates: -- run uv run scripts/advance_gate.py")
else:  # Write
    p = Path(fp)
    if p.exists() and gates_block(p.read_text()) != gates_block(ti.get("content", "")):
        deny("Write changes gates: -- use advance_gate.py")
sys.exit(0)
# deny() = print reason to stderr + sys.exit(2)
# Creating a fresh STATE.md (file absent) passes -- scaffold writing gates: {} is lawful
# Bash-sed bypass risk is caught downstream by ledger-audit's three-way reconciliation
```

**#2 `schema_on_write.py` (skeleton)**

```python
FILEMAP = {
    "STATE.md": "test_state", "hypothesis.md": "test_hypothesis",
    "kill-scan.md": "test_killscan", "pressure-report-alpha.md": "test_pressure",
    "pressure-report-beta.md": "test_pressure_beta", "customer-discovery.md": "test_synthesis",
    "evidence-ledger.jsonl": "test_ledger", "predictions.jsonl": "test_predictions",
    "market-sizing.md": "test_sizing", "startup-brief.md": "test_brief",
}
# pattern branches: interviews/*.md -> test_interview ; gates/criteria-*.yaml -> test_criteria
fp = (data.get("tool_input") or {}).get("file_path", "")
key = match(fp)                      # FILEMAP + patterns; no match -> exit 0
if not inside_ideas(fp):
    sys.exit(0)
r = subprocess.run(
    ["uv", "run", "pytest", "tests/schemas", "-q", "-k", key, "--artifact", fp],
    capture_output=True, text=True, cwd=data["cwd"])
if r.returncode != 0:
    sys.stderr.write(r.stdout[-1500:])   # fed back to the agent for self-repair: the doc-TDD closed loop
    sys.exit(2)
```

**#4 `stop_guard.py` (complete anti-deadlock logic)**

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
import json, sys, yaml
from pathlib import Path

data = json.load(sys.stdin)
if data.get("stop_hook_active"):           # official anti-infinite-loop flag: second pass always releases
    sys.exit(0)
root = Path(data["cwd"])
af = root / "ideas" / "ACTIVE"
if not af.exists():
    sys.exit(0)
sp = root / "ideas" / af.read_text().strip() / "STATE.md"
if not sp.exists():
    sys.exit(0)
st = yaml.safe_load(sp.read_text().split("---")[1])
if st.get("status") != "in_progress" or st.get("owner") == "human":
    sys.exit(0)                            # never push agents at human-owned items -- the deadlock fix
todo = [c["item"] for c in st.get("step_checklist", [])
        if c.get("owner") == "agent" and not c.get("done")]
if not todo:
    sys.exit(0)
print("Unfinished before stopping (owner=agent):\n- " + "\n- ".join(todo), file=sys.stderr)
sys.exit(2)
```

**#3 `run_log.py` and #5 `resume_inject.py` (cores)**

```python
# run_log.py -- append one line to logs/run-log.jsonl (slug from ideas/ACTIVE, null if unreadable)
rec = {"ts": now_iso(), "session": data.get("session_id"), "slug": active_slug(),
       "tool": data["tool_name"], "detail": detail(data["tool_input"])}  # file_path or cmd[:120]

# resume_inject.py -- on SessionStart(resume|compact), print to stdout (injected into context)
print(f"[resume] idea={slug} step={st['current_step']} ({st['step_name']}) owner={st['owner']}\n"
      f"next_action: {st['next_action']}\nopen items: {todo_items}")
```

### 7.5 Component-scoped hooks (the founder's tip, applied)

**Persona agent self-validating its contract** — `.claude/agents/persona-eisenmann.md` frontmatter:

```yaml
---
name: persona-eisenmann
description: Failure-pattern verdicts for pressure-test rounds; reads neutral-brief + ledger only.
tools: Read
model: sonnet
hooks:
  Stop:                      # auto-converted to SubagentStop for subagents
    - hooks:
        - type: command
          command: "uv run .claude/hooks/persona_contract_check.py"
---
```

`persona_contract_check.py` parses the persona's final output as JSON against the contract (p_success ∈ [0,1], base_rate_ref, change_my_mind non-empty…); exit 2 + reason makes the persona repair its answer **before** the orchestrator ever receives it. A malformed verdict now never reaches the judge.

**Pipeline skill carrying its own extra check** — e.g. `pressure-test` SKILL.md frontmatter:

```yaml
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          if: "Write(*pressure-report*)"
          command: "uv run .claude/hooks/citation_density_check.py"
```

This runs only while pressure-test is active — correct, because it is that skill's private standard, not a repo invariant.

### 7.6 Deprecation guard (W11) — `UserPromptExpansion`

```json
{"hooks": {"UserPromptExpansion": [
  {"matcher": "disconfirm|market-map|solution-design|idea-stage-exit",
   "hooks": [{"type": "command", "command": "uv run .claude/hooks/deprecated_redirect.py"}]}
]}}
```

The script blocks the expansion and prints the redirect ("retired — run /pressure-test | /kill-scan + /market-sizing | /startup-brief"). Legacy muscle memory now teaches the new map instead of silently running the old pipeline.

### 7.7 Prompt hooks — where regex can't judge

Hook handlers also come in `type: "prompt"` (single-turn LLM yes/no) and experimental `type: "agent"` variants. Use sparingly (cost per fire), but they cover what pytest can't: a prompt hook on interview-note writes asking *"does this note contain the founder pitching instead of listening?"* is a Mom-Test discipline check no regex expresses. Deterministic checks stay `command`+pytest; judgment checks may be `prompt`. Adopt only after W5 when the deterministic layer is proven.

-----

## 8. Script Skeletons

**`scripts/new_idea.py`** (T01; backfills the two existing concepts; later called inside generate-ideas' scaffold)

```python
# usage: uv run scripts/new_idea.py hk-broker-recon
# 1) mkdir ideas/<slug>/{customer-discovery/interviews,gates,poc}
# 2) write STATE.md from template (schema v2, current_step=1, gates: {})
# 3) write gates/criteria-g2.yaml from template (locked: true, locked_at=now)
# 4) open empty ledgers: evidence-ledger.jsonl / predictions.jsonl / decision-log.md
#    (DL-001 = why this idea -- prompts you for one sentence)
# 5) ideas/ACTIVE <- slug
# 6) print next_action: "run /sharpen-hypothesis <slug>"
```

**`scripts/advance_gate.py`** (T06; the only gate-write entrance)

```python
# usage: uv run scripts/advance_gate.py --slug hk-broker-recon --gate g4 \
#          --result proceed --p-agg 0.35 --attest g4-5
# steps (sequential; any failure stops cold, STATE untouched):
# 1) load gates/criteria-<gate>.yaml; verify locked==true and locked_at predates evidence mtimes
# 2) check:auto items -> run mapped pytest -k / file existence; check:human items -> require --attest <id>
# 3) lock-ahead: gates/criteria-g(n+1).yaml exists and is locked (g9 exempt)
# 4) append decision-log (new DL-id: source / verdict / criteria results / attestations)
# 5) write STATE: gates.<gate> = {result, date, criteria, decision[, p_agg]};
#    advance current_step / step_name / status / owner / fresh step_checklist from the step template
# 6) run test_state on itself; print the verdict summary
# Note: the script writes via plain Python file IO (under Bash), so it never trips gates_guard --
# that asymmetry IS how "script-only writes" is implemented.
```

**`scripts/make_brief.py`** (T10)

```python
# hypothesis.md -> neutral-brief.md:
# 1) strip the founder's name (from docs/founder-profile.md), first-person pronouns, company names
# 2) strip banned tokens (tests/fixtures/banned_tokens.txt -- SHARED with the brief validator):
#    enthusiasm adjectives (revolutionary/unique/huge...), sunk-cost phrasing (already built/invested...)
# 3) recast the four dimensions as neutral declaratives; 250-word cap
# 4) hook #2 then runs test_brief on the output -- mechanical de-identification + validator gate;
#    persona Appendix C adds the final layer ("ignore residual identity cues")
```

-----

## 9. Validators (the doc-TDD foundation)

Inventory and shipping weeks: STATE / hypothesis / criteria / ledger-lite → W1; brief(neutral) / pressure-α / predictions → W2; kill-scan → W3; interview / synthesis / ledger-full → W4; startup-brief → W6; pressure-β / sizing / poc → W7–8. **Validator before skill, always.**

**`tests/conftest.py`** (once, shared)

```python
from pathlib import Path
import pytest

def pytest_addoption(parser):
    parser.addoption("--artifact", action="store", default=None)

@pytest.fixture
def artifact_text(request):
    p = request.config.getoption("--artifact")
    p = Path(p) if p else Path("tests/fixtures") / request.module.FIXTURE
    return p.read_text(encoding="utf-8")
```

**`tests/schemas/test_hypothesis.py`** (T03, complete — translated from the existing template + output constraints)

```python
import re

FIXTURE = "hypothesis.sample.md"
SECTIONS = ["WHO", "HOW OFTEN", "HOW SEVERE", "STATUS QUO", "VALUE & GROWTH"]

def _sec(text, name):
    m = re.search(rf"^##\s*{name}\b(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    assert m, f"Missing section: {name}"
    return m.group(1)

def test_sections_present(artifact_text):
    for s in SECTIONS:
        _sec(artifact_text, s)

def test_length_cap(artifact_text):
    body = re.sub(r"[#>\-\s`*]", "", artifact_text)
    assert len(body) <= 2000, "Body too long (mechanical proxy for <=300 words; calibrate to your template)"

def test_provisional_flag(artifact_text):
    assert "provisional" in artifact_text.lower()

def test_quantified_dimensions(artifact_text):
    for s in ("HOW OFTEN", "HOW SEVERE"):
        assert re.search(r"\d", _sec(artifact_text, s)), f"{s} has no number -- forcing specificity failed"

def test_no_web_citations(artifact_text):
    assert "http" not in artifact_text, "hypothesis may not cite the web (sharpen, don't prove)"
```

Pattern: **every assert message is written for the agent** — hook #2 feeds it back verbatim for self-repair, so the message must say *what right looks like*, not just that it's wrong. Each validator ships with a green fixture and a red one (`hypothesis.bad.md`) proving the validator actually bites. **Red-to-green on fixtures before the skill is written — that is doc-TDD, literally.**

-----

## 10. Persona Subagent Sample (conversion recipe applied)

`.claude/agents/persona-eisenmann.md` — frontmatter as in §7.5 (incl. the self-validation hook), then:

```markdown
[Paste the body of /mnt/skills/user/tom-eisenmann-perspective/SKILL.md verbatim --
 first-person voice, Six Failure Patterns, RAWI, the Response Workflow, all of it]

---
## Appendix A -- Role Override (read first)
Your perspective rule "retrospective is fair game, prospective is off-limits -- I will not
name a living startup as likely to fail" has one explicit exception in this seat: the brief
is de-identified, and you act as a calibrated forecaster doing reference-class forecasting,
not as a public commentator naming names. Therefore p_success MUST be given, by your own
base-rate method.

## Appendix B -- Independent-round output contract (reply = a single JSON object, no preamble)
{"persona":"eisenmann",
 "p_success":0.0,
 "base_rate_ref":"which reference class and why",
 "risk_patterns":["six-pattern hits"],
 "sharpest_objection":{"objection":"...","falsifiable_assumption":"...","interview_question":"past-behaviour question"},
 "steelman_for":"the single strongest reason this idea works",
 "change_my_mind":"the evidence that would change my verdict"}

## Appendix C -- Access rules
- Read ONLY the two paths the spawn prompt gives you: neutral-brief.md, evidence-ledger.jsonl
- What the brief omits is unknown; reflect that in p. Never ask for more context
- Ignore residual identity cues; never echo them into output
- Cross-exam round: you receive sibling JSONs; you may revise p, but only with a "revision_note"
```

Thiel / Munger / Bezos: same recipe. **Appendix A is the only part that needs thought** — check each perspective for a principle that conflicts with the forecaster seat (Eisenmann's no-prospective rule is the known case) and override it explicitly.

-----

## 11. Automation Map — Claude Code Built-ins per Pipeline Step

### 11.1 The built-in inventory (what does the automating)

|Built-in|Role in this pipeline|
|---|---|
|**Skills as slash commands**|Skills and slash commands are unified: every pipeline skill is invocable as `/skill-name <slug>`, with `$ARGUMENTS` substitution; frontmatter (`disable-model-invocation`) controls whether Claude may auto-invoke it or only you may. Stage skills = human-triggered (`disable-model-invocation: true` is the safe default for gate-adjacent skills); utility skills (ledger-add) can stay auto-invocable|
|**Subagents (Task)**|The parallel fan-outs: personas, researchers, facet workers — already your core machinery|
|**Hooks**|The in-session closed loop (§7): validate-on-write, forced completion, path/gate police, contract checks|
|**Headless (`claude -p`)**|The out-of-session loop: cron jobs with `--output-format json`, scoped `--allowedTools`, a chosen `--permission-mode` for unattended runs; `Setup` hooks (`--init`/`--maintenance` flags) for one-time prep in scripts/CI|
|**`--resume` / `--continue`**|Re-enter a session programmatically; pairs with SessionStart(resume) injection|
|**Event hooks beyond the basic five**|`SubagentStop` (persona contract), `SessionStart(compact)` (state survives compaction), `UserPromptExpansion` (deprecation guard), `FileChanged` (watch e.g. STATE.md for out-of-band edits), `PostToolUseFailure` (log failures to run-log), `WorktreeCreate/Remove` (W9 worktree lifecycle)|
|**Plugins**|Bundle commands + agents + hooks + skills as one installable unit — the natural W12 packaging: the Gate-2 external founder installs the layer in one step, hooks included|
|**Agent SDK**|The "fully-automatic orchestration layer" the router already names as future work — only after the human-gated version validates (Rule Zero applies to automation itself)|

### 11.2 Per-step map: trigger → chain → what closes automatically → what stays human

|Step|Trigger|Automated chain|Auto-closed by|Human keeps|
|---|---|---|---|---|
|1 generate|`/generate-ideas <thesis>`|researcher + seed-gen agents → slate → scaffold script|slate/STATE validators|the pick (G1)|
|2 hypothesis|`/sharpen-hypothesis <slug>`|interactive by design (AskUserQuestion)|hook #2; advance_gate auto-checks|content testimony + G2 sign|
|3 kill-scan|`/kill-scan <slug>` — one command|research agent → ledger → artifact; **Stop hook refuses to let the agent finish with open agent-items**|validators + stop_guard|override only (G3)|
|4 α|`/pressure-test <slug>`|make_brief.py → 3 personas in parallel → **SubagentStop validates each JSON before return** → cross-exam → judge → aggregator → predictions locked|contract hooks + validators + advance_gate criteria|read change_my_mind; sign G4|
|5a design|`/customer-discovery-design <slug>`|sealed pack drafted; **never sends** (structural)|pack validators|—|
|5 interviews|none — human only|Cowork sends cold per approved batch; founder interviews|—|everything|
|5b synthesis|`/customer-discovery-synthesis <slug>`|per-note ledger extraction → scoring vs LOCKED criteria → bias-check|validators|G5 sign|
|6 β|`/pressure-test <slug> --beta`|α chain + citation enforcement + resolves due predictions|citation validator|G6 — the kill decision|
|7 sizing|`/market-sizing <slug>`|parallel facet agents → bottom-up sizing|validators|read|
|8 brief|`/startup-brief <slug>`|build_delta_ledger.py → crystallize → red-team → premortem → locks G9 criteria|validators|GO/NO-GO + drift ❌ rows|
|9 PoC|`/build-poc <slug>`|scope agent; functional builds in their own worktree (WorktreeCreate)|poc validators|pretotype, 5 conversations, G9|
|Nightly|cron: `claude -p "/idea-dashboard --all" --allowedTools ...`|dashboard rebuild + state-audit + ledger-audit → `reports/`|—|read the morning brief|
|Weekly|cron: calibration snapshot (from W10)|Brier deltas → `reports/`|—|persona/rubric tuning decision|

### 11.3 The automation ladder (adopt in this order)

1. **L0 — in-session closure (W1–W5)**: hooks. Validate-on-write feeds errors back for self-repair; stop_guard refuses early exits; gates_guard + write_path_guard police invariants. This is where "skill ran" becomes "skill ran *correctly or not at all*"
2. **L1 — one-command chains (W2–W8)**: each step = one slash invocation that runs a whole agent fan-out and ends at a gate the founder signs. The human acts exactly twice per step: trigger and signature
3. **L2 — scheduled headless (W7+)**: cron `claude -p` for everything no-judgment: dashboard, audits, Brier. Output to `reports/`, never into `ideas/`
4. **L3 — event-driven (W9+, optional)**: FileChanged on STATE.md (out-of-band edit alarm), SessionStart(compact) re-injection, UserPromptExpansion deprecation guard
5. **L4 — packaging and SDK (post-validation)**: plugin-ify the layer for Gate-2 distribution and beyond; SDK orchestration only after the human-gated pipeline has survived an external founder. Automating an unvalidated pipeline just produces wrong artifacts faster

### 11.4 Never automated (by design, not by limitation)

Interviews and commitments; outreach sending (Cowork per-batch approval); every `check: human` gate attestation; kill decisions on subjective merit; criteria thresholds; persona/rubric tuning timing (calibration-review only). These are the founder's skin in the game — the loop's contact points with reality.

-----

## 12. Build Schedule (condensed) + Change Log

|Wk|Build focus (tasks)|DoD / Gate|Evidence track|
|---|---|---|---|
|W1|State + validators + hooks #1/#1b/#3 + gate script + retrofit (T01–T08)|pytest green; concept #1 past G2|25-prospect tiered list (warm★ from demand mining)|
|W2|Persona conversion ×3, brief script, α orchestrator, canary test (T09–T14)|3 personas return schema-valid JSON; isolation proven|warm replies sent by hand; Cowork cold batch approved; book 3–5|
|W3|kill-scan, α full protocol, G5 lock wiring (T15–T18)|concept #1 through kill-scan + α; G4 triple lock|first 2–3 interviews|
|W4|interview/synthesis validators, synthesis wiring, dashboard v0.1 (T19–T21)|**Gate 1: ≥5 interviews logged; synthesis cites ledger vs LOCKED criteria**|interviews 4–5|
|W5|hooks #2/#4/#5, ledger-audit (T22–T24)|Stop-loop demo; audit report #1|top-up interviews if α predictions miss|
|W6|startup-brief validator → skill (T25–T26)|brief passes validator + qc|founder reads every drift ❌ row|
|W7|β mode, market-sizing, nightly headless, **Gate-2 founder recruiting opens** (T27–T30)|concept #1 β + sizing; **G6 signed**|≥2 Gate-2 candidates replied|
|W8|build-poc wiring (T31)|poc-spec valid; G8 stamped|pretotype live; Gate-2 slot locked|
|W9|worktrees, +Bezos, isolation re-test (T32–T33)|2 ideas in parallel, no cross-pollution|pretotype commitment data|
|W10|calibration-review + Brier v1 (T34)|first calibration report|evidence aligned across both concepts|
|W11|deprecation cleanup + UserPromptExpansion guard, concept #2 completion (T35–T36)|both concepts full artifact chains|PoC results in STATE|
|W12|Gate-2 walkthrough pack — consider plugin packaging (T37)|**Gate 2: external founder walks it end-to-end, feedback on record**|go → MVP layer / kill → next slate idea|

W1 daily: Fri T01+T04 + start Mom Test ｜ Sat (3h) T02+T03 + warm-tier mining ｜ Sun read 2h + T05 ｜ Mon T06 (flex item) ｜ Tue T07+T08 ｜ Wed list to 25 + outreach drafts ｜ Thu close: pytest green, g2 in STATE, DL-001 written. **Explicitly not in W1**: Nuwa distillation (personas exist — convert in W2), concept #2, microsandbox (PoC-stage only; this is the documented temptation).

### Change log vs the Chinese v2 + handbook

1. CLAUDE.md samples rewritten to the house schema (§5.1): numbered sections, keyword bullets, NEVER-with-replacement, pointer pattern, hook-enforced badges
2. Hook placement doctrine added (§7.2) on the verified skill/agent-frontmatter capability; persona contract check moved INTO the persona file (Stop→SubagentStop); per-skill extra checks allowed as additive layers; invariants stay project-level
3. New automation map (§11): step-by-step trigger/chain/human table, the five-level adoption ladder, the never-automated list; plugin packaging proposed for Gate-2 distribution
4. settings.json gains `if` filters, the `resume|compact` SessionStart matcher (state survives compaction), and the W11 UserPromptExpansion deprecation guard
5. Carried errata: run-log at repo level `logs/` with a slug field; hook #5 scheduled in T23; `stage-pipeline.md` 9-step map updated in W1