"""Shared pytest plumbing for the schema validators (doc-TDD foundation, ref §9).

Each validator module sets `FIXTURE = "<name>"` (a file in tests/fixtures/) as its
green sample. Run normally, the validator checks that green fixture. The schema_on_write
hook (W5) re-runs the same validator with `--artifact <path>` so it instead checks the
file the agent just wrote, feeding any assertion message back for self-repair.
"""
from pathlib import Path

import pytest

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def pytest_addoption(parser):
    parser.addoption(
        "--artifact",
        action="store",
        default=None,
        help="path to the artifact under validation (set by the schema_on_write hook); "
        "when absent, validators run against their bundled green fixture",
    )


@pytest.fixture
def artifact_text(request):
    """Text of --artifact if given, else the requesting module's green FIXTURE."""
    opt = request.config.getoption("--artifact")
    path = Path(opt) if opt else FIXTURE_DIR / request.module.FIXTURE
    return path.read_text(encoding="utf-8")
