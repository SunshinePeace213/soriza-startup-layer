#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
merge_research.py

Used at Nuwa's Phase 1.5 checkpoint. Scans the six per-agent research files
inside a skill directory, counts sources, classifies primary vs. secondary,
extracts the headline finding from each agent, and prints a clean markdown
summary that can be shown directly to the user.

Expected directory layout (created by Phase 0.5):

    <skill_dir>/
        SKILL.md
        references/
            research/
                01-writings.md
                02-conversations.md
                03-expression-dna.md
                04-external-views.md
                05-decisions.md
                06-timeline.md
            sources/...

Usage:
    uv run --script merge_research.py <skill_dir>
    uv run --script merge_research.py <skill_dir> --output summary.md
    uv run --script merge_research.py <skill_dir> --strict   # exit non-zero if any agent file is missing
    ./merge_research.py <skill_dir>                          # if executable bit set
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# The six expected agent files in the research subdirectory.
AGENT_FILES: list[tuple[str, str]] = [
    ("01-writings.md",       "1 Writings"),
    ("02-conversations.md",  "2 Conversations"),
    ("03-expression-dna.md", "3 Expression DNA"),
    ("04-external-views.md", "4 External views"),
    ("05-decisions.md",      "5 Decisions"),
    ("06-timeline.md",       "6 Timeline"),
]

# A "source" candidate is any URL or any markdown link, plus citation-style
# patterns like "(Source: ...)" or "— <Author>, <Date>".
URL_PATTERN = re.compile(r"https?://[^\s)>\]]+")
MD_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
CITATION_PATTERN = re.compile(r"\(Source:[^)]+\)|\(Per:[^)]+\)", re.IGNORECASE)

# Heuristics for classifying a source as primary vs. secondary.
# A line is treated as primary when it references the subject's own output
# (book, essay, podcast they appeared on, official channel, transcript of
# their own talk, their personal blog, etc.) and as secondary otherwise.
PRIMARY_HINTS = (
    "own ", "self-", "transcript", "his book", "her book", "their book",
    "interview with", "podcast appearance", "personal blog", "personal site",
    "newsletter", "talk at", "keynote", "ama", "twitter.com", "x.com",
    "youtube.com/watch", "youtu.be/", "speech",
)
SECONDARY_HINTS = (
    "review of", "analysis of", "biography", "biographer",
    "wikipedia", "the new york times", "tnyt", "according to", "as reported",
    "second-hand", "criticism of", "writes about", "wrote about",
)


@dataclass
class AgentSummary:
    label: str
    file: Path
    exists: bool
    line_count: int = 0
    source_count: int = 0
    primary_count: int = 0
    secondary_count: int = 0
    key_finding: str = ""
    contradictions: list[str] = field(default_factory=list)


def classify_source_line(line: str) -> str | None:
    """Return 'primary', 'secondary', or None if the line does not look like
    a source-bearing line."""
    if not (URL_PATTERN.search(line) or MD_LINK_PATTERN.search(line) or CITATION_PATTERN.search(line)):
        return None
    lower = line.lower()
    if any(hint in lower for hint in PRIMARY_HINTS):
        return "primary"
    if any(hint in lower for hint in SECONDARY_HINTS):
        return "secondary"
    # Default: a bare URL with no qualifier is treated as primary (their own
    # tweet, video, post, etc.), which is the most common case in this corpus.
    return "primary"


def first_meaningful_heading(text: str) -> str:
    """Return the first H2/H3 heading after the file's main title, or the
    first non-empty paragraph if no subheadings are present."""
    lines = [line.rstrip() for line in text.splitlines()]
    seen_title = False
    for line in lines:
        if line.startswith("# ") and not seen_title:
            seen_title = True
            continue
        if line.startswith(("## ", "### ")):
            return line.lstrip("# ").strip()
    # Fall back to the first non-empty paragraph
    for line in lines:
        if line.strip() and not line.startswith("#"):
            stripped = line.strip()
            return (stripped[:90] + "...") if len(stripped) > 90 else stripped
    return "(file is empty)"


def find_contradiction_markers(text: str) -> list[str]:
    """Pull out any lines flagged with contradiction markers. We accept a few
    conventions: lines containing 'CONTRADICTION', 'CONFLICT', or wrapped in
    a `> [!conflict]` callout."""
    markers: list[str] = []
    for line in text.splitlines():
        upper = line.upper()
        if "CONTRADICTION" in upper or "CONFLICT WITH" in upper:
            markers.append(line.strip(" >-"))
        elif line.lstrip().startswith("> [!") and "conflict" in line.lower():
            markers.append(line.lstrip(" >").strip())
    return markers


