#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# ///
"""Deprecation guard (W11 / T35) -- UserPromptExpansion. Spec: reference §2.11 + §7.6.

The 9-step migration retired four stage names (disconfirm / market-map / solution-design /
idea-stage-exit). Legacy muscle memory typing `/disconfirm` should not silently no-op (the
skills are archived) -- it should be redirected to the new map. This hook fires on the retired
command names (settings.json UserPromptExpansion matcher), blocks the expansion (exit 2), and
prints the redirect on stderr so the founder re-learns the new pipeline.

Robust to payload-field drift: scans every string value in the payload for a retired `/<name>`.
"""
import json
import re
import sys

# retired command -> the new map (reference §2.11 migration table)
REDIRECTS = {
    "disconfirm": "/pressure-test <slug>  (panel α; β with --beta)",
    "market-map": "/kill-scan <slug>  (demand/complaint mining)  +  /market-sizing <slug>  (TAM/buyer/trends)",
    "solution-design": "/startup-brief <slug>  (drift audit + red-team + premortem + GO/NO-GO)",
    "idea-stage-exit": "/startup-brief <slug>  (the GO/NO-GO + exit criteria live here now)",
}


def _all_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _all_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _all_strings(v)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # nothing to judge -> never block
    blob = "\n".join(_all_strings(data))
    for name, target in REDIRECTS.items():
        # match /disconfirm, disconfirm command, etc. -- word-bounded, optional leading slash
        if re.search(rf"(?<![\w-])/?{re.escape(name)}(?![\w-])", blob):
            print(
                f"[deprecated] `{name}` is RETIRED in the 9-step canon (reference §2.11).\n"
                f"  Run instead: {target}\n"
                f"  (The legacy skill is archived under .claude/skills-archive/.)",
                file=sys.stderr,
            )
            sys.exit(2)
    sys.exit(0)


main()
