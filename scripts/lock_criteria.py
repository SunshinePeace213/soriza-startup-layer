#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""lock_criteria.py -- render + LOCK a gate's pre-registered criteria (lock-ahead).

Spec: reference §1.3 #7 (lock-ahead) + §4 ("human drafts -> script locks") + §6.2.

The lock-ahead rule: before passing G(n), G(n+1)'s criteria must already be locked, with a
`locked_at` that predates the evidence the gate will judge. `new_idea.py` locks criteria-g2
inline at scaffold; every later gate's criteria are locked here -- the step's skill calls this
as part of closing the *previous* gate (kill-scan locks g4 before passing G3; sharpen-hypothesis
locks g3 before passing G2; and so on).

It fills scripts/templates/criteria-<gate>.yaml with the slug and a current timestamp, then
writes ideas/<slug>/gates/criteria-<gate>.yaml. Criteria are WRITE-ONCE (§4): an existing file
is never silently overwritten -- pass --force only to re-register (a loudly-stamped exception).
The written file is schema-checked by the schema_on_write hook (-> test_criteria).

Usage:
    uv run scripts/lock_criteria.py --slug <slug> --gate g4
    uv run scripts/lock_criteria.py --slug <slug> --gate g3 --force
"""
import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from string import Template

HKT = timezone(timedelta(hours=8))  # founder is in HK; timestamps match the reference samples
TEMPLATES = Path(__file__).resolve().parent / "templates"


def now_iso() -> str:
    s = datetime.now(HKT).strftime("%Y-%m-%dT%H:%M:%S%z")
    return s[:-2] + ":" + s[-2:]  # +0800 -> +08:00


def main() -> None:
    ap = argparse.ArgumentParser(description="Render + lock a gate's pre-registered criteria (lock-ahead).")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--gate", required=True, choices=[f"g{i}" for i in range(2, 10)])
    ap.add_argument("--force", action="store_true", help="re-register criteria already locked (write-once exception)")
    a = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    template = TEMPLATES / f"criteria-{a.gate}.yaml"
    if not template.exists():
        sys.exit(f"[lock_criteria] no template scripts/templates/criteria-{a.gate}.yaml -- draft it first")
    out = root / "ideas" / a.slug / "gates" / f"criteria-{a.gate}.yaml"
    if not out.parent.exists():
        sys.exit(f"[lock_criteria] {out.parent} not found -- scaffold the idea first (uv run scripts/new_idea.py {a.slug})")
    if out.exists() and not a.force:
        sys.exit(f"[lock_criteria] {out} already locked -- criteria are write-once (§4); pass --force to re-register")

    locked_at = now_iso()
    out.write_text(Template(template.read_text(encoding="utf-8")).substitute(slug=a.slug, locked_at=locked_at),
                   encoding="utf-8")
    print(f"[lock_criteria] locked {a.gate} for {a.slug} at {locked_at} -> {out.relative_to(root)}")


if __name__ == "__main__":
    main()
