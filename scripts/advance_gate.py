#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""advance_gate.py (T06) -- the ONLY writer of STATE.md's gates: block.

Spec: docs/loop-engineering-reference-en.md §3.4 (gate-write enforcement) + §8 (skeleton)
+ §6.4 (decision-log format). Constitution Hard Rule #6: gates: is written ONLY here.

This script writes STATE.md via plain Python file IO (run under Bash), so it never trips
the gates_guard PreToolUse hook -- that asymmetry IS how "script-only gate writes" is
enforced. Any failure stops cold and leaves STATE + decision-log untouched.

Sequence (any step failing aborts before a single byte is written):
  1. load criteria-<gate>.yaml; verify locked==true and locked_at predates the evidence mtime
     (g1 is the entry gate: its criteria are the scaffold artifacts + the DL-001 pick)
  2. check:auto criteria -> run the mapped validator via pytest; check:human -> require --attest <id>
  3. lock-ahead: criteria-g(n+1).yaml exists and is locked (g9 exempt)
  4. append decision-log (new DL-id)            [g1 references the existing DL-001 pick instead]
  5. write STATE: gates.<gate> = {...}; advance current_step / step_name / status / owner / checklist
  6. self-check the new STATE with test_state; restore + abort if it does not validate

Usage:
  uv run scripts/advance_gate.py --slug <slug> --gate g2 --attest g2-4
  uv run scripts/advance_gate.py --slug <slug> --gate g4 --result proceed --p-agg 0.35 --attest g4-5
