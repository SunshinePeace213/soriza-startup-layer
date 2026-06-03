---
name: idea-to-hypothesis
description: |
  DEPRECATED — superseded by the Idea-Stage Validator (`/idea-funnel`). This skill only ever wired
  three stages (generate-ideas → sharpen-hypothesis → pressure-test) one idea at a time, with the
  founder hand-driving every gate. The funnel now runs the WHOLE Idea Stage over many ideas
  automatically and distills a ranked Shortlist. This file remains only as a signpost: it routes
  "run the whole idea stage" to `/idea-funnel`, and single-idea work to the standalone skills.
when_to_use: |
  Triggers on the old phrasings — "turn my research into a hypothesis", "generate ideas AND sharpen
  one", "run the whole idea stage", "ideas then hypothesis", "take me from thesis to something
  testable". On any of these, route per the table below rather than orchestrating here.
argument-hint: "[theme-slug]"
allowed-tools: AskUserQuestion, Read, Glob, Skill
effort: low
---

# Idea to Hypothesis — DEPRECATED (signpost only)

This skill is superseded by the **Idea-Stage Validator** (`/idea-funnel`). It no longer orchestrates;
it only routes. See [CONTEXT.md](../../../CONTEXT.md),
[ADR-0002](../../../docs/adr/0002-validator-runtime-is-a-dynamic-workflow.md), and
[docs/skill-designs/idea-funnel.md](../../../docs/skill-designs/idea-funnel.md).

## Routing

| The founder wants… | Route to |
|---|---|
| To test **many** ideas / a thesis, distilled automatically to a Shortlist | **`/idea-funnel`** (pass the thesis or a seed list via the workflow's `args`) |
| To run **one** idea through the full human pipeline | the standalone skills in order: `/sharpen-hypothesis` → `/pressure-test` → `/market-research` → `/customer-discovery` → `/solution-design` |
| Just a menu of ideas from a thesis (no funnel) | `/generate-ideas` |
| To sharpen one concrete idea into a testable hypothesis | `/sharpen-hypothesis` |

## Why deprecated

`/idea-funnel` does everything this skill did and more: it runs founder-market-fit, testability, an
evidence-based disconfirmation screen (objections judged by evidence, not a simulated debate —
[ADR-0001](../../../docs/adr/0001-funnel-kills-on-evidence-not-debate.md)), and customer-discovery
design over a whole batch, killing weak ideas at each gate and returning a ranked Shortlist — while
keeping the one irreversible gate (cold outreach SEND) human. Don't orchestrate the on-ramp by hand
here; launch the funnel.
