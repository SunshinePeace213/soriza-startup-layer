"""Shared hook-runner: invoke a hook the way Claude Code does -- JSON on stdin, read the
exit code (0 = pass, 2 = block) and stderr. Hooks are PEP-723 scripts, so `uv run --script`
runs them isolated from the project env."""
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
HOOKS = ROOT / ".claude" / "hooks"


@pytest.fixture
def run_hook():
    def _run(name: str, payload: dict) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["uv", "run", "--script", str(HOOKS / name)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
        )
    return _run
