"""Validator (lite): ideas/<slug>/evidence-ledger.jsonl. Spec: §6.3 + CLAUDE.md §3.

W1 ships the lite version: unique ascending E-ids, grade 1..5, grade<=4 needs a source/url,
append-only. The empty file (scaffold) is valid. Corrections are NEW lines carrying
"corrects":"E-xxx" (never edits of old lines) -- the W4 full validator adds type/quote rules.
"""
import json
import re
from pathlib import Path

FIXTURE = "ledger.sample.jsonl"
EMPTY_FIXTURE = "ledger.empty.jsonl"
BAD_FIXTURE = "ledger.bad.jsonl"
ID_RE = re.compile(r"^E-(\d+)$")


def _validate(text):
    lines = [ln for ln in text.splitlines() if ln.strip()]
    last = None
    for i, ln in enumerate(lines, 1):
        try:
            rec = json.loads(ln)
        except json.JSONDecodeError as e:
            raise AssertionError(f"line {i} is not valid JSON: {e}")
        assert isinstance(rec, dict), f"line {i} must be a JSON object"
        m = ID_RE.match(str(rec.get("id", "")))
        assert m, f"line {i}: id must match E-<digits> (e.g. E-001)"
        num = int(m.group(1))
        grade = rec.get("grade")
        assert isinstance(grade, int) and 1 <= grade <= 5, f"{rec.get('id')}: grade must be an int in 1..5"
        assert isinstance(rec.get("claim"), str) and rec["claim"], f"{rec['id']}: claim must be a non-empty string"
        if grade <= 4 and not rec.get("corrects"):
            assert rec.get("source") or rec.get("url"), f"{rec['id']}: grade<=4 requires a source or url"
        if last is not None:
            assert num > last, f"{rec['id']}: ids must be unique and ascending (previous was E-{last:03d})"
        last = num


def test_valid_ledger(artifact_text):
    _validate(artifact_text)


def test_empty_ledger_is_valid():
    """The scaffold opens an empty ledger -- it must validate."""
    _validate((Path(__file__).parents[1] / "fixtures" / EMPTY_FIXTURE).read_text(encoding="utf-8"))


def test_bad_fixture_bites():
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    import pytest
    with pytest.raises(AssertionError):
        _validate(bad)
