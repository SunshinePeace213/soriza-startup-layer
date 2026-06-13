#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Hook #1 (T05) -- PreToolUse(Write|Edit). Spec: reference §7.4.

Invariant: only ideas/<ACTIVE>/ and ideas/_exploration/ are writable inside ideas/.
Writes outside ideas/ are not this hook's jurisdiction (exit 0). A stray write to a
non-active idea is exactly the threat model, so this lives in PROJECT settings and runs
no matter which skill (if any) is active.
"""
import json
import sys
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
    sys.exit(0)  # outside ideas/: not this hook's jurisdiction (type-safety hooks still apply)
active = (ideas / "ACTIVE").read_text().strip() if (ideas / "ACTIVE").exists() else ""
top = rel.parts[0] if rel.parts else ""
if top in {"_exploration", "ACTIVE", "CLAUDE.md"} or top == active:
    sys.exit(0)
print(f"[write-path] Only ideas/{active}/ and ideas/_exploration/ are writable; "
      f"you tried {fp}. Switch ideas via the script that updates ideas/ACTIVE.", file=sys.stderr)
sys.exit(2)
