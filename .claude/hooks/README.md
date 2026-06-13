# Hooks — in-session closed loop (#1 / #1b / #2 / #3 / #4 / #5)

These project-level hooks are the in-session closed loop (reference §7, §11.3 L0). They are
**invariants** — they must hold no matter which skill is active (or when none is) — so they live
in **project** `.claude/settings.json` (committed), not in any skill's frontmatter.

| # | Script | Event | Guards |
|---|---|---|---|
| 1 | `write_path_guard.py` | `PreToolUse(Write\|Edit)` | only `ideas/<ACTIVE>/` and `ideas/_exploration/` are writable inside `ideas/` |
| 1b | `gates_guard.py` | `PreToolUse(Write\|Edit on *STATE.md)` | the `gates:` block is changed ONLY by `scripts/advance_gate.py` |
| 2 | `schema_on_write.py` | `PostToolUse(Write\|Edit)` | re-runs the artifact's validator against the just-written file; failure → exit 2 + the validator's messages fed back for self-repair (doc-TDD loop) |
| 3 | `run_log.py` | `PostToolUse(Write\|Edit\|Bash\|Task)` | appends one observational line to `logs/run-log.jsonl` (never blocks) |
| 4 | `stop_guard.py` | `Stop` | refuses to stop while the ACTIVE idea has undone **agent-owned** checklist items (releases on `stop_hook_active` / `owner: human` / not `in_progress`) |
| 5 | `resume_inject.py` | `SessionStart(resume\|compact)` | re-injects the ACTIVE idea's pipeline position into context (survives compaction); informational, always exits 0 |

Each script is a self-contained PEP-723 `uv run --script` (`stop_guard`/`resume_inject` declare
`pyyaml`; the rest need nothing) and is covered by `tests/hooks/` (run `uv run pytest tests/hooks`).
They are **wired into `.claude/settings.json` and active** (the `"hooks"` block below). Hooks load
at session start, so a fresh session picks them up.

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
      { "matcher": "Write|Edit", "hooks": [ { "type": "command", "command": "uv run .claude/hooks/schema_on_write.py" } ] },
      { "matcher": "Write|Edit|Bash|Task", "hooks": [ { "type": "command", "command": "uv run .claude/hooks/run_log.py" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "uv run .claude/hooks/stop_guard.py" } ] }
    ],
    "SessionStart": [
      { "matcher": "resume|compact", "hooks": [ { "type": "command", "command": "uv run .claude/hooks/resume_inject.py" } ] }
    ]
  }
}
```

## Still pending (reference §7.5–§7.6, component-scoped / later weeks)

`persona_contract_check.py` (#W2, rides in persona-agent frontmatter, `Stop`→`SubagentStop`),
`citation_density_check.py` (rides in `pressure-test` frontmatter), and `deprecated_redirect.py`
(#W11, `UserPromptExpansion` guard for retired command names). The full settings sample is §7.3.

## schema_on_write routing note

`schema_on_write.py`'s `FILEMAP` names the full target set (§7.4), but only artifacts whose
validator file currently exists in `tests/schemas/` are enforced; the rest are safe no-ops until
their validator ships (validator-first, §9). Reference §7.4 collides neutral-brief and
startup-brief on one name `test_brief`; resolved here as `test_neutral_brief` / `test_startup_brief`
(confirm when building those validators).
