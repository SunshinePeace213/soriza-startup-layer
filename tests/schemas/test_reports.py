"""Report scripts (T21/T29 dashboard, T34 calibration): the state-audit must catch declared/derived
drift, and Brier must be the real (p-outcome)^2 -- a dashboard that can't go red, or a Brier that
hardcodes a number, would be worthless (the §3.3 insight: no status file can silently rot)."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parents[2]


def _mod(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _idea(tmp_path, slug, current_step, *artifacts):
    idea = tmp_path / slug
    idea.mkdir(parents=True)
    (idea / "STATE.md").write_text(
        f"---\nslug: {slug}\ncurrent_step: {current_step}\nstatus: in_progress\nowner: agent\n"
        f"next_action: do step {current_step}\nupdated: 2026-06-16T00:00+08:00\n---\n")
    (idea / "seed.md").write_text("seed")
    for rel in artifacts:
        p = idea / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x")
    return idea


def test_dashboard_flags_declared_derived_drift(tmp_path):
    d = _mod("render_dashboard")
    # STATE claims step 7 but only the hypothesis exists -> derived step 3 -> DRIFT
    idea = _idea(tmp_path, "rotten", 7, "hypothesis.md")
    row = d.audit_idea(idea)
    assert row["derived"] == 3 and row["drift"] is True, row
    assert "DRIFT" in d.render([row])


def test_dashboard_clean_when_consistent(tmp_path):
    d = _mod("render_dashboard")
    # hypothesis done (step 2 complete) -> derived next = 3; declared 3 is in {2,3} -> ok
    idea = _idea(tmp_path, "healthy", 3, "hypothesis.md")
    row = d.audit_idea(idea)
    assert row["derived"] == 3 and row["drift"] is False, row


def test_dashboard_step_in_progress_artifact_pending_is_not_drift(tmp_path):
    d = _mod("render_dashboard")
    # declared step 2, no hypothesis yet (scaffold only) -> derived 2 -> not drift
    idea = _idea(tmp_path, "fresh", 2)
    assert d.audit_idea(idea)["drift"] is False


def test_brier_math_and_per_persona(tmp_path, monkeypatch):
    c = _mod("calibration_review")
    locked = {
        "p-1": {"id": "p-1", "persona": "munger", "claim": "x", "p": 0.8},
        "p-2": {"id": "p-2", "persona": "thiel", "claim": "y", "p": 0.2},
    }
    outcomes = {"p-1": True, "p-2": True}  # munger right-ish (0.04), thiel wrong (0.64)
    s = c.score(locked, outcomes)
    assert s["resolved"] == 2 and s["open"] == 0
    assert s["per_persona"]["munger"] == 0.04, s
    assert s["per_persona"]["thiel"] == 0.64, s
    assert s["overall"] == 0.34


def test_calibration_handles_no_resolved(tmp_path):
    c = _mod("calibration_review")
    s = c.score({"p-1": {"id": "p-1", "persona": "x", "claim": "z", "p": 0.5}}, {})
    assert s["resolved"] == 0 and s["overall"] is None
    assert "No predictions resolved yet" in c.render(s)
