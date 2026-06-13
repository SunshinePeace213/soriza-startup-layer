#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Hook #4 (T23) -- Stop. Spec: reference §7.4 / §11.2.

Forced completion: refuse to let the agent stop while the ACTIVE idea has unfinished
agent-OWNED checklist items. The anti-deadlock teeth (so this never wedges a session):
  - stop_hook_active set  -> release (official second-pass flag)
  - no ACTIVE / no STATE   -> release (nothing to guard)
  - status != in_progress  -> release
  - owner == human         -> release (NEVER push the agent at human-owned items)
  - no undone agent items  -> release
Only an in-progress, agent-owned step with open agent items blocks (exit 2 + the list).
"""
import json
import sys

import yaml
from pathlib import Path

data = json.load(sys.stdin)
if data.get("stop_hook_active"):  # official anti-infinite-loop flag: a second pass always releases
    sys.exit(0)
root = Path(data.get("cwd", "."))
af = root / "ideas" / "ACTIVE"
if not af.exists():
    sys.exit(0)
sp = root / "ideas" / af.read_text(encoding="utf-8").strip() / "STATE.md"
if not sp.exists():
    sys.exit(0)
st = yaml.safe_load(sp.read_text(encoding="utf-8").split("---")[1])
if st.get("status") != "in_progress" or st.get("owner") == "human":
    sys.exit(0)  # never push the agent at human-owned items -- the deadlock fix
todo = [c["item"] for c in st.get("step_checklist", [])
        if c.get("owner") == "agent" and not c.get("done")]
if not todo:
    sys.exit(0)
print("Unfinished before stopping (owner=agent):\n- " + "\n- ".join(todo), file=sys.stderr)
sys.exit(2)
