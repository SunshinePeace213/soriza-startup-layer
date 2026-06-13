"""Hook #5 resume_inject: on SessionStart(resume|compact), print the ACTIVE idea's pipeline
position to stdout (context-injected). Informational -- always exits 0 (ref §7.4)."""

FM = """---
slug: hk-broker-recon
schema_version: 2
current_step: 5
step_name: customer_discovery
status: in_progress
owner: human
interview_budget: {total: 10, used: 4}
step_checklist:
  - {item: "Interviews 5-6 done", owner: human, done: false}
  - {item: "Extract ledger entries", owner: agent, done: true}
deltas_pending: []
gates: {}
next_action: "Finish interviews 5-6, then run synthesis"
blocking: null
updated: 2026-06-14T00:00+08:00
---
body
"""


def _run(run_hook, tmp_path):
    return run_hook("resume_inject.py", {"cwd": str(tmp_path), "source": "resume"})


def test_injects_active_state_summary(tmp_path, run_hook):
    ideas = tmp_path / "ideas" / "hk-broker-recon"
    ideas.mkdir(parents=True)
    (tmp_path / "ideas" / "ACTIVE").write_text("hk-broker-recon\n")
    (ideas / "STATE.md").write_text(FM)
    r = _run(run_hook, tmp_path)
    assert r.returncode == 0, r.stderr
    out = r.stdout
    assert "hk-broker-recon" in out and "step=5" in out
    assert "Finish interviews 5-6" in out          # next_action surfaced
    assert "Interviews 5-6 done (human)" in out     # open item with its owner surfaced


def test_no_active_prints_fallback_and_passes(tmp_path, run_hook):
    r = _run(run_hook, tmp_path)  # no ideas/ACTIVE
    assert r.returncode == 0, r.stderr
    assert "ideas/CLAUDE.md" in r.stdout  # tells the agent how to recover state manually
