"""Validator: ideas/<slug>/startup-brief.md (gate G8). Spec: reference §2 step 8 + §7.4.

Step 8 merges solution-design + idea-stage-exit. The brief's validator gates the four things
the step card names -- **drift-audit table + premortem + PoC criteria + upstream citations** --
plus the absorbed idea-stage-exit core: a stamped **GO / NO-GO** decision. Every assert message
is written FOR THE AGENT: the schema_on_write hook (mapped startup-brief.md -> test_startup_brief)
feeds it back verbatim on failure, so it must say what *right* looks like, not just that it's wrong.

Mechanical only -- structure, not merit. Whether the drift audit is HONEST (a real ❌ row vs a
laundered ✅) is the founder's signature at G8, never a regex.
"""
import re
from pathlib import Path

FIXTURE = "startup-brief.sample.md"
BAD_FIXTURE = "startup-brief.bad.md"

# Required ## sections (keyword anchors; headings may carry trailing text, e.g.
# "## Drift Audit — assumed → validated"). Each maps to a distinctive heading substring.
SECTIONS = {
    "Decision": r"Decision",
    "Drift Audit": r"Drift Audit",
    "Premortem": r"Premortem",
    "Exit-Criteria": r"Exit-Criteria",
    "PoC Kill-Criteria": r"PoC Kill-Criteria",
    "PoC Brief": r"PoC Brief",
}
# Eisenmann's six failure patterns -- the premortem checklist (reference §10 / why-startups-fail).
SIX_PATTERNS = ["Bad Bedfellows", "False Starts", "False Positives",
                "Speed Trap", "Help Wanted", "Cascading Miracles"]
DRIFT_MARKERS = ("✅", "⚠️", "❌")
# Upstream evidence the brief must cite: ledger ids OR named upstream artifacts (the synthesis chain).
CITE_RE = re.compile(r"E-\d{2,}")
UPSTREAM_DOCS = ("customer-discovery", "pressure-report-alpha", "pressure-report-beta",
                 "kill-scan", "market-sizing", "hypothesis")


def _sec(text, name, pattern):
    m = re.search(rf"^##\s*{pattern}\b(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    assert m, (f"Missing section: ## {name} -- the brief needs all {len(SECTIONS)}: "
               f"{', '.join(SECTIONS)} (solution-design + idea-stage-exit, merged)")
    return m.group(1)


def test_sections_present(artifact_text):
    for name, pat in SECTIONS.items():
        _sec(artifact_text, name, pat)


def test_decision_stamp(artifact_text):
    """The absorbed idea-stage-exit core: an explicit, on-record GO or NO-GO stamp."""
    body = _sec(artifact_text, "Decision", SECTIONS["Decision"])
    assert re.search(r"\*\*\s*(GO|NO-GO)\s*\*\*", body), (
        "Decision section must stamp a bold **GO** or **NO-GO** -- the deliberate, on-record "
        "stamp is the guard against drift (concede the diagnosis, keep the prescription)"
    )


def test_drift_audit_table(artifact_text):
    """A markdown table whose rows carry a verdict marker -- the load-bearing anti-drift device."""
    sec = _sec(artifact_text, "Drift Audit", SECTIONS["Drift Audit"])
    has_table = bool(re.search(r"^\s*\|.*\|", sec, re.M)) and bool(
        re.search(r"^\s*\|[\s:|-]+\|", sec, re.M))
    assert has_table, ("Drift Audit needs a markdown table (assumed → validated → does the concept "
                       "serve the VALIDATED version?). Reconstruct the baseline first; don't measure "
                       "against the stale hypothesis.md")
    assert any(mk in sec for mk in DRIFT_MARKERS), (
        "Drift Audit table needs a verdict per row: ✅ serves it / ⚠️ drifting / ❌ still solving the "
        "old problem. A ❌ is a finding, not a nuisance -- do not launder it into ✅"
    )


def test_premortem_six_patterns(artifact_text):
    sec = _sec(artifact_text, "Premortem", SECTIONS["Premortem"])
    missing = [p for p in SIX_PATTERNS if p.lower() not in sec.lower()]
    assert not missing, ("Premortem must run Eisenmann's six failure patterns -- missing: "
                         f"{missing}. The full checklist: {', '.join(SIX_PATTERNS)}")


def test_poc_criteria_locked(artifact_text):
    """The PoC kill-criteria the founder locks for G9 (step 8 ⑤; build-poc scores against them)."""
    sec = _sec(artifact_text, "PoC Kill-Criteria", SECTIONS["PoC Kill-Criteria"])
    assert re.search(r"\bg9\b|criteria-g9", sec, re.I), (
        "PoC Kill-Criteria must reference the locked G9 set (gates/criteria-g9.yaml) -- lock-ahead "
        "requires criteria-g9.yaml locked before G8; build-poc scores the PoC against it"
    )
    assert len(re.findall(r"^\s*[-|]", sec, re.M)) >= 2, (
        "PoC Kill-Criteria must list the concrete thresholds (≥2 criteria) the PoC will be scored "
        "against -- not 'TBD'. Pre-registration: these are never softened after the PoC runs"
    )


def test_upstream_citations(artifact_text):
    """The brief synthesizes upstream evidence -- it must cite it, not assert it."""
    ids = set(CITE_RE.findall(artifact_text))
    docs = {d for d in UPSTREAM_DOCS if d in artifact_text.lower()}
    assert len(ids) + len(docs) >= 2, (
        "Brief must cite upstream evidence (≥2 distinct): E-xxx ledger ids and/or named upstream "
        "artifacts (customer-discovery.md, pressure-report-*, kill-scan.md, market-sizing.md). "
        "A brief with no upstream citations is an opinion, not a synthesis"
    )


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_sections_present, test_decision_stamp, test_drift_audit_table,
                  test_premortem_six_patterns, test_poc_criteria_locked, test_upstream_citations):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "startup-brief.bad.md slipped past every check -- the validator does not bite"
