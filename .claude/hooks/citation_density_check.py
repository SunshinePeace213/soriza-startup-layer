#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Component-scoped hook -- rides in `pressure-test` SKILL.md frontmatter (ref §7.2 / §7.5).

The β citation tooth. PostToolUse(Write) fires only while pressure-test is active and only on a
`pressure-report-beta.md` write. It is the *stricter, additive* half of the step-6 citation
contract -- the always-on `test_pressure_beta` schema validator checks the report's shape and
that it is citation-grounded; this checks what a text-only validator cannot:

  1. Density   -- every claim row in the two evidence tables ("How the evidence moved",
                  "Ranked residual risks") carries a ledger E-xxx. β claims are evidence, not
                  opinion (α's open assumptions are NOT citation-enforced -- this is β-only).
  2. Integrity -- every E-xxx cited in the report actually exists in the sibling
                  evidence-ledger.jsonl. A dangling citation is exactly the failure mode the
                  "cite a ledger entry ID" rule exists to catch.

Exit 2 + an agent-facing message on violation (self-repair); exit 0 otherwise. No-op on α reports
and any non-β file, so the `if: Write(*pressure-report-beta.md)` matcher and this guard agree.
"""
import json
import re
import sys
from pathlib import Path

E_CITE = re.compile(r"\bE-\d+\b")          # a real ledger id; ignores the literal "E-xxx" placeholder
SEP_ROW = re.compile(r"^\|[\s\-:|]+\|$")    # a markdown table separator row (|---|---|)
CLAIM_SECTIONS = ["How the evidence moved", "Ranked residual risks"]


def _section(text: str, keyword: str) -> str:
    m = re.search(rf"^##\s*[^\n]*{re.escape(keyword)}[^\n]*\n(.*?)(?=^##\s|\Z)",
                  text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def _data_rows(section_body: str) -> list[str]:
    """Table data rows in a section (the lines after each |---| separator), header rows excluded."""
    rows, seen_sep = [], False
    for line in section_body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            if not s:
                seen_sep = False  # blank line ends a table block; a later table re-arms on its own separator
            continue
        if SEP_ROW.match(s):
            seen_sep = True
            continue
        if seen_sep:
            rows.append(s)
    return rows


def _ledger_ids(report_path: Path) -> set[str] | None:
    """Ids in the sibling evidence-ledger.jsonl, or None if it is absent (skip integrity then)."""
    ledger = report_path.parent / "evidence-ledger.jsonl"
    if not ledger.exists():
        return None
    ids = set()
    for line in ledger.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("id"):
            ids.add(rec["id"])
    return ids


def main() -> None:
    data = json.load(sys.stdin)
    fp = (data.get("tool_input") or {}).get("file_path", "")
    if not fp or Path(fp).name != "pressure-report-beta.md":
        sys.exit(0)  # β-only tooth: α reports and everything else are not this hook's jurisdiction
    path = Path(fp)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        sys.exit(0)  # existence/readability is schema_on_write's concern, not the citation tooth's

    problems: list[str] = []

    # 1) density -- every claim row in the evidence tables must cite an E-xxx
    for keyword in CLAIM_SECTIONS:
        for row in _data_rows(_section(text, keyword)):
            if not E_CITE.search(row):
                problems.append(f"uncited claim row under '...{keyword}...': {row}")

    # 2) integrity -- every cited id must exist in the sibling ledger
    ledger_ids = _ledger_ids(path)
    if ledger_ids is not None:
        for cid in sorted(set(E_CITE.findall(text))):
            if cid not in ledger_ids:
                problems.append(f"dangling citation {cid}: not in evidence-ledger.jsonl")

    if problems:
        print("[citation-density] β report fails the citation tooth -- every claim cites a ledger "
              "E-xxx and every E-xxx must exist in the ledger (append the entry first, then cite it):\n- "
              + "\n- ".join(problems), file=sys.stderr)
        sys.exit(2)
    sys.exit(0)


main()
