# Idea-Funnel v2 — Redesign Spec (the build contract)

Status: **design locked** (via `/grill-me`, 2026-06-05). Supersedes the v1 build plan in
[`idea-funnel.md`](./idea-funnel.md). This doc is the single source of truth for the rebuild; it is
self-contained (does not require reading CONTEXT.md / ADRs to implement).

> Note: per the self-containment decision (§9), the *runtime rules* below are authoritative and will be
> inlined into the skill's own `references/`. CONTEXT.md and the ADRs remain **human background /
> rationale only** — no agent reads them at runtime.

---

## 0. Why v2 (what v1 got wrong)

Two live runs killed **22 of 22 ideas** (empty shortlists). Root causes, evidence-backed:

1. **Gate 2 killed on "objection unrebutted by *web* evidence."** A brand-new idea has no public
   evidence to rebut with, so it was guilty-until-proven-innocent at the desk. The kill authority was
   *desk research*, when lean startup + the Founder's Playbook say the authority is **real users**.
2. **Founder-bias at generation.** The seed-generator was explicitly told to *"bias seeds toward the
   founder's market/skills/goals/capital."* This narrowed every run into red oceans (chatbots/HK/his
   skill set) that then died as "no moat, incumbent already ships it." (Confirmed by audit:
   `engine:121`, `seed-generator.md:23`.)
3. **VC-incubator win-condition** (Thiel monopoly / scale lenses as *kills*) applied to an **indie
   bootstrapper** whose goal is a profitable owned business, not venture scale.
4. **Truncated + over-confident:** it rendered a final verdict at the disconfirmation step (desk) and
   never reached the real-user evidence the Playbook says is decisive.

## 1. Core philosophy shift

| | v1 (VC-incubator filter) | **v2 (lean-startup tester)** |
|---|---|---|
| Desk stage's job | **kill** on a bar (bar-to-kill) | **rank + sharpen + route** |
| Who validates | desk evidence | **real users** |
| Win condition | venture-scale moat | **niche + real demand = a market** |
| Output when nothing's perfect | empty shortlist | **never empty** — best ideas ranked + routed to testing |
| Goal | a shortlist | **idea(s) that survive to *ready-to-test*** |

