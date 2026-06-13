"""Guard: every gate-criteria TEMPLATE references only validators that actually ship.

This is the regression test for the class of bug where criteria-g4.yaml referenced `test_pressure`
and `test_predictions` while neither validator file existed -- so advance_gate could never close G4.
For every `check: auto` criterion in scripts/templates/criteria-g*.yaml, its `test:` must (a) have a
tests/schemas/<test>.py file and (b) be a key in advance_gate.TEST_ARTIFACT (which maps it to the
artifact it runs against). Lock-ahead means these templates are locked before the evidence exists, so
a dangling reference is a silent, deferred gate deadlock -- exactly what this test makes loud.
"""
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[2]
TEMPLATES = ROOT / "scripts" / "templates"
SCHEMAS = ROOT / "tests" / "schemas"


def _advance_gate_module():
    spec = importlib.util.spec_from_file_location("advance_gate", ROOT / "scripts" / "advance_gate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_every_template_auto_test_resolves():
    ag = _advance_gate_module()
    problems = []
    templates = sorted(TEMPLATES.glob("criteria-g*.yaml"))
    assert templates, "no criteria templates found under scripts/templates/"
    for tpl in templates:
        text = tpl.read_text(encoding="utf-8").replace("$slug", "x").replace("$locked_at", "2026-01-01T00:00:00+08:00")
        doc = yaml.safe_load(text)
        for c in doc.get("criteria", []):
            if c.get("check") == "auto" and c.get("test"):
                t = c["test"]
                if not (SCHEMAS / f"{t}.py").exists():
                    problems.append(f"{tpl.name}:{c['id']} -> validator tests/schemas/{t}.py is missing")
                if t not in ag.TEST_ARTIFACT:
                    problems.append(f"{tpl.name}:{c['id']} -> '{t}' is not mapped in advance_gate.TEST_ARTIFACT")
    assert not problems, "gate-criteria templates reference unshipped validators:\n  " + "\n  ".join(problems)
