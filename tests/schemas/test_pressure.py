"""Validator: ideas/<slug>/pressure-report-alpha.md (gate G4). Spec: reference §2 (step 4) + §9.

Step 4 (pressure-test α) runs the persona panel over the neutral brief and compiles 5-8 OPEN
assumptions, each paired with a past-behaviour interview question, plus a calibrated p_success
distribution locked into predictions.jsonl. **α never kills** -- p_agg is a calibration prediction,
not a verdict. This validator guards the report's *shape* from text alone: frontmatter enums, the
5-8 open-assumptions invariant (criterion g4-2), and the required sections.

Every assert message is written FOR THE AGENT: the schema_on_write hook feeds it back verbatim,
so it must say what *right* looks like.
"""
import re
from pathlib import Path

import yaml

FIXTURE = "pressure-report-alpha.sample.md"
BAD_FIXTURE = "pressure-report-alpha.bad.md"

FATAL_FLAGS = {"none", "illegal", "demand_provably_negative"}
# stable substrings of the §2 / template headings (matched in ## headings, case-insensitive)
SECTIONS = ["Calibration", "Ranked risks", "Open assumptions", "Steelman", "Competitor steelman",
            "Closed by fact", "Fatal-flaw", "Cost"]
ROW_RE = re.compile(r"^\s*\|\s*\d+\s*\|", re.M)  # a numbered table data row: | 1 | ...


def _frontmatter(text):
    assert text.startswith("---"), "pressure-report-alpha.md must open with a YAML frontmatter block (---)"
    parts = text.split("---", 2)
    assert len(parts) >= 3, "frontmatter must be closed by a second --- line"
    fm = yaml.safe_load(parts[1])
    assert isinstance(fm, dict), "frontmatter must parse as a YAML mapping"
    return fm


def _section(text, keyword):
    """Body of the first ## heading containing `keyword` (case-insensitive), or None."""
    m = re.search(rf"^##\s*[^\n]*{re.escape(keyword)}[^\n]*\n(.*?)(?=^##\s|\Z)",
                  text, re.M | re.S | re.I)
    return m.group(1) if m else None


def test_stage(artifact_text):
    fm = _frontmatter(artifact_text)
    assert fm.get("stage") == "pressure_alpha", "frontmatter stage must be 'pressure_alpha' (this is the α report, not β)"


def test_p_agg_is_calibration(artifact_text):
    fm = _frontmatter(artifact_text)
    p = fm.get("p_agg")
    assert isinstance(p, (int, float)) and not isinstance(p, bool) and 0.0 <= p <= 1.0, (
        "p_agg must be a number in [0,1] -- a calibration prediction, NEVER a verdict (α does not kill)"
    )


def test_p_distribution_is_mapping(artifact_text):
    fm = _frontmatter(artifact_text)
    assert isinstance(fm.get("p_distribution"), dict), (
        "p_distribution must be a mapping {persona: p_success} (empty mapping {} allowed before the cross-exam round)"
    )


def test_fatal_flag_enum(artifact_text):
    fm = _frontmatter(artifact_text)
    assert fm.get("fatal_flag") in FATAL_FLAGS, (
        f"fatal_flag must be one of {sorted(FATAL_FLAGS)} -- 'none' unless an illegal/demand-provably-negative "
        "issue is objectively established with cited evidence (surfaced for the founder, never a desk kill)"
    )


def test_predictions_locked_is_bool(artifact_text):
    fm = _frontmatter(artifact_text)
    assert isinstance(fm.get("predictions_locked"), bool), (
        "predictions_locked must be a boolean -- true once one line per persona is in predictions.jsonl"
    )


def test_open_assumptions_count(artifact_text):
    """Criterion g4-2: 5-8 OPEN assumptions carried into discovery."""
    fm = _frontmatter(artifact_text)
    oa = fm.get("open_assumptions")
    assert isinstance(oa, list), "open_assumptions must be a list in the frontmatter"
    assert 5 <= len(oa) <= 8, (
        f"open_assumptions has {len(oa)} entries -- the α panel must compile 5-8 OPEN assumptions "
        "(too few = under-tested; too many = unranked); ref criterion g4-2"
    )


def test_sections_present(artifact_text):
    for s in SECTIONS:
        assert _section(artifact_text, s) is not None, (
            f"missing the '## ...{s}...' section -- an α report needs all of: {', '.join(SECTIONS)}"
        )


def test_open_assumptions_have_questions(artifact_text):
    """Criterion g4-2: each open assumption pairs with a past-behaviour interview question (table rows)."""
    sec = _section(artifact_text, "Open assumptions")
    assert sec is not None, "missing the '## Open assumptions → interview questions' section"
    rows = ROW_RE.findall(sec)
    assert len(rows) >= 5, (
        f"the Open-assumptions table has {len(rows)} numbered rows -- each of the 5-8 assumptions needs its "
        "own row pairing it with a past-behaviour Mom-Test question"
    )


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_stage, test_p_agg_is_calibration, test_p_distribution_is_mapping, test_fatal_flag_enum,
                  test_predictions_locked_is_bool, test_open_assumptions_count, test_sections_present,
                  test_open_assumptions_have_questions):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "pressure-report-alpha.bad.md slipped past every check -- the validator does not bite"
