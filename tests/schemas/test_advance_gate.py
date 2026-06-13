"""Integration test for scripts/advance_gate.py (T06) -- the only gates: writer.

Real connections, ephemeral: scaffolds a throwaway slug with --no-active (so the founder's
real ideas/ACTIVE is never touched), drives it through G1 -> G2, and asserts the gate-write,
lock-ahead, attestation, auto-check rejection, and self-check/rollback behaviour. The idea
dir is removed in teardown.
"""
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parents[2]
SLUG = "__advgate_test__"
IDEA = ROOT / "ideas" / SLUG

VALID_HYP = """---
stage: sharpen-hypothesis
status: testable
---

# Hypothesis -- test

**Testable sentence (provisional, to-be-tested):** test users feel a pain.

## WHO
A named role in a named segment. *Provisional.*

## HOW OFTEN
About 12 times a year.

## HOW SEVERE
Roughly 6 hours each time. *Provisional, to-be-tested.*

## STATUS QUO
They do it by hand today.

## VALUE & GROWTH
- Value: would they pay? *Provisional.*
- Growth: word of mouth. *Provisional.*
"""

G3_CRITERIA = """gate: g3
slug: __advgate_test__
locked: true
locked_at: 2026-06-13T15:27:21+08:00
criteria:
  - {id: g3-1, desc: "no disqualifier tripped", check: auto, test: test_killscan}
  - {id: g3-2, desc: "founder override if proceeding past a disqualifier", check: human}
"""


def sh(*args):
    return subprocess.run(["uv", "run", *args], cwd=str(ROOT), capture_output=True, text=True)


def state():
    fm = yaml.safe_load((IDEA / "STATE.md").read_text(encoding="utf-8").split("---")[1])
    return fm


def lock_g3():
    (IDEA / "gates" / "criteria-g3.yaml").write_text(G3_CRITERIA, encoding="utf-8")


def bump(p):  # ensure evidence mtime is after the criteria lock (pre-registration holds)
    os.utime(p, (time.time() + 2, time.time() + 2))


@pytest.fixture
def scaffolded():
    if IDEA.exists():
        shutil.rmtree(IDEA)
    r = sh("scripts/new_idea.py", SLUG, "--no-active", "--reason", "ephemeral advance_gate test")
    assert r.returncode == 0, r.stderr + r.stdout
    (IDEA / "seed.md").write_text("---\nidea: ephemeral test idea\n---\nseed body\n", encoding="utf-8")
    yield
    if IDEA.exists():
        shutil.rmtree(IDEA)


def test_g1_records_pick_and_advances_to_hypothesis(scaffolded):
    r = sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g1")
    assert r.returncode == 0, r.stderr + r.stdout
    fm = state()
    assert fm["gates"]["g1"]["decision"] == "DL-001"  # references the existing pick, no new DL
    assert fm["gates"]["g1"]["result"] == "pass"
    assert fm["current_step"] == 2 and fm["step_name"] == "hypothesis"
    assert fm["owner"] == "human" and "/sharpen-hypothesis" in fm["next_action"]


def test_g2_blocked_without_founder_attestation(scaffolded):
    assert sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g1").returncode == 0
    (IDEA / "hypothesis.md").write_text(VALID_HYP, encoding="utf-8")
    bump(IDEA / "hypothesis.md")
    lock_g3()
    r = sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g2")  # no --attest g2-4
    assert r.returncode != 0
    assert "attest" in (r.stderr + r.stdout).lower()
    assert "g2" not in state().get("gates", {})


def test_g2_passes_with_valid_hypothesis_and_attest(scaffolded):
    assert sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g1").returncode == 0
    (IDEA / "hypothesis.md").write_text(VALID_HYP, encoding="utf-8")
    bump(IDEA / "hypothesis.md")
    lock_g3()
    r = sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g2", "--attest", "g2-4")
    assert r.returncode == 0, r.stderr + r.stdout
    fm = state()
    assert fm["gates"]["g2"]["result"] == "pass"
    assert fm["gates"]["g2"]["criteria"] == "gates/criteria-g2.yaml"
    assert fm["current_step"] == 3 and fm["step_name"] == "kill_scan"
    dl = (IDEA / "decision-log.md").read_text(encoding="utf-8")
    assert re.search(r"##\s*DL-002\s*\|.*\|\s*g2 -> pass", dl)


def test_g2_blocked_when_hypothesis_invalid(scaffolded):
    assert sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g1").returncode == 0
    (IDEA / "hypothesis.md").write_text("# bad\n## WHO\njust one section\n", encoding="utf-8")
    bump(IDEA / "hypothesis.md")
    lock_g3()
    r = sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g2", "--attest", "g2-4")
    assert r.returncode != 0
    assert "g2" not in state().get("gates", {})  # STATE untouched on auto-check failure


def test_lock_ahead_blocks_g2_without_g3(scaffolded):
    assert sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g1").returncode == 0
    (IDEA / "hypothesis.md").write_text(VALID_HYP, encoding="utf-8")
    bump(IDEA / "hypothesis.md")
    # deliberately do NOT lock criteria-g3
    r = sh("scripts/advance_gate.py", "--slug", SLUG, "--gate", "g2", "--attest", "g2-4")
    assert r.returncode != 0
    assert "lock-ahead" in (r.stderr + r.stdout).lower()
