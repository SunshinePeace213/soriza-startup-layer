#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
srt_to_transcript.py

Convert a .srt (or .vtt) subtitle file into a clean, readable transcript.

The cleaning pipeline removes:
  * Cue numbers (the integer-only lines that index each block)
  * Timestamp lines like "00:01:23,456 --> 00:01:25,789"
  * VTT/WEBVTT headers and STYLE / NOTE blocks
  * HTML tags like <i>, <c.color>, <00:00:01.000>
  * Repeated lines (auto-generated subtitles often duplicate every cue twice)
  * Lines that are pure whitespace
  * "[Music]", "[Applause]" and similar bracketed sound tags (optional via flag)

The output is one paragraph per natural pause, suitable for archival under
references/sources/transcripts/ in a Nuwa perspective skill.

Usage:
    uv run --script srt_to_transcript.py <input.srt> [output.txt]
    uv run --script srt_to_transcript.py <input.srt> [output.txt] --keep-tags
    ./srt_to_transcript.py <input.srt> [output.txt]            # if executable bit set

If output is omitted, the result is written next to the input file with a
.txt extension.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------- Regex patterns ----------

# Matches "00:01:23,456 --> 00:01:25,789" or VTT "00:01:23.456 --> 00:01:25.789"
TIMESTAMP_LINE = re.compile(
    r"^\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,.]\d{3}.*$"
)

# A cue index: a line that is nothing but an integer
CUE_INDEX_LINE = re.compile(r"^\s*\d+\s*$")

# Any HTML-like tag, e.g. <i>, </i>, <c.colorE5E5E5>, <00:00:01.000>
HTML_TAG = re.compile(r"<[^>]+>")

# Inline timestamps inside auto-generated VTT: "<c><00:00:01.000><c>"
INLINE_TIMESTAMP = re.compile(r"<\d{2}:\d{2}:\d{2}[.,]\d{3}>")

# Bracketed sound tags: "[Music]", "[Applause]", "[laughter]"
SOUND_TAG = re.compile(r"\[[^\]]+\]")

# VTT structural lines to drop entirely
VTT_STRUCTURAL = re.compile(r"^\s*(WEBVTT|NOTE|STYLE|REGION|Kind:|Language:).*$", re.IGNORECASE)


def clean_lines(raw_text: str, drop_sound_tags: bool = True) -> list[str]:
    """Apply the cleaning pipeline to the raw subtitle text and return a list
    of cleaned, content-bearing lines (still possibly with duplicates)."""
    cleaned: list[str] = []
    for line in raw_text.splitlines():
        stripped = line.strip()

        # Drop empty lines (we'll re-introduce paragraph breaks later)
        if not stripped:
            continue

        # Drop VTT headers and metadata
        if VTT_STRUCTURAL.match(stripped):
            continue

        # Drop standalone cue index numbers
        if CUE_INDEX_LINE.match(stripped):
            continue

        # Drop timestamp lines
        if TIMESTAMP_LINE.match(stripped):
            continue

        # Strip inline timestamps and HTML tags from within the text
        text = INLINE_TIMESTAMP.sub("", stripped)
        text = HTML_TAG.sub("", text)

        # Optionally remove bracketed sound-effect tags
        if drop_sound_tags:
            text = SOUND_TAG.sub("", text)

        text = text.strip()
        if text:
            cleaned.append(text)
    return cleaned


def deduplicate_consecutive(lines: list[str]) -> list[str]:
    """Auto-generated YouTube subtitles often repeat every line as the cue
    rolls forward. Collapse consecutive duplicates and substring-overlap
    duplicates where one line is a strict prefix/suffix of the next."""
    if not lines:
        return []

    result: list[str] = [lines[0]]
    for current in lines[1:]:
        previous = result[-1]
        if current == previous:
            continue
        # Overlap case: "hello world" followed by "hello world today"
        # — keep only the longer one
        if current.startswith(previous):
            result[-1] = current
            continue
        if previous.endswith(current):
            continue
        result.append(current)
    return result


def reflow_paragraphs(lines: list[str], target_sentence_chars: int = 240) -> str:
    """Join short subtitle lines into readable paragraphs.

    Heuristic: append lines into a running paragraph; start a new paragraph
    when (a) the previous line ends with sentence punctuation AND the running
    paragraph is already over `target_sentence_chars`, or (b) the previous
    line ends with a hard sentence-ending mark (. ! ? . ! ?).
    """
    sentence_end_chars = set(".!?\u3002\uff01\uff1f")  # incl. full-width zh/jp
    paragraphs: list[str] = []
    buffer: list[str] = []
    buffer_len = 0
    for line in lines:
        buffer.append(line)
        buffer_len += len(line) + 1
        if line and line[-1] in sentence_end_chars and buffer_len >= target_sentence_chars:
            paragraphs.append(" ".join(buffer))
            buffer = []
            buffer_len = 0
    if buffer:
        paragraphs.append(" ".join(buffer))
    return "\n\n".join(paragraphs)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Convert an .srt or .vtt subtitle file to a clean transcript."
    )
    parser.add_argument("input", help="Path to the input .srt or .vtt file.")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Path to the output .txt file. Defaults to input filename with .txt extension.",
    )
    parser.add_argument(
        "--keep-tags",
        action="store_true",
        help="Keep bracketed sound tags like [Music], [Applause].",
    )
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.is_file():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else input_path.with_suffix(".txt")

    raw_text = input_path.read_text(encoding="utf-8", errors="replace")
    cleaned = clean_lines(raw_text, drop_sound_tags=not args.keep_tags)
    deduped = deduplicate_consecutive(cleaned)
    transcript = reflow_paragraphs(deduped)

    output_path.write_text(transcript + "\n", encoding="utf-8")

    print(f"Cleaned transcript written to: {output_path}")
    print(f"  Raw lines:        {len(raw_text.splitlines())}")
    print(f"  Content lines:    {len(cleaned)}")
    print(f"  After de-dup:     {len(deduped)}")
    print(f"  Paragraphs:       {transcript.count(chr(10)+chr(10)) + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
