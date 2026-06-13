#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Hook #3 (T05) -- PostToolUse(Write|Edit|Bash|Task). Spec: reference §6.5 / §7.4.

Append ONE line to logs/run-log.jsonl per tool call (repo-level, slug from ideas/ACTIVE,
null if unreadable). Humans never touch this file. The hook is observational: it must never
block a tool, so every failure path still exits 0.
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HKT = timezone(timedelta(hours=8))


def now_iso() -> str:
    s = datetime.now(HKT).strftime("%Y-%m-%dT%H:%M:%S%z")
    return s[:-2] + ":" + s[-2:]


def detail(tool_name: str, ti: dict) -> str:
    if tool_name in ("Write", "Edit"):
        return ti.get("file_path", "")
    if tool_name == "Bash":
        return (ti.get("command", "") or "")[:120]
    if tool_name == "Task":
        return ti.get("description") or ti.get("subagent_type") or ""
    return ""


def main() -> None:
    try:
        data = json.load(sys.stdin)
        root = Path(data.get("cwd", "."))
        ideas_active = root / "ideas" / "ACTIVE"
        slug = ideas_active.read_text(encoding="utf-8").strip() if ideas_active.exists() else None
        ti = data.get("tool_input") or {}
        tool = data.get("tool_name", "")
        rec = {
            "ts": now_iso(),
            "session": data.get("session_id"),
            "slug": slug,
            "tool": tool,
            "detail": detail(tool, ti),
        }
        logs = root / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        with (logs / "run-log.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass  # observational hook: never block the tool it observes
    sys.exit(0)


main()