The funnel **keeps testing the founder's ideas until at least one is a good *starting point*** — a
strong, testable hypothesis with a sharp discovery pack — then stops. It does **not** chase PMF
(that's downstream, via real users + the PoC workflow).

## 2. The flow (and where the funnel starts/stops)

```
╔══════════════ IDEA-FUNNEL WORKFLOW (automated, batch, breadth) ══════════════╗
║ generate (founder-BLIND, n=10)                                               ║
║   → fit-screen        (FIT axis — capability/legal/geo only; ignore $/time)   ║
║   → hypothesis        (testability)                                           ║
║   → disconfirmation   (expert debate → Disconfirmation Brief; NO kill)        ║
║   → market research   (demand-detection, niche-first; NO size kill)           ║
║   → CHECKPOINT        (drop only 3 fatal flaws · rank · cap top-K=1)          ║
║   → Phase A           (customer-discovery DESIGN: sealed, drafts only)        ║
║                                  ⛔ HARD STOP (irreversible send line)         ║
╚══════════════════════════════════════════════════════════════════════════════╝
        │  (founder owns everything below; per-idea, on the survivor)
        ▼
   PHASE B (human + Cowork, warm-first)  →  takes days–weeks
        ▼
   customer-discovery SYNTHESIS (reused skill) → verdict (4 buckets)
        ▼
   VALIDATED → solution-design ("forming solutions") → MVP brief
        ▼
   ⇒ exits the Idea stage → PoC workflow (landing page + waitlist) [SEPARATE]
```

## 3. The elimination model (what may kill, and where)

Desk stages **almost never kill.** The complete list of desk eliminations:

| Where | Kills ONLY on (objective, checkable) |
|---|---|
| Fit-screen | **durable-impossible** founder mismatch (can't legally/linguistically/geographically serve it; needs hardware/heavy-regulated licensing). **Money/time/runway ignored.** |
| Hypothesis gate | cannot be made into a **testable** hypothesis (who/how-often/how-severe/status-quo) after one sharpening pass |
| Disconfirmation + market | the **3 fatal flaws**: ① illegal/impossible · ② demand **provably negative** (graveyard of unused identical free tools, documented failed clones, review-mining shows the pain isn't felt) · ③ **no reachable audience** at all |

**Everything else never kills** — "no moat / incumbent exists / market small / they might not pay"
become **interview questions** and a **rank**, not deaths. Weak-but-not-fatal ideas **rank low and
queue alive** in the ledger (resurrectable). **Real users are the only validator** of subjective
merit.

## 4. Two-axis neutrality (idea-blind vs founder-aware)

The skill is **neutral** in the sense that the *idea evaluation* never bends to flatter the founder,
and the artifact is **general-purpose** (profile read as runtime *data*, works for any founder).

- **IDEA axis — founder-BLIND.** Generation, disconfirmation, market/demand research judge the idea
  **on its own merits** and **do not read the founder profile.** (This is the fix for the v1 bias and
  the Playbook's "loss of objectivity" trap.) **Generation is thesis + real-demand driven, wide** —
  not bent toward the founder.
- **FIT axis — founder-AWARE, isolated, explicit.** A single **fit-screen** reads the profile *only*
  for objective capability (legal/geo/language/buildable-surface), drops on true impossibility, and
  emits a **transparent fit score**.
- **Ranking shows both, unfused:** a `demand-strength` column (blind) and a `founder-fit` column
  (explicit). Never blended into one hidden number.

## 5. Per-stage spec

### 5.1 Generate (founder-blind)
- **In:** thesis (or founder-supplied seeds), grounding sweep (real trends/demand).
- **Do:** expand to **N=10** thin seeds (overridable), **wide**, **founder-blind** — driven by the
  thesis + real demand, NOT the founder profile. Tag each `idea_type` accurately (drives lens routing).
- **Out:** 10 seeds. **No kill.**
- **Change vs v1:** remove the "bias toward the founder" instruction (`engine:121`,
  `seed-generator.md:23`).

### 5.2 Fit-screen (FIT axis)
- **In:** seed + founder profile (as data).
- **Do:** assess **durable** capability/legal/geo/language fit; **ignore money/time/runway**.
- **Kill:** only on durable-impossible mismatch. **Out:** `{drop|keep, fit_score, reasons}`.

### 5.3 Hypothesis gate (testability)
- **Do:** sharpen to a testable hypothesis (who · how-often · how-severe · status-quo).
- **Kill:** only if not testable after one pass. **Out:** `hypothesis.md` + score. (founder-blind)

### 5.4 Disconfirmation → **Disconfirmation Brief** (no kill)
- **Do:** keep the **expert debate** (objection-lenses + competitor-steelman) — the angles are
  valuable. Convert each strongest objection into a **falsifiable assumption + an interview question.**
- **Rebuttal handling:** the AI does **not** debate-rebut. It marks an objection **closed only when a
  hard, checkable FACT settles it** (legality, technical feasibility). **Everything subjective**
  (demand, willingness to pay, behavior) **stays OPEN → interview question.**
- **Kill:** none here (except it may *surface* a fatal flaw → handled at checkpoint).
- **Out:** ranked risk list + the open assumptions/questions. (founder-blind)

### 5.5 Market research → **demand-detection** (niche-first)
- **Do:** detect a **reachable niche showing real demand** — who already *pays / complains / hacks a
  workaround* — **however small.** Mine existing public conversations (Reddit/X/HN/forums/reviews) for
  real-user language + unsolved complaints. Map competitors (context, not a kill).
- **Kill:** only ③ no reachable audience or ② provably-negative demand. **Size never kills.**
- **Out:** demand-signal strength + reachable niche + unsolved complaints. (founder-blind)

### 5.6 Checkpoint → **Go-to-Discovery Card** + rank + cap
- **Compile per idea:** hypothesis · open assumptions (from 5.4) · reachable niche + where they
  congregate · unsolved complaints · demand signals · fit score.
- **Kill:** only the 3 fatal flaws (now that research is in hand).
- **Rank:** primarily by **demand strength** (blind); **fit score shown alongside** (separate column +
  tiebreaker). Never fused.
- **Cap:** top-**K=1** (overridable) → Phase A. Rest **queued alive**.

### 5.7 Phase A — customer-discovery DESIGN (sealed, drafts only)
For each top-K idea, build the **ready-to-test pack**:
1. **Target profile** (role · context · segment).
2. **Reachability map** (named subreddits, X hashtags, forums, Discord/Slack, LinkedIn groups).
3. **Warm list ★** — real people who *already publicly complained*, each with `{link · their words ·
   drafted contextual reply/DM}`.
4. **Interview guide** — Mom-Test, past-behaviour, bias-audited, built from the open assumptions.
5. **Cold-email drafts** (secondary) for named prospects without a warm thread.
6. **Tracking sheet** (prospect · channel · status · follow-up · done).
- **Out:** one **SEALED** run-pack per idea. **Nothing sent.** ⛔ **Funnel ends here.**

## 6. Customer discovery — the human/automation boundary

Three layers by automation level:

| Layer | What | Who | Automated? |
|---|---|---|---|
| Demand-mining | read existing public threads for demand + language | **Agent** (in funnel) | ✅ fully (reading only) |
| Phase A prep | profile, reachability, warm list, guide, drafts | **Agent** (in funnel) | ✅ drafts only — nothing sent |
| Phase B execution | post / send / interview / collect | **You** (Cowork assists) | ⚠️ human-gated |

**Channel priority = Option A:** demand-mining + **warm** replies to existing complaints **first**;
cold email secondary; 1:1 interviews are the richest signal. **No landing page / waitlist here** —
that's the PoC workflow.

**Send/post line:** the agent **never sends or posts.** Agent drafts every channel → *you* post warm
replies / community posts (your account, platform rules) → **Cowork** sends email + schedules on your
**per-batch approval** → synthesis is agent-assisted.

**Tiered Phase B:** strong *objective* demand signal → **shorter confirmatory** interviews (~3–5,
focused on willingness-to-switch/pay) → then forming solutions → PoC. Weak/ambiguous → fuller
discovery. **Never a full skip** to PoC — interviews (the *why* + problem shape) and the PoC waitlist
(*will they act*) are **complementary**, and a wrong problem-shape makes the landing page test the
wrong promise.

## 7. Synthesis verdict (after Phase B) — agent-decided, founder-confirms

Reuse the **`customer-discovery` SYNTHESIS** phase (no new skill). It scores the open assumptions
against real evidence, **bias-checks** (flags pattern-matching to hope), and returns a verdict the
founder **confirms or overrides** — the founder never has to self-classify. Synthesize in batches of
**~5 interviews**.

| Verdict | Evidence rule | Next |
|---|---|---|
| **VALIDATED** | several *independent* users confirm problem real + frequent + painful **and** show *revealed* willingness (pay/switch/workaround) | **forming solutions** |
| **INCONCLUSIVE** | thin/mixed signal, < ~5 quality conversations | do ~5 more, re-synthesize |
| **PIVOT** | real pain but a *sharper/different* problem, or right problem **wrong segment** | redesign hypothesis → re-enter at hypothesis / market research |
| **INVALIDATED** | users don't have / don't care; status quo is fine | drop → promote next queued / regenerate |

## 8. Forming solutions → exit

Reuse **`solution-design`** on the **VALIDATED** idea: develop *and* challenge the concept against
**the problem the interviews revealed**; output a solution concept + MVP brief. This **exits the Idea
stage** → hands to the **PoC workflow** (landing page + waitlist) → MVP stage. **PoC is out of scope
for this funnel.**

## 9. Self-containment

- Inline the load-bearing runtime rules (kill criteria, ledger schema, gate definitions) into the
  skill's own `references/`. The skill is the **single source of truth** for its runtime.
- `CONTEXT.md` / `docs/adr` → demoted to **optional human background**; **no agent reads them at
  runtime**. The skill folder is portable (works copied to another repo).

## 10. Skill inventory changes

| Skill | Action |
|---|---|
| `generate-ideas` | **DELETE** (funnel replaces) |
| `sharpen-hypothesis` | **DELETE** |
| `pressure-test` | **DELETE** |
| `market-research` | **DELETE** |
| `customer-discovery` | **KEEP** — SYNTHESIS is first-class; DESIGN superseded by Phase A |
| `solution-design` | **KEEP** — first-class ("forming solutions") |
| gate subagents (`fmf-screen`, `sharpen-gate`, `objection-lens`, `disconfirmation-judge`, `cd-design-gate`) | **REWRITE** prompts to v2 logic; keep the slots |
| evidence-gatherers (`startup-idea-researcher`, `market-researcher`, `competitor-steelman`, `customer-discovery-personas-worker`) | **KEEP**, rewire to v2 logic |

**Deletion timing:** delete the 4 skills **after the new funnel is verified working** (so there's no
gap with no Idea-stage path), and clean up `CLAUDE.md` + cross-skill "what's next" routing in the same
change.

## 11. Params & infra

- **n = 10** seeds default (overridable). **K = 1** pack default (overridable).
- **Stateful ledger** (cross-run memory) + **resurrect/appeal**: **keep**.
- **FIX the v1 infra bug:** the engine inherited a polluted CWD → all file writes (ledger, per-idea
  docs) landed nowhere and 2 ideas were killed by-default on missing files. Ensure agents resolve
  paths against the repo root regardless of caller CWD.

## 12. Acceptance checks (for the build)

1. A novel, evidence-thin idea **survives** to a ready-to-test pack (no desk kill on "no moat /
   unproven demand"). v1 would have killed it.
2. An illegal / unreachable / provably-dead idea **is** killed at the desk, with the evidence cited.
3. Generation **never reads** the founder profile; the fit-screen **does**; the two axes appear as
   **separate columns** in the ledger.
4. The run **persists** (ledger + per-idea docs written under the repo) and **never returns empty**
   unless literally every seed hit a fatal flaw.
5. Disconfirmation output is an **interview brief**, not a verdict; only fact-settled objections are
   closed.
6. The funnel **stops at the sealed Phase A pack** — no outreach is ever sent.
