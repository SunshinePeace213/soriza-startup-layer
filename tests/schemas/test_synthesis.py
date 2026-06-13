"""Validator: ideas/<slug>/customer-discovery.md -- the Discovery Read (gate G5).

Scores REAL interview evidence against the LOCKED kill-criteria, two-list style, with a
mandatory independent bias-check, and (9-step canon) ledger citations: every claim traces
to a grade <=2 evidence-ledger entry E-xxx. This validator enforces PRESENCE of the read's
load-bearing parts mechanically; per-claim citation density is a beta concern, not here.

Every assert message is written FOR THE AGENT: the schema_on_write hook feeds it back
verbatim, so it must say what *right* looks like.
"""
import re
from pathlib import Path

FIXTURE = "customer-discovery.sample.md"
BAD_FIXTURE = "customer-discovery.bad.md"

# Statuses come from scripts/score_criteria.py verbatim -- do not invent new tokens.
STATUS_TOKENS = ("TRIPPED", "CLEARED", "INCONCLUSIVE", "MANUAL")
VERDICTS = ("CONTINUE", "PIVOT", "KILL", "KEEP-DISCOVERING")


def test_verdict_present(artifact_text):
    found = [v for v in VERDICTS if re.search(rf"\b{re.escape(v)}\b", artifact_text)]
    assert found, (
        "Discovery Read needs exactly one verdict token as its headline/section -- one of "
        f"{' | '.join(VERDICTS)} (case-sensitive). State the call the evidence supports."
    )


def test_scorecard_present(artifact_text):
    assert re.search(r"^##\s*Kill-Criteria Scorecard", artifact_text, re.M), (
        "Discovery Read must have a '## Kill-Criteria Scorecard' section -- the per-criterion "
        "table that scores evidence against the LOCKED kill-criteria.json thresholds."
    )


def test_scorecard_status_vocab(artifact_text):
    found = [t for t in STATUS_TOKENS if re.search(rf"\b{t}\b", artifact_text)]
    assert found, (
        "Scorecard must use the scorer's status tokens (from score_criteria.py): at least one of "
        f"{' | '.join(STATUS_TOKENS)}. Copy the script's statuses verbatim; do not relitigate them."
    )


def test_two_evidence_lists(artifact_text):
    low = artifact_text.lower()
    assert "supports" in low and "challenges" in low, (
        "Discovery Read needs BOTH a 'Supports the hypothesis' and a 'Challenges the hypothesis' "
        "evidence grouping -- the two-list discipline forces you to log disconfirming signals, not "
        "just the supportive ones."
    )


def test_bias_check_present(artifact_text):
    assert re.search(r"^##\s*Bias-check", artifact_text, re.M | re.I), (
        "Discovery Read must carry a '## Bias-check' section -- the independent "
        "customer-discovery-bias-check agent's fold-in is mandatory in the canon. Surface where the "
        "read pattern-matches to hope rather than data; do NOT soften the scorecard to accommodate it."
    )


def test_ledger_citation_present(artifact_text):
    assert re.search(r"\bE-\d{3,}", artifact_text), (
        "Discovery Read must cite ledger entries (E-xxx, grade <=2) -- every claim traces to "
        "evidence-ledger.jsonl; presence is enforced here, per-claim density at beta."
    )


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_verdict_present, test_scorecard_present, test_scorecard_status_vocab,
                  test_two_evidence_lists, test_bias_check_present, test_ledger_citation_present):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "customer-discovery.bad.md slipped past every check -- the validator does not bite"
