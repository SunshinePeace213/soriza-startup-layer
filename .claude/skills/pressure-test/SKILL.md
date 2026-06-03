---
name: pressure-test
description: |
  Second step in the Idea Stage of Soriza Startup Layer — pressure-tests the founder's
  hypothesis (from /sharpen-hypothesis) by orchestrating a 4-round adversarial panel of
  4–6 distilled expert personas (Thiel, Bezos, Munger, Taleb, Eisenmann, Tan, Musk,
  Naval, Jobs, Pareto, Horowitz, and any future *-perspective skills). Each expert
  opens with disconfirming objections in voice; the founder commits to substantive
  responses; experts rebut and judge. The panel — not the founder — decides whether
  the hypothesis is ready for customer discovery. Output: a pressure-test.md under
  the idea's docs/ideas-stages folder with disconfirmation questions, kill criteria,
  hypothesis updates, and per-expert provenance files.
when_to_use: |
  Use when the founder says "pressure-test", "stress-test my hypothesis", "argue
  against my idea", "find disconfirming evidence", "what would kill this",
  "red-team this hypothesis", "panel review", "what would Thiel/Bezos/Munger think",
  "ready for customer discovery", "next step after /sharpen-hypothesis", "find
  counterarguments". Also trigger when the founder says "what's next" or "the next
  step" AND a hypothesis.md exists in the idea's docs/ideas-stages folder but
  pressure-test.md does NOT yet exist — once pressure-test.md exists, "what's next"
  hands off to /market-research.
argument-hint: "[slug]"
allowed-tools: AskUserQuestion, Read, Write, Bash, Glob, Agent, Task
---

# Pressure-Test

Second step in the **Idea Stage** of the Soriza Startup Layer. Subjects the founder's hypothesis to an adversarial panel of 4–6 distilled persona skills, surfaces the strongest disconfirming evidence, and lets the panel decide whether the founder may proceed to customer discovery. The skill's job: argue against the founder's idea and surface the disconfirming evidence that would refute the hypothesis — before the founder spends weeks building or interviewing on a flawed premise.

- **Input:** `docs/ideas-stages/<slug>/hypothesis.md` (from `/sharpen-hypothesis`)
- **Output:** `docs/ideas-stages/<slug>/pressure-test.md` + per-expert files under `pressure-test/openings/` and `pressure-test/rebuttals/`
- **Personas:** Existing `.claude/skills/*-perspective/` skills, read by subagents at runtime

## When this skill applies

- Founder has a `hypothesis.md` at `docs/ideas-stages/<slug>/` and asks "what's next"
- "Pressure-test", "stress-test", "argue against this", "find disconfirming evidence"
- "What would Thiel/Bezos/Munger think about this hypothesis"
- "Ready for customer discovery" — let the panel decide whether they are

Out of scope: solution design, market sizing, competitor landscape (those are `/market-research`, the next pipeline step), editing `hypothesis.md` (that's `/sharpen-hypothesis`'s job), customer discovery itself (downstream, after `/market-research`).

## Gotchas

