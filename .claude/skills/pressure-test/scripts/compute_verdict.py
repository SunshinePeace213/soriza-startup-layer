#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Compute the pressure-test panel verdict from the per-expert rebuttal files.

Deterministic implementation of Step 8's truth table. Bundled so the model never
has to re-execute the tally or hand-parse 4-6 files by eye on every run (Thariq Tip 8).

Parse hardening (PARSE-5): malformed rebuttals are surfaced *explicitly* in the
`malformed` list and cause a non-zero exit by default, instead of silently being
coerced to RESTATE-HARDER. The main agent should retry a malformed expert (per the
skill's retry rule) before falling back. Pass --allow-malformed to apply the
documented RESTATE-HARDER fallback when a retry has already failed.

Usage:
  python3 compute_verdict.py <rebuttals_dir> --anti-thesis <persona_slug> [--allow-malformed]

<rebuttals_dir> contains one <persona_slug>.md per expert (the Round-4 outputs).
Prints a JSON object to stdout:
  {
    "verdict": "ship-with-conditions" | "refine-hypothesis" | "kill-suggested",
    "anti_thesis": "<slug>",
    "anti_thesis_flag": true|false,        # anti-thesis RESTATE-HARDER w/o fatal -> surface, don't block
    "per_expert": { "<slug>": {"verdict": "...", "fatal": bool, "anti_thesis": bool} },
    "malformed": ["<slug>", ...],
    "anti_thesis_warning": "...",          # present only if --anti-thesis matched no rebuttal file
    "tally": {"withdraw": n, "accept": n, "restate_harder_non_anti": n, "structurally_fatal": n}
  }

The --anti-thesis slug MUST equal the .md filename stem of the anti-thesis expert's rebuttal.
If it matches no file the exemption can't be applied, so by default the script refuses (exit 2)
rather than silently letting that seat's RESTATE-HARDER block the pass rule.

Exit codes: 0 = clean compute; 2 = malformed rebuttal(s) OR an --anti-thesis slug matching no
rebuttal file, with --allow-malformed not set.
"""
import argparse
import json
import re
import sys
from pathlib import Path

CANON = ["ACCEPT-WITH-CONDITIONS", "RESTATE-HARDER", "WITHDRAW"]  # order: longest/compound first
FATAL_TOKEN = "STRUCTURALLY-FATAL"


def _normalize(text: str) -> str:
    """Uppercase and collapse spaces/underscores to hyphens so 'restate harder',
    'RESTATE_HARDER' and 'RESTATE-HARDER' all match the canonical token."""
    up = text.upper()
    # turn runs of spaces/underscores between two word-chars into single hyphens
    up = re.sub(r"[ _]+", "-", up)
    return up


def _section(text: str, heading_regex: str):
    """Return the body of a `## <heading>` section (until the next `## ` or EOF), or None."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^\s*##\s", ln) and re.search(heading_regex, ln, re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return None
    body = []
    for ln in lines[start:]:
        if re.match(r"^\s*##\s", ln):
            break
        body.append(ln)
    return "\n".join(body)


def _find_verdict(text: str):
    """Find exactly one canonical verdict token. Prefer the `## Final Verdict`
    section; fall back to the whole file. Return token or None."""
    for scope in (_section(text, r"final\s+verdict"), text):
        if not scope:
            continue
        norm = _normalize(scope)
        for tok in CANON:
            # Guard against alphanumeric continuation only; hyphens/spaces are valid
            # boundaries (normalization already turned separators into hyphens, and the
            # compound tokens contain internal hyphens).
            if re.search(r"(?<![A-Z0-9])" + re.escape(tok) + r"(?![A-Z0-9])", norm):
                return tok
    return None


def _has_fatal(text: str) -> bool:
    # Prefer the Fatal flag section, but accept the token anywhere (the template
    # only emits it intentionally).
    scope = _section(text, r"fatal\s+flag") or text
    return FATAL_TOKEN in _normalize(scope)


def parse_rebuttal(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    return _find_verdict(text), _has_fatal(text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("rebuttals_dir")
    ap.add_argument("--anti-thesis", required=True, help="persona slug tagged anti-thesis in Step 3")
    ap.add_argument("--allow-malformed", action="store_true",
                    help="apply the documented RESTATE-HARDER fallback for unparseable files (use only after a retry has failed)")
    args = ap.parse_args()

    rdir = Path(args.rebuttals_dir)
    if not rdir.is_dir():
        print(json.dumps({"error": f"not a directory: {rdir}"}))
        return 2

    files = sorted(rdir.glob("*.md"))
    if not files:
        print(json.dumps({"error": f"no rebuttal files in {rdir}"}))
        return 2

    per_expert = {}
    malformed = []
    for f in files:
        slug = f.stem
        verdict, fatal = parse_rebuttal(f)
        if verdict is None:
            malformed.append(slug)
            if args.allow_malformed:
                verdict = "RESTATE-HARDER"  # documented fallback
            else:
                continue
        per_expert[slug] = {
            "verdict": verdict,
            "fatal": fatal,
            "anti_thesis": slug == args.anti_thesis,
        }

    if malformed and not args.allow_malformed:
        print(json.dumps({
            "verdict": None,
            "malformed": malformed,
            "message": "Malformed rebuttal(s): retry these experts (Step 7 retry rule), "
                       "then re-run; or pass --allow-malformed to coerce them to RESTATE-HARDER.",
        }, indent=2))
        return 2

    # Guard the anti-thesis exemption: if the slug matches no parsed rebuttal file, the
    # exemption silently fails to apply and the anti-thesis's RESTATE-HARDER would wrongly
    # count toward the pass rule. Surface it loudly instead of inverting the rule in silence.
    anti_thesis_warning = None
    if args.anti_thesis not in per_expert:
        anti_thesis_warning = (
            f"anti-thesis slug '{args.anti_thesis}' matched no rebuttal file "
            f"(seats on disk: {sorted(per_expert)}). The anti-thesis exemption was NOT applied, "
            f"so its RESTATE-HARDER (if any) wrongly counts toward the pass rule."
        )
        if not args.allow_malformed:
            print(json.dumps({
                "verdict": None,
                "anti_thesis": args.anti_thesis,
                "anti_thesis_warning": anti_thesis_warning,
                "seats": sorted(per_expert),
                "message": "Pass the exact persona_slug whose rebuttal file is on disk "
                           "(it equals the .md filename stem). Fix the slug and re-run, or "
                           "pass --allow-malformed to proceed without the exemption.",
            }, indent=2))
            return 2

    non_anti = [v for s, v in per_expert.items() if not v["anti_thesis"]]
    any_fatal = any(v["fatal"] for v in per_expert.values())  # any seat, incl. anti-thesis
    restate_non_anti = sum(1 for v in non_anti if v["verdict"] == "RESTATE-HARDER")
    withdraw = sum(1 for v in per_expert.values() if v["verdict"] == "WITHDRAW")
    accept = sum(1 for v in per_expert.values() if v["verdict"] == "ACCEPT-WITH-CONDITIONS")

    if any_fatal or restate_non_anti >= 3:
        verdict = "kill-suggested"
    elif restate_non_anti >= 1:
        verdict = "refine-hypothesis"
    else:
        verdict = "ship-with-conditions"

    anti = per_expert.get(args.anti_thesis)
    anti_thesis_flag = bool(anti and anti["verdict"] == "RESTATE-HARDER" and not anti["fatal"])

    result = {
        "verdict": verdict,
        "anti_thesis": args.anti_thesis,
        "anti_thesis_flag": anti_thesis_flag,
        "per_expert": per_expert,
        "malformed": malformed,
        "tally": {
            "withdraw": withdraw,
            "accept": accept,
            "restate_harder_non_anti": restate_non_anti,
            "structurally_fatal": sum(1 for v in per_expert.values() if v["fatal"]),
        },
    }
    if anti_thesis_warning:
        result["anti_thesis_warning"] = anti_thesis_warning
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
