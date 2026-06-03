---
name: darwin-skill
description: Autonomous skill optimizer inspired by Karpathy's autoresearch. Scores each SKILL.md against an 8-dimension rubric (structure + live effectiveness), then runs a hill-climbing loop with git as a ratchet — keeps every commit that raises the score, auto-reverts every one that doesn't, and pauses for human confirmation between skills. Trigger when the user asks to "optimize my skills", "score my skills", "improve SKILL.md", "audit skills", "run darwin", "auto-optimize skill", "evaluate skill quality", "review all skills", "make my skills better", or names a specific skill to grade/improve.
---

# Darwin — Train Your Skills Like You Train Models

> "You write the goals and constraints in `program.md`; let an agent generate and test code deltas indefinitely; keep only what measurably improves the objective."
> — Karpathy, autoresearch

Darwin applies that loop to Agent Skills. The single editable asset is each `SKILL.md`. The objective is an 8-dimension weighted score. The ratchet is git: improvements stay, regressions revert. A human confirms between skills.

---

## Core Philosophy

Five principles, in order of importance:

1. **Single editable asset.** One `SKILL.md` per experiment. One change, one measurement, one decision.
2. **Dual evaluation.** Structure scoring (static analysis) + effectiveness scoring (live test execution). A perfectly formatted skill that produces bad output is still a bad skill.
3. **Ratchet mechanism.** Score can only go up. Regressions are auto-reverted.
4. **Independent scoring.** The agent that edits a skill is never the agent that scores it. Spawn a sub-agent for re-evaluation to avoid the "graded my own homework" bias.
5. **Human in the loop.** Pause after each skill. Show diff + score delta. Wait for confirmation before continuing.

The distinction from a plain structural review: Darwin doesn't only check whether the markdown is well-formed. It also runs test prompts to verify the skill actually produces better output than no skill at all.

---

## The 8-Dimension Rubric (100 points total)

### Structure dimensions (60 points) — static analysis

| # | Dimension | Weight | Scoring criteria |
|---|---|---:|---|
| 1 | **Frontmatter quality** | 8 | `name` follows convention; `description` covers what-it-does + when-to-use + trigger phrases; ≤1024 chars |
| 2 | **Workflow clarity** | 15 | Steps are explicit, numbered, executable; each step has clear input/output |
| 3 | **Edge-case coverage** | 10 | Handles failure modes; defines fallbacks; recovers from errors |
| 4 | **Checkpoint design** | 7 | Pauses for user confirmation at major decisions; prevents runaway autonomy |
| 5 | **Instruction specificity** | 15 | No vague verbs; concrete parameters, formats, examples; directly executable |
| 6 | **Resource integration** | 5 | `references/`, `scripts/`, `assets/` paths exist and resolve correctly |

### Effectiveness dimensions (40 points) — requires live testing

| # | Dimension | Weight | Scoring criteria |
|---|---|---:|---|
| 7 | **Overall architecture** | 15 | Clear hierarchy; no redundancy; no gaps; consistent voice |
| 8 | **Live test performance** | 25 | Run the test prompts. Does the output match what the skill claims it can do? |

### Scoring rules

- Dimensions 1–7: each scored 1–10, multiplied by weight to give dimension score.
- Dimension 8: run 2–3 test prompts, score the outputs 1–10.
- **Total = Σ(dimension score × weight) / 10**, max 100.
- Improvement must be **strictly greater** than the previous score to be kept. No rounding up.

### How to score Dimension 8 (the one that matters most)

This is what separates Darwin from a structural linter.

1. For each skill, design 2–3 **typical user prompts** — not edge cases, just the most common usage.
2. Spawn two sub-agents per prompt:
   - **with_skill**: receives the SKILL.md in context, executes the prompt
   - **baseline**: same prompt, no skill
3. Compare outputs along three axes:
   - Did the output complete the user's intent?
   - Is quality clearly better than the no-skill baseline?
   - Did the skill introduce negative side effects (over-verbose, off-track, weird formatting)?

If sub-agents aren't available (time / resource limits), fall back to **dry-run validation**: read the skill, simulate executing a typical prompt mentally, judge whether the flow is sound. Mark these rows `dry_run` in `results.tsv`. A dry-run check is better than skipping Dimension 8 entirely.

---

## The Optimization Loop

### Phase 0 — Initialize

```
1. Confirm scope:
   - All skills → scan .claude/skills/*/SKILL.md
   - Specific skills → use the user-provided list
2. Create a git branch: auto-optimize/YYYYMMDD-HHMM
3. Initialize results.tsv if it doesn't exist
4. Read existing results.tsv to understand prior optimization history
```

### Phase 0.5 — Design test prompts

Before any evaluation, build the test set. Without test prompts, Dimension 8 can't be scored.

```
for each skill:
  1. Read SKILL.md and understand what it does
  2. Design 2-3 test prompts covering:
     - The most typical use case (happy path)
     - A slightly more complex or ambiguous case
  3. Save to {skill-dir}/test-prompts.json:
     [
       {"id": 1, "prompt": "what a real user would say", "expected": "short description of expected output"},
       {"id": 2, "prompt": "...", "expected": "..."}
     ]
```

Show the proposed test prompts to the user. **Wait for confirmation before scoring.** Test prompt quality determines whether optimization moves in the right direction.

### Phase 1 — Baseline evaluation

```
for each skill in scope:

  # Structure scoring (main agent can do this)
  1. Read the full SKILL.md
  2. Score dimensions 1-7 with brief reasoning per dimension

  # Effectiveness scoring (sub-agent, isolated from main context)
  3. For each test prompt, spawn sub-agents:
     - with_skill: executes the prompt with SKILL.md in context
     - baseline: executes the same prompt with no skill
  4. Compare and score Dimension 8

  # Aggregate
  5. Compute weighted total
  6. Append a row to results.tsv
```

If sub-agents aren't usable, score Dimension 8 via dry-run and tag the row `dry_run`. Don't skip the dimension.

After baseline, show a scorecard:

```
┌──────────────────────────┬───────┬─────────────────┬─────────────────┐
│ Skill                    │ Score │ Weakest struct  │ Weakest effect  │
├──────────────────────────┼───────┼─────────────────┼─────────────────┤
│ prompt-architect         │ 78    │ edge cases      │ test-prompt-2   │
│ grill-me                 │ 72    │ specificity     │ baseline tied   │
├──────────────────────────┼───────┼─────────────────┼─────────────────┤
│ average                  │ 75    │                 │                 │
└──────────────────────────┴───────┴─────────────────┴─────────────────┘
```

**Pause for user confirmation before entering the optimization loop.**

### Phase 2 — Hill-climbing loop

Once the user confirms, sort skills by baseline ascending — fix the weakest first.

```
for each skill:
  round = 0
  while round < MAX_ROUNDS (default 3):
    round += 1

    # Step 1: Diagnose
    Find the lowest-scoring dimension (structure or effectiveness).

    # Step 2: Propose one change
    Generate exactly one targeted improvement:
      - What to change (specific section/lines)
      - Why (which rubric criterion)
      - Expected point gain

    # Step 3: Apply
    Edit SKILL.md
    git add + commit ("optimize {skill}: {one-line summary}")

    # Step 4: Re-evaluate
    - Structure: main agent rescores
    - Effectiveness: spawn a NEW sub-agent, rerun the test prompts
      (critical: don't let the same context score its own edits)

    # Step 5: Decide
    if new_total > old_total:
      status = "keep"; update baseline
    else:
      status = "revert"
      git revert HEAD            # creates a new commit, doesn't rewrite history
      log the failed attempt in results.tsv
      break                       # this skill plateaued — move on

    # Step 6: Log the row in results.tsv

  # === Human checkpoint after each skill ===
  Show:
    - git diff (before vs after)
    - Score delta (which dimensions moved)
    - Test prompt output comparison (if sub-agents ran)
  Wait for confirmation before moving to the next skill.
  If the user says "no good", git revert back to that skill's pre-optimization commit.
```

### Phase 2.5 — Exploratory rewrite (optional)

When hill-climbing stalls — two skills in a row break after round 1 with no improvement — propose an **exploratory rewrite**:

```
1. Pick a stuck skill
2. git stash the current best version
3. Rewrite SKILL.md from scratch — not a tweak, a structural redo
4. Re-evaluate fully
5. if rewrite > stashed: adopt the rewrite
   else: git stash pop, restore the previous best
```

This breaks out of local maxima. Sometimes a skill needs to be torn down before it can grow. **Require explicit user permission before running this phase.**

### Phase 3 — Summary report

```
## Optimization Report

### Overview
- Skills optimized: N
- Total experiments: M
- Improvements kept: X (Y%)
- Reverts: Z
- Effectiveness validation: A full tests / B dry runs

### Score deltas
┌──────────────────────────┬────────┬────────┬────────┐
│ Skill                    │ Before │ After  │ Δ      │
├──────────────────────────┼────────┼────────┼────────┤
│ prompt-architect         │ 78     │ 87     │ +9     │
│ grill-me                 │ 72     │ 83     │ +11    │
├──────────────────────────┼────────┼────────┼────────┤
│ average                  │ 75     │ 85     │ +10    │
└──────────────────────────┴────────┴────────┴────────┘

### Headline improvements
1. [skill-A] Added edge-case handling; live test output quality jumped
2. [skill-B] Restructured workflow; advantage over baseline widened
```

---

## results.tsv Format

Stored at `.claude/skills/darwin-skill/results.tsv`. Single shared log across all optimization runs.

```tsv
timestamp	commit	skill	old_score	new_score	status	dimension	note	eval_mode
2026-05-24T10:00	baseline	prompt-architect	-	78	baseline	-	initial scoring	full_test
2026-05-24T10:05	a1b2c3d	prompt-architect	78	84	keep	edge_cases	added fallback path	full_test
2026-05-24T10:10	b2c3d4e	prompt-architect	84	82	revert	specificity	over-specified	dry_run
```

**Columns:**