- **The founder does not pick the verdict — the panel does.** Founder picks only the *response* to the verdict (accept / explicit-override / abort). This breaks confirmation-bias laundering and is the whole reason the skill exists; do not let the founder veto the pass-threshold rule.
- **The anti-thesis expert is structurally permitted to keep restating-harder at the end** without blocking pass. Their persistent objection becomes a flagged interview target. Without this rule the panel either never passes (anti-thesis always finds something) or anti-thesis is decorative.
- **Subagents read `*-perspective/SKILL.md` files from disk via the Read tool** — do not inline persona content into the parent context. Each persona skill is ~200 lines; inlining 4–6 of them blows the parent's context budget. Persona content lives in each subagent's window only.
- **Round 1 and Round 4 each dispatch all subagents in a single assistant message.** Parallel execution requires it. Sequential dispatch makes the skill ~6× slower without changing behaviour.
- **The single deliverable is `pressure-test.md`.** Files under `pressure-test/openings/` and `pressure-test/rebuttals/` are provenance; downstream skills (`/market-research`, then customer discovery) read `pressure-test.md`, not the per-expert files.
- **If `hypothesis.md` is missing, refuse.** No inline mini-sharpen. `/sharpen-hypothesis` owns `hypothesis.md`; the contract between the two skills is the file at the path.
- **Subagent rebuttal output must contain exactly one of `WITHDRAW`, `ACCEPT-WITH-CONDITIONS`, or `RESTATE-HARDER`** under `## Final Verdict`. Parsing depends on it. If a rebuttal file is malformed, dispatch a single retry subagent for that expert before treating it as a hard error.
- **Create the `pressure-test/openings/` and `pressure-test/rebuttals/` subdirectories before dispatching subagents.** Subagents use Write tool to a fixed path; if the parent directory doesn't exist, the Write fails and the round aborts.
- **This skill REQUIRES a real subagent-spawn tool — it must not degrade to inline role-play.** The spawn tool is named `Agent` in Claude Code and `Task` in some harnesses (both are in `allowed-tools`). Before Round 1, confirm a spawn tool is actually available. If neither is, **stop and tell the founder** — do NOT fall back to the main agent voicing all 4–6 personas in one context. Inline role-play silently destroys the whole value of the skill: the personas would share one context window, contaminate each other, and collapse into a single averaged voice instead of independent adversaries. The whole point is N isolated windows.
- **Dispatch the persona subagents at high reasoning effort.** Objection quality *is* the deliverable — a shallow, generic objection defeats the panel. If your harness's spawn tool exposes an `effort`/`model` parameter, set `effort: high` on every Opening/Rebuttal dispatch (`xhigh` for the rebuttal-judgment round). If it does not, run the whole `/pressure-test` session at high+ effort; the skill's value scales directly with how hard each persona reasons.
- **Persona skill paths are resolved at runtime, never hardcoded.** Step 3 globs `.claude/skills/*-perspective/` and captures each persona's absolute `SKILL.md` path; that path is substituted into the `<PERSONA_SKILL_PATH>` placeholder in the subagent templates. Do not bake any machine-specific path (a home directory, a Desktop path) into a dispatch — it breaks the moment the repo is cloned or moved.

## Workflow

Goal: assemble an adversarial expert panel, run a 4-round debate, compute a panel verdict, and either write `pressure-test.md` with the verdict or kick back to `/sharpen-hypothesis` for refinement.

Steps below are ordered because they're genuinely sequential (you cannot rebut before openings; you cannot compute verdict before rebuttals). Within each step, treat the bullets as constraints rather than a script — the *how* is your judgment unless a specific shape is named.

### Step 1 — Resolve slug and read hypothesis

If invoked with a slug argument (e.g., `/pressure-test contract-redline-tool`), use it. Otherwise glob `docs/ideas-stages/*/` and fire `AskUserQuestion` with the available slugs as options.

Read `docs/ideas-stages/<slug>/hypothesis.md`.

**Entry guard:** if `hypothesis.md` is missing, refuse with exactly: *"No hypothesis at `docs/ideas-stages/<slug>/hypothesis.md`. Run /sharpen-hypothesis first — it produces the input I need."* Stop. Do not write any files.

### Step 2 — Resume check

If `docs/ideas-stages/<slug>/pressure-test.md` already exists, fire `AskUserQuestion`:

- **Overwrite from scratch** — `rm -rf docs/ideas-stages/<slug>/pressure-test/` and proceed
- **Append timestamped new round** — keep existing file; write new round outputs under `pressure-test/<ISO-date>/openings/` and `pressure-test/<ISO-date>/rebuttals/`; append a new `## Round <N> (<date>)` section to `pressure-test.md`
- **Skip and exit** — print the existing verdict line, do nothing else

### Step 3 — Curate the panel

