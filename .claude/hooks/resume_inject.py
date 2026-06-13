#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Hook #5 (T23) -- SessionStart(resume|compact). Spec: reference §7.4 / §3.1 / ideas/CLAUDE.md §4.

On resume AND after context compaction, re-inject the ACTIVE idea's pipeline position into
context (stdout is context-injected for SessionStart). The `compact` matcher is the point:
pipeline position survives compaction. Purely informational -- always exits 0, never blocks.
If there is no ACTIVE idea or STATE, it prints the fallback hint (run ideas/CLAUDE.md §1 manually).
"""
import json
import sys

import yaml
from pathlib import Path

try:
    data = json.load(sys.stdin)
    root = Path(data.get("cwd", "."))
    af = root / "ideas" / "ACTIVE"
    slug = af.read_text(encoding="utf-8").strip() if af.exists() else ""
    sp = root / "ideas" / slug / "STATE.md" if slug else None
    if not slug or not sp.exists():
        print("[resume] No ACTIVE idea/STATE found -- follow ideas/CLAUDE.md §1 (read ACTIVE, then STATE).")
        sys.exit(0)
    st = yaml.safe_load(sp.read_text(encoding="utf-8").split("---")[1])
    todo = [f"{c['item']} ({c.get('owner')})" for c in st.get("step_checklist", []) if not c.get("done")]
    open_items = "; ".join(todo) if todo else "none"
    print(f"[resume] idea={slug} step={st.get('current_step')} ({st.get('step_name')}) "
          f"owner={st.get('owner')} status={st.get('status')}\n"
          f"next_action: {st.get('next_action')}\nopen items: {open_items}")
except Exception as e:
    print(f"[resume] state read failed ({e}) -- follow ideas/CLAUDE.md §1 manually.")
sys.exit(0)
