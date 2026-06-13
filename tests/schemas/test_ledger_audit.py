"""ledger_audit (T24): the three-way reconciliation must catch a gate written out-of-band.

The whole point (§3.4 #3): gates_guard blocks the file-tool path, but a Bash-sed bypass leaves
STATE.gates out of sync with the decision-log / criteria files. These tests plant exactly that
drift and assert the audit goes loud -- a green audit on a tampered tree would be worthless.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).parents[2]


def _audit_idea():
    spec = importlib.util.spec_from_file_location("ledger_audit", ROOT / "scripts" / "ledger_audit.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.audit_idea


def _make_idea(tmp_path, gates_block, dl="## DL-001 | 2026-06-16 | g1 | pick\n- Signed: Ringo\n",
               ledger=None, predictions=None, criteria_gates=("g2",)):
    idea = tmp_path / "demo-idea"
    (idea / "gates").mkdir(parents=True)
    for g in criteria_gates:
        (idea / "gates" / f"criteria-{g}.yaml").write_text(f"gate: {g}\nlocked: true\n")
    (idea / "STATE.md").write_text(
        "---\nslug: demo-idea\nschema_version: 2\ncurrent_step: 2\nstatus: in_progress\n"
        f"gates:\n{gates_block}"
        "next_action: x\nupdated: 2026-06-16T00:00+08:00\n---\nbody\n")
    (idea / "decision-log.md").write_text(dl)
    if ledger is not None:
        (idea / "evidence-ledger.jsonl").write_text(ledger)
    if predictions is not None:
        (idea / "predictions.jsonl").write_text(predictions)
    return idea


CLEAN_GATES = (
    "  g1: {result: pass, date: 2026-06-16, criteria: scaffold, decision: DL-001}\n"
    "  g2: {result: pass, date: 2026-06-17, criteria: gates/criteria-g2.yaml, decision: DL-001}\n"
)


def test_clean_idea_has_no_problems(tmp_path):
    idea = _make_idea(tmp_path, CLEAN_GATES)
    assert _audit_idea()(idea) == []


def test_gate_decision_not_in_decision_log_is_caught(tmp_path):
    # a Bash-sed bypass adds g2 -> DL-999 that was never appended to decision-log.md
    gates = CLEAN_GATES.replace("decision: DL-001}\n  g2", "decision: DL-001}\n  g2") + ""
    bad = ("  g1: {result: pass, criteria: scaffold, decision: DL-001}\n"
           "  g2: {result: pass, criteria: gates/criteria-g2.yaml, decision: DL-999}\n")
    idea = _make_idea(tmp_path, bad)
    probs = _audit_idea()(idea)
    assert any("DL-999" in p and "decision-log" in p for p in probs), probs


def test_gate_missing_criteria_file_is_caught(tmp_path):
    bad = ("  g1: {result: pass, criteria: scaffold, decision: DL-001}\n"
           "  g3: {result: pass, criteria: gates/criteria-g3.yaml, decision: DL-001}\n")
    idea = _make_idea(tmp_path, bad, criteria_gates=("g2",))  # g3 criteria deliberately absent
    probs = _audit_idea()(idea)
    assert any("criteria-g3.yaml" in p and "missing" in p for p in probs), probs


def test_non_ascending_ledger_id_is_caught(tmp_path):
    ledger = ('{"id":"E-001","grade":5,"type":"founder_belief","claim":"x","source":"founder"}\n'
              '{"id":"E-001","grade":5,"type":"founder_belief","claim":"y","source":"founder"}\n')
    idea = _make_idea(tmp_path, CLEAN_GATES, ledger=ledger)
    probs = _audit_idea()(idea)
    assert any("duplicate id E-001" in p or "not ascending" in p for p in probs), probs


def test_grade4_without_source_is_caught(tmp_path):
    ledger = '{"id":"E-001","grade":4,"type":"web","claim":"competitor complaint"}\n'  # no url/source
    idea = _make_idea(tmp_path, CLEAN_GATES, ledger=ledger)
    probs = _audit_idea()(idea)
    assert any("missing source/url" in p for p in probs), probs


def test_prediction_without_resolve_by_is_caught(tmp_path):
    preds = '{"id":"p-001","gate":"g4","claim":"x","p":0.5,"resolution_criteria":"table"}\n'  # no resolve_by
    idea = _make_idea(tmp_path, CLEAN_GATES, predictions=preds)
    probs = _audit_idea()(idea)
    assert any("resolution_criteria/resolve_by" in p for p in probs), probs