def summarize_agent_file(path: Path, label: str) -> AgentSummary:
    if not path.is_file():
        return AgentSummary(label=label, file=path, exists=False)

    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    primary = secondary = 0
    for line in lines:
        kind = classify_source_line(line)
        if kind == "primary":
            primary += 1
        elif kind == "secondary":
            secondary += 1

    return AgentSummary(
        label=label,
        file=path,
        exists=True,
        line_count=len(lines),
        source_count=primary + secondary,
        primary_count=primary,
        secondary_count=secondary,
        key_finding=first_meaningful_heading(text),
        contradictions=find_contradiction_markers(text),
    )


def truncate_for_table(text: str, max_len: int) -> str:
    """Truncate text to fit in a markdown table cell without breaking the table."""
    text = text.replace("|", "\\|").replace("\n", " ")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def build_markdown_summary(summaries: list[AgentSummary]) -> str:
    lines: list[str] = []
    lines.append("# Phase 1.5 — Research Quality Checkpoint\n")
    lines.append(
        "Review the table below. If a dimension looks under-researched, "
        "re-run that one agent before moving to Phase 2.\n"
    )
    lines.append("| Agent | Sources | Primary / Secondary | Key Finding |")
    lines.append("|-------|---------|---------------------|-------------|")

    total_sources = 0
    total_primary = 0
    total_secondary = 0
    all_contradictions: list[tuple[str, str]] = []
    missing: list[str] = []

    for s in summaries:
        if not s.exists:
            lines.append(f"| {s.label} | — | — | ⚠️ file missing: `{s.file.name}` |")
            missing.append(s.label)
            continue
        total_sources += s.source_count
        total_primary += s.primary_count
        total_secondary += s.secondary_count
        for c in s.contradictions:
            all_contradictions.append((s.label, c))
        ratio = f"{s.primary_count} / {s.secondary_count}"
        lines.append(
            f"| {s.label} | {s.source_count} | {ratio} | {truncate_for_table(s.key_finding, 60)} |"
        )

    # Totals row
    if total_sources:
        pct_primary = (total_primary / total_sources) * 100
        lines.append(
            f"| **Total** | **{total_sources}** | "
            f"**{total_primary} / {total_secondary}** "
            f"(**{pct_primary:.0f}%** primary) | |"
        )

    # Contradictions and missing files
    lines.append("")
    if all_contradictions:
        lines.append("## Contradictions Found")
        for label, text in all_contradictions:
            lines.append(f"- ({label}) {text}")
        lines.append("")
    else:
        lines.append("## Contradictions Found\n\n_None recorded._\n")

    if missing:
        lines.append("## Missing Files\n")
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")

    # Quality call-outs
    lines.append("## Quality Signals")
    if total_sources < 10:
        lines.append(
            "- ⚠️  **Low source count (<10).** Recommend lowering expectations: "
            "target 2–3 mental models max, and expand the Honest Limits section."
        )
    elif total_sources < 25:
        lines.append("- ℹ️  Moderate source count. Standard 3–5 mental models is realistic.")
    else:
        lines.append("- ✅ Healthy source count. Full 3–7 mental models is supportable.")

    if total_sources:
        primary_ratio = total_primary / total_sources
        if primary_ratio < 0.5:
            lines.append(
                f"- ⚠️  **Primary-source ratio is {primary_ratio*100:.0f}%** (target >50%). "
                "Add more first-hand material before moving on."
            )
        else:
            lines.append(f"- ✅ Primary-source ratio {primary_ratio*100:.0f}% meets the >50% target.")

    if all_contradictions:
        lines.append(
            f"- ✅ Found {len(all_contradictions)} contradiction marker(s) — "
            "these are signal, not noise. Preserve them through Phase 2."
        )
    else:
        lines.append(
            "- ℹ️  No contradictions flagged. Worth double-checking that none "
            "were silently smoothed over in the per-agent files."
        )

    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build the Phase 1.5 research-quality summary.")
    parser.add_argument("skill_dir", help="Path to the perspective-skill directory.")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write the summary to this file as well as stdout.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero status if any of the six agent files is missing.",
    )
    args = parser.parse_args(argv)

    skill_dir = Path(args.skill_dir).resolve()
    research_dir = skill_dir / "references" / "research"
    if not research_dir.is_dir():
        print(f"ERROR: research directory not found: {research_dir}", file=sys.stderr)
        return 2

    summaries = [
        summarize_agent_file(research_dir / fname, label)
        for fname, label in AGENT_FILES
    ]

    summary_md = build_markdown_summary(summaries)
    print(summary_md)

    if args.output:
        Path(args.output).write_text(summary_md, encoding="utf-8")
        print(f"(also written to {args.output})", file=sys.stderr)

    if args.strict and any(not s.exists for s in summaries):
        print("FAIL: --strict was set and one or more agent files are missing.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