`glob .claude/skills/*-perspective/SKILL.md` to discover the installed persona pool **and capture each one's absolute path** — you will substitute that path into the subagent templates' `<PERSONA_SKILL_PATH>` placeholder, so paths stay correct on any machine. Then read `references/shape-mapping.md` and apply the table to the hypothesis content:

1. Always include the default base (Eisenmann, Bezos)
2. Add specialists per hypothesis attributes (B2B SaaS → +Tan; hardware → +Musk; regulated → +Munger; fat-tail risk → +Taleb; etc.)
3. Pick the anti-thesis slot based on the hypothesis's dominant temperamental shape (see the anti-thesis selection rules in the reference)
4. If fewer than 4 experts, fill to 4 in priority order: Eisenmann, Munger, Thiel
5. If more than 6, drop lowest-priority specialist additions to cap at 6

Output of this step: a list of 4–6 `(persona_name, persona_slug, role, skill_path)` tuples with exactly one tagged `anti-thesis: true`. `skill_path` is the absolute path captured from the glob — never a hardcoded literal. Remember which `persona_slug` carries the anti-thesis tag; Step 8 needs it — and it must equal that expert's rebuttal `.md` filename stem, since the verdict script matches them by name.

Print the panel composition to chat. Example: *"Panel for this hypothesis: Eisenmann (failure scholar), Bezos (customer obsession), Tan (consumer/network), Taleb (anti-thesis: fragility lens)."* No question here — just inform.

Create the directory layout before any subagent dispatch:
```
docs/ideas-stages/<slug>/pressure-test/openings/
docs/ideas-stages/<slug>/pressure-test/rebuttals/
```

### Step 4 — Round 1: Openings (parallel)

Dispatch all 4–6 subagents in a single assistant message, **at high reasoning effort** (set `effort: high` on the spawn call if your tool supports it). Each call uses the **Opening template** (below), with `<PERSONA_SKILL_PATH>` substituted with the absolute path captured in Step 3. The subagents run in parallel; you'll receive task notifications as each completes.

Once all are reported complete, Read each `pressure-test/openings/<persona_slug>.md` to confirm content. Print a one-line summary per expert in chat: *"Thiel opened with: <verdict line from file>."*

### Step 5 — Round 2: Cross-fire synthesis (main agent only)

Read all opening files. Identify the **two** sharpest expert-vs-expert disagreements — points where two experts take incompatible positions on the same claim (e.g., Thiel: "this could be a monopoly because lock-in" vs. Taleb: "lock-in is fragility under tail events"). Write ~150 words of synthesized dialogue in chat — quote each expert's position briefly, frame the disagreement, name the tension.

No subagents in this step. This is the only round where the main agent speaks in personas' voices (paraphrasing). Keep it tight and substantive.

### Step 6 — Round 3: Founder fix (per-expert AskUserQuestion)

For each expert in the panel (4–6 rounds), fire one `AskUserQuestion`. Bundle that expert's 1–2 objections into the question prompt — the founder responds to both together.

**Question prompt shape:**
> *"How do you address `<expert_name>`'s objections?*
>
> *<expert_name>'s objections (from `pressure-test/openings/<slug>.md`):*
> *1. <objection 1>*
> *2. <objection 2 if present>*
>
> *Pick the response type and write your specific fix in notes."*

**Options:**
- **Concede — hypothesis needs updating** — founder writes the *specific* update in notes (e.g., "narrow Who to 'series A SaaS legal teams 50–200 employees'")
- **Plan to disconfirm in interviews** — founder writes the *specific* interview question in notes (e.g., "Ask 5 prospects 'how many hours per cycle?' — if median <2, severity claim dies")
- **Dispute** — founder writes counter-claim with reasoning in notes (e.g., "TAM is large; comparable Y did $100M ARR in this segment")
- **Acknowledge, no fix** — honest stance; will likely earn restate-harder in Round 4

The founder's `notes` text *is* the substantive fix and feeds Round 4. Capture it keyed by expert slug.

### Step 7 — Round 4: Rebuttals (parallel)

