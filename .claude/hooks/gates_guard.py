#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Hook #1b (T05) -- PreToolUse(Write|Edit on *STATE.md). Spec: reference §3.4 / §7.4.

The gates: block of STATE.md is written ONLY by scripts/advance_gate.py (Hard Rule #6).
advance_gate writes via plain Python file IO under Bash, so it never trips this hook --
that asymmetry IS the "script-only writes" enforcement. This hook denies any Write/Edit
TOOL call that would change gates:. Creating a fresh STATE.md (file absent) is lawful
(the scaffold writes `gates: {}`). Residual sed-bypass risk is caught downstream by
ledger-audit's three-way reconciliation (W5).
"""
import json
import re
import sys
from pathlib import Path

data = json.load(sys.stdin)
ti = data.get("tool_input") or {}
fp = ti.get("file_path", "")
if not fp.endswith("STATE.md"):
    sys.exit(0)


def deny(reason: str) -> None:
    print(f"[gates] {reason}", file=sys.stderr)
    sys.exit(2)


def gates_block(text: str) -> str:
    """Normalized raw gates: block from the YAML frontmatter ('' if none)."""
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ""
    fm = parts[1]
    m = re.search(r"^gates:.*?(?=^[A-Za-z_]\w*:|\Z)", fm, re.M | re.S)
    if not m:
        return ""
    return "\n".join(line.strip() for line in m.group(0).splitlines() if line.strip())


if data.get("tool_name") == "Edit":
    if "gates" in (ti.get("old_string", "") + ti.get("new_string", "")
                   + ti.get("old_str", "") + ti.get("new_str", "")):
        deny("Edit touches gates: -- run `uv run scripts/advance_gate.py` instead")
else:  # Write
    p = Path(fp)
    if p.exists() and gates_block(p.read_text(encoding="utf-8")) != gates_block(ti.get("content", "")):
        deny("Write changes the gates: block -- use scripts/advance_gate.py")
sys.exit(0)
