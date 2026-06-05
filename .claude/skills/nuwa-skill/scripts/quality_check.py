#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
quality_check.py

Used at Nuwa's Phase 4 quality-validation step. Reads a generated SKILL.md
file and checks it against the six pass criteria from extraction-framework.md
section 6, plus a seventh skill-listing-budget check. Prints a PASS / FAIL line
for each criterion and a final summary.

The checks (1–6 mirror extraction-framework.md; 7 guards the listing budget):

  1. Mental-model count is between 3 and 7 inclusive.
  2. Every mental model has an explicit "limits" / "where it fails" subsection.
  3. The Expression DNA section exists and lists multiple distinctive
     dimensions (sentence structure, vocabulary, certainty register, etc.).
  4. The Honest Limits section contains at least 3 specific bullet points,
     not just the generic "I am not the real person" boilerplate.
  5. The Values / Anti-patterns section names at least 2 internal tensions
     or contradiction pairs.
  6. The Research Sources section shows a primary-source ratio above 50%.
  7. The frontmatter description is a tight routing card (≤ ~300 chars; hard
     cap 1,536 for description+when_to_use) — not a bio paragraph.

Exit codes:
   0  All checks pass.
   1  At least one check failed.
   2  Could not read the SKILL.md file.

Usage:
    uv run --script quality_check.py <path/to/SKILL.md>
    uv run --script quality_check.py <path/to/SKILL.md> --json    # machine-readable output
    ./quality_check.py <path/to/SKILL.md>                         # if executable bit set
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

# ---------- Heading helpers ----------

# Regex for "## Heading" up to "## NextHeading". Captures the body of a
# named section.
SECTION_PATTERN_TEMPLATE = r"(?ms)^##\s+{0}.*?(?=^##\s+|\Z)"

MENTAL_MODEL_KEYWORDS = ("Mental Models", "Mental Model", "Core Mental Models")
DECISION_KEYWORDS = ("Decision Heuristics", "How I Decide")
DNA_KEYWORDS = ("Expression DNA", "How I Talk", "How I Speak")
HONEST_LIMITS_KEYWORDS = ("Honest Limits", "What This Skill Can't Do", "Limits", "Honest Boundaries")
VALUES_KEYWORDS = ("Values and Anti-Patterns", "Values & Anti-Patterns", "What I Stand For", "Values")
SOURCES_KEYWORDS = ("Research Sources", "Sources", "Where I Came From")

# ---------- Result type ----------

@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


def find_section(markdown: str, keyword_options: tuple[str, ...]) -> str | None:
    """Return the body of the first H2 section matching any of the keywords."""
    for kw in keyword_options:
        pattern = SECTION_PATTERN_TEMPLATE.format(re.escape(kw))
        m = re.search(pattern, markdown)
        if m:
            return m.group(0)
    return None


# ---------- Individual checks ----------

def check_mental_model_count(markdown: str) -> CheckResult:
    section = find_section(markdown, MENTAL_MODEL_KEYWORDS)
    if not section:
        return CheckResult(
            "1. Mental-model count is 3–7",
            False,
            "FAIL — no 'Mental Models' section found.",
        )
    # Count H3 subheadings within the section.
    h3_matches = re.findall(r"(?m)^###\s+", section)
    count = len(h3_matches)
    if 3 <= count <= 7:
        return CheckResult(
            "1. Mental-model count is 3–7",
            True,
            f"PASS — found {count} models.",
        )
    return CheckResult(
        "1. Mental-model count is 3–7",
        False,
        f"FAIL — found {count} models (need 3–7).",
    )


def check_mental_model_limits(markdown: str) -> CheckResult:
    section = find_section(markdown, MENTAL_MODEL_KEYWORDS)
    if not section:
        return CheckResult(
            "2. Every mental model has explicit limits",
            False,
            "FAIL — no 'Mental Models' section to inspect.",
        )
    # Split the section into model blocks at each ### heading.
    model_blocks = re.split(r"(?m)^###\s+.*$", section)[1:]
    if not model_blocks:
        return CheckResult(
            "2. Every mental model has explicit limits",
            False,
            "FAIL — section exists but contains no model subsections.",
        )
    limit_marker = re.compile(
        r"(where it fails|limits?|limitations?|fails when|breaks down|blind spot|"
        r"when this model misleads|where this lens misleads)",
        re.IGNORECASE,
    )
    missing: list[int] = []
    for i, block in enumerate(model_blocks, start=1):
        if not limit_marker.search(block):
            missing.append(i)
    if not missing:
        return CheckResult(
            "2. Every mental model has explicit limits",
            True,
            f"PASS — all {len(model_blocks)} models declare limits.",
        )
    return CheckResult(
        "2. Every mental model has explicit limits",
        False,
        f"FAIL — {len(missing)}/{len(model_blocks)} models missing a limits subsection "
        f"(model numbers: {missing}).",
    )


