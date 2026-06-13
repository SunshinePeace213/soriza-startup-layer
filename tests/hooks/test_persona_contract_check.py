"""persona_contract_check.py (SubagentStop): validate the α JSON contract a persona returns.
Fail-CLOSED on a malformed contract (JSON present, bad field), fail-OPEN when no JSON can be
extracted (transcript-format drift must never wedge the panel). Ref §7.5 / §10 Appendix B."""
import json

VALID = {
    "persona": "eisenmann",
    "p_success": 0.3,
    "base_rate_ref": "false-start base rate for pre-WTP tooling",
    "risk_patterns": ["false start"],
    "sharpest_objection": {
        "objection": "WTP unproven",
        "falsifiable_assumption": "a broker pays >=HK$500/mo",
        "interview_question": "when did you last pay for an admin tool?",
    },
    "steelman_for": "acute recurring calendar-locked pain",
    "change_my_mind": "a broker commits money in week one",
}


def _transcript(tmp_path, assistant_text: str):
    tp = tmp_path / "transcript.jsonl"
    tp.write_text(
        json.dumps({"type": "user", "message": {"role": "user", "content": "go"}}) + "\n"
        + json.dumps({"type": "assistant",
                      "message": {"role": "assistant", "content": [{"type": "text", "text": assistant_text}]}}) + "\n",
        encoding="utf-8",
    )
    return tp


def _run(run_hook, tmp_path, assistant_text, stop_hook_active=False):
    tp = _transcript(tmp_path, assistant_text)
    return run_hook("persona_contract_check.py",
                    {"cwd": str(tmp_path), "transcript_path": str(tp), "stop_hook_active": stop_hook_active})


def test_valid_contract_passes(tmp_path, run_hook):
    r = _run(run_hook, tmp_path, json.dumps(VALID))
    assert r.returncode == 0


def test_valid_contract_in_fences_passes(tmp_path, run_hook):
    r = _run(run_hook, tmp_path, "```json\n" + json.dumps(VALID) + "\n```")
    assert r.returncode == 0


def test_p_out_of_range_blocks(tmp_path, run_hook):
    bad = {**VALID, "p_success": 1.7}
    r = _run(run_hook, tmp_path, json.dumps(bad))
    assert r.returncode == 2
    assert "p_success" in r.stderr  # message names the offending field for self-repair


def test_missing_field_blocks(tmp_path, run_hook):
    bad = {k: v for k, v in VALID.items() if k != "change_my_mind"}
    r = _run(run_hook, tmp_path, json.dumps(bad))
    assert r.returncode == 2


def test_incomplete_objection_blocks(tmp_path, run_hook):
    bad = {**VALID, "sharpest_objection": {"objection": "x"}}  # missing falsifiable_assumption + question
    r = _run(run_hook, tmp_path, json.dumps(bad))
    assert r.returncode == 2


def test_no_json_fails_open(tmp_path, run_hook):
    # transcript has prose but no JSON object: degrade gracefully (the judge backstops), never wedge
    r = _run(run_hook, tmp_path, "I think the odds are roughly one in three.")
    assert r.returncode == 0


def test_stop_hook_active_releases(tmp_path, run_hook):
    bad = {**VALID, "p_success": 1.7}
    r = _run(run_hook, tmp_path, json.dumps(bad), stop_hook_active=True)
    assert r.returncode == 0  # anti-loop: second pass always releases
