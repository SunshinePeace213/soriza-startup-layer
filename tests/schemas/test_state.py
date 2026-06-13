"""Validator: ideas/<slug>/STATE.md (schema v2). Spec: reference §3.2.

Guards the machine-readable state every hook, gate and dashboard depends on. Must pass on
BOTH a fresh scaffold (gates: {}, status: done, step 1) and a mid-pipeline state (gates
g1..g4). advance_gate.py runs this on itself after every gate write (its self-check).
"""
import re
from pathlib import Path

import yaml

FIXTURE = "state.sample.md"
BAD_FIXTURE = "state.bad.md"
STATUSES = {"pending", "in_progress", "blocked", "done", "killed"}
OWNERS = {"human", "agent"}
GATE_RE = re.compile(r"^g[1-9]$")
GATE_REQUIRED = ("result", "date", "criteria", "decision")


def _frontmatter(text):
    assert text.startswith("---"), "STATE.md must open with a YAML frontmatter block (---)"
    parts = text.split("---", 2)
    assert len(parts) >= 3, "STATE.md frontmatter must be closed by a second --- line"
    fm = yaml.safe_load(parts[1])
    assert isinstance(fm, dict), "STATE.md frontmatter must parse as a YAML mapping"
    return fm


def _validate(fm):
    assert fm.get("schema_version") == 2, "schema_version must be 2 (bump it + add a migration note to change the schema)"
    assert isinstance(fm.get("slug"), str) and fm["slug"], "slug must be a non-empty string"
    step = fm.get("current_step")
    assert isinstance(step, int) and 1 <= step <= 9, "current_step must be an int in 1..9"
    assert isinstance(fm.get("step_name"), str) and fm["step_name"], "step_name must be a non-empty string"
    assert fm.get("status") in STATUSES, f"status must be one of {sorted(STATUSES)}"
    assert fm.get("owner") in OWNERS, f"owner must be one of {sorted(OWNERS)} -- who holds the NEXT action"

    ib = fm.get("interview_budget")
    assert (isinstance(ib, dict) and isinstance(ib.get("total"), int) and isinstance(ib.get("used"), int)
            and ib["used"] <= ib["total"]), "interview_budget must be {total: int, used: int} with used <= total"

    checklist = fm.get("step_checklist")
    assert isinstance(checklist, list), "step_checklist must be a list (empty list allowed)"
    for item in checklist:
        assert (isinstance(item, dict) and isinstance(item.get("item"), str) and item.get("owner") in OWNERS
                and isinstance(item.get("done"), bool)), \
            "each step_checklist entry needs {item: str, owner: human|agent, done: bool}"

    assert isinstance(fm.get("deltas_pending"), list), "deltas_pending must be a list (stages with unfolded delta blocks)"

    gates = fm.get("gates")
    assert isinstance(gates, dict), "gates must be a mapping ({} at scaffold; written ONLY by advance_gate.py)"
    for key, val in gates.items():
        assert GATE_RE.match(str(key)), f"gate key {key!r} must look like g1..g9"
        assert isinstance(val, dict), f"gate {key} entry must be a mapping"
        for field in GATE_REQUIRED:
            assert field in val, f"gate {key} entry missing required field {field!r} (advance_gate.py writes all of {GATE_REQUIRED})"

    assert isinstance(fm.get("next_action"), str) and fm["next_action"], "next_action must be a non-empty string"
    assert "blocking" in fm, "blocking field must be present (null when not blocked)"
    assert fm.get("updated"), "updated must be a non-empty ISO timestamp"


def test_valid_state(artifact_text):
    _validate(_frontmatter(artifact_text))


def test_bad_fixture_bites():
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    import pytest
    with pytest.raises(AssertionError):
        _validate(_frontmatter(bad))
