# Design Contract: `/solution-design` — Soriza Startup Layer, Stage 6

> Produced by `/grill-me` (2026-06-03). This is the design contract the `/prompt-architect`
> build consumes (it skips its own Phase-1 interview when it sees this grill transcript). Source
> method: *The Founder's Playbook: Building an AI-Native Startup* — "Design your final solution
> concept" (develop **and challenge** the concept from every angle: gaps, alternatives, scale, and
> the reality checkpoint — *does the design address the problem the validation revealed, not the one
> you assumed going in?*). Stage sits after `/customer-discovery`, before the MVP stage (not yet built).

## One-paragraph summary

`/solution-design` is the Claude Code skill for Stage 6 of the Idea Stage pipeline. It is a
**crystallize-then-challenge engine**: it mines the solution concept already *latent* across the
validated evidence (`hypothesis.md` + `pressure-test.md` + `market-research.md` + `customer-discovery.md`),
articulates it into one crisp concept the founder confirms, then attacks it from every angle the
Playbook names — a **drift audit** (does the design serve the problem discovery *validated*, or the one
the hypothesis *assumed*?), the **three most load-bearing assumptions** + what would have to be true for
each, **alternatives**, and **scale conditions** — with a separate-context, **blind** `solution-red-team`
adversary. It writes a `solution-design.md` action card carrying a non-binding **Concept Read**
(`build` / `narrow` / `redesign` / `reconsider`) and a forward **MVP Brief**. The whole skill is aimed
at this founder's one documented failure mode — *"concede the diagnosis, keep the prescription"* — which
**is** drift: discovery revised the diagnosis, but the design keeps serving the old prescription.

## The root decision (Q1) — "crystallize, then challenge"

| The concept is… | …and the skill's job is | Why |
|---|---|---|
| already *implicit* in the validated docs (hypothesis + discovery wedge + market positioning) | **extract & articulate** it sharply, **then challenge** it (drift, assumptions, alternatives, scale) | matches the Playbook's "develop and challenge"; the founder owns the design — the skill sharpens and stress-tests, it does not invent the product |

Not chosen: *generate-and-select* (skill fans out alternative concepts → risks designing the product *for* the founder) or *pure red-team* (founder hand-writes the whole concept → wastes the synthesis leverage of the upstream evidence).

## The spine — the drift audit (assumed → validated)

The reason the stage exists. **The "validated problem" is not just `customer-discovery.md`.** Every
upstream stage emits a *"Hypothesis Updates Flagged"* block, and only `/sharpen-hypothesis` may fold
those back into `hypothesis.md`. Mid-pipeline, `hypothesis.md` is therefore usually **stale**, so the
real validated baseline = **original hypothesis + all accumulated, possibly-unapplied flagged deltas**
from `pressure-test.md`, `market-research.md`, and `customer-discovery.md`. The drift audit measures the
crystallized concept against *that reconstructed baseline* — not against the stale file — and flags every
place the design is still solving the old assumed problem. This is the load-bearing anti-self-deception
device of the stage.

## Resolved decision tree (Q1–Q10)

1. **Center of gravity (Q1):** crystallize-then-challenge. Must gracefully handle a Discovery Read that
   is not a clean CONTINUE (never cheerfully design a corpse).
2. **Name & file (Q2):** skill `solution-design`; deliverable `solution-design.md` (naming parallels
   `market-research` / `customer-discovery`). Internal verdict = the **Concept Read**.
