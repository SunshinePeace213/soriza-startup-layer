---
name: customer-discovery-design
description: |
  Fifth stage of the Idea Stage: build the SEALED customer-discovery pack for a validated-enough idea —
  a precise target profile, a reachability map, a WARM LIST of real people who already publicly
  complained (each with a drafted contextual reply), a Mom-Test interview guide built from the
  Disconfirmation Brief's OPEN assumptions, cold-email drafts, and a tracking sheet — AND lock the
  kill-criteria.json before any data comes in. DRAFTS ONLY — the skill never sends; you post warm replies
  and Cowork sends cold email on per-batch approval. Use for "design my customer discovery", "build my
  interview guide", "who do I talk to and what do I ask", "build my outreach", "set up customer discovery".
when_to_use: |
  Gate: a disconfirmation-brief.md + hypothesis.md exist for the idea. Not scoring real interviews (/customer-discovery-synthesis) and not sending email (Cowork does that, gated).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Agent, WebSearch, WebFetch
effort: high
---

# Customer Discovery — Design

Build the sealed run-pack for talking to real people, and **lock the kill-criteria before any data comes
in**. This skill **designs and drafts**; it **never sends**. Cold outreach is irreversible and
reputation-/jurisdiction-sensitive, so sending lives off-skill: *you* post warm replies from your own
account, and **Cowork** sends the cold email + schedules calls on your **per-batch approval**.

## When this applies

- `disconfirmation-brief.md` + `hypothesis.md` exist; "design customer discovery", "build my interview
  guide / outreach", "who do I talk to and what do I ask".
- **Entry guard:** missing brief or hypothesis → point to `/disconfirm` (and `/sharpen-hypothesis`).

## What it does (goal + constraints)

Goal: the **sealed** `ideas/<slug>/customer-discovery/cowork-runpack.md` + the **locked**
`customer-discovery/kill-criteria.json`.

- **Target profile** — specific job titles, company types, team structures, seniority most likely to feel
  the problem acutely (from `hypothesis.md` + the user-language in `market-research.md`).
- **Reachability map** — the named communities / subreddits / Slack-Discord / LinkedIn groups / events
  where they congregate, with a prioritization (closest-to-the-problem first).
- **Warm list ★ (warm-first)** — real people who **already publicly complained**, each as
  `{link · their words · a drafted contextual reply/DM}`. Mine the demand signals from market research.
- **Mom-Test interview guide** — built **from the Brief's OPEN assumptions + interview questions**; past
  behaviour not future intentions; audited for leading / future-facing / too-broad questions (read
  `references/mom-test.md`). Separate question sets per persona if the hypothesis has more than one.
- **Cold-email drafts** — personalized to role/context (secondary to the warm list).
- **Tracking sheet** — prospect · channel · status · follow-up · done.
- **Lock the kill-criteria** — encode each OPEN assumption + its interview question into
  `kill-criteria.json` (write-once) with a trip-threshold (schema in
  `../customer-discovery-synthesis/references/kill-criteria-anchoring.md`). This pre-registration *before*
  data is the anti-confirmation-bias device — never softened later.
- **Soft-stop only** if there is no reachable audience at all; never re-judge merit (the idea already
  cleared the desk).

## Gotchas

- **No send tool, by design.** `allowed-tools` excludes every send-capable MCP tool. Drafts live in the
  sealed pack; Cowork sends, gated per batch. Never reach for a Gmail-send tool to "be helpful."
- **Warm-first.** The warm list (people who already complained) outperforms cold email — lead with it.

## Output

`ideas/<slug>/customer-discovery/cowork-runpack.md` (sealed; `assets/cowork-runpack-template.md`) +
`customer-discovery/kill-criteria.json`. Next: run the pack, interview ~5–15, drop notes into
`customer-discovery/interviews/<date>-<prospect>.md`, then `/customer-discovery-synthesis`.

## Workers & references

- Workers: `customer-discovery-design-worker` (the pack), `customer-discovery-personas-worker` (per-persona
  profiles + outreach drafts).
- `references/mom-test.md` (interview discipline); kill-criteria schema in
  `../customer-discovery-synthesis/references/kill-criteria-anchoring.md`; `assets/cowork-runpack-template.md`.