def check_expression_dna(markdown: str) -> CheckResult:
    section = find_section(markdown, DNA_KEYWORDS)
    if not section:
        return CheckResult(
            "3. Expression DNA section is present and detailed",
            False,
            "FAIL — no 'Expression DNA' section found.",
        )
    expected_axes = (
        "sentence", "vocabulary", "humor", "certainty", "analogy", "register",
    )
    body_lower = section.lower()
    hits = sum(1 for axis in expected_axes if axis in body_lower)
    if hits >= 4:
        return CheckResult(
            "3. Expression DNA section is present and detailed",
            True,
            f"PASS — covers {hits} of {len(expected_axes)} expected axes.",
        )
    return CheckResult(
        "3. Expression DNA section is present and detailed",
        False,
        f"FAIL — covers only {hits} of {len(expected_axes)} expected axes "
        "(need at least 4: sentence, vocabulary, humor, certainty, analogy, register).",
    )


def check_honest_limits(markdown: str) -> CheckResult:
    section = find_section(markdown, HONEST_LIMITS_KEYWORDS)
    if not section:
        return CheckResult(
            "4. Honest limits has ≥3 specific bullets",
            False,
            "FAIL — no 'Honest Limits' section found.",
        )
    bullets = re.findall(r"(?m)^[-*+]\s+.+$", section)
    # Strip the boilerplate "I cannot replace the real person" entries
    boilerplate = re.compile(
        r"(cannot replace|cannot substitute|am not the real|am a snapshot|am only a model)",
        re.IGNORECASE,
    )
    specific = [b for b in bullets if not boilerplate.search(b)]
    if len(bullets) >= 3 and len(specific) >= 2:
        return CheckResult(
            "4. Honest limits has ≥3 specific bullets",
            True,
            f"PASS — {len(bullets)} bullets total, {len(specific)} beyond boilerplate.",
        )
    return CheckResult(
        "4. Honest limits has ≥3 specific bullets",
        False,
        f"FAIL — {len(bullets)} bullets total, only {len(specific)} go beyond boilerplate "
        "(need ≥3 total and ≥2 beyond boilerplate).",
    )


def check_internal_tensions(markdown: str) -> CheckResult:
    section = find_section(markdown, VALUES_KEYWORDS)
    if not section:
        return CheckResult(
            "5. Values section names ≥2 internal tensions",
            False,
            "FAIL — no 'Values' section found.",
        )
    # Look for a subsection on tensions and count bullets within it, OR
    # count "pulls against" / "tension between" / "X vs Y" lines anywhere.
    tension_sub = re.search(
        r"(?ms)(?:^###?\s+.*tension.*$|^.*Internal tensions.*$).*?(?=^##\s+|^###\s+|\Z)",
        section,
        re.IGNORECASE,
    )
    if tension_sub:
        bullets = re.findall(r"(?m)^[-*+]\s+.+$", tension_sub.group(0))
        if len(bullets) >= 2:
            return CheckResult(
                "5. Values section names ≥2 internal tensions",
                True,
                f"PASS — tension subsection lists {len(bullets)} pairs.",
            )
    tension_marker = re.compile(
        r"(pulls? against|tension between|in tension with|contradict)",
        re.IGNORECASE,
    )
    tension_lines = [
        line for line in section.splitlines() if tension_marker.search(line)
    ]
    if len(tension_lines) >= 2:
        return CheckResult(
            "5. Values section names ≥2 internal tensions",
            True,
            f"PASS — found {len(tension_lines)} tension statements.",
        )
    return CheckResult(
        "5. Values section names ≥2 internal tensions",
        False,
        f"FAIL — found only {len(tension_lines)} tension statements (need ≥2).",
    )


