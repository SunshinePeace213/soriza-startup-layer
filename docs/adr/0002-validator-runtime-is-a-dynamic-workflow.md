# The Validator runtime is a dynamic Workflow over headless gate-subagents, not an orchestrator skill

**Status:** accepted

Per the official docs (https://code.claude.com/docs/en/workflows), skills and subagents let *Claude*
hold the plan turn-by-turn with intermediate results in the context window, and scale to "a few per
turn"; a **dynamic workflow** moves the loop, branching, and intermediate state into a script the
runtime executes and scales to "dozens to hundreds of agents per run." A 100-Candidate funnel with
deterministic per-gate kill logic is the workflow case, not the skill case.

**Decision.** The Idea-Stage Validator's runtime is a **saved dynamic Workflow**
(`.claude/workflows/idea-funnel-engine.js`, launched by the `/idea-funnel` skill via the Workflow tool, batch passed via the `args` global)
that `pipeline()`s Candidates through ordered **gate-subagents** (`.claude/agents/*.md`). Each gate
emits a **schema-validated** advance/kill verdict (the Workflow `schema` option). Existing research
subagents are reused as stages; new gate-subagents + kill-rubrics are built and verified with
**prompt-architect**. The interactive skills remain the human-facing path (single-idea runs; the
survivors' full debate, customer-discovery SEND, and solution-design).

## Considered Options

- **One orchestrator skill** (a scaled-up idea-to-hypothesis). Rejected: a skill can't fan out
  deterministically — Claude decides turn-by-turn, every result floods the context window, and the
  docs cap this at "a few per turn." Wrong grain for 100 Candidates.
- **Both, as equals.** Rejected: the only useful "skill" here is a thin launcher/reporter; the heavy
  interactive skills are a separate path, not part of the funnel.

## Consequences

- **No mid-run user input** (docs): the Workflow terminates at the **Shortlist**; the irreversible
  SEND and the full debate run *outside* any workflow. Official guidance: "for sign-off between
  stages, run each stage as its own workflow."
- **Research preview**: requires Claude Code v2.1.154+, all paid plans; on Pro enable via `/config`.
- Workflow subagents run in `acceptEdits` and inherit the tool allowlist — **allowlist WebSearch/
  WebFetch (and any research MCP) before a run** so agents don't hit mid-run permission prompts.
- Resume works only within the same session; exiting Claude Code mid-run restarts the workflow fresh.
