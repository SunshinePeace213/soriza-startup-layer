"""Validator: ideas/<slug>/gates/criteria-g*.yaml (pre-registered, write-once). Spec: §6.2.

Criteria are locked BEFORE the evidence they judge (lock-ahead / pre-registration). This
validator guards the shape; advance_gate.py separately enforces locked==true and that
locked_at predates the evidence file mtimes.
"""
import re
from pathlib import Path

import yaml

FIXTURE = "criteria.sample.yaml"
BAD_FIXTURE = "criteria.bad.yaml"
GATE_RE = re.compile(r"^g[1-9]$")
CHECK_KINDS = {"auto", "human"}


def _validate(text):
    doc = yaml.safe_load(text)
    assert isinstance(doc, dict), "criteria file must be a YAML mapping"
    assert GATE_RE.match(str(doc.get("gate", ""))), "gate must be g1..g9"
    assert isinstance(doc.get("slug"), str) and doc["slug"], "slug must be a non-empty string"
    assert doc.get("locked") is True, "locked must be true -- criteria are pre-registered and never edited after lock"
    assert doc.get("locked_at"), "locked_at timestamp required (must predate the evidence this gate judges)"

    criteria = doc.get("criteria")
    assert isinstance(criteria, list) and criteria, "criteria must be a non-empty list"
    seen = set()
    for c in criteria:
        assert isinstance(c, dict), "each criterion must be a mapping {id, desc, check[, test]}"
        cid = c.get("id")
        assert isinstance(cid, str) and cid, "each criterion needs a non-empty id"
        assert cid not in seen, f"duplicate criterion id {cid!r}"
        seen.add(cid)
        assert isinstance(c.get("desc"), str) and c["desc"], f"criterion {cid} needs a desc"
        assert c.get("check") in CHECK_KINDS, f"criterion {cid} check must be 'auto' or 'human'"


def test_valid_criteria(artifact_text):
    _validate(artifact_text)


def test_bad_fixture_bites():
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    import pytest
    with pytest.raises(AssertionError):
        _validate(bad)
