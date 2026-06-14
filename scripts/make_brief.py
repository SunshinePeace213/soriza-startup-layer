#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""make_brief.py -- T10. hypothesis.md -> neutral-brief.md (the founder-blind pressure-test input).

Spec: pressure-test α (step 4) -- see .claude/skills/idea-stage/references/stage-pipeline.md. Produces the de-identified brief that
the pressure-test α panel (objection-lens / competitor-steelman) reads INSTEAD of hypothesis.md, so
the panel judges the idea on its merits and can't be swayed by the founder's identity or enthusiasm.

Source of truth = the hypothesis FRONTMATTER (who / how_often / how_severe / status_quo +
value_hypothesis / growth_hypothesis). Those fields are template-guaranteed concise declaratives
(.claude/skills/sharpen-hypothesis/assets/hypothesis-template.md); the verbose body carries the
founder's meta-commentary and identity cues, which we deliberately drop.

De-identification is MECHANICAL and deliberately imperfect -- it is the first of three layers:
  1. this script (strip founder name + brand + first-person + banned tokens),
  2. the test_neutral_brief validator (gates banned tokens + length -- hook #2, ships later),
  3. the persona's Appendix C ("ignore residual identity cues").

Usage: uv run scripts/make_brief.py --slug <slug>
"""
import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

HKT = timezone(timedelta(hours=8))
WORD_CAP = 250

REQUIRED = ["who", "how_often", "how_severe", "status_quo"]          # the four dimensions
OPTIONAL = ["value_hypothesis", "growth_hypothesis"]                 # the idea's thesis
LABELS = {"who": "Who", "how_often": "How often", "how_severe": "How severe",
          "status_quo": "Status quo", "value_hypothesis": "Value", "growth_hypothesis": "Growth"}

# first-person -> neutral third-person (whole-word, case-insensitive). The frontmatter is normally
# third-person already, so this is defence-in-depth for a field that slips into founder voice.
FIRST_PERSON = {"we": "the team", "our": "the team's", "ours": "the team's", "us": "the team",
                "i": "the founder", "my": "the founder's", "mine": "the founder's", "me": "the founder"}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def now_iso() -> str:
    s = datetime.now(HKT).strftime("%Y-%m-%dT%H:%M%z")
    return s[:-2] + ":" + s[-2:]


def fail(msg: str) -> None:
    sys.exit(f"[make_brief] {msg}")


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        fail(f"{path} has no leading YAML frontmatter block")
    fm = yaml.safe_load(parts[1]) or {}
    if not isinstance(fm, dict):
        fail(f"{path} frontmatter is not a mapping")
    missing = [k for k in REQUIRED if not str(fm.get(k, "")).strip()]
    if missing:
        fail(f"{path} frontmatter is missing required dimension(s): {', '.join(missing)} "
             f"-- run /sharpen-hypothesis to complete it before pressure-test")
    return fm


def founder_terms(root: Path) -> list[str]:
    """Identity strings to strip: the founder's full name + each name token (len >= 3)."""
    prof = root / "docs" / "founder-profile.md"
    if not prof.exists():
        return []
    m = re.match(r"#\s*Founder Profile:\s*(.+)", prof.read_text(encoding="utf-8").splitlines()[0])
    if not m:
        return []
    name = m.group(1).strip()
    terms = {name} | {tok for tok in name.split() if len(tok) >= 3}
    return sorted(terms, key=len, reverse=True)   # longest first so "Ringo Ma" strips before "Ringo"


def brand_terms(slug: str) -> list[str]:
    """The brand is the slug's leading segment (e.g. soriza-... -> Soriza), if it's not a short code."""
    head = slug.split("-")[0]
    return [head] if len(head) >= 3 else []


def load_banned(root: Path) -> list[str]:
    f = root / "tests" / "fixtures" / "banned_tokens.txt"
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line)
    return sorted(out, key=len, reverse=True)     # multi-word phrases before their substrings


def replace_word(text: str, term: str, repl: str) -> str:
    return re.sub(rf"\b{re.escape(term)}\b", repl, text, flags=re.IGNORECASE)


def tidy(text: str) -> str:
    text = re.sub(r"\(\s*\)", "", text)           # empty parens left by a removed token
    text = re.sub(r"\s+([,.;:)])", r"\1", text)   # space before punctuation
    text = re.sub(r"\s{2,}", " ", text)           # collapsed whitespace from removals
    return text.strip(" -—")


def deidentify(text: str, identity: list[str], banned: list[str]) -> str:
    for term in identity:
        text = replace_word(text, term, "the founder" if " " in term or term.istitle() else "the venture")
    for term in banned:
        text = replace_word(text, term, "")
    for pron, repl in FIRST_PERSON.items():
        text = replace_word(text, pron, repl)
    return tidy(text)


def build_brief(slug: str, fm: dict, root: Path) -> tuple[str, int]:
    identity = founder_terms(root) + brand_terms(slug)
    banned = load_banned(root)
    fields = {k: deidentify(str(fm[k]), identity, banned) for k in REQUIRED + OPTIONAL if fm.get(k)}
    words = sum(len(v.split()) for v in fields.values())

    problem = "\n".join(f"- **{LABELS[k]}:** {fields[k]}" for k in REQUIRED if k in fields)
    thesis = "\n".join(f"- **{LABELS[k]}:** {fields[k]}" for k in OPTIONAL if k in fields)
    # The slug embeds the brand (soriza-...), so it is kept OUT of the brief content; the file's
    # path under ideas/<slug>/ provides machine linkage, and the persona's Appendix C covers that
    # residual cue. "Candidate" is the panel's own word for the idea under review.
    body = [
        "---", "stage: make_brief", "status: neutral-brief",
        "source: hypothesis.md", f"words: {words}", f"generated: {now_iso()}", "---", "",
        "# Neutral Brief — Candidate", "",
        "De-identified statement of the idea for the founder-blind pressure-test panel. Mechanical "
        "de-identification only — ignore any residual identity cues.", "",
        "## Problem", problem,
    ]
    if thesis:
        body += ["", "## Idea thesis", thesis]
    return "\n".join(body) + "\n", words


def main() -> None:
    ap = argparse.ArgumentParser(description="hypothesis.md -> de-identified neutral-brief.md")
    ap.add_argument("--slug", required=True)
    args = ap.parse_args()

    root = repo_root()
    idea = root / "ideas" / args.slug
    hyp = idea / "hypothesis.md"
    if not hyp.exists():
        fail(f"no hypothesis at {hyp} -- run /sharpen-hypothesis first")

    fm = load_frontmatter(hyp)
    brief, words = build_brief(args.slug, fm, root)
    out = idea / "neutral-brief.md"
    out.write_text(brief, encoding="utf-8")

    note = f"  (>{WORD_CAP}-word cap -- tighten the hypothesis fields)" if words > WORD_CAP else ""
    print(f"[make_brief] wrote {out.relative_to(root)} -- {words} words{note}")
    if words > WORD_CAP:
        print(f"[make_brief] WARNING: brief is {words} words (cap {WORD_CAP}); "
              f"the neutral-brief validator will reject it -- tighten hypothesis.md", file=sys.stderr)


main()