Dispatch all 4–6 rebuttal subagents in a single assistant message, **at high reasoning effort** (`effort: xhigh` if supported — this is the judgment round). Each call uses the **Rebuttal template** (below), with `<PERSONA_SKILL_PATH>` substituted from Step 3, and passed its expert's opening file path plus the founder's notes text for that expert.

Once all are complete, each `pressure-test/rebuttals/<persona_slug>.md` carries:

- `## Final Verdict` — exactly one of `WITHDRAW`, `ACCEPT-WITH-CONDITIONS`, `RESTATE-HARDER`
- `## Fatal flag` section — `STRUCTURALLY-FATAL` token present or absent

If `compute_verdict.py` (Step 8) reports any file in its `malformed` list, dispatch one retry subagent for that expert with the malformed file appended to the prompt, then re-run the script. If the retry still fails, re-run with `--allow-malformed` (the documented fallback coerces it to `RESTATE-HARDER`) and note the coercion in the action card.

### Step 8 — Compute verdict (pass-threshold rule)

The verdict is a deterministic tally — **run the bundled script rather than tallying by eye**, so a mis-count can't silently flip a verdict:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/compute_verdict.py" \
  docs/ideas-stages/<slug>/pressure-test/rebuttals \
  --anti-thesis <anti_thesis_slug>
```

It parses each rebuttal's `## Final Verdict` and `## Fatal flag` tokens (tolerant of case/spacing), applies the truth table below, and **on a clean compute (exit 0)** prints `verdict`, `anti_thesis_flag`, `per_expert`, `tally`, and `malformed` (empty). The `<anti_thesis_slug>` you pass **must be the exact `persona_slug` whose rebuttal file is on disk** — it equals that rebuttal's `.md` filename stem (Step 3). If it matches no file the anti-thesis exemption can't be applied, so the script instead prints `{verdict: null, anti_thesis_warning, seats, message}` and exits 2 — fix the slug and re-run, don't read a verdict from it. Likewise if any rebuttal is malformed it prints `{verdict: null, malformed, message}` and exits 2 — go back to the Step 7 retry rule rather than guessing. The truth table it implements, evaluated among the **non-anti-thesis** experts (3–5 of them):

| Outcome | Verdict |
|---|---|
| All returned `WITHDRAW` or `ACCEPT-WITH-CONDITIONS` | `ship-with-conditions` |
| ≥1 returned `RESTATE-HARDER` without `STRUCTURALLY-FATAL` | `refine-hypothesis` |
| ≥1 expert (any seat, including anti-thesis) flagged `STRUCTURALLY-FATAL`, OR ≥3 non-anti-thesis experts returned `RESTATE-HARDER` | `kill-suggested` |

The anti-thesis expert's `RESTATE-HARDER` (without `STRUCTURALLY-FATAL`) does NOT block pass — the script returns `anti_thesis_flag: true`, which surfaces as the **Anti-thesis Flag** in the action card.

### Step 9 — Draft action card and confirm

Synthesize the action card sections from collected round data:

- **Verdict** — computed in Step 8
- **Disconfirmation Questions** — from founder's "Plan to disconfirm" notes across Round 3 (deduplicate and tighten phrasing)
- **Kill Criteria** — from `STRUCTURALLY-FATAL` flags + your synthesis of severity signals across rebuttals
- **Hypothesis Updates Required** — from founder's "Concede" notes
- **Open Risks** — from founder's "Dispute" notes + experts who returned `RESTATE-HARDER` whose objections the founder did not concede
- **Anti-thesis Flag** — if and only if the anti-thesis returned `RESTATE-HARDER`, one line: *"`<expert>` still calls this `<their persistent characterization>`. Your interview script must address this."*

Print the full draft action card in chat. Fire `AskUserQuestion`:

- **Accept verdict** → Step 10
- **Explicit-override** *(only meaningful when verdict ≠ `ship-with-conditions`)* → Step 10, but the file's `## Verdict` line gets stamped: `<verdict> | Override: founder proceeded against panel verdict on <ISO-date>`
- **Abort** → no file written; exit cleanly with the panel's verdict printed in chat

