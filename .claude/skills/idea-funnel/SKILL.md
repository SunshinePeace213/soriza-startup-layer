---
name: idea-funnel
description: |
  Run the Idea-Stage Validator — an automated, lean-startup distillation funnel that takes MANY
  startup ideas (a founder thesis to expand, or a supplied list) through a founder-aware fit-screen,
  a testability gate, an evidence-based disconfirmation pass (expert objections turned into interview
  questions, not debate-kills), and niche-first demand detection — then ranks the survivors and builds
  a SEALED customer-discovery pack for the single best one. Never returns empty. Stops before any
  outreach is sent. Use for "validate these ideas", "run the idea funnel", "distill my ideas",
  "test 100 ideas", "run the whole idea stage". Launches the idea-funnel-engine workflow.
when_to_use: |
  Use when the founder wants to test/validate MANY ideas at once or expand a thesis into ideas and
  distill the best one to take to customers — "run the idea funnel", "validate these N ideas",
  "distill my ideas to the best one", "test these startup ideas", "run the whole idea stage
  automatically", "which idea should I take to customers". For ONE idea through the standalone human
  pipeline, route to /customer-discovery (synthesis) or /solution-design as appropriate.
argument-hint: "[thesis | 'seeds']"
allowed-tools: Read, Glob, AskUserQuestion, Workflow
effort: high
---

# Idea-Stage Validator — `/idea-funnel`

The front door to the funnel. You gather the inputs, launch the **idea-funnel-engine** workflow, then
render the result and explain the two-phase model. The engine owns all the orchestration; your job is
**launch + render + frame the boundary**. The load-bearing runtime rules live in
[`references/`](./references/) — this skill folder is the single source of truth for its runtime.
(CONTEXT.md and docs/adr are optional human background/rationale only; nothing here reads them at
runtime.)

## What the funnel is (and isn't)

This is a **lean-startup tester**, not a VC-incubator filter. Its job at the desk is to **rank,
sharpen, and route** — not to kill on a bar. It keeps working the founder's ideas until at least one
is a strong, testable starting point with a sharp discovery pack, then stops. It does **not** chase
PMF — that's downstream (real users + the PoC workflow).

