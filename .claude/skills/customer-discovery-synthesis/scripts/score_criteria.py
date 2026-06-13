#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Score customer-discovery interview evidence against LOCKED kill-criteria thresholds.

Deterministic implementation of /customer-discovery-synthesis Step S4. Bundled so the
thresholds pre-registered at G4 from /pressure-test α's pressure-report (OPEN assumptions +
interview questions, locked once into kill-criteria.json) are applied mechanically — the
model tags each interview (reasoning), the script applies the threshold (arithmetic), and a
criterion can't be quietly soft-pedaled by eye to keep an idea alive. Same write-once,
never-soften discipline (Thariq Tip 8).

The script decides ONLY per-criterion status (TRIPPED / CLEARED / INCONCLUSIVE / MANUAL)
and reports coverage. The overall CONTINUE/PIVOT/KILL/KEEP-DISCOVERING call is the model's
soft judgment, made downstream from this output.

Usage:
  python3 score_criteria.py <kill_criteria.json> <scoring.json>

kill_criteria.json (locked at G4 by /pressure-test α, never edited after data exists):
  {
    "slug": "...", "locked_on": "YYYY-MM-DD",
    "criteria": [
      {"id": "wtp-against-free", "label": "No willingness-to-pay against free",
       "source": "pressure-report-alpha.md open assumption #1",
       "type": "support_proportion", "field": "ever_paid_comparable",
       "clear_at": 0.20, "trip_below": 0.10, "min_n": 8},
      {"id": "fomo-not-need", "label": "Behaviour is FOMO, not need",
       "type": "support_proportion", "field": "took_concrete_action",
       "clear_at": 0.30, "trip_below": 0.30, "min_n": 8},
      {"id": "native-good-enough", "label": "Native personalization is good enough",
       "type": "against_majority", "field": "native_suffices", "min_n": 8},
      {"id": "no-capturable-signal", "label": "No capturable signal the labs lack",
       "type": "manual"}
    ]
  }

scoring.json (assembled in Step S2 from the interview notes):
  {
    "n_total": 12,
    "interviews": [
      {"id": "2026-06-12-jane", "persona": "PM",
       "tags": {"ever_paid_comparable": false, "took_concrete_action": true, "native_suffices": false}},
      ...
    ]
  }

Scoring types:
  support_proportion  field is a SUPPORT signal. p = true/scored.
                      CLEARED if p >= clear_at; TRIPPED if p < trip_below; else INCONCLUSIVE.
                      (clear_at == trip_below collapses the band: a single CLEAR/TRIP boundary.)
  against_proportion  field is a REFUTING signal.
                      TRIPPED if p >= trip_at; CLEARED if p < clear_below; else INCONCLUSIVE.
  against_majority    field is a REFUTING signal. TRIPPED if a strict majority is true; else CLEARED.
  manual              qualitative — not auto-scorable. Status MANUAL; the model judges in prose.

A tag that is missing or null for an interview is excluded from that criterion's denominator.
n_scored < min_n (default 5) -> INCONCLUSIVE with small_sample=true regardless of proportion.