### Step 10 — Write `pressure-test.md`

Assemble the file using the structure in `## Output file structure` below. The per-expert files at `pressure-test/openings/` and `pressure-test/rebuttals/` are already on disk from Rounds 1 and 4; the main file cross-references them.

### Step 11 — Exit chat message

Based on the verdict, print one of:

- **ship-with-conditions:** *"Verdict: ship-with-conditions — the panel couldn't kill it from the armchair, which is not the same as validation. Next: run `/market-research <slug>` to map the competition, sizing, and timing for this idea, then take the disconfirmation questions in pressure-test.md into customer discovery with real people."*
- **refine-hypothesis:** *"Verdict: refine-hypothesis. Run `/sharpen-hypothesis <slug>` to apply the conceded updates, then re-run `/pressure-test <slug>`."*
- **kill-suggested:** *"Verdict: kill-suggested. The panel converged on fatal flaws — see pressure-test.md. To proceed anyway, re-run and choose explicit-override."*
- **override-applied:** *"Override applied. File written and stamped. The panel's verdict is in the file; the decision to proceed is on the record."*

## Subagent prompt templates

These are literal templates. Substitute `<UPPER_PLACEHOLDERS>` at dispatch time. `<PERSONA_SKILL_PATH>` is the absolute `SKILL.md` path you captured for this persona from the Step-3 glob of `.claude/skills/*-perspective/` — subagents Read it directly, so it must resolve on the current machine (never a hardcoded literal). Dispatch at high effort (Step 4 / Step 7).

### Opening template (Round 1)

```
You will channel <PERSONA_NAME> for this single critique task. You are NOT a generic critic — you are this specific person. Reason hard before you write: produce your single sharpest *disconfirming* objection, the one most likely to kill this idea, not a quick surface take.

First: Use the Read tool to read <PERSONA_SKILL_PATH> in full. Follow ALL its voice rules — especially the first-person rule (no "X would think…", no "from X's perspective…").

Then critique this startup hypothesis from your perspective.

Use the Write tool to write your output to:
docs/ideas-stages/<SLUG>/pressure-test/openings/<PERSONA_SLUG>.md

Output structure (Markdown):
# <PERSONA_NAME> — Opening

## Verdict
<one line in voice, max 20 words>

## Objections
1. <strongest objection in voice, max 60 words>
2. <second-strongest objection in voice, max 60 words — omit if only one>

No preamble. No caveats outside voice. Voice rules from your SKILL.md apply throughout.

Hypothesis to critique:
<HYPOTHESIS_FULL_CONTENT>
```

### Rebuttal template (Round 4)

```
You will channel <PERSONA_NAME>. You opened the panel earlier with objections to a founder's hypothesis. The founder has now responded substantively. Judge — hard and honestly — whether their response actually addresses your concern, or merely sounds like it does.

First: Use the Read tool to read <PERSONA_SKILL_PATH> and stay in voice throughout.

Also Read: docs/ideas-stages/<SLUG>/pressure-test/openings/<PERSONA_SLUG>.md (your original objections).

Use the Write tool to write your rebuttal to:
docs/ideas-stages/<SLUG>/pressure-test/rebuttals/<PERSONA_SLUG>.md

Output structure (Markdown):
# <PERSONA_NAME> — Rebuttal

## Final Verdict
One of EXACTLY these three labels (uppercase, with hyphens as shown):
WITHDRAW | ACCEPT-WITH-CONDITIONS | RESTATE-HARDER

## Reasoning
<2–4 sentences in voice explaining the verdict>

## Conditions (only if your Final Verdict is ACCEPT-WITH-CONDITIONS)
- <condition 1>
- <condition 2>

## Fatal flag (only if you believe your objection is structurally fatal — no interview can rescue it)
STRUCTURALLY-FATAL

Pick one verdict. If you cannot honestly say the founder's fix addresses your concern, do NOT WITHDRAW — escalate to RESTATE-HARDER. Voice rules from your SKILL.md apply throughout.

The founder's response to your objections:
<FOUNDER_RESPONSE_TEXT>
```

