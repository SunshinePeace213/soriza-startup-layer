"""Hook #1 write_path_guard: only ideas/<ACTIVE>/ and ideas/_exploration/ are writable."""


def _payload(tmp, rel_path):
    return {"tool_name": "Write", "tool_input": {"file_path": str(tmp / rel_path)}, "cwd": str(tmp)}


def _setup(tmp, active="active-idea"):
    (tmp / "ideas").mkdir()
    (tmp / "ideas" / "ACTIVE").write_text(active + "\n")


def test_allows_active_idea(tmp_path, run_hook):
    _setup(tmp_path)
    r = run_hook("write_path_guard.py", _payload(tmp_path, "ideas/active-idea/hypothesis.md"))
    assert r.returncode == 0, r.stderr


def test_allows_exploration(tmp_path, run_hook):
    _setup(tmp_path)
    r = run_hook("write_path_guard.py", _payload(tmp_path, "ideas/_exploration/thesis/slate.md"))
    assert r.returncode == 0, r.stderr


def test_blocks_inactive_idea(tmp_path, run_hook):
    _setup(tmp_path)
    r = run_hook("write_path_guard.py", _payload(tmp_path, "ideas/other-idea/STATE.md"))
    assert r.returncode == 2
    assert "write-path" in r.stderr


def test_allows_paths_outside_ideas(tmp_path, run_hook):
    _setup(tmp_path)
    r = run_hook("write_path_guard.py", _payload(tmp_path, "scripts/foo.py"))
    assert r.returncode == 0, r.stderr


def test_no_file_path_is_noop(tmp_path, run_hook):
    _setup(tmp_path)
    r = run_hook("write_path_guard.py", {"tool_name": "Write", "tool_input": {}, "cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr
