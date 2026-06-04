# Gate rubrics — the v2 elimination model (what may kill, and where)

This file is the **single source of truth** for the funnel's runtime kill logic. Everything needed to
run the desk stages is inlined here — no other doc needs to be read at runtime.

## The one rule

**Desk stages almost never kill. They rank, sharpen, and route.** The validator of subjective merit
(moat, demand, willingness to pay, "is it big enough") is **real users in Phase B**, never desk
research. A brand-new idea has no public evidence to prove itself with, so the desk must not treat it
as guilty-until-proven-innocent.

A desk stage may eliminate a candidate **only** on an **objective, checkable** condition from the
table below. Everything else — "no moat / incumbent exists / market small / they might not pay" —
becomes an **interview question** and a **rank position**, not a death. Weak-but-not-fatal ideas
**rank low and queue alive** in the ledger (resurrectable), they are not killed.

When in doubt, **advance.** The funnel must **never return empty** unless literally every seed hit a
fatal flaw, and it must keep testing the founder's ideas until at least one survives to a
ready-to-test pack.

## The complete list of desk eliminations

| Stage | Slot | Kills ONLY on (objective, checkable) | Everything else |
|---|---|---|---|
| **Fit-screen** | `gate0_fmf` | **durable-impossible** founder mismatch | → lowers `fit_score`, never kills |
| **Hypothesis gate** | `gate1_sharpen` | **not testable** after one sharpening pass | → lowers score, never kills |
| **Disconfirmation** | `gate2_disconfirmation` | **none** (no kill here) — may only *surface* a fatal flaw for the checkpoint | → open assumptions + interview questions + risk rank |
| **Market / demand-detection** | (part of `gate2`) | one of the **3 fatal flaws** (①②③ below) | → demand-signal strength + reachable niche (ranks, never kills) |
| **Checkpoint** | `gate3_cd_design` precheck | the **3 fatal flaws** (①②③), now that all research is in hand | → rank by demand strength + cap to top-K; rest queued alive |
| **Phase A — CD design** | `gate3_cd_design` | none (produces the sealed pack) | → sealed run-pack only; nothing sent |

> Slot names (`gate0_fmf` … `gate3_cd_design`) are the ledger keys the stages still write to — the
> v2 model renames the *jobs* but keeps the *slots* so the ledger stays stable across runs.

### The 3 fatal flaws (the only desk deaths after research is in hand)

These are the **sole** reasons the checkpoint (or the demand-detection stage that surfaces them) may
kill. Each must be **cited with the evidence** that proves it — no silent or inferred kills.

1. **Illegal / impossible.** The idea cannot be legally offered, or cannot be built at all with the
   available technology (a hard, checkable fact — legality, physical/technical feasibility), not a
   judgement call.
2. **Demand provably NEGATIVE.** Not "unproven" — **proven dead.** Acceptable evidence: a graveyard
   of unused *identical free* tools; documented failed clones; review-mining that shows the supposed
   pain is **not actually felt**. Absence of evidence is **not** evidence of negative demand — unproven
   demand advances (it becomes an interview question).
3. **No reachable audience at all.** There is **no** identifiable community, channel, or list where
   the target could ever be reached for an interview. A *small* or *hard* audience is not fatal —
   only a genuinely **unreachable** one.

---

## Stage rubrics (the runtime detail)

### Fit-screen — `gate0_fmf`  (FIT axis, founder-AWARE)

The only founder-aware desk stage. Reads `docs/founder-profile.md` as **runtime data** (read
`docs/founder-dossier.md` only if a factor is ambiguous). Its job: assess **durable** capability fit
and emit a **transparent fit score** — *not* to kill marginal ideas.

**Kills ONLY on durable-impossible mismatch:** the founder **cannot legally, linguistically, or
geographically serve** the market, or the idea **requires hardware / heavy-regulated licensing** the
founder structurally cannot obtain. These are durable, structural impossibilities — not preferences.

**Ignore money / time / runway entirely.** Capital, capacity, and runway are **never** a fit kill and
do not lower the fit score — they are downstream sequencing concerns, not idea-fitness concerns. (This
is a deliberate v2 change: v1 hard-failed on capital/capacity/regulatory appetite; v2 does not.)

| Dimension | Reads from profile | Durable-impossible (the ONLY kill) | Soft signal (lowers `fit_score` only) |
|---|---|---|---|
| Geography / language | Location & serviceable geography | Requires a market/language the founder structurally **cannot** serve | Weak language/cultural fit for the target |
| Buildable surface | Skills & unfair advantage | Requires hardware or a heavy-regulated **licence** the founder structurally cannot obtain | Stretch beyond current level but learnable |
| Legality of the activity | Risk & regulatory appetite | The activity is **illegal** for the founder to perform in their jurisdiction | Adjacent to regulation (a flag, not a kill) |
| Money / time / runway | — | **never a kill, never lowers the score** | — (ignored) |

A missing/declined fit value is scored **conservatively** for the score, but a blank **never**
manufactures a durable-impossible kill. Output: `{ verdict, fit_score, reasons, hard_fail | null }`.

### Hypothesis gate — `gate1_sharpen`  (testability; founder-BLIND)

Runs the sharpen rubric on the seed's own merits (does **not** read the founder profile). A seed
advances if it **can be made into a testable hypothesis** naming all four dimensions specifically
after **one** sharpening pass.

