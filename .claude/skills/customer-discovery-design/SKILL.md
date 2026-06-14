---
name: customer-discovery-design
description: |
  Step 5a of the Idea Stage: build the SEALED customer-discovery pack — target profile, warm★ list, Mom-Test interview guide, cold-email drafts — from pressure-test α's OPEN assumptions + the kill-scan demand-scan. Consumes the kill-criteria locked at G4; never re-locks them. Drafts only; never sends. Use for "design my customer discovery", "build my interview guide", "build my outreach".
when_to_use: |
  Gate: current_step 5 (pressure-test α passed) — pressure-report-alpha.md + the G4-locked kill-criteria.json exist. Not scoring real interviews (/customer-discovery-synthesis) and not sending email (Cowork does that, gated).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Agent, WebSearch, WebFetch
effort: high
---

# Customer Discovery — Design (Step 5a)

Build the sealed run-pack for talking to real people. This skill **designs and drafts**; it **never
sends**. Cold outreach is irreversible and reputation-/jurisdiction-sensitive, so sending lives off-skill:
*you* post warm replies from your own account, and **Cowork** sends the cold email + schedules calls on
your **per-batch approval**.

The kill-criteria this discovery will trip-or-clear were **pre-registered and locked at G4** by
`/pressure-test` α (from the panel's OPEN assumptions, write-once) — this skill **consumes** them and
builds the guide to test them; it never creates or softens them.

## When this applies

- `current_step: 5` with `pressure-report-alpha.md` + a locked `customer-discovery/kill-criteria.json`
  present; "design customer discovery", "build my interview guide / outreach", "who do I talk to and what
  do I ask".
- **Entry guard:** no `pressure-report-alpha.md` (or step < 5) → point to `/pressure-test` (and, if no
  hypothesis, `/sharpen-hypothesis`). No locked `kill-criteria.json` → it should have been locked at G4;
  re-run `/pressure-test` α to lock it before designing discovery.

## What it does (goal + constraints)

Goal: the **sealed** `ideas/<slug>/customer-discovery/cowork-runpack.md`, built to test the **G4-locked**
`customer-discovery/kill-criteria.json`.

- **Target profile** — specific job titles, company types, team structures, seniority most likely to feel
  the problem acutely (from `hypothesis.md` + the real-user language mined in the `kill-scan.md`
  demand-scan).
- **Reachability map** — the named communities / subreddits / Slack-Discord / LinkedIn groups / events
  where they congregate, with a prioritization (closest-to-the-problem first).
- **Outreach strategy** — the **2–3 highest-leverage methods** for this segment, picked from
  `references/outreach-methods.md` (the leverage ladder: flag-planting / warm intros > go-to-them > cold),
  each tagged **Tier A** (founder builds it; never Cowork) or **Tier B** (per-prospect drafts — warm replies
  the founder posts, cold emails Cowork sends, gated). Not the whole menu — focus. Landing-page signups are a
  lead source for conversations, never validation.
- **Warm list ★ (warm-first)** — real people who **already publicly complained**, each as
  `{link · their words · a drafted V.F.W.P.A.-framed reply/DM}`. Mine the demand signals from the kill-scan
  demand-scan — the named complainers seeded as grade-4 entries in `evidence-ledger.jsonl`.
- **Mom-Test interview guide** — built **from pressure-test α's OPEN assumptions + their interview
  questions** (in `pressure-report-alpha.md`); past behaviour not future intentions; audited for leading /
  future-facing / too-broad questions (read `references/mom-test.md`). Each question maps to the OPEN
  assumption (and the locked kill-criterion) it trips-or-clears. Separate question sets per persona if the
  hypothesis has more than one.
- **Cold-email drafts** — personalized to role/context, **V.F.W.P.A.-framed** (secondary to the warm list).
- **Tracking sheet** — prospect · channel · status · follow-up · done.
- **Consume the locked kill-criteria** — read `customer-discovery/kill-criteria.json` (locked at G4) and
  ensure every interview question traces to a criterion it tests. **Never edit a threshold** —
  pre-registration before data is the anti-confirmation-bias device, and the lock belongs to G4. If the
  file is somehow absent, do not lock it here — stop and route back to `/pressure-test` α (that is where
  the OPEN assumptions become locked criteria).
- **Soft-stop only** if there is no reachable audience at all; never re-judge merit (the idea already
  cleared the desk and the α panel).

## STATE wiring

Read `ideas/<slug>/STATE.md` (`current_step: 5`). On finishing the pack: flip the step's `owner: agent`
checklist item to `done: true`, append a human-owned item (e.g. *"Run the sealed pack with real people;
drop notes in customer-discovery/interviews/<date>-<prospect>.md"*), and set `next_action` to
*"run the pack (warm-first), interview ~5–15, then /customer-discovery-synthesis"*. Do **not** touch the
`gates:` block or `owner` (the gate stays open until `/customer-discovery-synthesis` signs G5; only
`advance_gate.py` writes gates). Agent-writable fields are `status / next_action / step_checklist /
deltas_pending` only.

## Gotchas

- **No send tool, by design.** `allowed-tools` excludes every send-capable MCP tool. Drafts live in the
  sealed pack; Cowork sends, gated per batch. Never reach for a Gmail-send tool to "be helpful."
- **Warm-first.** The warm list (people who already complained, mined in the kill-scan demand-scan)
  outperforms cold email — lead with it.
- **The kill-criteria are not yours to write.** They were locked at G4 from the OPEN assumptions; you
  build the guide to test them and never soften a threshold.

## Output

`ideas/<slug>/customer-discovery/cowork-runpack.md` (sealed; `assets/cowork-runpack-template.md`). Next:
run the pack, interview ~5–15, and capture each conversation with `assets/interview-note-template.md`
(the emoji legend — drop notes into `customer-discovery/interviews/<date>-<prospect>.md`), then
`/customer-discovery-synthesis`.

## Workers & references

- Workers: `customer-discovery-design-worker` (the pack), `customer-discovery-personas-worker` (per-persona
  profiles + outreach drafts). Pass them pressure-test α's OPEN assumptions + interview questions, the
  kill-scan demand-scan findings, and the reference paths (`mom-test.md`, `outreach-methods.md`).
- `references/mom-test.md` (interview discipline); `references/outreach-methods.md` (the outreach leverage
  ladder — methods, V.F.W.P.A. framing, the landing-page vanity-metric guardrail); the locked kill-criteria
  schema in `../customer-discovery-synthesis/references/kill-criteria-anchoring.md`;
  `assets/cowork-runpack-template.md`; `assets/interview-note-template.md` (the emoji capture legend).
- Spec: `docs/loop-engineering-reference-en.md` §2 (step 5a).
