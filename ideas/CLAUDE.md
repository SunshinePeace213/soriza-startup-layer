# ideas/ -- Operating Protocol

## 1. Session Start (read in this order)
- **ACTIVE**: read `ideas/ACTIVE` for the slug
- **STATE**: read `ideas/<slug>/STATE.md` -- current_step / owner / next_action / step_checklist
- **Ownership**: if `owner: human`, NEVER perform the step for the founder -> prepare drafts, organize material, remind. Nothing more

## 2. Doing Work
- **Checklist scope**: only items with `owner: agent`
- **On completion**: flip the item to `done: true` immediately; when the step clears, update `next_action` and run `uv run scripts/advance_gate.py --slug <slug> --gate gN ...`
- **Citations**: append the ledger entry FIRST, then cite `E-xxx` in the artifact

## 3. Never (each has its lawful alternative)
- **Gates / locked criteria**: never edit -> `advance_gate.py` / reopen via decision-log
- **hypothesis.md**: never edit (unless you ARE sharpen-hypothesis) -> emit a flagged-delta block
- **Ledger history**: never modify old lines -> append a correction line referencing the old ID
- **New file types**: never invent files this protocol does not name -> report it; the scaffold gets fixed instead

## 4. Resume
- **SessionStart(resume|compact) hook** injects the ACTIVE STATE summary; if absent, run SS1 manually