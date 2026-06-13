"""Deprecation guard (T35): retired stage commands are blocked + redirected, live ones pass."""


def test_disconfirm_is_blocked_and_redirects_to_pressure_test(run_hook):
    r = run_hook("deprecated_redirect.py", {"prompt": "please run /disconfirm hk-broker-recon"})
    assert r.returncode == 2, "retired /disconfirm must block the expansion"
    assert "pressure-test" in r.stderr, "must redirect to the new command"
    assert "RETIRED" in r.stderr


def test_market_map_redirects_to_killscan_and_sizing(run_hook):
    r = run_hook("deprecated_redirect.py", {"prompt": "/market-map"})
    assert r.returncode == 2
    assert "kill-scan" in r.stderr and "market-sizing" in r.stderr, "market-map split across two skills"


def test_solution_design_and_exit_redirect_to_startup_brief(run_hook):
    for name in ("solution-design", "idea-stage-exit"):
        r = run_hook("deprecated_redirect.py", {"prompt": f"/{name} <slug>"})
        assert r.returncode == 2, f"{name} must block"
        assert "startup-brief" in r.stderr


def test_live_command_passes(run_hook):
    # a current 9-step command must never be blocked
    r = run_hook("deprecated_redirect.py", {"prompt": "/pressure-test hk-broker-recon --beta"})
    assert r.returncode == 0, r.stderr


def test_substring_does_not_false_trigger(run_hook):
    # 'market-mapping-tool' or 'predisconfirmation' must NOT trip the word-bounded matcher
    r = run_hook("deprecated_redirect.py", {"prompt": "discuss the market-mapping-tool roadmap"})
    assert r.returncode == 0, r.stderr


def test_malformed_payload_never_blocks(run_hook):
    r = run_hook("deprecated_redirect.py", {})
    assert r.returncode == 0
