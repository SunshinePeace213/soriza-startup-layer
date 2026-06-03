# The Cowork Run-Pack

`cowork-runpack.md` is the one artifact that runs on a surface this skill can't see into. **Cowork is
headless from the repo's perspective** — it cannot read `target-profile.md` or `interview-guide.md`. So
the run-pack is **sealed**: everything Cowork needs is inlined. The founder connects Gmail/Calendar/Drive
MCP in Cowork, pastes this file, and it runs.

The seam it enforces: Cowork does the *labor* (build list → draft → schedule → follow-up → track) but a
human approves the *trigger* (each send batch). The skill never sends; Cowork sends, gated.

## Structure (compose all sections inlined)

```markdown
# Cowork Run-Pack — Customer Discovery: <slug>

## Mission
Run customer-discovery outreach for <one-line idea>. Goal: book ~10–15 interviews across the personas
below, in the founder's overlap windows. You build the list, draft outreach, schedule, follow up, and
keep the tracking sheet current. You do NOT send any email without per-batch approval (see Send Protocol).

## Target profile (inlined — your sourcing spec)
<for each persona: titles, company type, seniority, and the ranked reachability channels — communities,
Slack workspaces, subreddits, LinkedIn groups, events — proximity-to-pain order>

## Sourcing rules
- Source from the channels above, highest proximity-to-pain first.
- Qualify against the profile before adding — a wrong-fit contact wastes a scarce interview slot.
- Target a working list of ~3–4× the interview goal (reply rates are low).

## Outreach templates (per persona — personalize every send)
<per-persona email drafts with personalization slots; each ends with a plain opt-out line>

## SEND PROTOCOL (the gate — do not skip)
- Draft a batch, show the founder the batch, and WAIT for explicit approval before sending.
- Batch size 5–10/day from a personal Gmail; ramp slowly — protects deliverability and reputation.
- One personalized email per recipient (no mail-merge blasts).
- Auto-stop and report if bounces or spam complaints appear; do not keep sending into a degrading sender reputation.
- Respect each channel's norms — do not blast a Slack workspace or DM-spam a community.

## Scheduling (overlap windows only)
- Founder availability (from founder-profile): <inlined availability, e.g. evenings + off-day mornings, HKT>.
- Propose live slots ONLY where the founder's window overlaps the prospect's working hours (see logic below).
- Use Gmail + Calendar MCP to offer 2–3 concrete slots, confirm, and place the event with a video link.
- Prospects who can't do live, or are lower priority: send the async question subset instead (inlined below).

## Follow-up cadence
- Day-7 follow-up draft for any contact who hasn't replied (one polite nudge, then stop).
- Update the tracking sheet after every state change.

## Tracking sheet (create in Google Sheets via Drive MCP)
Columns: Name | Role | Company | Persona | Channel-found | Contact | Proximity-rank |
Outreach-status (not-contacted/sent/replied/bounced/opted-out) | Follow-up-due | Interview-scheduled |
Interview-done | Notes-link

## Report-back contract
At each round boundary, give the founder: (1) a one-line status (sent / replied / scheduled / done counts),
(2) the list of scheduled interviews with times in the founder's timezone, and (3) a CSV export of the
sheet to drop into the repo as `customer-discovery/prospects-<date>.csv`.

## MCP setup (before running)
Connect Gmail, Google Calendar, and Google Drive (the authenticate flow). If any is missing, say so and
do only the steps that don't need it (e.g. build the list, draft emails) until it's connected.
```

## Overlap-window scheduling logic

Compute the windows once, from the founder's availability (in `founder-profile.md`) and the target
geographies, and inline the result into the Scheduling section. A live slot is viable only where the
founder's available hours overlap the prospect's normal working hours (~9–18 local).

Derive **all** recurring windows from the founder's actual schedule — a rotating shift pattern often
yields more than one (e.g. an evening window on some days and a morning window on others, each serving
different geographies). Don't stop at the single illustrative case below.

Worked example — founder available **HK evenings (~20:00–23:00 HKT)** + **off-day mornings**, targeting a
global English-speaking market:

| Founder window (HKT) | Lands at | Viable? |
|---|---|---|
| 21:00–23:00 | US-East 08:00–10:00 | ✓ prime |
| 20:00–23:00 | London 12:00–15:00 | ✓ prime |
| off-day 08:00–10:00 | US-East 19:00–21:00 (prev day) | ✓ workable |
| evening | US-West ~05:00 | ✗ → async |

Rule of thumb: HKT evenings serve **US-East + Europe** live; **US-West** routes to async. Recompute for the
founder's actual availability and target geos — never offer a slot that lands in either party's night.

## Async question subset

For unschedulable or lower-priority prospects, inline a structured written/voice-memo version of the guide
— the same kill-anchored questions, framed for a written answer, with the note that follow-up probing will
be weaker (lower-richness signal). Keep it short; ask for the *last specific time*, same as live.