def check_primary_source_ratio(markdown: str) -> CheckResult:
    section = find_section(markdown, SOURCES_KEYWORDS)
    if not section:
        return CheckResult(
            "6. Primary-source ratio is >50%",
            False,
            "FAIL — no 'Research Sources' section found.",
        )
    primary_sub = re.search(
        r"(?ms)\*\*Primary[^*]*\*\*.*?(?=\*\*(?:Secondary|Local)|^---|\Z)",
        section,
    )
    secondary_sub = re.search(
        r"(?ms)\*\*Secondary[^*]*\*\*.*?(?=\*\*(?:Primary|Local)|^---|\Z)",
        section,
    )
    primary_count = (
        len(re.findall(r"(?m)^[-*+]\s+.+$", primary_sub.group(0))) if primary_sub else 0
    )
    secondary_count = (
        len(re.findall(r"(?m)^[-*+]\s+.+$", secondary_sub.group(0))) if secondary_sub else 0
    )
    total = primary_count + secondary_count
    if total == 0:
        return CheckResult(
            "6. Primary-source ratio is >50%",
            False,
            "FAIL — no sources enumerated. Add Primary / Secondary subsections with bullets.",
        )
    ratio = primary_count / total
    if ratio > 0.5:
        return CheckResult(
            "6. Primary-source ratio is >50%",
            True,
            f"PASS — {primary_count}/{total} ({ratio*100:.0f}%) sources are primary.",
        )
    return CheckResult(
        "6. Primary-source ratio is >50%",
        False,
        f"FAIL — only {primary_count}/{total} ({ratio*100:.0f}%) sources are primary (need >50%).",
    )


_FM_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _frontmatter_field(markdown: str, key: str) -> str | None:
    """Extract a scalar frontmatter field (inline or block scalar), no YAML dep."""
    m = _FM_RE.match(markdown)
    if not m:
        return None
    lines = m.group(1).split("\n")
    for i, ln in enumerate(lines):
        km = re.match(rf"^{re.escape(key)}:\s*(.*)$", ln)
        if not km:
            continue
        rest = km.group(1).strip()
        if rest in ("|", ">", "|-", ">-", "|+", ">+", ""):
            buf = []
            for nl in lines[i + 1:]:
                if nl[:1].isspace() or nl.strip() == "":
                    buf.append(nl.strip())
                else:
                    break
            return " ".join(x for x in buf if x).strip()
        if len(rest) >= 2 and rest[0] in "\"'" and rest[-1] == rest[0]:
            rest = rest[1:-1]
        return rest
    return None


def check_description_budget(markdown: str) -> CheckResult:
    """A perspective skill's description is a routing card, not a bio. It sits in
    the skill listing of EVERY session under a global ~1% budget; long ones evict
    other skills. Keep it tight."""
    name = "7. Description is a tight routing card (≤ ~300 chars)"
    desc = _frontmatter_field(markdown, "description")
    wtu = _frontmatter_field(markdown, "when_to_use")
    if not desc:
        return CheckResult(name, False, "FAIL — no frontmatter description found.")
    combined = len(desc) + (1 + len(wtu) if wtu else 0)
    if combined > 1536:
        return CheckResult(name, False,
            f"FAIL — description+when_to_use is {combined} chars, over the 1,536 per-entry "
            "listing cap (it will be truncated). Cut to a tight routing card; move bio to the Identity Card.")
    if combined > 500:
        return CheckResult(name, False,
            f"FAIL — description+when_to_use is {combined} chars. Target ≤ ~300 for a perspective "
            "skill: 'Think like X — <identity>. Use for X's lens. Triggers — …'. No bio in the description.")
    return CheckResult(name, True, f"PASS — {combined} chars (lean routing card).")


# ---------- Orchestrator ----------

ALL_CHECKS = (
    check_mental_model_count,
    check_mental_model_limits,
    check_expression_dna,
    check_honest_limits,
    check_internal_tensions,
    check_primary_source_ratio,
    check_description_budget,
)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate a Nuwa-generated SKILL.md against Phase 4 criteria.")
    parser.add_argument("skill_md", help="Path to the SKILL.md file to check.")
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON instead of text."
    )
    args = parser.parse_args(argv)

    path = Path(args.skill_md)
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    markdown = path.read_text(encoding="utf-8", errors="replace")
    results = [check(markdown) for check in ALL_CHECKS]
    passed = sum(1 for r in results if r.passed)
    total = len(results)

    if args.json:
        print(json.dumps(
            {
                "file": str(path),
                "passed_count": passed,
                "total": total,
                "all_passed": passed == total,
                "results": [asdict(r) for r in results],
            },
            indent=2,
        ))
    else:
        print(f"\nQuality check for: {path}")
        print("=" * 72)
        for r in results:
            marker = "✅" if r.passed else "❌"
            print(f"  {marker}  {r.name}")
            print(f"        {r.detail}")
        print("-" * 72)
        if passed == total:
            print(f"  RESULT: all {total} checks PASSED. Ready for human Voice Test (Phase 4.3).")
        else:
            print(f"  RESULT: {passed}/{total} checks passed. Fix the items above and re-run.")
        print("=" * 72)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
