# Idea-funnel eval fixtures

Labelled Candidate fixtures for Phase 7 verification. Each fixture is a seed + the gate it should
resolve at + why. Use them to check the gate-subagents (via `artifact-eval` or a manual pass) and to
tune `gate-rubrics.md`: a known should-advance that gets killed, or a known should-kill that survives,
means a bar needs moving.

| Fixture | Expected outcome | Tests |
|---|---|---|
| `should-advance-personalized-ai-digest.md` | clears G0+G1+G2 (real pass) | the funnel doesn't kill a genuinely good idea |
| `should-kill-fmf.md` | killed at **Gate 0** | founder-market-fit hard fails (regulation/capital) |
| `should-kill-sharpen.md` | killed at **Gate 1** | un-sharpenable vague problem |
| `should-kill-gate2.md` | killed at **Gate 2** | me-too / no moat / tiny market, objection unrebutted |

Run order in Phase 7: each gate-subagent against its fixture in isolation first (does it return the
labelled verdict + a sensible reason?), then the whole `idea-funnel-engine` on all four as one small
batch (does the ledger show each resolving where expected?).
