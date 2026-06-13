"""Validator: ideas/<slug>/neutral-brief.md (the founder-blind pressure-test input). Spec: §8 (make_brief).

The brief is the de-identified statement the α/β panel reads INSTEAD of hypothesis.md, so the panel
judges the idea on merit. make_brief.py STRIPS the shared banned-token list; this validator FLAGS any
that survived (the second of three de-identification layers, §8). It also caps length and requires the
Problem section. Because make_brief strips the exact same list, a brief it produces passes by construction.

Every assert message is written FOR THE AGENT (schema_on_write feeds it back for self-repair).
"""
import re
from pathlib import Path

FIXTURE = "neutral-brief.sample.md"
BAD_FIXTURE = "neutral-brief.bad.md"

WORD_CAP = 250


def _banned_terms():
    f = Path(__file__).parents[1] / "fixtures" / "banned_tokens.txt"
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line)
    return out


def _body(text):
    """Everything after the closing frontmatter --- (or the whole text if none)."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return text


def test_has_problem_section(artifact_text):
    assert re.search(r"^##\s*Problem\b", artifact_text, re.M), (
        "neutral-brief.md must carry a '## Problem' section (the de-identified four dimensions)"
    )


def test_status_frontmatter(artifact_text):
    assert artifact_text.startswith("---"), "neutral-brief.md must open with a YAML frontmatter block"
    head = artifact_text.split("---", 2)[1] if artifact_text.count("---") >= 2 else ""
    assert "neutral-brief" in head, "frontmatter must mark status: neutral-brief (this is the make_brief output)"


def test_length_cap(artifact_text):
    words = len(_body(artifact_text).split())
    assert words <= WORD_CAP, (
        f"brief body is {words} words (cap {WORD_CAP}) -- tighten the hypothesis dimensions; "
        "a verbose brief leaks identity and dilutes the panel's read"
    )


def test_no_banned_tokens(artifact_text):
    low = artifact_text.lower()
    hits = [t for t in _banned_terms() if re.search(rf"\b{re.escape(t.lower())}\b", low)]
    assert not hits, (
        f"banned enthusiasm/sunk-cost token(s) survived de-identification: {hits} -- make_brief strips this "
        "list; if one is here the brief was hand-edited. Remove them (the panel must be founder-blind)"
    )


def test_red_fixture_bites():
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_has_problem_section, test_status_frontmatter, test_length_cap, test_no_banned_tokens):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "neutral-brief.bad.md slipped past every check -- the validator does not bite"
