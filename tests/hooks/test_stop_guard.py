"""Hook #4 stop_guard: block stopping while the ACTIVE idea has undone agent-owned items,
but release on every anti-deadlock condition (ref §7.4). Encodes WHY each release exists,
not just that the exit code is 0."""

FM = """---
slug: x
schema_version: 2
current_step: 5
step_name: customer_discovery
status: {status}
owner: {owner}
interview_budget: {{total: 10, used: 0}}
step_checklist:
{checklist}
deltas_pending: []
gates: {{}}
next_action: "do the thing"
blocking: null
updated: 2026-06-14T00:00+08:00
---
body
"""

AGENT_OPEN = '  - {item: "Extract ledger entries", owner: agent, done: false}'
AGENT_DONE = '  - {item: "Extract ledger entries", owner: agent, done: true}'
HUMAN_OPEN = '  - {item: "Run interviews 5-6", owner: human, done: false}'


def _state(tmp_path, status="in_progress", owner="agent", checklist=AGENT_OPEN, slug="x"):
    ideas = tmp_path / "ideas"
    (ideas / slug).mkdir(parents=True)
    (ideas / "ACTIVE").write_text(slug + "\n")
    (ideas / slug / "STATE.md").write_text(FM.format(status=status, owner=owner, checklist=checklist))


def _run(run_hook, tmp_path, stop_hook_active=False):
    return run_hook("stop_guard.py", {"cwd": str(tmp_path), "stop_hook_active": stop_hook_active})


def test_blocks_on_open_agent_item(tmp_path, run_hook):
    _state(tmp_path)
    r = _run(run_hook, tmp_path)
    assert r.returncode == 2
    assert "Extract ledger entries" in r.stderr  # the open item is named so the agent knows what to finish


def test_stop_hook_active_releases(tmp_path, run_hook):
    # official second-pass flag: never wedge a session in an infinite stop loop
    _state(tmp_path)
    r = _run(run_hook, tmp_path, stop_hook_active=True)
    assert r.returncode == 0, r.stderr


def test_owner_human_releases(tmp_path, run_hook):
    # the deadlock fix: never push the agent at a human-owned step
    _state(tmp_path, owner="human")
    r = _run(run_hook, tmp_path)
    assert r.returncode == 0, r.stderr


def test_status_done_releases(tmp_path, run_hook):
    _state(tmp_path, status="done")
    r = _run(run_hook, tmp_path)
    assert r.returncode == 0, r.stderr


def test_all_agent_items_done_releases(tmp_path, run_hook):
    _state(tmp_path, checklist=AGENT_DONE)
    r = _run(run_hook, tmp_path)
    assert r.returncode == 0, r.stderr


def test_open_human_item_does_not_block(tmp_path, run_hook):
    # owner: agent on STATE but the only open item is human-owned -> agent has nothing to finish
    _state(tmp_path, owner="agent", checklist=AGENT_DONE + "\n" + HUMAN_OPEN)
    r = _run(run_hook, tmp_path)
    assert r.returncode == 0, r.stderr


def test_no_active_idea_releases(tmp_path, run_hook):
    r = _run(run_hook, tmp_path)  # no ideas/ACTIVE at all
    assert r.returncode == 0, r.stderr