"""
import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

HKT = timezone(timedelta(hours=8))

STEPS = {1: "generate", 2: "hypothesis", 3: "kill_scan", 4: "pressure_alpha",
         5: "customer_discovery", 6: "pressure_beta", 7: "market_sizing", 8: "startup_brief", 9: "poc"}
NEXT_SKILL = {2: "/sharpen-hypothesis", 3: "/kill-scan", 4: "/pressure-test",
              5: "/customer-discovery-design", 6: "/pressure-test --beta", 7: "/market-sizing",
              8: "/startup-brief", 9: "/build-poc"}
# who holds the NEXT action when the pipeline arrives at each step
STEP_OWNER = {2: "human", 3: "agent", 4: "agent", 5: "agent", 6: "agent", 7: "agent", 8: "agent", 9: "human"}
# pytest validator -> the artifact (relative to the idea dir) it should run against
TEST_ARTIFACT = {"test_hypothesis": "hypothesis.md", "test_killscan": "kill-scan.md",
                 "test_pressure": "pressure-report-alpha.md", "test_pressure_beta": "pressure-report-beta.md",
                 "test_synthesis": "customer-discovery.md", "test_sizing": "market-sizing.md",
                 "test_brief": "startup-brief.md"}
DEFAULT_RESULT = {"g4": "proceed"}


def now_iso(seconds: bool = True) -> str:
    fmt = "%Y-%m-%dT%H:%M:%S%z" if seconds else "%Y-%m-%dT%H:%M%z"
    s = datetime.now(HKT).strftime(fmt)
    return s[:-2] + ":" + s[-2:]


def today() -> str:
    return datetime.now(HKT).strftime("%Y-%m-%d")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def fail(msg: str) -> None:
    sys.exit(f"[advance_gate] {msg}")


# ----- STATE (de)serialization: a controlled dumper that matches the scaffold's house style -----

def _q(s) -> str:
    return '"' + str(s).replace('"', '\\"') + '"'


def _gate_entry(g: dict) -> str:
    parts = [f"result: {g['result']}"]
    if g.get("p_agg") is not None:
        parts.append(f"p_agg: {g['p_agg']}")
    parts += [f"date: {g['date']}", f"criteria: {g['criteria']}", f"decision: {g['decision']}"]
    return "{" + ", ".join(parts) + "}"


def load_state(sp: Path):
    text = sp.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{sp} has no closed YAML frontmatter")
    fm = yaml.safe_load(parts[1])
    if not isinstance(fm, dict):
        fail(f"{sp} frontmatter did not parse as a mapping")
    return fm, parts[2], text


def render_state(fm: dict, body: str) -> str:
    L = ["---",
         f"slug: {fm['slug']}",
         "schema_version: 2",
         f"current_step: {fm['current_step']}",
         f"step_name: {fm['step_name']}",
         f"status: {fm['status']}",
         f"owner: {fm['owner']}"]
    ib = fm["interview_budget"]
    L.append(f"interview_budget: {{total: {ib['total']}, used: {ib['used']}}}")
    checklist = fm.get("step_checklist") or []
    if checklist:
        L.append("step_checklist:")
        for it in checklist:
            L.append(f"  - {{item: {_q(it['item'])}, owner: {it['owner']}, done: {'true' if it['done'] else 'false'}}}")
    else:
        L.append("step_checklist: []")
    dp = fm.get("deltas_pending") or []
    L.append("deltas_pending: [" + ", ".join(str(x) for x in dp) + "]")
    gates = fm.get("gates") or {}
    if gates:
        L.append("gates:")
        for k in sorted(gates):
            L.append(f"  {k}: {_gate_entry(gates[k])}")
    else:
        L.append("gates: {}")
    L.append(f"next_action: {_q(fm['next_action'])}")
    bl = fm.get("blocking")
    L.append("blocking: " + ("null" if bl is None else _q(bl)))
    L.append(f"updated: {fm['updated']}")
    L.append("---")
    return "\n".join(L) + body


def run_pytest(root: Path, test: str, artifact: Path) -> bool:
    r = subprocess.run(["uv", "run", "pytest", "tests/schemas", "-q", "-k", test, "--artifact", str(artifact)],
                       cwd=str(root), capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-1500:] + "\n")
    return r.returncode == 0


def _locked_at_ts(value) -> float:
    if isinstance(value, datetime):
        return value.timestamp()
    if isinstance(value, str):
        return datetime.fromisoformat(value).timestamp()
    fail("criteria locked_at is missing or unparseable")


def advance(args) -> None:
    root = repo_root()
    idea = root / "ideas" / args.slug
    sp = idea / "STATE.md"
    if not sp.exists():
        fail(f"{sp} not found -- scaffold the idea first (uv run scripts/new_idea.py {args.slug})")
    gate = args.gate
    n = int(gate[1:])
    fm, body, _ = load_state(sp)

    if not args.force and isinstance(fm.get("gates"), dict) and gate in fm["gates"]:
        fail(f"{gate} already recorded in STATE -- pass --force to re-record")

    attests = set(args.attest or [])
    summary = []

    if n == 1:
        # entry gate: criteria are intrinsic (scaffold artifacts + the founder's recorded pick)
        for f in ("STATE.md", "seed.md", "decision-log.md"):
            if not (idea / f).exists():
                fail(f"g1: scaffold artifact {f} is missing")
        if "DL-001" not in (idea / "decision-log.md").read_text(encoding="utf-8"):
            fail("g1: DL-001 (the founder's pick) not found in decision-log")
        criteria_ref = "scaffold"
        decision = "DL-001"
        result = args.result or "pass"
        summary.append("scaffold artifacts present; pick recorded in DL-001 (founder-signed)")
    else:
        cf = idea / "gates" / f"criteria-{gate}.yaml"
        if not cf.exists():
            fail(f"{cf} not found -- {gate} criteria must be pre-registered and locked before this gate")
        crit = yaml.safe_load(cf.read_text(encoding="utf-8"))
        if crit.get("locked") is not True:
            fail(f"{gate} criteria are not locked (locked: true required)")
        locked_ts = _locked_at_ts(crit.get("locked_at"))
        criteria_ref = f"gates/criteria-{gate}.yaml"

        tests_to_run, human_needed = {}, []
        for c in crit.get("criteria", []):
            if c.get("check") == "auto":
                t = c.get("test")
                if t:
                    tests_to_run.setdefault(t, []).append(c["id"])
                else:
                    summary.append(f"{c['id']}: auto (no validator mapped; skipped -- W1 has none)")
            else:
                human_needed.append(c["id"])

        missing = [cid for cid in human_needed if cid not in attests]
        if missing:
            fail(f"{gate}: missing founder attestation for {missing} -- pass --attest " + " --attest ".join(missing))

        for t, ids in tests_to_run.items():
            art = idea / TEST_ARTIFACT.get(t, "")
            if not TEST_ARTIFACT.get(t) or not art.exists():
                fail(f"{gate}: criterion(s) {ids} need {t}'s artifact ({TEST_ARTIFACT.get(t, '?')}) which is absent")
            if art.stat().st_mtime < locked_ts:
                fail(f"{gate}: criteria were locked AFTER {art.name} was written -- pre-registration violated")
            if not run_pytest(root, t, art):
                fail(f"{gate}: auto-check {t} failed (criteria {ids}) -- fix {art.name} and re-run")
            summary.append(f"{t} green ({', '.join(ids)})")
        for cid in human_needed:
            summary.append(f"{cid}: founder-attested")
        result = args.result or DEFAULT_RESULT.get(gate, "pass")
        decision = None  # a new DL id is allocated below

    # lock-ahead (g9 exempt)
    if n < 9:
        nf = idea / "gates" / f"criteria-g{n + 1}.yaml"
        if not nf.exists():
            fail(f"lock-ahead: gates/criteria-g{n + 1}.yaml must exist and be locked before passing {gate}")
        nxt = yaml.safe_load(nf.read_text(encoding="utf-8"))
        if nxt.get("locked") is not True:
            fail(f"lock-ahead: gates/criteria-g{n + 1}.yaml is not locked")

    # snapshot for rollback
    dl = idea / "decision-log.md"
    dl_orig = dl.read_text(encoding="utf-8") if dl.exists() else ""
    state_orig = sp.read_text(encoding="utf-8")

    # decision-log: g1 references the existing DL-001 pick; every other gate appends a new entry
    if n != 1:
        ids = [int(m) for m in re.findall(r"##\s*DL-(\d+)", dl_orig)]
        decision = f"DL-{(max(ids) + 1) if ids else 1:03d}"
        attest_str = ", ".join(sorted(attests)) if attests else "none"
        entry = (f"\n## {decision} | {today()} | {gate} -> {result}\n"
                 f"- Source: scripts/advance_gate.py (criteria-{gate}.yaml; attested: {attest_str})\n"
                 f"- Verdict: {result}" + (f" (p_agg {args.p_agg})" if args.p_agg is not None else "") + "\n"
                 f"- Rationale: " + "; ".join(summary) + "; lock-ahead criteria-g"
                 + (str(n + 1) if n < 9 else "9") + (" locked" if n < 9 else " exempt") + "\n"
                 f"- Signed: Ringo (via advance_gate)\n")
        dl.write_text(dl_orig + entry, encoding="utf-8")

    # write STATE
    g_entry = {"result": result, "date": today(), "criteria": criteria_ref, "decision": decision}
    if args.p_agg is not None:
        g_entry["p_agg"] = args.p_agg
    if not isinstance(fm.get("gates"), dict):
        fm["gates"] = {}
    fm["gates"][gate] = g_entry

    if n == 9:
        fm.update(current_step=9, step_name="poc", status="done", owner="human",
                  next_action="PoC complete -- graduate to the MVP layer or loop back (see learning-log)",
                  step_checklist=[])
    else:
        ns = n + 1
        fm.update(current_step=ns, step_name=STEPS[ns], status="in_progress", owner=STEP_OWNER[ns],
                  next_action=f"run {NEXT_SKILL[ns]} {args.slug}",
                  step_checklist=[{"item": f"Run {NEXT_SKILL[ns]} for step {ns} ({STEPS[ns]})",
                                   "owner": STEP_OWNER[ns], "done": False}])
    fm["updated"] = now_iso(seconds=False)
    sp.write_text(render_state(fm, body), encoding="utf-8")

    # self-check: the gate writer must never leave an invalid STATE on disk
    if not run_pytest(root, "test_state", sp):
        sp.write_text(state_orig, encoding="utf-8")
        if n != 1:
            dl.write_text(dl_orig, encoding="utf-8")
        fail("FATAL: produced a STATE.md that fails test_state -- rolled back; this is a bug in advance_gate")

    print(f"[advance_gate] {gate} -> {result}  (now step {fm['current_step']}: {fm['step_name']}, owner {fm['owner']})")
    print(f"               decision: {decision} | next_action: {fm['next_action']}")
    for s in summary:
        print(f"               - {s}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Advance an idea past a gate (the only gates: writer).")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--gate", required=True, choices=[f"g{i}" for i in range(1, 10)])
    ap.add_argument("--result", default="", help="gate result (default: pass; g4 default: proceed)")
    ap.add_argument("--p-agg", type=float, default=None, dest="p_agg", help="aggregated p_success (g4/g6)")
    ap.add_argument("--attest", action="append", default=[], help="criterion id the founder attests (repeatable)")
    ap.add_argument("--force", action="store_true", help="re-record a gate already in STATE")
    advance(ap.parse_args())


if __name__ == "__main__":
    main()
