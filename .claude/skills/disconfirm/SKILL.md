---
name: disconfirm
description: |
  Third stage of the Idea Stage — the structured devil's advocate. Pressure-test a hypothesis with a
  bounded expert panel (core-3 Thiel/Munger/Bezos) + competitor steelman + doctrine angles + one
  idea-type specialist, turning each disconfirming objection into a falsifiable assumption + a Mom-Test
  interview question. Produces a Disconfirmation Brief, NOT a verdict — nothing kills here; real users
  validate subjective merit. Use for "disconfirm my idea", "argue against this", "find disconfirming
  evidence", "pressure-test my hypothesis", "red-team the idea", "what could kill this".
when_to_use: |
  Trigger on "disconfirm", "argue against this idea", "find disconfirming evidence", "pressure-test my
  hypothesis", "play devil's advocate", "what could kill this", "competitor neglect" — when a
  hypothesis.md exists. Not for sizing the market (/market-map) or scoring real interviews
  (/customer-discovery-synthesis).
argument-hint: "[slug]"
allowed-tools: Read, Glob, Write, Agent, WebSearch, WebFetch
effort: high
---

# Disconfirm — the structured devil's advocate

Convene a bounded advisory board, fire the strongest disconfirming objections, and convert each into a
**falsifiable assumption + a Mom-Test interview question** for the Brief. **Nothing kills here** — the
desk hands you the right risks to go trip-or-clear with real people; real users are the only validator of
subjective merit (moat, demand, willingness-to-pay, behaviour).

## When this applies

- `hypothesis.md` exists; "disconfirm", "argue against this", "find disconfirming evidence",
  "pressure-test", "red-team the idea", "what could kill this".
- **Entry guard:** no `hypothesis.md` → point to `/sharpen-hypothesis`.

## What it does (goal + constraints)

Goal: `ideas/<slug>/disconfirmation-brief.md` — ranked risks + OPEN assumptions + interview questions.

- Read the panel roster in `../idea-stage/references/expert-lens-map.md`: **fixed core-3** (Thiel = edge/
  monopoly, Munger = inversion/failure, Bezos = customer/demand) + **competitor-steelman** + the
  **doctrine angles** (`forward-deployed-founder` no-distribution, `lean-startup` riskiest-assumption) +
  **≤1 idea-type specialist** (the founder may swap any seat).
- Dispatch `objection-lens` **in parallel**, once per persona seat, each channelling the named
  `*-perspective` SKILL.md to fire **one sharpest objection** → 1 falsifiable assumption + 1
  past-behaviour interview question. Dispatch `competitor-steelman` (writes its provenance).
- Dispatch `disconfirmation-judge`: dedupe + risk-rank into **~5–8 OPEN assumptions** + interview
  questions. An objection **closes only on a hard, checkable fact** (legality / technical feasibility);
  everything subjective stays **OPEN → interview question**. The judge may *flag* a fatal-flaw-class issue
  (illegal/impossible) with cited evidence — it does **not** act on it.

## Gotchas

- **No kill, no rebuttal.** A weak-looking idea advances with sharper interview questions; "no moat /
  crowded / might not pay" are OPEN assumptions, not deaths.
- Keep the brief **testable and short** (~5–8 assumptions) — it's the pre-registration source for the
  kill-criteria, not an exhaustive critique.

## Output

`ideas/<slug>/disconfirmation-brief.md` (`assets/disconfirmation-brief-template.md`) + `disconfirmation/`
provenance. Next: `/market-map`, then `/customer-discovery-design` (which builds the interview pack from
this brief's OPEN assumptions).

## Workers & references

- Workers: `objection-lens` (×panel, parallel), `competitor-steelman`, `disconfirmation-judge`.
- Panel roster: `../idea-stage/references/expert-lens-map.md`. Template: `assets/disconfirmation-brief-template.md`.
