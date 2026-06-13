#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""persona_contract_check.py -- component-scoped Stop hook (auto-converted to SubagentStop) for the
objection-lens persona seat. Spec: reference §7.5 + §10 (Appendix B output contract).

The pressure-test α/β panel consumes each persona's reply as a single JSON object (the α contract).
This hook validates that contract the moment the persona finishes, BEFORE the orchestrator/judge ever
sees a malformed verdict -- exit 2 with a repair message makes the persona fix its own answer.

Safety posture (deliberate): FAIL-CLOSED on a positively-malformed contract (JSON present but a field
is missing or out of range -- the common, high-value catch), but FAIL-OPEN when no JSON object can be
extracted from the transcript at all. The latter degrades gracefully: a hook that can't read the
transcript format must never wedge the whole panel. The downstream judge/aggregator is the backstop.
"""
import json
import re
import sys

REQUIRED = ("persona", "p_success", "base_rate_ref", "risk_patterns", "sharpest_objection",
            "steelman_for", "change_my_mind")
OBJECTION_KEYS = ("objection", "falsifiable_assumption", "interview_question")


def fail(msg: str) -> None:
    sys.stderr.write("persona contract violation: " + msg +
                     "\nReply with a SINGLE JSON object matching the α contract (Appendix B) and nothing else.\n")
    sys.exit(2)


def last_assistant_text(transcript_path: str) -> str | None:
    """Best-effort: the text of the last assistant message in a JSONL transcript."""
    try:
        lines = open(transcript_path, encoding="utf-8").read().splitlines()
    except OSError:
        return None
    text = None
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        try:
            ev = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(ev, dict):
            continue
        msg = ev.get("message", ev)
        role = ev.get("type") or (msg.get("role") if isinstance(msg, dict) else None)
        if role != "assistant":
            continue
        content = msg.get("content") if isinstance(msg, dict) else None
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
            if parts:
                text = "\n".join(parts)
    return text


def extract_json_object(text: str):
    """The last balanced {...} object in the text, or None. Tolerates ```json fences / preamble."""
    if not text:
        return None
    stripped = re.sub(r"```(?:json)?|```", "", text).strip()
    try:
        obj = json.loads(stripped)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass
    # fall back to the last {...} span
    start, depth = None, 0
    last = None
    for i, ch in enumerate(stripped):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                chunk = stripped[start:i + 1]
                try:
                    cand = json.loads(chunk)
                    if isinstance(cand, dict):
                        last = cand
                except json.JSONDecodeError:
                    pass
    return last


def validate(obj: dict) -> None:
    missing = [k for k in REQUIRED if k not in obj]
    if missing:
        fail(f"missing required field(s) {missing}")
    p = obj.get("p_success")
    if not (isinstance(p, (int, float)) and not isinstance(p, bool) and 0.0 <= p <= 1.0):
        fail("p_success must be a number in [0,1] (a calibration prediction, never a verdict)")
    if not str(obj.get("base_rate_ref", "")).strip():
        fail("base_rate_ref must name the reference class and why")
    if not isinstance(obj.get("risk_patterns"), list):
        fail("risk_patterns must be a list")
    so = obj.get("sharpest_objection")
    if not isinstance(so, dict) or any(not str(so.get(k, "")).strip() for k in OBJECTION_KEYS):
        fail(f"sharpest_objection must be an object with non-empty {list(OBJECTION_KEYS)}")
    for k in ("steelman_for", "change_my_mind"):
        if not str(obj.get(k, "")).strip():
            fail(f"{k} must be non-empty")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    if data.get("stop_hook_active"):          # anti-loop: a second pass always releases
        sys.exit(0)
    tp = data.get("transcript_path")
    if not tp:
        sys.exit(0)                            # nothing to read -> degrade gracefully
    text = last_assistant_text(tp)
    obj = extract_json_object(text) if text else None
    if obj is None:
        sys.exit(0)                            # FAIL-OPEN: no JSON found (format drift) -> let the judge backstop it
    validate(obj)                              # FAIL-CLOSED: JSON present but malformed -> exit 2, repair
    sys.exit(0)


main()
