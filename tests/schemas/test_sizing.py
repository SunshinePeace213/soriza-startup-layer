"""Validator: ideas/<slug>/market-sizing.md (gate G7). Spec: reference §2 (step 7) + §9.

Step 7 is CONTEXT, never a gate -- "size never kills." G7 is a completeness check, not a
verdict. This validator enforces that the four sizing facets are present and built the right
way -- bottom-up TAM/SAM/SOM pressure-tested for inflation, budget-holder vs influencer, 3
named trends each scored tailwind/headwind, analogues -- and that the doc declares its own
non-gate status. Every assert message is written FOR THE AGENT: the schema_on_write hook feeds
it back verbatim, so it must say what *right* looks like.
"""
import re
from pathlib import Path

FIXTURE = "market-sizing.sample.md"
BAD_FIXTURE = "market-sizing.bad.md"
SECTIONS = ["Sizing", "Buyer", "Trends", "Analogues"]


def _sec(text, name):
    m = re.search(rf"^##\s*{name}\b(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    assert m, f"Missing section: ## {name} (market-sizing needs all 4 facets: {', '.join(SECTIONS)})"
    return m.group(1)


def test_sections_present(artifact_text):
    for s in SECTIONS:
        _sec(artifact_text, s)


def test_tam_sam_som_bottom_up(artifact_text):
    sizing = _sec(artifact_text, "Sizing")
    for tier in ("TAM", "SAM", "SOM"):
        assert re.search(rf"\b{tier}\b", sizing), (
            f"Sizing is missing {tier} -- size with all three tiers (TAM/SAM/SOM), not one headline number"
        )
    assert re.search(r"\d", sizing), "Sizing has no numbers -- bottom-up sizing must show the actual arithmetic"
    assert re.search(r"bottom-up", sizing, re.I), (
        "Sizing must be built BOTTOM-UP (count real units x price), not top-down off a market headline -- say so"
    )


def test_inflation_pressure_tested(artifact_text):
    sizing = _sec(artifact_text, "Sizing")
    assert re.search(r"inflat", sizing, re.I), (
        "Sizing must flag TAM inflation (pressure-test the number, don't launder it) -- surface where a "
        "top-down model would have inflated the figure"
    )


def test_buyer_vs_influencer(artifact_text):
    buyer = _sec(artifact_text, "Buyer")
    assert re.search(r"budget", buyer, re.I) and re.search(r"influenc", buyer, re.I), (
        "Buyer landscape must distinguish who holds BUDGET from who INFLUENCES (and whether they are the same person)"
    )


def test_three_trends_scored(artifact_text):
    trends = _sec(artifact_text, "Trends")
    scored = len(re.findall(r"tailwind|headwind", trends, re.I))
    assert scored >= 3, (
        f"Trends has only {scored} scored trend(s) -- name 3 trends, each scored tailwind or headwind"
    )


def test_size_never_kills(artifact_text):
    assert re.search(r"size never kills", artifact_text, re.I), (
        "market-sizing is CONTEXT, not a verdict -- state 'size never kills'; a small TAM is a rank input, never a gate"
    )


def test_red_fixture_bites():
    """The bad fixture must fail at least one check -- proves the validator actually bites."""
    bad = (Path(__file__).parents[1] / "fixtures" / BAD_FIXTURE).read_text(encoding="utf-8")
    failed = 0
    for check in (test_sections_present, test_tam_sam_som_bottom_up, test_inflation_pressure_tested,
                  test_buyer_vs_influencer, test_three_trends_scored, test_size_never_kills):
        try:
            check(bad)
        except AssertionError:
            failed += 1
    assert failed >= 1, "market-sizing.bad.md slipped past every check -- the validator does not bite"