Prints a JSON object to stdout. Exit codes: 0 = clean; 2 = malformed input.
"""
import argparse
import json
import sys
from pathlib import Path

DEFAULT_MIN_N = 5


def _load(path_str):
    p = Path(path_str)
    if not p.is_file():
        return None, f"not a file: {p}"
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"invalid JSON in {p}: {e}"


def _tally(interviews, field):
    """Return (n_scored, n_true) over interviews whose tag for `field` is a real bool."""
    n_scored = 0
    n_true = 0
    for iv in interviews:
        if not isinstance(iv, dict):
            continue
        tags = iv.get("tags")
        if isinstance(tags, dict) and field in tags and isinstance(tags[field], bool):
            n_scored += 1
            if tags[field]:
                n_true += 1
    return n_scored, n_true


def _round(x):
    return round(x, 3)


def score_criterion(c, interviews):
    if not isinstance(c, dict):
        return {"id": None, "label": "", "type": None, "source": "", "status": "ERROR",
                "detail": "criterion entry is not a JSON object"}
    ctype = c.get("type")
    out = {"id": c.get("id"), "label": c.get("label", ""), "type": ctype,
           "source": c.get("source", "")}

    if ctype == "manual":
        out.update(status="MANUAL", detail="qualitative — judge in prose, mark explicitly in the Read")
        return out

    field = c.get("field")
    if not field:
        out.update(status="ERROR", detail="criterion missing 'field'")
        return out

    min_n = c.get("min_n", DEFAULT_MIN_N)
    n_scored, n_true = _tally(interviews, field)
    out.update(field=field, n_scored=n_scored, n_true=n_true)

    if n_scored == 0:
        out.update(status="INCONCLUSIVE", small_sample=True,
                   detail=f"no interview tagged '{field}' — nothing to score")
        return out

    p = n_true / n_scored
    out["proportion"] = _round(p)
    small = n_scored < min_n
    out["small_sample"] = small

    if ctype == "support_proportion":
        clear_at = c.get("clear_at")
        trip_below = c.get("trip_below")
        if clear_at is None or trip_below is None:
            out.update(status="ERROR", detail="support_proportion needs 'clear_at' and 'trip_below'")
            return out
        if small:
            status = "INCONCLUSIVE"
        elif p >= clear_at:
            status = "CLEARED"
        elif p < trip_below:
            status = "TRIPPED"
        else:
            status = "INCONCLUSIVE"
        out["detail"] = (f"{n_true}/{n_scored} ({p:.0%}) support; "
                         f"clear>={clear_at:.0%}, trip<{trip_below:.0%}"
                         + (f"; n<{min_n} -> small sample" if small else ""))
    elif ctype == "against_proportion":
        trip_at = c.get("trip_at")
        clear_below = c.get("clear_below")
        if trip_at is None or clear_below is None:
            out.update(status="ERROR", detail="against_proportion needs 'trip_at' and 'clear_below'")
            return out
        if small:
            status = "INCONCLUSIVE"
        elif p >= trip_at:
            status = "TRIPPED"
        elif p < clear_below:
            status = "CLEARED"
        else:
            status = "INCONCLUSIVE"
        out["detail"] = (f"{n_true}/{n_scored} ({p:.0%}) refute; "
                         f"trip>={trip_at:.0%}, clear<{clear_below:.0%}"
                         + (f"; n<{min_n} -> small sample" if small else ""))
    elif ctype == "against_majority":
        if small:
            status = "INCONCLUSIVE"
        elif n_true * 2 > n_scored:
            status = "TRIPPED"
        else:
            status = "CLEARED"
        out["detail"] = (f"{n_true}/{n_scored} ({p:.0%}) refute; "
                         f"trip if strict majority (>50%)"
                         + (f"; n<{min_n} -> small sample" if small else ""))
    else:
        out.update(status="ERROR", detail=f"unknown scoring type: {ctype}")
        return out

    out["status"] = status
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kill_criteria_json")
    ap.add_argument("scoring_json")
    args = ap.parse_args()

    kc, err = _load(args.kill_criteria_json)
    if err:
        print(json.dumps({"error": err}))
        return 2
    sc, err = _load(args.scoring_json)
    if err:
        print(json.dumps({"error": err}))
        return 2

    criteria = kc.get("criteria")
    interviews = sc.get("interviews")
    if not isinstance(criteria, list) or not criteria:
        print(json.dumps({"error": "kill_criteria.json has no 'criteria' list"}))
        return 2
    if not isinstance(interviews, list):
        print(json.dumps({"error": "scoring.json has no 'interviews' list"}))
        return 2

    # Coverage by persona (interview-only — the scorer does NOT read the prospects CSV)
    coverage = {}
    for iv in interviews:
        persona = (iv.get("persona") if isinstance(iv, dict) else None) or "unspecified"
        coverage[persona] = coverage.get(persona, 0) + 1

    scored = [score_criterion(c, interviews) for c in criteria]
    summary = {"tripped": 0, "cleared": 0, "inconclusive": 0, "manual": 0, "error": 0}
    for s in scored:
        key = s["status"].lower()
        summary[key] = summary.get(key, 0) + 1

    result = {
        "slug": kc.get("slug"),
        "locked_on": kc.get("locked_on"),
        "n_total": len(interviews),
        "coverage": coverage,
        "criteria": scored,
        "summary": summary,
    }
    # n_total is the array length (source of truth); warn if the declared field disagrees,
    # so a truncated interviews array can't masquerade as a full sample.
    declared = sc.get("n_total")
    if isinstance(declared, int) and declared != len(interviews):
        result["n_total_warning"] = (
            f"scoring.json declares n_total={declared} but the interviews array has "
            f"{len(interviews)} — using the array length")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
