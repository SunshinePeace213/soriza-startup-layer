# Design Contract: `/customer-discovery` — Soriza Startup Layer, Stage 5

> Produced by `/grill-me` (2026-06-03). This is the design contract the `/prompt-architect`
> build consumes. Source method: *The Founder's Playbook: Building an AI-Native Startup*,
> "Plan and design customer discovery" (target profile → interview framework → post-interview
> analysis → outreach & scheduling). Stage sits after `/market-research`, before MVP.

## One-paragraph summary

`/customer-discovery` is the Claude Code skill for Stage 5 of the Idea Stage pipeline. It is a
**design + synthesis engine** that turns the upstream `pressure-test.md` Kill Criteria /
Disconfirmation Questions and `market-research.md` buyer map into (a) a precise target profile +
reachability map, (b) per-persona, kill-criteria-anchored interview guides, and (c) a sealed,
paste-and-go **Cowork run-pack** that drives the *operational* outreach/scheduling/tracking on a
separate surface. After the founder runs interviews, the same skill (synthesis phase) scores the
evidence against the **pre-registered, locked** kill-criteria thresholds and produces a
`customer-discovery.md` Discovery Read. The skill **structurally cannot send email** — sending is
exclusively Cowork's job, gated per batch.

## The seam (root decision, Q1) — "think vs. send"

| Surface | Owns | Why |
|---|---|---|
| **Claude Code** `/customer-discovery` | target profile, interview guides, post-interview synthesis, bias-check; **emits** `cowork-runpack.md` (drafts, NOT sent) | reasoning/design work; one-shot, reversible, internal; keeps the `docs/ideas-stages/` file-contract + "what's next" chaining |
| **Cowork + Gmail/Calendar/Drive MCP** | build/enrich prospect list, personalized outreach, scheduling, day-7 follow-up cadence, live tracking sheet | long-running (multi-day cadence), outward-facing, irreversible; persistent subagent coordination runs while the founder is on shift |

Seam in practice: **Cowork tracks _that_ you talked to someone (status, schedule); the repo holds
_what they said_ (notes, synthesis, kill-criteria verdicts).** Ops data vs. reasoning data.

## Resolved decision tree (Q1–Q11)

