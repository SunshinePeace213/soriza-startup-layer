#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Assemble the validation delta ledger for /startup-brief Step 8 (the merged solution-design step).

The "validated problem" is NOT just customer-discovery.md. Every upstream step emits a
"Hypothesis Updates Flagged" block, and only /sharpen-hypothesis folds those back into
hypothesis.md — so mid-pipeline hypothesis.md is usually stale. This script scans the idea's
9-step upstream docs and prints every flagged delta + the Discovery Read verdict + the
TRIPPED/CLEARED criteria + any override stamp, VERBATIM, so none is silently dropped before the
drift audit reasons over them (mirrors /customer-discovery's score_criteria.py: the bookkeeping
is mechanical so it can't be soft-pedaled by eye). The drift audit then measures the concept
against the reconstructed baseline (hypothesis + these deltas), never the stale file.

UPSTREAM DOCS (9-step canon): kill-scan.md (3), pressure-report-alpha.md (4), customer-discovery.md
(5), pressure-report-beta.md (6), market-sizing.md (7). The Discovery Read verdict lives in
customer-discovery.md; the β report carries the go/pivot/kill recommendation but the binding kill
decision is the founder's G6 signature (a tripped-then-overridden criterion shows up as an override
stamp). Any of these docs may carry a "Hypothesis Updates Flagged" block.

APPEND-ROUND SEMANTICS: customer-discovery.md is an append-round doc — synthesis rounds are
appended as `## Discovery Read — Round <N>`, latest last. The BINDING verdict is the LATEST round
(highest Round N / last in the file), not the first. All rounds are reported in discovery_read_rounds.

This script LOCATES and quotes; it does not interpret. The reconstruction and the
assumed->validated judgment are the model's, downstream from this output.

Usage:
  python3 build_delta_ledger.py <idea_dir>            # e.g. ideas/hk-broker-recon
  python3 build_delta_ledger.py <idea_dir> --docs a.md b.md

Prints a JSON object to stdout. Exit codes: 0 = clean (even if some docs absent); 2 = bad idea_dir.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_DOCS = ["kill-scan.md", "pressure-report-alpha.md", "customer-discovery.md",
                "pressure-report-beta.md", "market-sizing.md"]
# Compound verdict first so it isn't shadowed; final selection is by position, not list order.
VERDICTS = ["KEEP-DISCOVERING", "CONTINUE", "PIVOT", "KILL"]
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
DELTA_RE = re.compile(r"hypothesis\s+update", re.I)
DISCOVERY_READ_RE = re.compile(r"discovery\s+read", re.I)
ROUND_RE = re.compile(r"round\s+(\d+)", re.I)
OVERRIDE_RE = re.compile(r"Override:.*\d{4}-\d{2}-\d{2}")


def _headings(lines):
    """List of (line_index, level, title) for every markdown heading."""
    out = []
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip()))
    return out


def _section_block(lines, headings, start_idx):
    """Verbatim block from headings[start_idx] until the next heading of level <= its own."""
    h_i, h_level, _ = headings[start_idx]
    end = len(lines)
    for j in range(start_idx + 1, len(headings)):
        nj_i, nj_level, _ = headings[j]
        if nj_level <= h_level:
            end = nj_i
            break
    return "\n".join(lines[h_i:end]).strip()


def _first_verdict(block):
    """The verdict token appearing earliest in the block (by position, not list order)."""
    best = None
    for v in VERDICTS:
        m = re.search(r"\b" + re.escape(v) + r"\b", block)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), v)
    return best[1] if best else None


def scan_doc_deltas(name, lines, headings):
    """Verbatim 'Hypothesis Updates Flagged' blocks + a warning if none parse cleanly."""
    deltas = []
    for idx, (_, _, title) in enumerate(headings):
        if DELTA_RE.search(title):
            deltas.append({"source": name, "header": title,
                           "text": _section_block(lines, headings, idx)})
    warning = None
    if not deltas:
        titles = [t for (_, _, t) in headings]
        # Raw fallback: catch a malformed (e.g. no-space '###Hypothesis Updates') heading the
        # CommonMark heading regex misses, so a fat-fingered delta still surfaces for manual review.
        raw_hits = [f"L{i + 1}: {ln.strip()}" for i, ln in enumerate(lines) if DELTA_RE.search(ln)]
        warning = (f"{name}: no 'Hypothesis Updates Flagged' heading parsed — check these sections "
                   f"by hand: {titles}")
        if raw_hits:
            warning += f"; RAW 'hypothesis update' lines to inspect: {raw_hits}"
    return deltas, warning


def discovery_read_rounds(lines, headings):
    """Every Discovery Read section, with its parsed round number and verdict (file order)."""
    rounds = []
    for idx, (li, _, title) in enumerate(headings):
        if DISCOVERY_READ_RE.search(title):
            m = ROUND_RE.search(title)
            rounds.append({
                "round": int(m.group(1)) if m else None,
                "heading": title,
                "line": li + 1,
                "verdict": _first_verdict(_section_block(lines, headings, idx)),
            })
    return rounds


