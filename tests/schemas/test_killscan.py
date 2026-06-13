"""Validator: ideas/<slug>/kill-scan.md (gate G3). Spec: reference §2 step 3 + §7.2 + §9.

The desk-scan artifact. Three sections (Disqualifier Scan / Demand Scan / G3 Verdict); the
disqualifier scan covers all four axes (regulatory wall / technical feasibility / platform
single-point risk / graveyard); EVERY verdict rests on a cited, checkable fact -- the section
carries an E-xxx per axis (§7.2, the citation teeth). No raw web URLs: web content enters
artifacts ONLY via evidence-ledger.jsonl (grade 4, url required) and is cited here as E-xxx
(CLAUDE.md §3). Every assert message is written FOR THE AGENT -- the schema_on_write hook
feeds it back verbatim for self-repair, so it must say what *right* looks like.
"""
import re
from pathlib import Path

FIXTURE = "kill-scan.sample.md"
BAD_FIXTURE = "kill-scan.bad.md"
SECTIONS = ["Disqualifier Scan", "Demand Scan", "G3 Verdict"]
# axis keyword -> human label (keyword is a lenient substring so phrasing stays free)
AXES = {"regulat": "regulatory wall", "technical": "technical feasibility",
        "platform": "platform single-point risk", "graveyard": "graveyard / failed-clone cases"}
E_RE = re.compile(r"E-\d+")


def _sec(text, name):
    m = re.search(rf"^##\s*{re.escape(name)}\b(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    assert m, f"Missing section: ## {name} (kill-scan needs all three: {', '.join(SECTIONS)})"
    return m.group(1)


def test_sections_present(artifact_text):
    for s in SECTIONS:
        _sec(artifact_text, s)


def test_four_axes(artifact_text):
    scan = _sec(artifact_text, "Disqualifier Scan").lower()
    for kw, label in AXES.items():
        assert kw in scan, f"Disqualifier Scan must cover the {label} axis -- all 4 are mandatory (missing '{kw}*')"


def test_disqualifier_verdicts_cite_evidence(artifact_text):
    scan = _sec(artifact_text, "Disqualifier Scan")
    n = len(set(E_RE.findall(scan)))
    assert n >= 4, (f"Disqualifier Scan cites {n} ledger entries; needs >=4 (one E-xxx per axis) -- "
                    "every verdict must rest on a cited, checkable fact (§7.2), not an opinion")


def test_demand_scan_cites_evidence(artifact_text):
    demand = _sec(artifact_text, "Demand Scan")
    assert E_RE.search(demand), ("Demand Scan cites no ledger entry -- complaints and user language must cite "
                                 "grade-4 E-xxx entries (the named complainers seed 5a's warm list)")


def test_g3_verdict_present(artifact_text):
    verdict = _sec(artifact_text, "G3 Verdict")
    assert re.search(r"\b(CLEAR|TRIPPED)\b", verdict), (
        "G3 Verdict must state CLEAR or TRIPPED -- CLEAR advances to pressure-test α; TRIPPED stops the "
        "gate for a founder override (the only legitimate desk-kill in the pipeline)")


def test_no_raw_web_urls(artifact_text):
    assert "http" not in artifact_text, (
        "kill-scan.md may not contain raw URLs -- web facts enter via evidence-ledger.jsonl (grade 4, url "
        "required) and are cited here as E-xxx (CLAUDE.md §3: web enters artifacts only via the ledger)")


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_sections_present, test_four_axes, test_disqualifier_verdicts_cite_evidence,
                  test_demand_scan_cites_evidence, test_g3_verdict_present, test_no_raw_web_urls):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "kill-scan.bad.md slipped past every check -- the validator does not bite"
