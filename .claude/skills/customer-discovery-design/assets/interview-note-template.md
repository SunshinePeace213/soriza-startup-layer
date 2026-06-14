# Interview Note — capture template (emoji legend)

Copy this into `ideas/<slug>/customer-discovery/interviews/<date>-<prospect>.md`, one file per
conversation. **Capture behaviour, in their words.** Messy is fine; empty is not. The synthesis step
(`/customer-discovery-synthesis`) extracts the ledger and scores the kill-criteria from these notes — so
what you write here is what becomes evidence.

> Two non-negotiables: **(1) verbatim quotes go in "quotation marks"** so synthesis knows it's their
> words (grade-2 evidence), and **(2) write down what they DID, not what they said they'd do.** "Would
> pay" is not evidence; "paid £X last month" is.

---

## Emoji legend (Rob Fitzpatrick's 12 symbols, as emoji)

Tag any line with these so signals are sortable later. Make up more in the field as needed.

| Emoji | Means | Why it matters |
|---|---|---|
| ⚡ | **pain / problem** | a real pain — candidate grade-2 quote |
| 🎯 | **goal / job-to-be-done** | what they're actually trying to achieve ("why do you bother?") |
| 🚧 | **obstacle** | what blocks them (e.g. an IT policy) — you'll have to clear it too |
| 🩹 | **workaround** | their duct-tape fix — a strong earlyvangelist tell |
| 🏔️ | **background / context** | situational detail; segment context |
| ✅ | **feature request / buying criterion** | understand the motive behind it; don't just obey it |
| 💰 | **money / budget / buying process** | price anchor, who pays, who can veto |
| 👤 | **specific person / company** | named contact (→ ask for an intro) or competitor (→ research it) |
| ⭐ | **follow-up task** | something you promised or must chase |
| 🤩 / 😠 / 😳 | **emotion: excited / angry / embarrassed** | intensity changes the weight of a "that's a problem" |

**Three signals this pipeline adds (capture them explicitly — synthesis reads them):**

| Emoji | Means | Feeds |
|---|---|---|
| 🤝 | **commitment given** — they gave up something real (time / reputation / cash) | **grade-1 ledger entry** (the strongest evidence there is) |
| ➡️ | **advancement** — a concrete next step actually got booked | the Discovery Read's advancement signal (not a compliment-stall) |
| 🔥 | **earlyvangelist** — "this is the worst part of my life, I'll pay now" energy | the candidate-first-customer line in the Read |

> **Currencies of commitment (🤝), weakest → strongest:** *time* (feedback on wireframes, a real trial, a
> booked next meeting *with an agenda*) → *reputation* (intro to their boss / the budget-holder, agreeing
> to be a named case study) → *cash* (letter of intent, pre-order, deposit). A compliment costs nothing,
> so it is worth nothing — do not record it as a 🤝.

---

## Blank template (copy below this line)

```markdown
# Interview — <role>, <company/context>

- **Date:** <YYYY-MM-DD>   ·   **Persona:** <PM | marketer | developer | founder | …>
- **Channel:** <warm intro | warm reply | cold | meetup | …>   ·   **Medium:** <in person | call>

## What they actually do today (their workflow, last real instance)
- 🏔️ <context: their setup, role, scale>
- ⚡ "<verbatim pain, in their words>"
- 🩹 <the workaround they've cobbled together>
- 💰 <what it costs them today / what they pay / whose budget>

## The last time it came up (specifics, not generics)
- <walk-through of the most recent concrete instance — when, what they opened first, what happened>
- 🎯 <the underlying goal behind the pain>
- 🚧 <obstacle that stops them solving it themselves>

## Signals
- ✅ <feature request / buying criterion — + the motive behind it>
- 👤 <named person/company mentioned — competitor or intro candidate>
- 🤩/😠/😳 <strong emotion + what triggered it>
- 🔥 <earlyvangelist? has the problem + knows it + has budget + already built a workaround + emotional>

## Commitment & advancement (the end of the conversation)
- 🤝 <commitment given: which currency — time / reputation / cash — or "none (compliment only)">
- ➡️ <next step booked: what, when — or "none; conversation ended on a compliment-stall">
- ⭐ <follow-up I owe them / must chase>

## Who else / what did I miss
- 👤 <intro they offered — who, and is it concrete?>
- <"is there anything else I should have asked?" — their answer>
```

---

## Worked example (what "good" looks like)

```markdown
# Interview — Finance Manager, mid-size SaaS

- **Date:** 2026-06-12   ·   **Persona:** finance ops
- **Channel:** warm reply (Reddit complaint)   ·   **Medium:** call

## What they actually do today
- 🏔️ 6-person finance team, closes the books monthly, lives in Excel + a legacy ERP.
- ⚡😠 "Month-end close took us **four days** last month just to reconcile the spreadsheets — it's a
  disaster every single time."
- 🩹 Home-brew: one analyst manually merges 9 exported reports into a master sheet.
- 💰 Pays an outside agency "**about £120k a year**" to keep the reporting site alive.

## The last time it came up
- Last close (week of June 2): pulled reports Mon–Thu, found two mismatches Thu night, re-ran Friday.
- 🎯 Real goal: "be *certain* everyone's working off the latest numbers" — not "better messaging."
- 🚧 IT won't allow a new cloud tool without a security review (8-week queue).

## Signals
- ✅ Asked for "Excel sync" — but the motive is *single source of truth*, not Excel itself.
- 👤 Evaluated Acme Reporting last year; "the sync always broke."
- 🔥 Strong: has the problem, knows it, owns the budget, already built a workaround, visibly angry.

## Commitment & advancement
- 🤝 **time + reputation:** agreed to a 2-week trial *and* to introduce me to their controller.
- ➡️ Next step booked: intro call with the controller, **June 19**.
- ⭐ Send the trial scope doc by June 16.

## Who else / what I missed
- 👤 Controller (budget veto) — intro confirmed for the 19th.
- "You should've asked how we handle audit trails — that's the other half of the pain."
```

This single note yields: multiple grade-2 quotes (⚡), a price anchor (💰 £120k), a grade-1 commitment
(🤝 trial + intro), an advancement (➡️ booked call), and an earlyvangelist flag (🔥) — everything
synthesis needs, none of it invented.
