#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Rank a solution concept's load-bearing assumptions for /startup-brief Step 5.

The Playbook exercise: identify the three assumptions the design depends on most heavily, then
ask what would have to be true for each. The scariest founder move is quietly DEMOTING the
assumption they can't defend so it never reaches the top 3 — so the ranking is mechanical: the
model scores each assumption on leverage (impact if wrong) and uncertainty (how unvalidated),
this script ranks by leverage x uncertainty and features the top 3. You can't fudge the order by
eye (mirrors /customer-discovery's score_criteria.py).

It also flags any assumption the blind solution-red-team raised (source="adversary") that reaches
the top 3 — an assumption the founder never listed turning out to be among the riskiest is a
loud reconciliation signal.

Usage:
  python3 rank_assumptions.py <assumptions.json>

assumptions.json (assembled in Step 5 from the founder's concept + the red-team's blind list):
  {
    "slug": "...",
    "assumptions": [
      {"id": "wtp-senior-eng", "statement": "...", "leverage": 5, "uncertainty": 4,
       "source": "agent", "what_would_have_to_be_true": "...", "evidence": "...",
       "cheapest_test": "..."},
      ...
    ]
  }

leverage / uncertainty: values in [1,5] (out-of-range clamped with a warning; missing or
non-numeric -> score null, ranked last). score = leverage x uncertainty (max 25).

Prints a JSON object to stdout. Exit codes: 0 = clean; 2 = malformed input.
"""
import argparse
import json
import sys
from pathlib import Path

PASSTHROUGH = ("statement", "source", "what_would_have_to_be_true", "evidence", "cheapest_test")


def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _clamp(x):
    return max(1.0, min(5.0, float(x)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("assumptions_json")
    args = ap.parse_args()

    p = Path(args.assumptions_json)
    if not p.is_file():
        print(json.dumps({"error": f"not a file: {p}"}))
        return 2
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"invalid JSON in {p}: {e}"}))
        return 2

    assumptions = data.get("assumptions")
    if not isinstance(assumptions, list) or not assumptions:
        print(json.dumps({"error": "assumptions.json has no non-empty 'assumptions' list"}))
        return 2

    warnings = []
    scored = []   # (orig_index, record)
    unscored = []

    for i, a in enumerate(assumptions):
        if not isinstance(a, dict):
            warnings.append(f"assumption #{i} is not an object — skipped")
            continue
        rec = {"id": a.get("id") or f"assumption-{i}"}
        for k in PASSTHROUGH:
            if k in a:
                rec[k] = a[k]
        lev, unc = a.get("leverage"), a.get("uncertainty")
        if _is_number(lev) and _is_number(unc):
            lev_c, unc_c = _clamp(lev), _clamp(unc)
            if lev_c != float(lev) or unc_c != float(unc):
                warnings.append(f"{rec['id']}: leverage/uncertainty out of 1-5 range — clamped")
            rec["leverage"], rec["uncertainty"] = lev_c, unc_c
            rec["score"] = round(lev_c * unc_c, 2)
            scored.append((i, rec))
        else:
            rec["leverage"], rec["uncertainty"], rec["score"] = lev, unc, None
            warnings.append(f"{rec['id']}: leverage/uncertainty missing or non-numeric — ranked last")
            unscored.append((i, rec))

    if not scored and not unscored:
        print(json.dumps({"error": "no valid assumption objects found"}))
        return 2

    # score desc, then leverage desc, then uncertainty desc, then stable input order
    scored.sort(key=lambda t: (-t[1]["score"], -t[1]["leverage"], -t[1]["uncertainty"], t[0]))
    ordered = [rec for _, rec in scored] + [rec for _, rec in unscored]

    for rank, rec in enumerate(ordered, 1):
        rec["rank"] = rank
        rec["featured"] = rec["score"] is not None and rank <= 3

    top_3 = [rec["id"] for rec in ordered if rec["featured"]]
    adversary_in_top_3 = [rec["id"] for rec in ordered
                          if rec["featured"] and rec.get("source") == "adversary"]

    result = {
        "slug": data.get("slug"),
        "n": len(ordered),
        "scale": "leverage & uncertainty each 1-5; score = leverage x uncertainty (max 25)",
        "ranked": ordered,
        "top_3": top_3,
        "adversary_in_top_3": adversary_in_top_3,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
