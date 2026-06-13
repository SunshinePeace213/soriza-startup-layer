#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Hook #2 (T22) -- PostToolUse(Write|Edit). Spec: reference §7.3 / §7.4 / §9.

The doc-TDD closed loop: when an agent writes a pipeline artifact under ideas/, re-run that
artifact's schema validator against the file it just wrote (`--artifact <fp>`). On failure,
the validator's own assertion messages -- written FOR the agent (§9) -- are fed back on stderr
(exit 2) so the agent self-repairs. Coverage is project-level: artifacts get validated even
when written outside their "home" skill.

Routing: FILEMAP (by filename) + two pattern branches (interviews/*.md, gates/criteria-*.yaml).
A file with no validator (not in the map, or its validator not shipped yet -- validator-first
means some land later, §9) is a no-op (exit 0): no validator == no contract to enforce yet.
"""
import json
import subprocess
import sys
from pathlib import Path

# Target routing map (reference §7.4). Entries whose validator file does not exist yet are
# safe no-ops (the vfile.exists() guard below), so this can name the full target set while
# validators ship incrementally (§9). NOTE: reference §7.4 maps both neutral-brief and
# startup-brief to "test_brief" -- a collision (one name, two artifacts). Resolved here by
# distinct names (test_neutral_brief / test_startup_brief); confirm when those validators ship.
FILEMAP = {
    "STATE.md": "test_state",
    "hypothesis.md": "test_hypothesis",
    "kill-scan.md": "test_killscan",
    "pressure-report-alpha.md": "test_pressure",
    "pressure-report-beta.md": "test_pressure_beta",
    "customer-discovery.md": "test_synthesis",
    "evidence-ledger.jsonl": "test_ledger",
    "predictions.jsonl": "test_predictions",
    "market-sizing.md": "test_sizing",
    "neutral-brief.md": "test_neutral_brief",
    "startup-brief.md": "test_startup_brief",
}


def validator_key(fp: str) -> str | None:
    """Module stem of the validator for this artifact, or None if none applies."""
    name = Path(fp).name
    if name in FILEMAP:
        return FILEMAP[name]
    parts = Path(fp).parts
    if name.startswith("criteria-") and name.endswith(".yaml"):
        return "test_criteria"
    if name.endswith(".md") and "interviews" in parts:
        return "test_interview"
    return None


def main() -> None:
    data = json.load(sys.stdin)
    fp = (data.get("tool_input") or {}).get("file_path", "")
    if not fp or "ideas" not in Path(fp).parts:
        sys.exit(0)  # only pipeline artifacts under ideas/ are schema-governed
    key = validator_key(fp)
    if key is None:
        sys.exit(0)  # no validator routes to this artifact
    cwd = Path(data.get("cwd", "."))
    vfile = cwd / "tests" / "schemas" / f"{key}.py"
    if not vfile.exists():
        sys.exit(0)  # validator-first: this one has not shipped yet -- nothing to enforce

    r = subprocess.run(
        ["uv", "run", "pytest", str(vfile), "-q", "--artifact", fp],
        capture_output=True, text=True, cwd=str(cwd),
    )
    if r.returncode != 0:
        # feed the validator's assertion messages back to the agent for self-repair
        sys.stderr.write((r.stdout + r.stderr)[-1500:])
        sys.exit(2)
    sys.exit(0)


main()
