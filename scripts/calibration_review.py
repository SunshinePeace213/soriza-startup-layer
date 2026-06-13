#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""calibration_review.py (T34, W10) -- Brier scoring across resolved predictions. Spec: §3.5 + §11.2.

Every persona p_success and α/β prediction is locked into predictions.jsonl with resolution_criteria
+ resolve_by (§3.5). β resolves due ones (appends an outcome line, same id); this weekly review scores
the resolved set with the Brier score (lower = better calibrated) per persona, so persona/rubric tuning
is a DATA decision, never a vibe (Hard Rule: personas/rubric tuned ONLY after a calibration-review).

A locked line has `claim`+`p`; a resolution line (same id) has `outcome` (bool). Brier = (p - outcome)^2.

Usage: uv run scripts/calibration_review.py [--report reports/calibration.md]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def collect() -> tuple[dict, dict]:
    """Return ({id: locked_rec}, {id: outcome_bool}) merged across every idea's predictions.jsonl."""
    locked, outcomes = {}, {}
    for pred in sorted((ROOT / "ideas").glob("*/predictions.jsonl")):
        for line in pred.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            pid = rec.get("id")
            if not pid:
                continue
            if "claim" in rec and "p" in rec:
                locked[pid] = rec
            if rec.get("resolved") and rec.get("outcome") is not None:
                outcomes[pid] = bool(rec["outcome"])
    return locked, outcomes


def score(locked: dict, outcomes: dict) -> dict:
    per_persona = defaultdict(list)
    rows = []
    for pid, out in outcomes.items():
        rec = locked.get(pid)
        if not rec:
            continue
        p = float(rec["p"])
        brier = (p - (1.0 if out else 0.0)) ** 2
        persona = rec.get("persona", "?")
        per_persona[persona].append(brier)
        rows.append({"id": pid, "persona": persona, "p": p, "outcome": out, "brier": round(brier, 4)})
    summary = {k: round(sum(v) / len(v), 4) for k, v in per_persona.items()}
    overall = round(sum(r["brier"] for r in rows) / len(rows), 4) if rows else None
    return {"rows": rows, "per_persona": summary, "overall": overall,
            "resolved": len(rows), "open": len(locked) - len(outcomes)}


def render(s: dict) -> str:
    out = ["# Calibration review (Brier)", ""]
    out.append(f"- resolved predictions scored: **{s['resolved']}**")
    out.append(f"- still open (locked, unresolved): **{s['open']}**")
    out.append(f"- overall Brier: **{s['overall'] if s['overall'] is not None else 'n/a (no resolved predictions yet)'}**")
    if s["per_persona"]:
        out += ["", "## Per-persona Brier (lower = better calibrated)", "", "| persona | mean Brier | n |", "|---|---|---|"]
        counts = defaultdict(int)
        for r in s["rows"]:
            counts[r["persona"]] += 1
        for persona, b in sorted(s["per_persona"].items(), key=lambda kv: kv[1]):
            out.append(f"| {persona} | {b} | {counts[persona]} |")
    if s["rows"]:
        out += ["", "## Resolved predictions", "", "| id | persona | p | outcome | Brier |", "|---|---|---|---|---|"]
        for r in s["rows"]:
            out.append(f"| {r['id']} | {r['persona']} | {r['p']} | {r['outcome']} | {r['brier']} |")
    else:
        out += ["", "_No predictions resolved yet -- nothing to tune. Re-run after β resolves the first batch._"]
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Brier calibration review (T34).")
    ap.add_argument("--report", help="write to this path (e.g. reports/calibration.md)")
    args = ap.parse_args()
    locked, outcomes = collect()
    s = score(locked, outcomes)
    report = render(s)
    print(report)
    if args.report:
        rp = ROOT / args.report
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
