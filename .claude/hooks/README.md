# Hooks — W1 invariant guards (#1 / #1b / #3)

These three project-level hooks are the in-session closed loop's W1 layer (reference §7).
They are **invariants** — they must hold no matter which skill is active — so they live in
**project** `.claude/settings.json` (committed), not in any skill's frontmatter.

| # | Script | Event | Guards |
|---|---|---|---|
| 1 | `write_path_guard.py` | `PreToolUse(Write\|Edit)` | only `ideas/<ACTIVE>/` and `ideas/_exploration/` are writable inside `ideas/` |
| 1b | `gates_guard.py` | `PreToolUse(Write\|Edit on *STATE.md)` | the `gates:` block is changed ONLY by `scripts/advance_gate.py` |
| 3 | `run_log.py` | `PostToolUse(Write\|Edit\|Bash\|Task)` | appends one observational line to `logs/run-log.jsonl` (never blocks) |

Each script is a self-contained PEP-723 `uv run --script` (no project deps) and is covered by
`tests/hooks/` (run `uv run pytest tests/hooks`). They are **wired into `.claude/settings.json`
and active** (the `"hooks"` block below). Hooks load at session start, so a fresh session picks
them up.

## Wiring (live in `.claude/settings.json`)

> The `"hooks"` key below is already present in `.claude/settings.json`. Reproduced here for
> reference; editing agent startup config is otherwise guarded, so changes are a deliberate step:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "uv run .claude/hooks/write_path_guard.py" },
          { "type": "command", "if": "Edit(*STATE.md)|Write(*STATE.md)", "command": "uv run .claude/hooks/gates_guard.py" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash|Task",
        "hooks": [
          { "type": "command", "command": "uv run .claude/hooks/run_log.py" }
        ]
      }
    ]
  }
}
```

## W5 additions (NOT in W1 — placeholders only)

`schema_on_write.py` (#2, T22), `stop_guard.py` (#4, T23), `resume_inject.py` (#5, T23) join the
block in W5. The full settings sample with those marked is reference §7.3.
