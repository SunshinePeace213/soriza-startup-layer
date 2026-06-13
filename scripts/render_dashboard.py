#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""render_dashboard.py (T21 dashboard / T29 nightly headless). Spec: reference §3.3 + §11.2.

The dual-state audit. STATE.md is the DECLARED layer (current_step). The router's
"derive stage from which artifacts exist" rule is the DERIVED layer. This renders both and
flags **derived != declared = a drift alarm** -- so no status file can silently rot (a STATE
claiming step 7 with no artifacts past step 2 lights up red). Machine-rebuilt, never hand-edited;
the nightly cron writes it to reports/ (never into ideas/).

Usage: uv run scripts/render_dashboard.py [--report reports/dashboard.md]
"""
import argparse
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# artifact -> the step it proves COMPLETE (reference §3.3 / stage-pipeline.md derive-map).
# Highest matching step = derived "done"; the step to work on next is done+1 (cap 9).
LADDER = [
    (2, "hypothesis.md"),
    (3, "kill-scan.md"),
    (4, "pressure-report-alpha.md"),
    (5, "customer-discovery.md"),
    (6, "pressure-report-beta.md"),
    (7, "market-sizing.md"),
    (8, "startup-brief.md"),
    (9, "poc/reactions.md"),
]


def _frontmatter(text: str) -> dict:
    parts = text.split("---")
    return yaml.safe_load(parts[1]) if len(parts) >= 3 else {}


def derived_step(idea: Path) -> int:
    """The step to work on, derived purely from which artifacts exist (1 = only scaffold)."""
    done = 1  # scaffold present (STATE + seed) == step 1 complete
    for step, rel in LADDER:
        if (idea / rel).exists():
            done = step
    return min(done + 1, 9)


def audit_idea(idea: Path) -> dict:
    fm = _frontmatter((idea / "STATE.md").read_text(encoding="utf-8")) or {}
    declared = fm.get("current_step")
    derived = derived_step(idea)
    # tolerance: declared is the step IN PROGRESS; an artifact for the current step may already
    # exist with its gate still pending. So {derived-? } -> allowed = {derived-1, derived}.
    allowed = {derived - 1, derived}
    drift = not (isinstance(declared, int) and declared in allowed)
    return {
        "slug": idea.name, "declared": declared, "derived": derived,
        "status": fm.get("status"), "owner": fm.get("owner"),
        "next_action": fm.get("next_action"), "drift": drift,
    }


def render(rows: list[dict]) -> str:
    drifts = [r for r in rows if r["drift"]]
    out = [f"# Idea-Stage dashboard -- {len(rows)} idea(s), {len(drifts)} drift alarm(s)", ""]
    out.append("| idea | declared | derived | status | owner | state-audit |")
    out.append("|---|---|---|---|---|---|")
    for r in rows:
        flag = "🔴 DRIFT" if r["drift"] else "✅ ok"
        out.append(f"| {r['slug']} | {r['declared']} | {r['derived']} | {r['status']} | {r['owner']} | {flag} |")
    if drifts:
        out += ["", "## ⚠️ Drift alarms (declared step not reconcilable with artifacts on disk)"]
        for r in drifts:
            out.append(f"- **{r['slug']}**: STATE says step {r['declared']} but artifacts imply step {r['derived']}")
    out += ["", "## Next actions"]
    for r in rows:
        out.append(f"- **{r['slug']}** (step {r['declared']}): {r['next_action']}")
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Dual-state dashboard + state-audit (T21/T29).")
    ap.add_argument("--report", help="write the dashboard to this path (e.g. reports/dashboard.md)")
    args = ap.parse_args()
    ideas = [d for d in sorted((ROOT / "ideas").iterdir()) if (d / "STATE.md").exists()]
    rows = [audit_idea(d) for d in ideas]
    report = render(rows)
    print(report)
    if args.report:
        rp = ROOT / args.report
        rp.parent.mkdir(parents=True, exist_ok=True)
        rp.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
