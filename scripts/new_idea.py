#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""new_idea.py -- T01 scaffold script for the Soriza Idea Stage.

Spec: STATE schema v2 + criteria/decision-log scaffold; validators in tests/schemas/
(test_state, test_criteria) + the pipeline canon in
.claude/skills/idea-stage/references/stage-pipeline.md.

Lays down the state-layer scaffold for ONE idea slug:

    ideas/<slug>/
        STATE.md                         # schema v2, current_step=1, gates: {}
        gates/criteria-g2.yaml           # pre-registered G2 criteria, locked immediately
        evidence-ledger.jsonl            # empty (append-only thereafter)
        predictions.jsonl                # empty (append-only thereafter)
        decision-log.md                  # DL-001 = why this idea
        customer-discovery/interviews/   # empty (.gitkeep so it survives a clone)
        poc/                             # empty (.gitkeep)
    ideas/ACTIVE                         # <- slug (unless --no-active)

The file contents come from scripts/templates/ (STATE.md, criteria-g2.yaml,
decision-log.md); edit those to change what a scaffold looks like. They use
$placeholder substitution (string.Template), so the YAML stays plain YAML.

Constitution: this script writes `gates: {}` (empty) ONLY. Gate *results* are
written exclusively by scripts/advance_gate.py (§3.4 / Hard Rule #6); the empty
scaffold block is the one lawful exception (gates_guard.py allows a fresh STATE.md).

Usage:
    uv run scripts/new_idea.py <slug> [--reason "one sentence: why this idea"]
                                      [--no-active]   # scaffold without moving ACTIVE
                                      [--force]       # overwrite an existing STATE.md
"""
import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from string import Template

HKT = timezone(timedelta(hours=8))  # founder is in HK; timestamps match the reference samples
TEMPLATES = Path(__file__).resolve().parent / "templates"  # scripts/templates/


def now_iso(seconds: bool = True) -> str:
    fmt = "%Y-%m-%dT%H:%M:%S%z" if seconds else "%Y-%m-%dT%H:%M%z"
    s = datetime.now(HKT).strftime(fmt)
    return s[:-2] + ":" + s[-2:]  # +0800 -> +08:00


def today() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent  # <root>/scripts/new_idea.py


def seed_oneliner(seed_path: Path) -> str:
    """Best-effort one-line rationale from seed.md.

    Prefer the frontmatter `idea:`/`title:` value (the seed's own one-liner);
    fall back to the first prose line of the body.
    """
    if not seed_path.exists():
        return ""
    text = seed_path.read_text(encoding="utf-8")

    # split off a leading YAML frontmatter block, if any
    fm, body = "", text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            fm, body = parts[1], parts[2]

    m = re.search(r"^\s*(?:idea|title)\s*:\s*(.+?)\s*$", fm, re.M)
    if m:
        return m.group(1).strip().strip('"').strip()[:200]

    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "---", ">", "|")):
            continue
        s = re.sub(r"^[-*]\s+", "", s).replace("**", "").strip()
        if s:
            return s[:200]
    return ""


def render(name: str, **fields: str) -> str:
    """Fill scripts/templates/<name>'s $placeholders. Raises if a field is missing."""
    return Template((TEMPLATES / name).read_text(encoding="utf-8")).substitute(**fields)


def scaffold(slug: str, reason: str, set_active: bool, force: bool) -> None:
    root = repo_root()
    ideas = root / "ideas"
    if not ideas.is_dir():
        sys.exit(f"[new_idea] {ideas} not found -- run from the repo root.")
    idea = ideas / slug

    state = idea / "STATE.md"
    if state.exists() and not force:
        sys.exit(f"[new_idea] {state} already exists -- pass --force to overwrite.")

    # 1) directories (+ .gitkeep so empty scaffold dirs survive a clone)
    (idea / "customer-discovery" / "interviews").mkdir(parents=True, exist_ok=True)
    (idea / "gates").mkdir(parents=True, exist_ok=True)
    (idea / "poc").mkdir(parents=True, exist_ok=True)
    for keep in (idea / "customer-discovery" / "interviews" / ".gitkeep", idea / "poc" / ".gitkeep"):
        keep.touch()

    # rationale: explicit flag > seed one-liner > placeholder
    reason = reason or seed_oneliner(idea / "seed.md") or "(rationale pending -- fill in)"

    # 2) STATE.md  (gates: {} only)
    state.write_text(render("STATE.md", slug=slug, updated=now_iso(seconds=False), summary=reason), encoding="utf-8")
    # 3) gates/criteria-g2.yaml (locked immediately)
    (idea / "gates" / "criteria-g2.yaml").write_text(render("criteria-g2.yaml", slug=slug, locked_at=now_iso()), encoding="utf-8")
    # 4) empty ledgers + decision-log DL-001
    for ledger in ("evidence-ledger.jsonl", "predictions.jsonl"):
        (idea / ledger).touch()
    dl = idea / "decision-log.md"
    if not dl.exists() or force:
        dl.write_text(render("decision-log.md", date=today(), reason=reason), encoding="utf-8")
    # 5) ACTIVE
    if set_active:
        (ideas / "ACTIVE").write_text(slug + "\n", encoding="utf-8")

    # 6) next action
    print(f"[new_idea] scaffolded ideas/{slug}  (active={'yes' if set_active else 'no'})")
    print(f"           next_action: run /sharpen-hypothesis {slug}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Scaffold an idea folder (Idea-Stage T01).")
    ap.add_argument("slug", help="idea slug, e.g. soriza-ai-persona-agency")
    ap.add_argument("--reason", default="", help="one-sentence rationale for DL-001 (defaults to seed.md's first line)")
    ap.add_argument("--no-active", action="store_true", help="scaffold without pointing ideas/ACTIVE at this slug")
    ap.add_argument("--force", action="store_true", help="overwrite an existing STATE.md / decision-log")
    a = ap.parse_args()
    scaffold(a.slug, a.reason.strip(), not a.no_active, a.force)


if __name__ == "__main__":
    main()