1. **Seam (Q1):** split at think-vs-send. Skill = design+synthesis + emits run-pack; Cowork+MCP = ops. *(MCP-from-Claude-Code is a documented fallback only, never primary.)*
2. **Skill shape (Q2):** ONE phased skill, phase auto-detected by folder state. Synthesis stays in Claude Code as **append-rounds** (mirrors `market-research`'s timestamped-round resume). Cowork stays pure ops.
3. **Entry guard (Q3):** hard-require `pressure-test.md` (it defines what discovery tests). Fold in `market-research.md` if present, else warn + explicit-proceed. Always read `hypothesis.md` + `docs/founder-profile.md`. **Loudly reframe a `kill-suggested` verdict** as "go trip-or-clear these kill criteria with real people."
4. **Notes & files (Q4):** in-repo templated notes — one `interviews/<date>-<prospect>.md` per conversation; synthesis reads the folder. Interview guide is **per-persona** when the hypothesis names several (the running idea names four: PM / marketer / dev / founder). Cowork owns the tracking sheet; repo owns transcripts.
5. **Send gate (Q5):** **structural** — the skill's `allowed-tools` exclude all send-capable MCP tools, so it cannot email anyone; it only writes files. The run-pack encodes a conservative Cowork protocol: per-batch founder approval, ~5–10/day ramp, full per-recipient personalization, opt-out line, auto-stop on bounces/complaints, channel-norm respect. Plus a non-legal pre-flight jurisdiction note (HK PDPO / EU GDPR / US CAN-SPAM) and a nudge toward warm/community channels.
6. **Run-pack (Q6):** **sealed, self-contained, paste-and-go.** Everything Cowork needs is inlined (mission, target-profile excerpt, sourcing rules, per-persona templates, send-gate protocol, scheduling rules, follow-up cadence, tracking schema, MCP-setup reminder, report-back contract). Zero dependence on Cowork seeing the repo.
7. **Tracking (Q7):** live **Google Sheet** via Drive MCP (Cowork-owned, phone dashboard) + a **round-boundary CSV snapshot** dropped into `customer-discovery/prospects-<date>.csv` that **the synthesis phase reads to flag coverage skew** (e.g., "all PMs, no marketers" → checks the willingness-to-pay denominator). Schema: Name / Role / Company / **Persona** / Channel-found / Contact / **Proximity-to-pain rank** / Outreach-status / Follow-up-due / Interview-scheduled / Interview-done / **Notes-link** (bridge to repo).
8. **Interview Qs (Q8):** **generate-then-audit, kill-anchored.** Generate a per-persona guide where *every* question is anchored to a specific Kill Criterion / Disconfirmation Question + its **trip-threshold**, past-behavior framed ("tell me about the last time…", never "would you use…"); then run the **Mom-Test audit** on the skill's own output (flag + rewrite any leading / future-facing / too-broad / socially-desirable question); AND offer to audit questions the founder drafts. Design 2–3 deflection probes per persona.
9. **Read type (Q9):** **scored criteria + soft call.** Each pre-registered kill criterion is mechanically scored **TRIPPED / CLEARED / INCONCLUSIVE** vs its **LOCKED** threshold (report `n` + small-sample caveat; *no relitigating the threshold after seeing data*). Overall **CONTINUE / PIVOT / KILL / KEEP-DISCOVERING** is non-binding, but proceeding past a TRIPPED criterion is **stamped as an explicit override on record** (pressure-test style). Plus two-list evidence (supports / challenges) + coverage-skew flag. *Directly counters the founder's documented "concede the diagnosis, keep the prescription" failure mode.*
10. **Fan-out (Q10):** **targeted.** (a) One **design worker per persona** in parallel (guide + outreach template + reachability notes). (b) A **separate, adversarial bias-check agent** at synthesis — independent of the agent that wrote the read, given notes + read + coverage snapshot, prompted to *refute* the read and find where it flatters the founder. Everything else inline. *The bias-check MUST NOT be the same context that wrote the read.*
11. **Modality (Q11):** **live-first within computed overlap windows, async fallback.** Skill computes evening-HKT / off-day availability and bakes the real overlap windows (HK evening = US-East morning / EU afternoon) into the run-pack so Cowork's Calendar MCP only proposes both-sides-sane slots (no 3am calls; US-West → async). Live = default (real-time deflection-probing). Structured async written/voice subset = fallback for unschedulable / lower-priority prospects. Cadence: synthesize every 5; aim ~10–15 total; small-n caveats always on.

## File layout (deliverable + provenance)

```
docs/ideas-stages/<slug>/
├── customer-discovery.md            ← THE deliverable: the Discovery Read action card (feeds MVP)
└── customer-discovery/
    ├── kill-criteria.json           ← the LOCKED thresholds (write-once, Step D2)
    ├── persona-<slug>.md            ← one per persona: sub-profile + kill-anchored guide + outreach drafts
    ├── target-profile.md            ← merged profile + reachability map + proximity ranking
    ├── cowork-runpack.md            ← sealed paste-into-Cowork brief — drafts, NOT sent
    ├── prospects-<date>.csv         ← round-boundary snapshot of the Google Sheet (synthesis reads)
    ├── interviews/
    │   └── <date>-<prospect>.md     ← per-interview notes/transcript (founder fills)
    └── synthesis/
        ├── round-<N>-scoring.json   ← per-interview tags (scorer input)
        └── round-<N>.md             ← script output + bias-check challenge (append-round)
```

## Discovery Read — `customer-discovery.md` structure

```markdown
# Customer Discovery: <project-name>

> This Read scores REAL interview evidence against the kill criteria you pre-registered in
> pressure-test.md BEFORE collecting data. Thresholds are locked. n is small — read the caveats.

## Discovery Read
<CONTINUE | PIVOT | KILL | KEEP-DISCOVERING> — 1 line + rationale tied to evidence (non-binding;
override stamped if proceeding past a TRIPPED criterion)

## Kill-Criteria Scorecard
| Kill criterion (from pressure-test.md) | Threshold (LOCKED) | Evidence | n | Status |
|---|---|---|---|---|
| ... | <pre-registered> | ... | k/N | TRIPPED / CLEARED / INCONCLUSIVE |

## Evidence — two lists
**Supports the hypothesis:** ...
**Challenges the hypothesis:** ...
*(If supports >> challenges, the bias-check interrogates whether that asymmetry is in the data or in the hope.)*

## Coverage & skew (from prospects-<date>.csv)
Interviewed by persona/channel; gaps that bias the Read (e.g. "WTP 18% = founders only").

## Bias-check (independent agent)
Where the Read pattern-matches to what the founder hoped, not what the data says.

## Hypothesis Updates Flagged
Route to /sharpen-hypothesis; do not edit hypothesis.md here.

## Override (only if proceeding past a TRIPPED criterion)
<verdict> | Override: founder proceeded past TRIPPED <criterion> on <ISO-date>
```

## Build spec for `/prompt-architect` (Q12 = full package)

- **Artifact:** one Claude Code **skill** `customer-discovery` (naming matches `sharpen-hypothesis` / `pressure-test` / `market-research`).
- **Subagents** (`.claude/agents/`): `customer-discovery-personas-worker` (per-persona guide + template + reachability), `customer-discovery-bias-check` (adversarial synthesis refuter). Dedicated definitions, like `market-researcher` / `competitor-steelman`.
- **Reference files** (`references/`): Mom-Test audit checklist; kill-criteria-anchoring spec (criterion → past-behavior question → trip-threshold → deflection probe); sealed run-pack template; Discovery-Read action-card template.
- **`allowed-tools`:** AskUserQuestion, Read, Write, Bash, Glob, Agent/Task, WebSearch, WebFetch, Skill. **Exclude every send-capable `mcp__*` tool** (structural send-ban, Q5).
- **Triggering / "what's next" precedence (extend the chain):** no `hypothesis.md` → `/sharpen-hypothesis`; `hypothesis.md` only → `/pressure-test`; `pressure-test.md` → `/market-research`; **`market-research.md` exists → `/customer-discovery`.** Also: design phase vs synthesis phase auto-detected by folder state. Update `market-research`'s exit message to point here.
- **Effort:** high (per-persona workers + bias-check carry their own).
- **Gotchas to encode:** create subdirs before dispatching writers; never edit `hypothesis.md`; bias-check must be a separate context; thresholds are read from `pressure-test.md` and never relitigated; degrade gracefully if no spawn tool; honesty rule on small-n / coverage skew.

## Composition

- **Upstream:** `/market-research` (and `/pressure-test` for the Kill Criteria + Disconfirmation Questions). Floor guard = `pressure-test.md`.
- **Downstream:** MVP stage (not yet built) consumes `customer-discovery.md`. Hypothesis updates route back through `/sharpen-hypothesis`.
- **Off-surface:** Cowork (+ Gmail/Calendar/Drive MCP) executes the run-pack. Not a versioned artifact — generated per-run as `cowork-runpack.md`.
