# Memory Index

- [idea-funnel bg isolation write-block](idea-funnel-bg-isolation-write-block.md) — /idea-funnel in a non-isolated bg session writes nothing; recover from transcripts, EnterWorktree first
- [idea-funnel rate-limit fragility](idea-funnel-ratelimit-fragility.md) — engine crashes/drops candidates when schema sub-agents skip StructuredOutput; hardened (agentSafe retry+degrade) but fix keeps getting lost in unmerged worktrees → MERGE the engine to main; resume-after-edit works + needs args; judge lacks Write tool so backfill disconfirmation-brief.md
- [subagent schema vs prose-return conflict](idea-funnel-subagent-schema-prose-conflict.md) — a schema/StructuredOutput subagent told to "return one line of prose, not the findings" systematically skips the tool call (market-researcher failed 0/10); fix the agent def, not just retries
- [skill-listing budget](skill-listing-budget.md) — skill descriptions: per-entry 1,536-char cap + global ~1% budget (drops least-used); the layer's standard = description field <300 chars (keyword-dense triggers) + when_to_use = gate+boundaries only; factory enforcement in prompt-architect/nuwa; all 31 trimmed <300 on 2026-06-06