| Dimension | Specific (pass) | Vague (still vague after one pass = fail) |
|---|---|---|
| WHO | named role + context + segment | "businesses", "people" |
| HOW OFTEN | a frequency | "sometimes" |
| HOW SEVERE | a cost/pain magnitude | "it's annoying" |
| STATUS QUO | what they do now | "nothing" / unknown |

**Kills ONLY if** the hypothesis cannot be made testable — i.e. a dimension stays vague after one
sharpening pass, or the result is unfalsifiable. This is a *testability* kill, **not** a quality kill:
a perfectly testable hypothesis about a weak-looking idea **advances** (its weakness becomes the thing
the interviews test). On advance, write `hypothesis.md` (sharpened sentence + the four dimensions).
Output: `{ verdict, score, reason, testable, hypothesis }`.

### Disconfirmation — `gate2_disconfirmation` → **Disconfirmation Brief**  (NO KILL; founder-BLIND)

Keep the **expert debate** (objection-lenses + competitor-steelman) — the angles are valuable. But the
output is an **interview brief, not a verdict.**

- Each strongest objection is converted into a **falsifiable assumption + an interview question.**
- The AI does **not** debate-rebut. An objection is marked **closed only when a hard, checkable FACT
  settles it** (legality, technical feasibility). **Everything subjective** (demand, willingness to
  pay, behaviour, "no moat") **stays OPEN → becomes an interview question.**
- **This stage never kills.** It may only *surface* a fatal flaw (e.g. an objection that turns out to
  be flaw ① illegal/impossible) — and even then the **kill is recorded at the checkpoint**, with the
  fact cited, not here.

Output: ranked risk list + the open assumptions/questions + any surfaced-fatal-flaw flag.

### Market research — **demand-detection** (niche-first; founder-BLIND)

Detect a **reachable niche showing real demand** — who already **pays / complains / hacks a
workaround** — **however small.** Mine existing public conversations (Reddit / X / HN / forums /
reviews) for real-user language and unsolved complaints. Map competitors **as context, not as a kill.**

**Kills ONLY on fatal flaw ② (demand provably NEGATIVE) or ③ (no reachable audience at all).**
**Size NEVER kills.** A tiny-but-real niche is a *pass* — niche + real demand = a market. Competitor
presence, unproven demand, and "looks small" are **rank inputs and interview questions**, never deaths.

Output: demand-signal strength + reachable niche (where they congregate) + unsolved complaints.

### Checkpoint → **Go-to-Discovery Card** + rank + cap  (`gate3_cd_design` precheck)

With all research in hand, compile per idea: hypothesis · open assumptions (from disconfirmation) ·
reachable niche + where they congregate · unsolved complaints · demand signals · fit score.

- **Kills ONLY on the 3 fatal flaws (①②③),** each cited with its evidence. Nothing else.
- **Rank** primarily by **demand strength** (the founder-blind signal); the **fit score is shown
  alongside** as a separate column and a tiebreaker. **The two axes are never fused into one hidden
  number.**
- **Cap** to top-**K = 1** (overridable) → those go to Phase A. **The rest are queued alive** in the
  ledger (status not killed; resurrectable on a later run). A cap is **not** a kill.

### Phase A — customer-discovery DESIGN — `gate3_cd_design`  (soft; reachability only)

Not a quality kill — the idea already cleared the desk. Produce the **sealed** run-pack (target
profile, reachability map, warm list, Mom-Test interview guide built from the open assumptions,
cold-email drafts, tracking sheet). **Nothing is ever sent — the funnel ends at the sealed pack.**
The only thing that could stop a candidate here is fatal flaw ③ (no reachable audience), which the
checkpoint already screened. Output: `{ verdict, reachable, runpack_path, reason }`.

---

## Two-axis neutrality (carried through every stage)

- **IDEA axis — founder-BLIND.** Generation, disconfirmation, and demand-detection judge the idea
  **on its own merits** and **do not read the founder profile.** Generation is **thesis + real-demand
  driven and wide** — never bent toward the founder's market/skills/goals.
- **FIT axis — founder-AWARE, isolated.** Only the **fit-screen** reads the profile, only for durable
  capability, and emits a transparent `fit_score`.
- The ranking shows both **unfused**: a `demand-strength` column (blind) and a `founder-fit` column
  (explicit). Never blended.

## Logging

Log **every** cut with its one-line reason and the cited evidence — **no silent kills**. A kill that
cannot name flaw ①/②/③ (or a durable-impossible fit mismatch, or an untestable hypothesis) is not a
valid kill: advance instead and let the candidate rank low / queue alive.

---

## Background (human only)

The following are **rationale / design background for humans** and are **not read at runtime** by any
agent — this file is self-contained. They explain *why* v2 dropped the v1 bar-to-kill model:

- `docs/skill-designs/idea-funnel-v2-redesign.md` — the locked v2 build contract (§3 elimination
  model, §5 per-stage spec, §9 self-containment).
- `CONTEXT.md` and `docs/adr/0001`–`0004` — the original v1 design and its decision history (the
  bar-to-kill / harsh-Gate-2 model that v2 replaces). Optional reading; the skill folder is portable
  and does not depend on them.
