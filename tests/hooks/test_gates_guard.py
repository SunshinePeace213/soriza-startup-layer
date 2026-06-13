"""Hook #1b gates_guard: only advance_gate.py may change STATE.md's gates: block."""

FM = """---
slug: x
schema_version: 2
current_step: 1
step_name: generate
status: {status}
owner: human
interview_budget: {{total: 10, used: 0}}
step_checklist: []
deltas_pending: []
{gates}
next_action: "run /sharpen-hypothesis x"
blocking: null
updated: 2026-06-13T15:27+08:00
---
body
"""

EMPTY_GATES = "gates: {}"
G1_GATES = "gates:\n  g1: {result: pass, date: 2026-06-16, criteria: scaffold, decision: DL-001}"


def _state(status="done", gates=EMPTY_GATES):
    return FM.format(status=status, gates=gates)


def test_non_state_file_is_noop(tmp_path, run_hook):
    r = run_hook("gates_guard.py", {"tool_name": "Write",
                 "tool_input": {"file_path": str(tmp_path / "hypothesis.md"), "content": "x"}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr


def test_edit_touching_gates_blocked(tmp_path, run_hook):
    r = run_hook("gates_guard.py", {"tool_name": "Edit", "tool_input": {
        "file_path": str(tmp_path / "STATE.md"),
        "old_string": "gates: {}", "new_string": G1_GATES}, "cwd": str(tmp_path)})
    assert r.returncode == 2
    assert "gates" in r.stderr


def test_edit_not_touching_gates_allowed(tmp_path, run_hook):
    r = run_hook("gates_guard.py", {"tool_name": "Edit", "tool_input": {
        "file_path": str(tmp_path / "STATE.md"),
        "old_string": "status: done", "new_string": "status: in_progress"}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr


def test_write_fresh_state_allowed(tmp_path, run_hook):
    # file absent -> scaffold writing gates: {} is lawful
    sp = tmp_path / "STATE.md"
    r = run_hook("gates_guard.py", {"tool_name": "Write",
                 "tool_input": {"file_path": str(sp), "content": _state()}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr


def test_write_preserving_gates_allowed(tmp_path, run_hook):
    sp = tmp_path / "STATE.md"
    sp.write_text(_state(status="done", gates=G1_GATES))
    # agent rewrites status/next_action but keeps gates byte-identical
    r = run_hook("gates_guard.py", {"tool_name": "Write", "tool_input": {
        "file_path": str(sp), "content": _state(status="in_progress", gates=G1_GATES)}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr


def test_write_changing_gates_blocked(tmp_path, run_hook):
    sp = tmp_path / "STATE.md"
    sp.write_text(_state(gates=EMPTY_GATES))
    r = run_hook("gates_guard.py", {"tool_name": "Write", "tool_input": {
        "file_path": str(sp), "content": _state(gates=G1_GATES)}, "cwd": str(tmp_path)})
    assert r.returncode == 2
    assert "gates" in r.stderr