- **Never empty.** Desk stages almost never kill. The only desk deaths are the **3 fatal flaws**:
  ① illegal/impossible · ② demand **provably negative** (graveyard of unused identical free tools,
  documented failed clones, review-mining shows the pain isn't felt) · ③ **no reachable audience at
  all**. Everything else — "no moat / incumbent exists / market small / they might not pay" — becomes
  an **interview question** and a **rank**, not a death. Weak-but-not-fatal ideas rank low and queue
  alive (resurrectable).
- **Real users are the only validator** of subjective merit. The desk never renders a final verdict.
- **Two axes, never fused.** The IDEA is judged **founder-blind** (generation, disconfirmation,
  demand research ignore the profile). FIT is judged **founder-aware** by one isolated fit-screen.
  The board shows them as **two separate columns** — a `demand-strength` column and a `founder-fit`
  column — never blended into one hidden number.

## The flow (one screen) — TWO PHASES

```
╔════════ IDEA-FUNNEL (automated, batch — this skill launches it) ════════╗
║ generate (founder-BLIND, wide, n=10 default)                            ║
║   → fit-screen     (FIT axis: capability/legal/geo/language; ignore $/time)
║   → hypothesis     (testability)                                         ║
║   → disconfirmation (expert debate → interview questions; NO kill)       ║
║   → demand-detect  (niche-first reachable demand; NO size kill)          ║
║   → CHECKPOINT     (drop ONLY 3 fatal flaws · rank · cap top-K=1)        ║
║   → PHASE A        (customer-discovery DESIGN: SEALED pack, drafts only) ║
║                                ⛔ HARD STOP — funnel ends here           ║
╚═════════════════════════════════════════════════════════════════════════╝
        │  (the founder owns everything below, per-idea, on the survivor)
        ▼
   PHASE B (human + Cowork, WARM-FIRST)  →  days–weeks
        ▼
   customer-discovery SYNTHESIS (reused skill) → verdict (4 buckets)
        ▼
   VALIDATED → solution-design ("forming solutions") → MVP brief → exits Idea stage → PoC workflow
```

## Step 1 — Gather inputs (don't over-ask)

Determine the mode and collect only what's missing:

- **Thesis mode** — the founder gives a theme/thesis to expand. Need: `thesis` (string). Optional `n`
  (seeds to generate, **default 10**).
- **Ingest mode** — the founder supplies their own ideas. Need: `seeds` — an array of
  `{ title, problem, who, why_now, idea_type? }`. Accept a pasted list and normalize it. `idea_type`
  drives lens routing, so tag it where you can.
- **Optional for both:** `k` (Shortlist cap — **default 1**, only set it if the founder overrides),
  `resurrect` (array of Candidate IDs to re-enter from a prior run), `coworkSharePath` (a path to a
  Cowork share to also write the run-pack to, if the founder uses one).

If neither a thesis nor seeds is available, ask one question to get one. Don't re-ask the cap or
anything already in `docs/founder-profile.md`.

## Step 2 — Launch the engine

Call the **Workflow** tool with the engine script and the assembled args:

- `scriptPath: ".claude/workflows/idea-funnel-engine.js"`
- `args: { thesis?, seeds?, n?, k?, resurrect?, coworkSharePath? }` — pass a real JSON object.
  Defaults are **n=10, K=1**; omit them to take the defaults.

The run executes in the background; watch it with `/workflows`. It cannot pause for input (by design),
so let it run through demand-detection, the checkpoint, and Phase A.

## Step 3 — Render the board (SEPARATE demand + fit columns)

The engine returns `{ run_label, ledger, shortlist_doc, shortlist, counts }` and the **ledger-writer**
has already written the board. Show the founder:

- **Funnel counts** (entered → cleared the desk → shortlisted), the cap **K** with its profile
  justification, and a note that any non-shortlisted survivors are **queued alive**, not dead.
- **The board**, with **two unfused columns** per idea: a `demand-strength` column (founder-blind,
  the primary rank key) and a `founder-fit` column (the isolated fit-screen score, shown alongside
  as a tiebreaker). Make clear these are never blended.
- **The survivor (≤K)** — its testable hypothesis, the **open assumptions / interview questions** the
  disconfirmation pass surfaced, the **reachable niche** (where they congregate) and unsolved
  complaints, and the path to its **SEALED Phase A pack**.
- Where the full board lives: `docs/ideas-stages/_funnel-runs/<run_label>/ledger.md`.

If a desk death happened, it cleared only on a cited fatal flaw (illegal/impossible · provably-dead
demand · no reachable audience). The run **never returns empty unless every seed hit a fatal flaw.**

## Step 4 — Explain the two-phase boundary (do this every run)

State it plainly: **the funnel stops at the sealed Phase A pack. Nothing has been sent or posted.**
Then walk the founder through what happens next — this is the load-bearing handoff:

- **Phase A (done, by the funnel):** the sealed run-pack — target profile, reachability map, a
  **warm list** of real people who already publicly complained (with their words + a drafted
  contextual reply for each), a Mom-Test interview guide built from the open assumptions, secondary
  cold-email drafts, and a tracking sheet. **Drafts only — the funnel never sends or posts anything.**
- **Phase B (the founder runs it, warm-first):** *you* post the warm replies / community posts from
  your own account; **Cowork** sends the cold emails and schedules calls on your **per-batch
  approval**; 1:1 interviews are the richest signal. Strong objective demand → a **shorter
  confirmatory** round (~3–5 interviews on willingness-to-switch/pay); weak/ambiguous → fuller
  discovery. This takes days–weeks. (No landing page / waitlist here — that's the PoC workflow.)
- **Then SYNTHESIS:** when interviews are in (synthesize in batches of ~5), run the reused
  **`customer-discovery` SYNTHESIS** phase on the **single survivor**. It scores the open assumptions
  against real evidence, bias-checks, and returns one of four verdicts the founder confirms or
  overrides — **VALIDATED** (→ forming solutions) · **INCONCLUSIVE** (do ~5 more) · **PIVOT**
  (re-enter at hypothesis/market) · **INVALIDATED** (drop → promote the next queued idea or
  regenerate).
- **Then forming solutions:** on a VALIDATED idea, run **`solution-design`** to develop and challenge
  the concept against the problem the interviews actually revealed → solution concept + MVP brief.
  That **exits the Idea stage** → hands to the PoC workflow (out of scope here).

## Step 5 — Appeal / resurrect (on request)

If the founder disagrees with a desk kill (one of the 3 fatal flaws), they appeal: re-launch with
`resurrect: ["cand-..."]` and the killed Candidate re-enters the funnel where it was cut. The ledger
is stateful — settled Candidates aren't re-run (cheap re-runs), and a re-run promotes the next-ranked
queued survivor when the current one resolves.

## Boundaries

- **Never send or post outreach.** The funnel ends at the sealed Phase A pack; sending warm replies is
  the founder's job and cold email/scheduling is Cowork's, gated per batch. This skill has no send
  tool and the engine sends nothing.
- **Don't kill on subjective merit.** No moat / small market / "might not pay" are interview
  questions, not desk deaths. Only the 3 fatal flaws clear an idea at the desk.
- **Keep the two axes separate.** Never fuse demand-strength and founder-fit into one number.
- **Don't hand-orchestrate the gates.** The engine owns the pipeline; your job is launch + render +
  frame the boundary.