## Output file structure (`pressure-test.md`)

```markdown
# Pressure-Test: <project-name>

> **This verdict is a structured AI stress-test, not evidence.** It is the output of
> distilled expert *personas* reasoning over your hypothesis — not customers, not the
> market. A `ship-with-conditions` does not validate the idea; it means the panel could
> not kill it from the armchair. The disconfirmation questions and kill criteria below
> are what you go *test with real people*. This panel does not replace customer discovery.

## Verdict
<one line: ship-with-conditions | refine-hypothesis | kill-suggested | <verdict> | Override: ...>

## Disconfirmation Questions for Customer Discovery
1. <question that, if answered X, would refute Who>
2. <question that, if answered X, would refute Severity>
3. ...

## Kill Criteria
- If interviews show <signal X>, abandon
- ...

## Hypothesis Updates Required (from conceded objections)
- <specific update>
- ...

## Open Risks (founder disputed, but flagged)
- ...

## Anti-thesis Flag
- <expert>: <persistent characterization>. Your interview script must address this.
*(Omit this section if the anti-thesis withdrew or accepted-with-conditions.)*

---

## Panel Transcript Summary

### Panel composition
- <expert 1> — <one-line lens>
- <expert 2> — <one-line lens>
- <expert N> (anti-thesis) — <one-line lens>

### Round 1 — Opening verdicts
For each expert: one-line verdict + link to `pressure-test/openings/<slug>.md`.

### Round 2 — Cross-fire (top 2 disagreements)
<synthesized dialogue, ~150 words>

### Round 3 — Founder responses
For each expert: one line on response type + summary of fix.

### Round 4 — Rebuttals
| Expert | Final verdict | Fatal? | File |
|---|---|---|---|
| <expert> | WITHDRAW / ACCEPT-WITH-CONDITIONS / RESTATE-HARDER | yes/no | `pressure-test/rebuttals/<slug>.md` |
```

## Reference files

- `references/shape-mapping.md` — panel curation table + anti-thesis selection rules; read during Step 3

## Bundled scripts

- `scripts/compute_verdict.py` — deterministic Step-8 verdict computation. Parses the rebuttal files (tolerant of case/spacing), applies the pass-threshold truth table, and prints JSON (`verdict`, `anti_thesis_flag`, `tally`, `malformed`). Surfaces malformed rebuttals explicitly and exits non-zero rather than silently coercing them. Stdlib-only; runs under `python3` or self-executes via `uv run --script`.

## Composition

- **Upstream:** `/sharpen-hypothesis` writes the input `hypothesis.md`. Without it, this skill refuses.
- **Downstream:** `/market-research` is the immediate next stage — it reads `pressure-test.md` (the verdict, open risks, and anti-thesis flag) to scope its research. Then `/customer-discovery` consumes the Disconfirmation Questions and Kill Criteria — it anchors every interview question to a criterion and scores real interview evidence against those pre-registered (locked) thresholds.
- **Personas:** existing `*-perspective` skills under `.claude/skills/`. Subagents Read them at runtime; this skill never depends on any specific persona existing — it discovers the pool via `glob .claude/skills/*-perspective/` and applies the shape-mapping table.

## Scope

- **In:** orchestrating the 4-round debate, computing the panel verdict, writing the deliverable file plus per-expert provenance, kicking back to `/sharpen-hypothesis` when refinement is needed.
- **Out:** inline editing of `hypothesis.md` (`/sharpen-hypothesis` owns that file). Auto-retry loops (iteration is founder-driven across skill invocations). Market sizing & competitor mapping (`/market-research`, the next stage). Customer discovery itself (downstream). Inventing new persona skills (`/nuwa-skill` does that).