def select_latest_round(rounds):
    """Latest = highest Round N; ties / no number -> last in file (append-round puts latest last)."""
    if not rounds:
        return None
    return max(rounds, key=lambda r: (r["round"] if r["round"] is not None else -1, r["line"]))


def _clean_cell(c):
    return c.strip().strip("*` ").strip()


def parse_status_tables(lines):
    """Read the Kill-Criteria Scorecard by COLUMN: find a table whose header has a 'Status' column,
    then classify each data row by its Status cell value (exact match). Scoped + exact so a CLEARED
    row whose prose mentions 'TRIPPED', a legend cell, or an unrelated table can't leak in.
    Rows whose Status is neither TRIPPED nor CLEARED (INCONCLUSIVE / MANUAL / ERROR / …) are
    captured in `unsettled` as {criterion, status} — so a criterion still unsettled at the latest
    round surfaces in the ledger instead of being silently dropped."""
    tripped, cleared, unsettled = [], [], []
    n = len(lines)
    i = 0
    while i < n:
        s = lines[i].strip()
        if s.startswith("|"):
            header = [_clean_cell(c) for c in s.strip("|").split("|")]
            status_idx = next((idx for idx, h in enumerate(header) if h.lower() == "status"), None)
            if status_idx is not None:
                j = i + 1
                while j < n and lines[j].strip().startswith("|"):
                    row = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                    is_sep = bool(row) and all(set(c) <= set("-: ") for c in row if c != "")
                    if not is_sep and len(row) > status_idx:
                        status = _clean_cell(row[status_idx]).upper()
                        crit = _clean_cell(row[0])
                        if status == "TRIPPED":
                            tripped.append(crit)
                        elif status == "CLEARED":
                            cleared.append(crit)
                        elif status:
                            unsettled.append({"criterion": crit, "status": status})
                    j += 1
                i = j
                continue
        i += 1
    return tripped, cleared, unsettled


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("idea_dir")
    ap.add_argument("--docs", nargs="*", default=None,
                    help="override the doc filenames to scan (default: the 9-step upstream docs)")
    args = ap.parse_args()

    idea_dir = Path(args.idea_dir)
    if not idea_dir.is_dir():
        print(json.dumps({"error": f"not a directory: {idea_dir}"}))
        return 2

    doc_names = args.docs if args.docs else DEFAULT_DOCS
    flagged_deltas, warnings, docs_scanned, overrides = [], [], [], []
    verdict = verdict_source = None
    rounds, tripped, cleared, unsettled = [], [], [], []

    for name in doc_names:
        p = idea_dir / name
        if not p.is_file():
            warnings.append(f"{name}: not found in {idea_dir} — skipped")
            continue
        docs_scanned.append(name)
        lines = p.read_text(encoding="utf-8").splitlines()
        headings = _headings(lines)
        deltas, warning = scan_doc_deltas(name, lines, headings)
        flagged_deltas.extend(deltas)
        if warning:
            warnings.append(warning)
        # An override may be stamped in any doc (a tripped-then-overridden criterion); collect all.
        overrides += [f"{name}: {ln.strip()}" for ln in lines if OVERRIDE_RE.search(ln)]
        if name == "customer-discovery.md":
            rounds = discovery_read_rounds(lines, headings)
            latest = select_latest_round(rounds)
            if latest:
                verdict, verdict_source = latest["verdict"], "discovery-read-heading"
                if verdict is None:
                    warnings.append("customer-discovery.md: latest Discovery Read section has no "
                                    "recognizable verdict token — verify by hand")
            else:
                v = _first_verdict("\n".join(lines))
                verdict = v
                verdict_source = "prose-fallback" if v else "none"
                warnings.append(
                    "customer-discovery.md: no '## Discovery Read' heading found — verdict is "
                    "prose-guessed (verdict_source=prose-fallback); verify by hand" if v else
                    "customer-discovery.md: no '## Discovery Read' heading and no verdict token found")
            # Scope the scorecard to the LATEST round's region (its scorecard follows its heading),
            # so an earlier round's statuses can't contradict the binding latest verdict.
            scope = lines[(latest["line"] - 1):] if latest else lines
            tripped, cleared, unsettled = parse_status_tables(scope)

    if "customer-discovery.md" not in docs_scanned:
        warnings.append("customer-discovery.md absent — Discovery verdict/criteria not read. "
                        "/startup-brief's entry guard should have stopped before here.")

    result = {
        "slug": idea_dir.name,
        "docs_scanned": docs_scanned,
        "discovery_verdict": verdict,
        "verdict_source": verdict_source,
        "discovery_read_rounds": rounds,
        "tripped_criteria": tripped,
        "cleared_criteria": cleared,
        "unsettled_criteria": unsettled,
        "override_stamps": overrides,
        "flagged_deltas": flagged_deltas,
        "n_flagged_deltas": len(flagged_deltas),
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
