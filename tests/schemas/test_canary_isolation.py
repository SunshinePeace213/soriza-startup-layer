"""Canary: the independent round is sacred (Hard Rule #3, T14).

Hard Rule #3 names TWO guarantees of independence: isolated subagent contexts (the harness spawns
each `objection-lens` seat in its own context) AND *the canary test* -- explicitly "not by prompts".
The live runtime isolation can't be exercised in pytest, so this canary guards the CONFIG that makes
isolation hold from silent regression: the day someone grants a persona seat a spawn/read tool, or
deletes the "siblings are cross-exam-round-only" boundary, or unwires the contract hook, this goes red.
A leak introduced into the independent round would otherwise pass every behavioural test.
"""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
LENS = ROOT / ".claude" / "agents" / "objection-lens.md"
SKILL = ROOT / ".claude" / "skills" / "pressure-test" / "SKILL.md"


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "no frontmatter"
    return yaml.safe_load(m.group(1))


def test_persona_seat_cannot_spawn_or_read_siblings():
    fm = _frontmatter(LENS.read_text(encoding="utf-8"))
    tools = {t.strip() for t in str(fm.get("tools", "")).split(",")}
    # a seat that can spawn/dispatch could read a sibling's verdict in round 1 -> isolation breach
    assert "Task" not in tools and "Agent" not in tools, f"objection-lens must not hold spawn tools: {tools}"
    assert tools <= {"Read", "Glob"}, f"objection-lens read surface widened beyond Read/Glob: {tools}"


def test_contract_hook_is_wired_subagentstop():
    fm = _frontmatter(LENS.read_text(encoding="utf-8"))
    hooks = yaml.safe_dump(fm.get("hooks", {}))
    assert "persona_contract_check.py" in hooks, "the Stop->SubagentStop contract hook must stay wired"


def test_sibling_verdicts_are_cross_exam_round_only():
    body = LENS.read_text(encoding="utf-8").lower()
    # the access rules must scope sibling verdicts to the cross-exam round, never the independent one
    assert "cross-exam" in body and "sibling" in body
    assert re.search(r"sibling[^.\n]*cross-exam", body) or re.search(r"cross-exam[^.\n]*sibling", body), \
        "objection-lens must bind sibling-verdict access to the cross-exam round only"


def test_skill_keeps_independent_round_isolated_and_ordered():
    body = SKILL.read_text(encoding="utf-8").lower()
    assert "independent round" in body and "cross-examination" in body
    # the load-bearing promise: no seat sees a sibling before cross-exam, spawned in parallel/isolated
    assert "no seat may see a sibling" in body or "no persona touches a sibling" in body, \
        "the skill must state the independent round is sealed from sibling verdicts"
    assert "parallel" in body and ("isolat" in body or "one message" in body), \
        "seats must be spawned in parallel isolated contexts in a single message"
