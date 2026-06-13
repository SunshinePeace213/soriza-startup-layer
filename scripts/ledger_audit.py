#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""ledger_audit.py (T24, W5) -- the three-way reconciliation. Spec: reference §3.4 #3 + §11.2.

gates_guard.py blocks the file-tool path to STATE.md's `gates:` block, but an agent could still
sed-bypass via Bash. The residual risk is caught HERE: for every gate entry in STATE.md, this
asserts a matching (a) criteria file and (b) decision-log entry exist -- a gate written by any
route other than advance_gate.py leaves one of the three out of sync, and that drift becomes loud.

Also runs ledger sanity (append-only discipline, §6.3): evidence-ledger ids unique + ascending,
grade<=4 carries source/url, corrections reference a real id; predictions carry resolution_criteria
+ resolve_by and resolution lines reference a locked id.

Usage:
  uv run scripts/ledger_audit.py --slug hk-broker-recon
  uv run scripts/ledger_audit.py --all [--report reports/ledger-audit.md]
Exit 0 = clean; exit 1 = drift found (problems printed / written to the report).
"""
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _frontmatter(text: str) -> dict:
    parts = text.split("---")
    return yaml.safe_load(parts[1]) if len(parts) >= 3 else {}


def audit_idea(idea: Path) -> list[str]:
    """Return a list of drift problems for one idea dir (empty == clean)."""
    problems: list[str] = []
    slug = idea.name
    state = idea / "STATE.md"
    if not state.exists():
        return [f"{slug}: no STATE.md"]
    fm = _frontmatter(state.read_text(encoding="utf-8")) or {}

    # --- three-way: gates <-> criteria file <-> decision-log entry ---
    dl = idea / "decision-log.md"
    dl_ids = set(re.findall(r"##\s*(DL-\d+)", dl.read_text(encoding="utf-8"))) if dl.exists() else set()
    for gate, entry in (fm.get("gates") or {}).items():
        if not isinstance(entry, dict):
            problems.append(f"{slug}.{gate}: gate entry is not a mapping")
            continue
        crit = entry.get("criteria")
        if crit and crit != "scaffold":
            if not (idea / crit).exists():
                problems.append(f"{slug}.{gate}: criteria file '{crit}' is missing (gate recorded without its criteria)")
        dec = entry.get("decision")
        if not dec:
            problems.append(f"{slug}.{gate}: no `decision:` DL-id recorded")
        elif dec not in dl_ids:
            problems.append(f"{slug}.{gate}: decision '{dec}' has no matching entry in decision-log.md")

    # --- evidence-ledger sanity (§6.3) ---
    led = idea / "evidence-ledger.jsonl"
    if led.exists():
        seen, last = set(), -1
        for n, line in enumerate(led.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"{slug} evidence-ledger:{n}: not valid JSON")
                continue
            rid = rec.get("id", "")
            m = re.fullmatch(r"E-(\d+)", rid)
            if not m:
                problems.append(f"{slug} evidence-ledger:{n}: bad id '{rid}'")
                continue
            num = int(m.group(1))
            if rid in seen:
                problems.append(f"{slug} evidence-ledger:{n}: duplicate id {rid}")
            seen.add(rid)
            if num <= last:
                problems.append(f"{slug} evidence-ledger:{n}: id {rid} not ascending (append-only)")
            last = max(last, num)
            if rec.get("grade", 5) <= 4 and not (rec.get("source") or rec.get("url")):
                problems.append(f"{slug} evidence-ledger:{n}: grade<=4 {rid} missing source/url")
            corr = rec.get("corrects")
            if corr and corr not in seen:
                problems.append(f"{slug} evidence-ledger:{n}: corrects '{corr}' which is not an earlier id")

    # --- predictions sanity (§3.5) ---
    pred = idea / "predictions.jsonl"
    if pred.exists():
        locked = set()
        for n, line in enumerate(pred.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"{slug} predictions:{n}: not valid JSON")
                continue
            pid = rec.get("id", "")
            is_resolution = "resolved" in rec and rec.get("resolved") and "claim" not in rec
            if is_resolution:
                if pid not in locked:
                    problems.append(f"{slug} predictions:{n}: resolution for '{pid}' has no locked claim line")
            else:
                if not rec.get("resolution_criteria") or not rec.get("resolve_by"):
                    problems.append(f"{slug} predictions:{n}: {pid} missing resolution_criteria/resolve_by")
                locked.add(pid)
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description="Three-way gate/ledger reconciliation (T24).")
    ap.add_argument("--slug", help="audit one idea")
    ap.add_argument("--all", action="store_true", help="audit every idea folder")
    ap.add_argument("--report", help="also write the report to this path (e.g. reports/ledger-audit.md)")
    args = ap.parse_args()

    ideas_dir = ROOT / "ideas"
    if args.all:
        ideas = [d for d in sorted(ideas_dir.iterdir()) if (d / "STATE.md").exists()]
    elif args.slug:
        ideas = [ideas_dir / args.slug]
    else:
        ap.error("pass --slug <slug> or --all")

    lines, total = [], 0
    for idea in ideas:
        probs = audit_idea(idea)
        total += len(probs)
        if probs:
            lines.append(f"## {idea.name} -- {len(probs)} issue(s)")
            lines += [f"- {p}" for p in probs]
        else:
            lines.append(f"## {idea.name} -- clean")
    header = f"# Ledger audit -- {total} issue(s) across {len(ideas)} idea(s)\n"
    report = header + "\n".join(lines) + "\n"
    print(report)
    if args.report:
        rp = ROOT / args.report
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report, encoding="utf-8")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
