"""Hook #2 schema_on_write: re-run an artifact's validator against the just-written file,
feeding assertion messages back on failure (exit 2). The doc-TDD closed loop (ref §9).

cwd is set to the real repo ROOT so the hook's `pytest tests/schemas/...` resolves; the
artifact lives at an absolute tmp path that goes through an `ideas/` directory (the hook's
gate). Validators + fixtures are the REAL ones (no mocks) -- the point is to prove the loop
actually bites on a bad artifact and stays silent on a good one.
"""
from pathlib import Path

ROOT = Path(__file__).parents[2]
FIX = ROOT / "tests" / "fixtures"


def _payload(fp, cwd=ROOT):
    return {"tool_name": "Write", "tool_input": {"file_path": str(fp)}, "cwd": str(cwd)}


def _artifact(tmp_path, relparts, fixture_name):
    """Write a copy of a real fixture at tmp_path/<relparts...> and return its path."""
    p = tmp_path.joinpath(*relparts)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text((FIX / fixture_name).read_text(encoding="utf-8"), encoding="utf-8")
    return p


def test_valid_state_passes(tmp_path, run_hook):
    p = _artifact(tmp_path, ("ideas", "slug", "STATE.md"), "state.sample.md")
    r = run_hook("schema_on_write.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_invalid_state_blocks_with_validator_message(tmp_path, run_hook):
    p = _artifact(tmp_path, ("ideas", "slug", "STATE.md"), "state.bad.md")
    r = run_hook("schema_on_write.py", _payload(p))
    assert r.returncode == 2
    # the validator's OWN assertion message is fed back for self-repair (not a generic error)
    assert "schema_version" in r.stderr


def test_criteria_pattern_is_validated(tmp_path, run_hook):
    # gates/criteria-*.yaml routes via the pattern branch -> test_criteria
    p = _artifact(tmp_path, ("ideas", "slug", "gates", "criteria-g2.yaml"), "criteria.sample.yaml")
    r = run_hook("schema_on_write.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_unmapped_artifact_is_noop(tmp_path, run_hook):
    # seed.md has no validator route -> no contract to enforce
    p = tmp_path / "ideas" / "slug" / "seed.md"
    p.parent.mkdir(parents=True)
    p.write_text("anything goes here")
    r = run_hook("schema_on_write.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_unshipped_validator_is_noop(tmp_path, run_hook):
    # kill-scan.md maps to test_killscan, which has not shipped yet (validator-first):
    # a write must NOT be blocked just because its validator does not exist yet
    p = tmp_path / "ideas" / "slug" / "kill-scan.md"
    p.parent.mkdir(parents=True)
    p.write_text("# kill-scan\nnonsense that no validator checks yet")
    r = run_hook("schema_on_write.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_outside_ideas_is_noop(tmp_path, run_hook):
    # a STATE.md NOT under ideas/ (e.g. scripts/templates/STATE.md) is not schema-governed
    p = tmp_path / "scripts" / "templates" / "STATE.md"
    p.parent.mkdir(parents=True)
    p.write_text("garbage: not even valid frontmatter")
    r = run_hook("schema_on_write.py", _payload(p))
    assert r.returncode == 0, r.stderr
