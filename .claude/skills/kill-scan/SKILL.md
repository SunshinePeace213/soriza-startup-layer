---
name: kill-scan
description: |
  Third Idea-Stage stage: desk-scan a sharpened hypothesis for hard disqualifiers (regulatory / technical / platform / graveyard) and mine public demand, every verdict ledger-cited. Use for "run my kill-scan", "scan for disqualifiers / fatal flaws", "demand-scan this idea".
when_to_use: |
  Gate: hypothesis.md exists and STATE is at step 3 (kill_scan) with no kill-scan.md yet. Not the persona debate (/pressure-test α) or market sizing (/market-sizing).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Agent, Bash
effort: high
disable-model-invocation: true
---

# Kill-Scan

Step 3 of the Idea Stage. Desk-scan the sharpened hypothesis for **hard disqualifiers** (the
only legitimate desk-kill in the pipeline) and mine **public demand** in one pass. You spawn the
research agents — they are the **only** thing here that touches the web — then write `kill-scan.md`
with every verdict cited from `evidence-ledger.jsonl`. A clean scan auto-advances; a tripped
disqualifier stops the gate for the founder, who alone may override or kill.

## When this skill applies

- `ideas/<slug>/hypothesis.md` exists, `STATE.md` reads `current_step: 3` / `step_name: kill_scan`,
  and no `kill-scan.md` yet — or the founder runs `/kill-scan <slug>`.
- **Entry guard:** no `hypothesis.md` → point to `/sharpen-hypothesis`. Already past G3 → `/pressure-test`.

## Gotchas

- **The main context has no web tools — by design.** `allowed-tools` omits WebSearch/WebFetch so the
  *only* web ingress is the research subagents you spawn. Web content enters artifacts **only** via the
  ledger (CLAUDE.md §3); never reach for a web tool here, and never paste a raw URL into `kill-scan.md`
  (the validator rejects `http`). Cite `E-xxx` instead.
- **Append the grade-4 ledger entry FIRST, then cite it.** Every web fact a research agent returns
  becomes one `evidence-ledger.jsonl` line (`grade: 4`, `url` required, `added_by: research-agent`,
  `source: disqualifier-scan` | `demand-scan`) *before* you cite its `E-xxx` in `kill-scan.md`
  (ideas/CLAUDE.md §2). Ledger ids are unique and ascending.
- **A TRIPPED disqualifier is not a kill *you* perform.** It stops the gate. Only the founder may
  proceed (a stamped override in `decision-log.md` — the pipeline's single legitimate desk-kill) or
  kill the idea. On a trip, set STATE `status: blocked` and a `next_action` for the founder; do **not**
  call `advance_gate`. Only `status / next_action / step_checklist / deltas_pending` are agent-writable
  — never hand-edit `owner` or the `gates:` block.
- **Size never kills.** The demand-scan hunts a reachable niche and named public complainers for 5a's
  warm list. "Market looks small / incumbent exists / they might not pay" is context and an interview
  question — never a disqualifier.
- **Lock-ahead before the gate.** `advance_gate --gate g3` requires `criteria-g4.yaml` locked (you lock
  it — see Output) **and** `criteria-g3.yaml` already locked (that is step 2 / sharpen-hypothesis's
  lock-ahead duty). If g3 criteria are absent, `advance_gate` fails loudly — surface it as an upstream
  gap, don't work around it.

## What it does (goal + constraints)

Goal: `ideas/<slug>/kill-scan.md` (4-axis disqualifier scan + demand scan + G3 verdict) backed by
grade-4 ledger entries — the validator is `tests/schemas/test_killscan.py`.

- Read `ideas/<slug>/STATE.md` (confirm step 3), `hypothesis.md`, and `evidence-ledger.jsonl`.
- **Run two legs via subagents (the sole web ingress), in parallel:**
  - **Disqualifiers** — spawn `startup-idea-researcher` with a facet brief covering the four axes:
    **regulatory walls**, **technical impossibility**, **platform single-point risk**, **graveyard /
    failed-clone cases**. You want hard, checkable facts, not vibes.
  - **Demand-scan** — spawn `market-researcher` (founder-blind) to mine public conversations for
    unsolved complaints, real-user language, and **named people who publicly complained** (warm-list
    seeds for 5a).
- **Transcribe their cited findings into `evidence-ledger.jsonl`** as grade-4 entries (one per fact,
  `url` required), then write `kill-scan.md` from `assets/kill-scan-template.md`: a disqualifier table
  (each axis PASS or TRIPPED, each row citing `E-xxx`) + a demand-scan section (each claim citing
  `E-xxx`, named complainers called out) + the **G3 Verdict** (CLEAR or TRIPPED).
- **Verdict rule:** TRIPPED only on a hard, checkable fact (an actual regulatory wall, a real technical
  impossibility, a true single-platform dependency, a genuine graveyard). Everything subjective —
  weak demand, an incumbent, doubtful willingness-to-pay — is CLEAR-with-context, carried as an
  interview question into discovery. The desk does not kill on merit.

## Output

`ideas/<slug>/kill-scan.md` + grade-4 ledger entries. Then **close the step**:

- **CLEAR** — lock the next gate's criteria (lock-ahead), then advance:
  ```bash
  uv run scripts/lock_criteria.py --slug <slug> --gate g4   # lock-ahead: criteria-g4 (write-once)
  uv run scripts/advance_gate.py --slug <slug> --gate g3    # runs test_killscan, checks lock-ahead, advances STATE
  ```
  Flip the agent-owned `step_checklist` items to `done: true` so the Stop hook releases. `advance_gate`
  rewrites STATE to step 4 (pressure-test α) and appends the decision-log entry. Next: `/pressure-test`.
- **TRIPPED** — do **not** advance. Leave the TRIPPED verdict in `kill-scan.md`, set STATE
  `status: blocked` with `next_action` naming the tripped axis and pointing the founder at the override
  decision, and flip the agent-owned checklist items done. The founder reads it and either stamps an
  override in `decision-log.md` + runs `advance_gate --gate g3` themselves, or kills the idea.

Never hand-edit the `gates:` block — `advance_gate.py` is its only writer.

## References

- `assets/kill-scan-template.md` — the `kill-scan.md` structure (its sections match the validator).
- Agents: `market-researcher` (demand-scan, founder-blind), `startup-idea-researcher` (disqualifier
  web leg) — spawned via the Agent tool; they hold the web tools, you don't.