- `timestamp` — ISO 8601, minute precision
- `commit` — short SHA, or `baseline` for initial rows
- `skill` — directory name (matches `.claude/skills/<name>/`)
- `old_score` / `new_score` — one decimal, max 100
- `status` — `baseline` | `keep` | `revert` | `error`
- `dimension` — which dimension drove the change (matches the rubric)
- `note` — short human-readable summary
- `eval_mode` — `full_test` (sub-agents ran) | `dry_run` (simulated)

---

## Optimization Strategy Library

Pick the highest-priority issue each round. One change per round — never bundle.

### P0 — Effectiveness failures (found via live testing)
- Test output drifts from user intent → check the skill for misleading instructions
- With-skill is worse than baseline → skill is over-constraining, simplify
- Output format doesn't match what's promised → add an explicit output template

### P1 — Structural problems
- Frontmatter missing trigger phrases → add the phrasings users actually type
- No Phase / Step structure → reorganize into a linear flow with explicit phase headers
- No user confirmation checkpoints → insert them before destructive or large-blast-radius operations

### P2 — Specificity problems
- Vague steps ("process the image") → replace with concrete operation + parameters
- Missing input / output specs → add format, path, example
- No exception handling → add "if X fails, then Y"

### P3 — Readability problems
- Paragraphs too long → break into bullets or tables
- Repeated explanations → merge and dedupe
- No quick reference → add a TL;DR or decision tree at the top

---

## Exception Handling

The loop assumes an ideal environment, but in practice things go wrong. Pre-defined fallbacks below — none should ever silently skip or silently fail.

| Scenario | Trigger | Action |
|---|---|---|
| Not in a git repo | `git rev-parse` fails | Suggest `git init`; if user declines, use `cp SKILL.md SKILL.md.bak.YYYYMMDD-HHMM` for rollback instead of `git revert` |
| `results.tsv` missing | File not found | Create it with the 9-column header |
| `results.tsv` corrupted | Columns don't match / not TSV | Back up to `.bak.YYYYMMDD-HHMM`, rebuild, inform user |
| Branch already exists | `git checkout -b` fails | Append `-2`, `-3`; after 3 attempts, ask user to continue on existing branch or pick a new name |
| `git revert` fails | Conflict / dirty worktree | `git stash`, retry; if still failing, manually restore SKILL.md from the prior commit |
| MAX_ROUNDS hit (default 3) | 3 rounds complete with remaining weakness | Show current weakest dimension; ask user: continue another round / enter Phase 2.5 / stop |
| Optimized file > 150% original size | New file > original × 1.5 | Reject the commit; loop back to the change step and tighten (remove redundancy, merge duplicates) before rescoring |
| `test-prompts.json` already exists | File present in skill dir | Default to reuse; show prompts; ask user: reuse / rewrite / append |
| `SKILL.md` not found | Skill directory exists but no SKILL.md | Skip this skill; log `status=error` to results.tsv; continue with the next |
| Floating-point drift | Score on the boundary | Round totals to 1 decimal; improvement must be **strictly** greater (no rounding up) |

**Principle:** notify, then handle. Never silently skip; never silently fail.

---

## Hard Constraints

1. **Don't change what the skill is for** — only optimize *how it's written* and *how it executes*, never *what it does*.
2. **Don't add new dependencies** — no new files under `scripts/`, `references/`, etc. that the original skill didn't have.
3. **One dimension per round** — multiple changes in one commit make it impossible to attribute the score delta.
4. **Keep file size reasonable** — optimized SKILL.md must not exceed 150% of the original.
5. **All changes go on a git branch** — use `git revert` (new commit) rather than `git reset --hard` (history rewrite).
6. **Scoring independence** — Dimension 8 must be evaluated by a sub-agent or, at minimum, a dry-run mental simulation. Never let the same context that just edited a skill also score its effectiveness.
7. **Human checkpoints are non-negotiable** — pause after baseline, pause after each skill, pause before Phase 2.5.

---

## Usage Modes

### Full optimization (recommended for first run)
```
User: "optimize all my skills"
→ Run Phase 0 → 3 end-to-end
→ Suggestion: after baseline, focus the optimization pass on the bottom 5
```

### Single-skill optimization
```
User: "optimize the prompt-architect skill"
→ Run Phase 0.5 → 2 on that one skill only
```

### Evaluate only (no changes)
```
User: "score my skills" or "audit all skills"
→ Run Phase 0.5 → 1 (test prompts + baseline)
→ Print the scorecard; stop before Phase 2
```

### History
```
User: "show me the optimization history"
→ Read and pretty-print results.tsv
```

---

## Mapping Back to autoresearch

| autoresearch | darwin-skill | Why |
|---|---|---|
| `program.md` | This SKILL.md | Defines goals + constraints |
| `train.py` | Each target SKILL.md | The single editable asset |
| `val_bpb` | 8-dimension weighted total | The objective number |
| git ratchet | `keep` / `revert` mechanism | Only improvements survive |
| test set | Per-skill `test-prompts.json` | Validates real-world improvement |
| Fully autonomous | **Human in the loop** | Skill quality has dimensions a loss number can't capture |

The deliberate departure from autoresearch is the human checkpoint. Loss is just a number; skill quality has flavor. The system pauses, shows the diff and score delta, and waits for a human signal before continuing.
