"""Validator: ideas/<slug>/predictions.jsonl (locked at G4, resolved by β / W10). Spec: reference §3.5.

Two line shapes share one append-only file (ledger discipline):
  - LOCK line   (written at G4): id, slug, gate, persona, claim, p∈[0,1], resolution_criteria, resolve_by
  - SUPPLEMENT  (written at β/W10): same id, resolved date, outcome, brier -- the resolution, appended.

Rules (reference §3.5): once locked, claim/p never change; the validator REJECTS any LOCK line missing
resolution_criteria or resolve_by, and any SUPPLEMENT missing an outcome. An empty file passes (the
scaffold opens it empty; it is filled at G4).

Every assert message is written FOR THE AGENT (schema_on_write feeds it back for self-repair).
"""
import json
from pathlib import Path

FIXTURE = "predictions.sample.jsonl"
BAD_FIXTURE = "predictions.bad.jsonl"


def _lines(text):
    out = []
    for i, raw in enumerate(text.splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as e:
            raise AssertionError(f"line {i} is not valid JSON ({e}) -- predictions.jsonl is one JSON object per line")
        assert isinstance(obj, dict), f"line {i} must be a JSON object"
        out.append(obj)
    return out


def _is_lock(obj):
    return "claim" in obj


def _validate(text):
    objs = _lines(text)
    lock_ids = []
    for obj in objs:
        cid = obj.get("id")
        assert isinstance(cid, str) and cid, "every prediction line needs a non-empty string id"
        if _is_lock(obj):
            assert str(obj.get("claim", "")).strip(), f"{cid}: a lock line needs a non-empty claim"
            p = obj.get("p")
            assert isinstance(p, (int, float)) and not isinstance(p, bool) and 0.0 <= p <= 1.0, (
                f"{cid}: p must be a number in [0,1] -- a calibration prediction"
            )
            assert str(obj.get("resolution_criteria", "")).strip(), (
                f"{cid}: missing resolution_criteria -- a prediction with no way to resolve it is unfalsifiable (§3.5)"
            )
            assert str(obj.get("resolve_by", "")).strip(), (
                f"{cid}: missing resolve_by -- every locked prediction needs a resolution deadline (§3.5)"
            )
            lock_ids.append(cid)
        else:
            # a supplement / resolution line: must carry a recorded outcome for the referenced id
            assert obj.get("resolved"), (
                f"{cid}: a non-lock line must be a resolution -- set 'resolved' (date) + 'outcome'"
            )
            assert "outcome" in obj and obj["outcome"] is not None, (
                f"{cid}: a resolution line must record an outcome (true/false) -- §3.5 resolution protocol"
            )
    assert len(lock_ids) == len(set(lock_ids)), "duplicate lock-line id -- each prediction is locked once (resolutions reuse the id as supplements)"


def test_valid_predictions(artifact_text):
    _validate(artifact_text)


def test_empty_file_passes():
    _validate("")  # scaffold opens predictions.jsonl empty; it is filled at G4


def test_bad_fixture_bites():
    import pytest
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    with pytest.raises(AssertionError):
        _validate(bad)
