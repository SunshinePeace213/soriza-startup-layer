"""Validator: ideas/<slug>/hypothesis.md (gate G2). Spec: reference §9 + criteria-g2.yaml.

5 sections, <=300 words (mechanical proxy), each dimension a falsifiable claim, no web
citations (sharpen, don't prove). Every assert message is written FOR THE AGENT: the
schema_on_write hook feeds it back verbatim, so it must say what *right* looks like.
"""
import re
from pathlib import Path

FIXTURE = "hypothesis.sample.md"
BAD_FIXTURE = "hypothesis.bad.md"
SECTIONS = ["WHO", "HOW OFTEN", "HOW SEVERE", "STATUS QUO", "VALUE & GROWTH"]


def _sec(text, name):
    m = re.search(rf"^##\s*{name}\b(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    assert m, f"Missing section: ## {name} (hypothesis needs all 5: {', '.join(SECTIONS)})"
    return m.group(1)


def test_sections_present(artifact_text):
    for s in SECTIONS:
        _sec(artifact_text, s)


def test_length_cap(artifact_text):
    body = re.sub(r"[#>\-\s`*]", "", artifact_text)
    assert len(body) <= 2000, "Body too long (mechanical proxy for <=300 words; trim to the sharp claim)"


def test_provisional_flag(artifact_text):
    assert "provisional" in artifact_text.lower(), (
        "hypothesis must be marked 'provisional, to-be-tested' -- it is a claim to test, not a proven fact"
    )


def test_quantified_dimensions(artifact_text):
    for s in ("HOW OFTEN", "HOW SEVERE"):
        assert re.search(r"\d", _sec(artifact_text, s)), f"{s} has no number -- forcing specificity failed"


def test_no_web_citations(artifact_text):
    assert "http" not in artifact_text, "hypothesis may not cite the web (sharpen, don't prove)"


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_sections_present, test_length_cap, test_provisional_flag,
                  test_quantified_dimensions, test_no_web_citations):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "hypothesis.bad.md slipped past every check -- the validator does not bite"
