"""Component hook citation_density_check: the β citation tooth (rides in pressure-test
frontmatter, ref §7.2/§7.5). Density (every evidence-table claim row cites an E-xxx) + integrity
(every cited E-xxx exists in the sibling ledger). β-only: a no-op on α and non-report writes.
Encodes WHY each branch exists, not just the exit code."""
from pathlib import Path

ROOT = Path(__file__).parents[2]
FIX = ROOT / "tests" / "fixtures"

# minimal β reports built inline so each test isolates ONE failure mode (the green path uses the
# real shipped fixture, proving the validator's fixture also satisfies the stricter hook).
UNCITED_ROW = """---
stage: pressure_beta
recommendation: pivot
---
# β
## How the evidence moved the assumptions
| α open assumption | Discovery evidence (E-xxx) | Now |
|---|---|---|
| They will pay | the founder is sure they will | still open |
## Cost
180k
"""

DANGLING_CITE = """---
stage: pressure_beta
recommendation: pivot
---
# β
## How the evidence moved the assumptions
| α open assumption | Discovery evidence (E-xxx) | Now |
|---|---|---|
| They will pay | E-999: a citation to nothing | confirmed |
## Cost
180k
"""


def _payload(fp):
    return {"tool_name": "Write", "tool_input": {"file_path": str(fp)}}


def _beta(tmp_path, content, with_ledger=True, name="pressure-report-beta.md"):
    d = tmp_path / "ideas" / "slug"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(content, encoding="utf-8")
    if with_ledger:
        (d / "evidence-ledger.jsonl").write_text(
            (FIX / "ledger.sample.jsonl").read_text(encoding="utf-8"), encoding="utf-8")
    return p


def test_green_fixture_passes(tmp_path, run_hook):
    # the real shipped β fixture cites only ids present in ledger.sample.jsonl -> clean
    sample = (FIX / "pressure-report-beta.sample.md").read_text(encoding="utf-8")
    p = _beta(tmp_path, sample)
    r = run_hook("citation_density_check.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_uncited_claim_row_blocks(tmp_path, run_hook):
    p = _beta(tmp_path, UNCITED_ROW)
    r = run_hook("citation_density_check.py", _payload(p))
    assert r.returncode == 2
    assert "uncited claim row" in r.stderr  # the offending row is named so the agent knows what to cite


def test_dangling_citation_blocks(tmp_path, run_hook):
    p = _beta(tmp_path, DANGLING_CITE)
    r = run_hook("citation_density_check.py", _payload(p))
    assert r.returncode == 2
    assert "E-999" in r.stderr  # the dangling id is named


def test_alpha_report_is_noop(tmp_path, run_hook):
    # α's open assumptions are NOT citation-enforced -- the tooth is β-only
    p = _beta(tmp_path, UNCITED_ROW, with_ledger=False, name="pressure-report-alpha.md")
    r = run_hook("citation_density_check.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_non_report_write_is_noop(tmp_path, run_hook):
    p = tmp_path / "ideas" / "slug" / "STATE.md"
    p.parent.mkdir(parents=True)
    p.write_text("not a report")
    r = run_hook("citation_density_check.py", _payload(p))
    assert r.returncode == 0, r.stderr


def test_missing_ledger_skips_integrity_only(tmp_path, run_hook):
    # no ledger present: integrity can't be checked, but density still holds -> a clean report passes
    p = _beta(tmp_path, DANGLING_CITE.replace("E-999", "E-019"), with_ledger=False)
    r = run_hook("citation_density_check.py", _payload(p))
    assert r.returncode == 0, r.stderr