3. **Entry gate & verdict handling (Q3):** hard-require `customer-discovery.md` (it *is* "the validation
   work"); missing → refuse with an exact string pointing at `/customer-discovery`, write nothing. Then
   branch on the Discovery Read verdict — **loud gate, narrow override**:
   - `CONTINUE` → proceed normally.
   - `PIVOT` → proceed; "the concept" is the *pivoted* one; drift audit front-and-center.
   - `KEEP-DISCOVERING` → proceed only as a **provisional** concept whose top assumptions become explicit
     `/customer-discovery` targets (route back).
   - `KILL` → **stop loudly.** The only legitimate proceed: the founder contests the kill as an *artifact*
     (e.g. coverage skew — no founders interviewed, marketer truncated) **and** designs only the
     *narrowed* concept the cleared evidence supports (effectively a pivot). Override stamped on record.
     Rationale: this stage gathers **no new evidence about the problem**, so a discovery KILL is far
     harder to legitimately override than a kill from an earlier stage — designing a slick concept proves
     nothing about whether the killed problem is real.
4. **Deliverable & Concept Read (Q4):** **full 9-section card** (below). Concept Read =
   **`build` / `narrow` / `redesign` / `reconsider`**, paralleling `/market-research`'s
   `enter / enter-narrower / reposition / reconsider`, in build-readiness terms. Non-binding (it is a
   recommendation, not a gate — over-claiming it as pass/fail is the failure mode); proceeding past a
   KILL Discovery Read is stamped as an override.
5. **Drift spine machinery (Q5):** **delta-ledger script + reasoned audit + blind separate-context
   adversary.** A deterministic stdlib script surfaces every flagged delta (+ Discovery verdict + tripped
   criteria) **verbatim** so none is silently dropped before reasoning starts; the main agent reconstructs
   the validated baseline and writes the Drift Audit; the `solution-red-team` adversary (separate context)
   independently challenges it. The separate context is non-negotiable — self-grading this judgment inline
   is structurally compromised (the customer-discovery-bias-check principle).
6. **Three-assumptions exercise (Q6):** **all material assumptions → script-ranked by leverage ×
   uncertainty → feature the top 3** (rest listed). The deterministic ranking stops the founder quietly
   demoting the assumption they can't defend out of the top 3. The adversary **independently generates its
   own assumption list blind, then reconcile** — catching the load-bearing assumption that was never
   written down (unknown-unknowns). Each top assumption carries its **cheapest test → an MVP
   riskiest-assumption-test (RAT)** (the forward bridge).
7. **Challenge engine (Q7):** **one blind `solution-red-team` agent**, dispatched in a separate context
   with the validation docs + the founder-confirmed concept wedge **but not the main agent's draft**
   (blind by construction) — it produces (a) its top assumptions, (b) where the concept still serves the
   *assumed* problem, (c) how it fails at scale, (d) the single most-likely self-deception; the main agent
   **reconciles** and surfaces every gap. This delivers Q5's refutation *and* Q6's blind generation in one
   dispatch. **No generative parallel worker** (crystallizing one concept is synthesis, not naturally
   parallel). The diverse-persona critique already happened at `/pressure-test`, so the panel is **not**
   reused here (respects the documented "panel lives only at `/pressure-test`" boundary). **Optional
   a-la-carte lens:** the founder may ask the skill to run *one* named perspective skill (e.g.
   `/steve-jobs-perspective` for "is this focused / whole-widget?") as a design critique — no panel
   machinery, no verdict. **Degrade:** if no spawn tool, run the challenge as a deliberately adversarial
   fresh-framing second pass and tell the founder it is weaker without context isolation.
8. **Interaction model (Q8):** **one phase, two gates.** Gate 1 (concept-confirm / scope-lock): the skill
   crystallizes a *draft* concept (wedge · validated-who · core job · what it does NOT do · win thesis),
   surfaces the Discovery verdict + any KILL override, and the founder confirms/corrects (this is the
   highest-leverage human input — a wrong crystallization poisons the whole challenge, like
   `/market-research`'s competitor-set). Autonomous core: delta-ledger → drift audit → blind adversary →
   assumption ranking → reconciliation. Gate 2 (final review): full card → **Ship / Refine / Abort.**
   **Resume:** if `solution-design.md` exists → **Overwrite from scratch / Append a timestamped round /
   Skip-and-exit** (append-round records how the concept *evolved* across redesigns). Effort: `high`.
9. **Composition (Q9):** floor `customer-discovery.md`; reads all upstream + `founder-profile.md`; **never
   edits `hypothesis.md`** (flags + routes to `/sharpen-hypothesis`). Routing by Concept Read —
   `build`/`narrow` → MVP stage (forward); `redesign` → stay in `/solution-design` (Refine; drift
   unresolved); `reconsider` → back to `/customer-discovery` or `/sharpen-hypothesis`; any flagged
   hypothesis update → `/sharpen-hypothesis`. **MVP Brief forward-contract defined now** (Q9) so the
   not-yet-built MVP skill has a stable input the day it is created.
10. **Build package (Q10):** full package — skill + one subagent (`solution-red-team`) + three references
    + adversary brief + two stdlib scripts. Details in the build spec below.

## File layout (deliverable + provenance)

```
docs/ideas-stages/<slug>/
├── solution-design.md               ← THE deliverable: the Solution Design action card (feeds MVP)
└── solution-design/
    ├── delta-ledger.md              ← script output: every flagged delta + Discovery verdict, verbatim
    ├── validated-baseline.md        ← reconstructed problem = hypothesis + applied/unapplied deltas
    ├── assumptions.json             ← per-assumption leverage/uncertainty scores fed to the ranker
    ├── red-team.md                  ← the blind solution-red-team adversary's raw challenge
    ├── reconciliation.md            ← agent's reconcile of its draft vs the blind adversary (gaps surfaced)
    └── rounds/
        └── round-<N>.md             ← append-round provenance when the concept is redesigned + re-run
```

## Deliverable — `solution-design.md` structure (the full 9-section card)

```markdown
# Solution Design: <project-name>

> Crystallizes & challenges the concept the validated evidence supports. The design must serve the
> problem DISCOVERY revealed — not the one the hypothesis ASSUMED. n is small; read the caveats.

## Concept Read
<build | narrow | redesign | reconsider> — 1 line + rationale tied to evidence (non-binding;
override stamped if proceeding past a KILL Discovery Read)

## The Solution Concept
- Wedge (narrowest first version) · Validated who (narrowed from discovery) · Core job/workflow it owns
- The "whole product" sketch · What it deliberately does NOT do (focus = subtraction)
- Why it wins — unfair-advantage / moat thesis (ties to the founder's agentic-coding edge + any
  defensible signal surfaced in discovery)

## Drift Audit — assumed → validated   ← the spine
| Originally assumed (hypothesis.md) | What validation revealed (reconstructed baseline) | Does the concept serve the VALIDATED version? |
|---|---|---|
| ... | ... | ✅ serves it / ⚠️ drifting / ❌ still solving the old problem |
*(Baseline = original hypothesis + accumulated flagged deltas from pressure-test / market-research /
customer-discovery, applied or not. Measured against the reconstruction, never the stale file.)*

## Three Load-Bearing Assumptions   ← the Playbook exercise (script-ranked top 3 of all material)
| # | Assumption | Why load-bearing (what collapses if false) | What would have to be true | Current evidence (cited) | Cheapest test → MVP RAT |
|---|---|---|---|---|---|
*(Ranked by leverage × uncertainty; the rest listed below the table. Blind-adversary additions flagged.)*

## Alternatives Considered
the other concepts/approaches + why this one wins (or honestly, where one might beat it)

## Scale Conditions
what must hold for this to work at scale (distribution, unit economics, defensibility, agentic-leverage)

## Challenge (independent blind solution-red-team agent)
where the concept is weakest; the single most likely way the founder is fooling himself; reconciliation
gaps (assumptions/drift the adversary found that the draft missed)

## MVP Brief (forward contract → MVP stage)
wedge + prioritized riskiest-assumption-tests + validated profile + non-goals, packaged self-contained

## Hypothesis Updates Flagged → /sharpen-hypothesis (do NOT edit hypothesis.md here)

## Override (only if proceeding past a KILL Discovery Read)
<Read> | Override: founder proceeded past KILL Discovery Read on <ISO-date> — concept narrowed to <wedge>
```

## Build spec for `/prompt-architect`

- **Artifact:** one Claude Code **skill** `solution-design` (naming matches `sharpen-hypothesis` /
  `pressure-test` / `market-research` / `customer-discovery`).
- **Subagent** (`.claude/agents/`): **`solution-red-team`** — the blind adversary. Dispatched with the
  validation docs + the confirmed concept wedge but NOT the main agent's draft; prompted to refute, to
  generate its own top assumptions, to find drift, scale-failure, and the single self-deception. Dedicated
  definition, like `customer-discovery-bias-check` / `competitor-steelman`. Opus + `high` in frontmatter.
- **Reference files** (`references/`):
  - `solution-design-template.md` — the 9-section card structure (read in the synthesis step).
  - `drift-audit.md` — how to reconstruct the validated baseline (original hypothesis + accumulated flagged
    deltas) and build the assumed→validated table; what counts as drift.
  - `assumption-ranking.md` — the leverage × uncertainty rubric, the `assumptions.json` schema, the
    per-assumption row schema, and the RAT-→-MVP mapping.
  - `red-team-brief.md` — the `solution-red-team` blind-challenge protocol (read by the adversary at
    dispatch, mirroring how `workstream-briefs.md` / `kill-criteria-anchoring.md` are read by workers).
- **Bundled scripts** (`scripts/`, stdlib-only, self-executing via `uv run --script` like
  `score_criteria.py` / `compute_verdict.py`):
  - `build_delta_ledger.py` — scans the idea's docs for every `## Hypothesis Updates Flagged` block + the
    Discovery Read verdict + tripped criteria and prints them verbatim as the consolidated ledger; degrades
    to listing candidate sections if a doc deviates from the header convention.
  - `rank_assumptions.py` — reads `assumptions.json` (per-assumption leverage + uncertainty), computes
    leverage × uncertainty, sorts, and emits the ranked list + the top-3 selection. Deterministic so the
    ranking can't be fudged by eye.
- **`allowed-tools`:** `AskUserQuestion, Read, Write, Bash, Glob, Agent, Task, WebSearch, WebFetch, Skill`
  (mirrors `/customer-discovery`). WebSearch/WebFetch are for light verification only — **scope guard: do
  NOT re-run market research or discovery.**
- **Triggering / `when_to_use` — extend the chain:** no `hypothesis.md` → `/sharpen-hypothesis`;
  `hypothesis.md` only → `/pressure-test`; `pressure-test.md` → `/market-research`; `market-research.md` →
  `/customer-discovery`; **`customer-discovery.md` exists → `/solution-design`.** Trigger on "design my
  solution", "solution concept", "final solution concept", "design the solution", "what's next" WHEN
  `customer-discovery.md` exists but `solution-design.md` does not. Do NOT trigger to edit the hypothesis
  (`/sharpen-hypothesis`), to size the market (`/market-research`), or to run/synthesize interviews
  (`/customer-discovery`).
- **Effort:** `high` (the adversary carries its own).
- **Gotchas to encode:**
  - The drift spine is the point — never let "concede the diagnosis, keep the prescription" through; the
    Drift Audit must measure against the **reconstructed** validated baseline, not the stale `hypothesis.md`.
  - KILL gate: loud stop, narrow override (contest-as-artifact + design only the narrowed concept), stamped.
  - The `solution-red-team` adversary MUST run in a separate context, dispatched **blind** (no draft).
  - Thresholds / flagged deltas are read from upstream docs and **never relitigated** here.
  - Never edit `hypothesis.md` — flag + route to `/sharpen-hypothesis`.
  - Create `solution-design/` (and `rounds/`) before dispatching the adversary / running scripts.
  - Degrade gracefully if no spawn tool (adversarial second pass, flagged as weaker).
  - The Concept Read is **non-binding** — do not overclaim it as a pass/fail gate.
  - Scope guard: do not re-run market research / customer discovery.
- **Upstream sync** (`references/upstream-sync.md` territory): update `/customer-discovery`'s exit message
  to point to `/solution-design`, and update the "what's next" precedence comments across the chain
  (`/market-research`, `/customer-discovery` `when_to_use`) so the new terminal stage is reflected.

## Composition

- **Upstream:** `/customer-discovery` writes the required `customer-discovery.md`; `/pressure-test`,
  `/market-research`, `/sharpen-hypothesis` supply the assumptions, positioning, and the assumed baseline.
  Floor guard = `customer-discovery.md`.
- **Downstream:** the **MVP stage (not yet built)** consumes `solution-design.md`'s **MVP Brief** — the
  wedge, the prioritized riskiest-assumption-tests, the validated profile, and the non-goals. Hypothesis
  updates route back through `/sharpen-hypothesis`; a `reconsider` Read routes back to `/customer-discovery`.
- **Workers:** `solution-red-team` under `.claude/agents/`, dispatched at runtime.
- **Optional:** any one `*-perspective` skill as an a-la-carte design lens (never the full panel).
```
