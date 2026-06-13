"""Validator: ideas/<slug>/pressure-report-beta.md (gate G6). Spec: reference §2 (step 6) + §9.

Step 6 is α's panel run over the Discovery Read, with two added teeth: a go/pivot/kill
**recommendation** and a **citation tooth** (every load-bearing claim cites a ledger E-xxx).
This validator guards the report's *shape* from text alone — frontmatter enums, required
sections, and that the report (and its recommendation rationale) is citation-grounded. The
stricter per-claim density + referential-integrity check rides in the pressure-test skill's
own frontmatter hook (citation_density_check.py, ref §7.2/§7.5) — additive, not a replacement.

Every assert message is written FOR THE AGENT: the schema_on_write hook feeds it back verbatim,
so it must say what *right* looks like.
"""
import re
from pathlib import Path

import yaml

FIXTURE = "pressure-report-beta.sample.md"
BAD_FIXTURE = "pressure-report-beta.bad.md"

RECOMMENDATIONS = {"go", "pivot", "kill"}
FATAL_FLAGS = {"none", "illegal", "demand_provably_negative"}
# stable substrings of the §2 / template headings (matched in ## headings, case-insensitive)
SECTIONS = ["Recommendation", "Calibration", "How the evidence moved", "Resolved",
            "Ranked residual risks", "Fatal-flaw", "Cost"]
E_CITE = re.compile(r"\bE-\d+\b")  # a real ledger id (E-001); ignores the literal "E-xxx" placeholder


def _frontmatter(text):
    assert text.startswith("---"), "pressure-report-beta.md must open with a YAML frontmatter block (---)"
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
    assert fm.get("stage") == "pressure_beta", "frontmatter stage must be 'pressure_beta' (this is the β report, not α)"


def test_recommendation_enum(artifact_text):
    fm = _frontmatter(artifact_text)
    rec = fm.get("recommendation")
    assert rec in RECOMMENDATIONS, (
        f"recommendation must be one of {sorted(RECOMMENDATIONS)} -- the β panel RECOMMENDS go/pivot/kill; "
        "the founder's G6 signature decides"
    )


def test_p_agg_is_calibration(artifact_text):
    fm = _frontmatter(artifact_text)
    p = fm.get("p_agg")
    assert isinstance(p, (int, float)) and not isinstance(p, bool) and 0.0 <= p <= 1.0, (
        "p_agg must be a number in [0,1] -- a calibration prediction, never a verdict"
    )


def test_fatal_flag_enum(artifact_text):
    fm = _frontmatter(artifact_text)
    assert fm.get("fatal_flag") in FATAL_FLAGS, (
        f"fatal_flag must be one of {sorted(FATAL_FLAGS)} -- 'none' unless an illegal/demand-provably-negative "
        "issue is objectively established with cited evidence (surfaced for the founder, never a desk kill)"
    )


def test_lists_are_lists(artifact_text):
    fm = _frontmatter(artifact_text)
    for field in ("open_assumptions", "predictions_resolved"):
        assert isinstance(fm.get(field), list), f"{field} must be a list (empty list allowed)"


def test_sections_present(artifact_text):
    for s in SECTIONS:
        assert _section(artifact_text, s) is not None, (
            f"missing the '## ...{s}...' section -- a β report needs all of: {', '.join(SECTIONS)}"
        )


def test_cites_ledger(artifact_text):
    assert E_CITE.search(artifact_text), (
        "β report cites no ledger entry -- every load-bearing claim must cite an E-xxx "
        "(interview-derived claims cite grade <=2)"
    )
    rec = _section(artifact_text, "Recommendation")
    assert rec and E_CITE.search(rec), (
        "the Recommendation rationale must cite at least one ledger E-xxx -- the go/pivot/kill call is "
        "evidence-grounded, not opinion"
    )


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_stage, test_recommendation_enum, test_p_agg_is_calibration, test_fatal_flag_enum,
                  test_lists_are_lists, test_sections_present, test_cites_ledger):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "pressure-report-beta.bad.md slipped past every check -- the validator does not bite"
