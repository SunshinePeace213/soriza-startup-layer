"""Hook #3 run_log: appends one observational line per tool call; never blocks."""
import json


def _last_line(tmp):
    return json.loads((tmp / "logs" / "run-log.jsonl").read_text().splitlines()[-1])


def test_logs_bash_with_slug(tmp_path, run_hook):
    (tmp_path / "ideas").mkdir()
    (tmp_path / "ideas" / "ACTIVE").write_text("my-slug\n")
    r = run_hook("run_log.py", {"tool_name": "Bash", "session_id": "sess1",
                 "tool_input": {"command": "echo hi"}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr
    rec = _last_line(tmp_path)
    assert rec["tool"] == "Bash" and rec["detail"] == "echo hi"
    assert rec["slug"] == "my-slug" and rec["session"] == "sess1"
    assert rec["ts"]


def test_logs_write_detail_is_filepath(tmp_path, run_hook):
    (tmp_path / "ideas").mkdir()
    (tmp_path / "ideas" / "ACTIVE").write_text("my-slug\n")
    r = run_hook("run_log.py", {"tool_name": "Write",
                 "tool_input": {"file_path": "ideas/my-slug/hypothesis.md"}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr
    assert _last_line(tmp_path)["detail"] == "ideas/my-slug/hypothesis.md"


def test_no_active_slug_is_null_and_still_passes(tmp_path, run_hook):
    # no ideas/ACTIVE -> slug null, but the observational hook must never block the tool
    r = run_hook("run_log.py", {"tool_name": "Bash",
                 "tool_input": {"command": "ls"}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr
    assert _last_line(tmp_path)["slug"] is None
