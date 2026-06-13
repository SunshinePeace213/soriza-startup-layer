"""Validator: ideas/<slug>/customer-discovery/interviews/<date>-<prospect>.md.

Interview notes are HUMAN-AUTHORED -- the founder writes them. This validator is
DELIBERATELY PERMISSIVE: it runs on PostToolUse(Write) and must NOT bounce a founder's
legitimate raw note (Rule Zero: evidence wins; never obstruct real interview capture). It
catches ONLY genuinely-broken/placeholder files (empty stubs, no date, no heading) -- never
a messy-but-real note. Do not add structural requirements here.

Every assert message is written FOR THE AGENT: the schema_on_write hook feeds it back
verbatim, so it must say what *right* looks like.
"""
import re
from pathlib import Path

FIXTURE = "interview.sample.md"
BAD_FIXTURE = "interview.bad.md"


def test_substantive(artifact_text):
    assert len(artifact_text.strip()) >= 200, (
        "Interview note looks like an empty stub (<200 chars). A real note is expected here: "
        "what the prospect actually did, in their words -- past behaviour and verbatim quotes, "
        "not a placeholder. Messy is fine; empty is not."
    )


def test_has_date(artifact_text):
    assert re.search(r"\b\d{4}-\d{2}-\d{2}\b", artifact_text), (
        "Interview note needs an ISO date (YYYY-MM-DD) for provenance -- when the interview "
        "happened. The file convention is interviews/<date>-<prospect>.md; put the date in the note."
    )


def test_has_prospect_heading(artifact_text):
    assert re.search(r"^#", artifact_text, re.M), (
        "Interview note needs at least one markdown heading (a line starting with '#') -- a "
        "who/title for the note, e.g. '# Interview -- <role>, <company>'."
    )


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_substantive, test_has_date, test_has_prospect_heading):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "interview.bad.md slipped past every check -- the validator does not bite"
