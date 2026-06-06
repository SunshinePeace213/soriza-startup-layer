---
name: idea-funnel-subagent-schema-prose-conflict
description: "schema/StructuredOutput subagents fail if their SKILL.md tells them to \"return one line of prose\""
metadata: 
  node_type: memory
  type: project
  originSessionId: acb94bc9-6b28-4df5-aedc-5247d27a3c83
---

In the AI-native-services /idea-funnel run, demand-detection failed 10/10 (every market-researcher
subagent did its web research, wrote market-research.md, then ended without calling StructuredOutput).
Root cause: `.claude/agents/market-researcher.md` ended with "return to the main conversation one line
… **not the findings**", which directly conflicts with the workflow's forced StructuredOutput contract.
The agent obeyed its own SKILL.md and skipped the tool call. Fixed by making the structured return the
agent's required final action (and the .md prose-return line was the ONLY sibling with this anti-pattern).

**Why:** an explicit "end with a prose summary" instruction in the agent body beats the schema-forcing
nudge the Workflow appends — the agent's own prompt wins. This is distinct from the rate-limit flakiness
in [[idea-funnel-ratelimit-fragility]] (that hit many agents intermittently; this was systematic, 0/10).

**How to apply:** any subagent invoked with a schema — `agent(..., {schema})` in a Workflow, or any forced
StructuredOutput — must NOT be told to finish with a one-line/prose summary. Tell it the structured call IS
its final required deliverable (file/side-effects are secondary). When adding a schema to an existing agent,
grep its def for "return … one line / return to the main conversation" and fix it first. Engine-side, the
fix was a `safeStage` wrapper in idea-funnel-engine.js so a structured-output failure degrades a candidate
to alive-but-degraded instead of nulling it and crashing the checkpoint tally.

**Generalizes to non-schema Write agents (2026-06-07, generate-ideas SaaS-Challengers run):** the same
"return ONE line … NOT the findings themselves; they live in the file" instruction in
`.claude/agents/startup-idea-researcher.md` made 1 of 4 parallel instances *invert* — it dumped the full
findings inline and SKIPPED the Write entirely (even claiming a non-existent "instruction that prohibits
writing .md files"). So the anti-pattern is not schema-only: any agent whose real deliverable is a
side-effect (a file write) but is told to "return a confirmation, NOT the artifact" can intermittently drop
the side-effect and over-return prose. Here it was intermittent (1/4), not systematic — so it slips through
unless the main loop verifies. Fix the def: make the Write the explicit final REQUIRED action and keep the
"don't paste findings in chat" nudge SEPARATE from the success contract. Until fixed, after any fan-out
always `ls`/`wc -l` the expected output paths and backfill any agent that returned content instead of
writing it (what I did this run).
