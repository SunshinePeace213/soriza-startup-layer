---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Follow-up when grilling on artifact-building

If the topic being grilled is building a skill, slash command, subagent, or Claude Code artifact of any kind (cues: "create a skill", "build a /command", "make an agent", "develop a workflow", "design a subagent"), plan to invoke `/prompt-architect` after we reach shared understanding. `/prompt-architect` picks up the grilled context, picks the right artifact type and template, drafts the artifact, runs the validation loop with bundled scripts, and ships the deliverable. The grill produces the design contract; `/prompt-architect` produces the artifact.

For non-artifact topics, this section does not apply — just complete the grilling and return the resolved design tree to the user.