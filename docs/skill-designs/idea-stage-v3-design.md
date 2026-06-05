# Idea Stage v3 — Design Contract

> **Status:** locked design contract, produced by a `/grill-me` session (2026-06).
> **Supersedes:** the v2 `idea-funnel` (the automated batch ranker) — see *Cleanup*.
> **Consumed by:** `/prompt-architect`, which builds each artifact from this spec.
> **Source method:** *The Founder's Playbook: Building an AI-Native Startup* (Anthropic) — Idea Stage — plus the founder's doctrine (Lean Startup, "Why Startups Fail," Zero to One, the forward-deployed-founder / business-builder thesis, the solo-founder model).

---

## 0. The one-line reframe

The v2 funnel was built like a **VC allocator**: generate 10 ideas → score → rank by demand → auto-pick K=1 → track in a ledger → hard-stop at a sealed pack. That is *selection* behaviour for a portfolio. A **founder in the Idea Stage is not a VC.** Their job is to take **one** problem to **problem-solution fit through real human conversations** (Build→Measure→Learn), deciding **pivot-or-persevere** on evidence, using their conviction and unfair advantage as **assets, not biases to remove**. v3 rebuilds the Idea Stage as a **founder-validator**, not an allocator.

The doctrine reinforces this: in 2026 the moat is **workflow-understanding + owned distribution, not code** (forward-deployed-founder). So a "good idea" here is a **reachable niche with a real painful workflow you can get close to and own distribution to** — not a big-TAM abstract SaaS play ranked at a desk.

---

## 1. Architecture decisions (resolved)

| # | Decision | Resolution |
|---|---|---|
| Shape | Stage skills vs one workflow | **Founder-gated stage pipeline** — each milestone is its own repeatable skill; the founder decides at every gate. Manual orchestration **now**; the automatic workflow is a **future** step (validate the human-gated version first). |
| Spine | Skills vs subagents | **Skills = founder-facing spine.** Subagents are workers, spawned **only** for (a) context-isolation of adversaries (red-team, bias-check, steelman, objection-lenses) or (b) parallel fan-out. |
| Front-end | Generate / select | Generate a **wide blind slate of 10**, the skill **recommends** one (weighing demand + fit + moat + **distribution**), **the founder picks**. No auto-pick, no K-cap, no portfolio ledger. After the pick, everything is single-idea and deep. |
| Axes | Founder-blind vs aware | Generation is **blind & wide** (anti-bias) **plus** a labelled founder-reachable-workflow track; the **recommendation is founder-aware**; disconfirmation & market stay idea-blind. The v2 "two unfused axes" machinery is dropped — fit is just one input to an advisory recommendation. |
| Kills | Gate philosophy | **The desk almost never kills.** It produces context + interview questions; the **founder** decides advance/pivot/persevere. The only mechanical kill is a **pre-registered kill-criterion firing at synthesis** (founder may override on record). No fatal-flaw checkpoint, no fit-screen kill-gate. |

### The salvage list (keep / drop from v2)

**KEEP** (good lean-startup discipline): structured disconfirmation / devil's advocate · competitor steelman (competitor-neglect antidote) · demand mining from real public complaints · testable-hypothesis sharpening · **pre-registered kill-criteria before interviews** · independent bias-check on synthesis · Mom Test interview design.

**DROP** (the VC-allocator skeleton): auto-rank by demand score + auto-pick K=1 · founder-blind-as-spine + two-unfused-axes machinery · the stateful ledger + resurrect/appeal/portfolio · the batch-of-10 framing · "kill gates" + the fatal-flaw checkpoint as the spine.

---

## 2. Knowledge layer (deliverable #1)

Valuable startup knowledge is converted into **reusable skills** the stages read. Two archetypes, deliberately kept distinct:

- **Methodology / doctrine skills** — bodies of applicable frameworks/checklists/decision-rules to *apply* (not personas). The founder can also invoke them standalone for advice.
- **Persona lenses** — nuwa-generated first-person clones, channelled as disconfirmation lenses (existing convention).

### 2a. Three NEW methodology skills

**`lean-startup`** — Build-Measure-Learn (+ minimize cycle time) · value-hypothesis vs growth-hypothesis · **MVP types** (video/Dropbox, concierge/Food-on-the-Table, Wizard-of-Oz/Aardvark) · validated learning vs vanity metrics + innovation accounting · the **10 pivot types** + "runway = pivots left" · 3 growth engines (sticky/viral/paid, flagged later-stage) · the "*should we even build this?*" gate.

**`forward-deployed-founder`** (the business-builder / AI-era-moat doctrine; renamed from "business-builder" so the name keeps the thesis honest — the moat is business+distribution, **not** code) —
1. **AI-era moat thesis** — software is commoditized (10–100× cheaper, supply glut, Apple +80% submissions/30-day review); technical strength is **not** a moat; durable moats are deep workflow-understanding, **owned distribution/relationships**, proprietary access/data.
2. **FDE / business-builder playbook** — find the customer/niche first → embed & learn the workflow (ops, cash flow, marketing, accounting) → isolate the painful repeatable task → build a custom agentic system → convert unique knowledge into repeatable skills → own the relationship.
3. **"Good idea in 2026" rubric** — reachable niche + real painful workflow + you can get close to customers + a distribution path + AI-buildable. Anti-criteria: undifferentiated SaaS, "rebuildable in a weekend with Claude," no distribution, no customer access.
4. **The 3 failure mindsets** (anti-patterns) — the can-build-but-can't-sell SWE; the can-MVP-but-can't-sell PM; the took-courses-posted-nobody-paid non-technical. Each a self-check.
5. **Distribution-first** — *building ≠ distribution* (the founder's own documented lesson); how to test distribution before building. (Pairs with Zero to One's distribution chapter — see 2c.)

**`solo-founder`** — the one-person-business model (vision-holder/orchestrator) · the **keep-vs-delegate/automate matrix** · AI-as-cofounder + contractor orchestration · solo failure modes (decision fatigue, isolation, GTM skill-gap, bus-factor) · ruthless prioritization / "good enough" / one-project focus · solo-vs-cofounder.

### 2b. Consumption (resolved)

**Inline reference read.** A stage READS the specific doctrine it needs (exactly how disconfirmation already reads `expert-lens-map.md` + `gate-rubrics.md`). Cheap, deterministic, no extra orchestration. A small **`doctrine-map`** (in `idea-stage/references/`) routes stage → doctrine. Each methodology skill is also standalone-invokable (`/lean-startup`). Persona lenses keep their existing **subagent** mechanism.

Doctrine-map (stage → doctrine):

| Stage | Reads |
|---|---|
| generate-ideas | forward-deployed-founder + lean-startup |
| sharpen-hypothesis | lean-startup (value/growth assumptions) |
| disconfirm | persona lenses + a forward-deployed-founder "no-distribution/SaaS-dead" angle + a lean-startup "riskiest-assumption" angle |
| market-map | forward-deployed-founder (moat/distribution) |
| solution-design | lean-startup (MVP/pivot) + forward-deployed-founder + solo-founder |
| idea-stage-exit | lean-startup ("should we build?") |
| build-poc | lean-startup (MVP types) + solo-founder (scope) |

### 2c. Two REUSED + ENRICHED persona lenses

**`peter-thiel-perspective`** ← enrich with Zero to One operational frameworks (research: `docs/skill-designs/research/zero-to-one.md`). Frame additions as **tools Thiel fires** (it's a first-person persona, not a methodology doc):
- Add a decision tool **"Run the Seven Questions"** (Engineering · Timing · Monopoly · People · **Distribution** · Durability · Secret) — fired when channelled as a disconfirmation lens.
- **Distribution test** (PRIORITY for this founder's GTM weakness): the channel spectrum (complex sales $1M+ / personal sales $10K–100K / **the "dead zone" $100–10K** / marketing & ads / viral) + **CAC < CLV** gate + **"nail ONE channel"** (power law of distribution) + "sales works best when hidden."
- Extend Model 1 (Monopoly) with the **4 monopoly characteristics + 10× rule** and the **start-small → scale-up → don't-disrupt** sequence.
- Add CEO-pay/equity operating rules — **$150k cap** (~$100–125k empirically), cash-is-present / equity-is-future, don't split equity equally. **Correction:** *not* $300k (that's the warn-level, not the recommendation).

**`tom-eisenmann-perspective`** ← enrich with the full *Why Startups Fail* (research: `docs/skill-designs/research/why-startups-fail.md`). It is the Chinese 不受傷創業; the **six stories are written in English**. Additions / fixes:
- **Fix:** RAWI is a **scaling** gate (Ready/Able/Willing/Impelled = "should we floor it into hypergrowth *now*?"), **not** a should-I-found gate.
- **Fix:** horse-or-jockey = **"it's *neither*, usually"** — failure most often traces to **Bad Bedfellows** (a third party).
- **Fix:** Baroo = **False Positives** (Speed-Trap's anchor is **Fab.com**).
- **Add Model — The Catch-22** (resources need de-risking · de-risking needs starting · starting needs resources) + its 4 tactics (resolve / defer / shift / get-others-to-ignore).
- **Add Model — the Six S's** scaling diagnostic (Speed, Scope, Series-X funding, Staff, Structure, Shared Values), pairs with RAWI.
- **Diamond-and-Square** corners: diamond = CVP / Technology & Operations / Marketing-GTM / Profit Formula; square = Founders / Team / Investors / Partners.
- **Add "Failing Better" module** (引擎空轉 endgame sequencing): pivot → bridge from *existing* investors → new investors → sell/acquihire → layoffs (WARN Act) → orderly dissolution (creditor→employees→taxes→unsecured); the danger is *delaying* the plug-pull because emotion distorts the call.
- **Add Recovery module** (重整旗鼓): Recovery → Reflection → Reentry (Kübler-Ross frame; ~half of failed founders try again).
- **Failure definition** (two-layer): general = "outcome short of expectations (whose? which?)"; operational = "early investors never made / will make money." Shutting down ≠ failing.

**Research lifecycle (migrate-then-clean).** The staging docs `docs/skill-designs/research/{zero-to-one,why-startups-fail}.md` are **migrated INTO each persona skill's own `references/research/`** (the nuwa citation backbone — e.g. a new `07-zero-to-one-frameworks.md` / `07-why-startups-fail.md`), so each skill stays **self-contained and portable**. Once Phase 1 is built **and verified**, **delete `docs/skill-designs/research/`** to stay clean. The 3 new methodology skills have no staging docs (their content is baked in from the founder-supplied source text). **Keep** this design contract in `docs/skill-designs/` as the V3 design record (human-only background, per the v2-redesign convention).

### 2d. References

- `mom-test` — stays a **customer-discovery reference** (interview discipline: past behaviour, not future intentions; question auditing).
- `failure-patterns` (English) — the six *Why Startups Fail* / 不受傷創業 stories; since they ARE Eisenmann's six, they live alongside `tom-eisenmann-perspective` and are read by `disconfirm`.

---

## 3. Stage skills (deliverable #2) — 8 stages + index + exit

**Naming:** clean unprefixed slash-commands; the **`idea-stage` index** is the canonical map.
**Per stage:** one human-readable `<artifact>.md` (thin YAML frontmatter contract + readable body) + a same-named provenance subfolder; mechanical-scored data only as `.json`; each skill bundles its output **template** in `assets/` (scaffold to fill), separate from `references/` (knowledge to read).

### `idea-stage` (INDEX / spine)
- **Role:** dashboard across all ideas (which stage each is at + next action) **and** the BML **validated-learning + pivot ledger** (innovation accounting; runway = pivots left); models the loop-backs. Holds the shared spine config.
- **References:** `stage-pipeline.md` (canonical order + entry-guards + handoff fields), `doctrine-map.md`, `expert-lens-map.md`.
- **State:** stage-state is **derived live** from which artifacts exist (no status file to drift); the validated-learning/pivot history persists in each `ideas/<slug>/learning-log.md`.

### 1. `generate-ideas`
- **In:** thesis or seed-list (arg). **Reads:** forward-deployed-founder, lean-startup, founder-profile. **Founder:** thesis; **the pick**.
- **Does:** a blind-wide slate of 10 **+** a labelled founder-reachable-workflow track; **flags undifferentiated-SaaS seeds** with "what's your moat in the AI era?"; recommends one (weighing demand + fit + moat + **distribution as a first-class factor**). The founder picks; the skill scaffolds `ideas/<slug>/`.
- **Out:** a SINGLE `ideas/_exploration/<thesis>/slate.md` — a Recommendation header + 10 thin cards (`assets/slate-template.md`), the blind-wide vs reachable-workflow tracks labelled (+ `grounding.md`). The slate is a **comparison artifact** (the founder picks by reading the 10 side-by-side). At pick time the chosen card is **promoted into `ideas/<slug>/`** (the seed for the deep dive); the un-picked 9 stay in `slate.md` as a **lightweight dormant-idea backlog** — this replaces the v2 ledger/resurrect (re-run `sharpen-hypothesis` on any of them later, no machinery). **Workers:** seed-generator, startup-idea-researcher.

### 2. `sharpen-hypothesis`  *(founder-AWARE, interactive — changed from v2's blind headless gate)*
- **In:** the picked idea (the promoted slate card). **Reads:** lean-startup, the upstream `grounding.md`, founder-profile. **Founder:** **refine / inject domain specifics** (not just confirm).
- **Does — draft-then-refine, NO web research** (sharpen, don't *prove* — the confirmation-bias guard; a hypothesis is a *claim to test*, not a fact to establish). The skill **drafts** the four dimensions (who · how-often · how-severe · status-quo) from the seed + grounding + reasoning, marks each **"provisional, to-be-tested,"** and surfaces the lean-startup **value hypothesis** (will they find it valuable enough to switch/pay?) + **growth hypothesis** (how do new users discover it?) as named assumptions for the downstream stages to test. The founder then refines with real domain knowledge if they have it. Kills only if it genuinely can't be made testable. Done **inline by the skill** (sharpening is one interactive reasoning task — no subagent). Real grounding = `market-map`; real validation = the interviews.
- **Out:** `ideas/<slug>/hypothesis.md` (`assets/hypothesis-template.md`) — the sharpened sentence + 4 provisional dimensions + the value/growth hypotheses.

### 3. `disconfirm`
- **In:** `hypothesis.md`. **Reads:** doctrine-map, expert-lens-map. **Founder:** — (autonomous).
- **Does:** convene the **persona panel** (see §4) + competitor-steelman + the FDF/lean doctrine angles; each lens fires **one sharpest objection** → falsifiable assumption + Mom-Test question; the judge dedupes + risk-ranks into ~5–8 OPEN assumptions. **No kill** (a lens may *flag* a fatal-flaw-class issue to the judge only).
- **Out:** `ideas/<slug>/disconfirmation-brief.md` (+ `disconfirmation/` provenance). **Workers:** objection-lens (×panel), competitor-steelman, disconfirmation-judge.

### 4. `market-map`
- **In:** `hypothesis.md` (+ brief). **Reads:** forward-deployed-founder. **Founder:** —.
- **Does — parallel research fan-out, then synthesize.** Spawns ~3–4 focused **Opus** research subagents **in parallel** (each keeps its web-fetch noise OUT of the founder-facing context); the skill synthesizes their distilled findings. Runs once, for the committed idea, so depth > saving agents. **Full article scope:**
  1. **Competitor tiers** — direct / indirect / acquirers / adjacent.
  2. **Review-complaint mining → PSF signal** — mine competitor *reviews* for the top **unresolved** complaints; flag whether the hypothesis addresses them (a problem-solution-fit signal); capture **user language** (feeds the interview guide + outreach).
  3. **Sizing + buyer landscape** — TAM/SAM/SOM **pressure-tested for inflation**; market maturity (expanding / consolidating / mature); **who holds budget · who influences · are they the same person**.
  4. **Trends + analogues** — **3 named external trends** (regulatory / technological / demographic), each scored tailwind/headwind; **analogous markets** where a similar problem was solved (what worked / didn't).
  Plus the FDF **moat/distribution read**. **Context, never a gate — size NEVER kills.**
- **Out:** `ideas/<slug>/market-research.md` (`assets/market-research-template.md`) + `market-research/` (per-facet provenance). **Workers:** market-researcher + facet researchers (parallel fan-out).

### 5. `customer-discovery-design`
- **In:** `disconfirmation-brief.md` + `hypothesis.md` (+ market-research). **Reads:** mom-test, run-pack-template, founder-profile (reachability). **Founder:** approve pack.
- **Does:** the **sealed** pack — target profile, reachability map, **warm list** (real public complainers, each with a drafted contextual reply), Mom-Test guide built from the OPEN assumptions, cold-email drafts, tracking sheet. Also writes the **locked** `kill-criteria.json` (write-once) from the brief's OPEN assumptions. **Drafts only — never sends.**
- **Out:** `ideas/<slug>/customer-discovery/cowork-runpack.md` + `kill-criteria.json`. **Workers:** customer-discovery-design-worker (←cd-design-gate), customer-discovery-personas-worker.
- **Off-skill execution:** you post warm replies; **Cowork** (Gmail/Calendar MCP) sends cold email + schedules on **per-batch approval**.

### 6. `customer-discovery-synthesis`  *(renamed from `customer-discovery`)*
- **In:** `kill-criteria.json` + **the founder's interview notes** (`customer-discovery/interviews/*.md`). **Reads:** kill-criteria-anchoring, mom-test. **Founder:** notes; ship/override.
- **Does:** tag → score real evidence vs the **locked** thresholds (bundled `score_criteria.py`) → coverage/skew + **false-positive guard** (early-adopters ≠ market) → **independent bias-check** (separate context, refute) → verdict (CONTINUE / PIVOT / KILL / KEEP-DISCOVERING). **Never softens a threshold after data.**
- **Out:** `ideas/<slug>/customer-discovery.md` (Discovery Read) + `synthesis/round-N.*`. **Worker:** customer-discovery-bias-check.

### 7. `solution-design`  *(kept, light rewire of paths)*
- **In:** `customer-discovery.md` (+ upstream). **Reads:** lean-startup, forward-deployed-founder, solo-founder, founder-profile. **Founder:** confirm concept.
- **Does:** crystallize the concept latent in the validated evidence → **drift audit** (serves the VALIDATED, not the ASSUMED, problem) + 3 load-bearing assumptions + alternatives + scale, with a **blind separate-context red-team** → Concept Read (build/narrow/redesign/reconsider) + **PoC brief**.
- **Out:** `ideas/<slug>/solution-design.md` (+ `solution-design/`). **Worker:** solution-red-team.

### 8. `idea-stage-exit`  *(NEW — the deliberate GO/NO-GO)*
- **In:** `solution-design.md` + the kill-criteria verdict. **Reads:** lean-startup, the 3 exit-criteria. **Founder:** **GO / NO-GO**.
- **Does:** re-state the **validated** problem; check the article's **3 exit-criteria** (problem real & specific? · solution addresses the *validated* problem? · enough signal to justify building?) + Lean Startup's "should we even build this?" against the pre-registered kill-criteria; stamp an explicit decision on record. This is a *conscious act* — the guard against the founder's documented drift failure mode.
- **Out:** `ideas/<slug>/idea-stage-exit.md` (GO/NO-GO stamp).

### 9. `build-poc`  *(NEW — final Idea-Stage deliverable; owns the full build→test→synthesize loop)*
- **In:** `idea-stage-exit.md` = GO + the PoC brief. **Reads:** lean-startup (MVP types / validated learning), solo-founder (scope). **Founder:** pick archetype; run the 5 conversations.
- **PoC ≠ MVP (the boundary):** the PoC is a **throwaway, learning-only** prototype (often fake-backed) built to provoke a *genuine reaction to the solution* from real users — deliberately **NOT** the first shippable product. Over-building it into an MVP is the failure mode this stage guards against. The MVP (next layer) answers "what to build *first*" and **locks scope there**, not here.
- **Does — the full loop:**
  1. **Scope (list what to build).** `poc-brief.md` explicitly lists the **build scope** — the single core interaction + the minimum to make it *touchable* — AND the explicit **NON-GOALS** (everything dropped because it isn't needed for learning). This IN/OUT list is the anti-scope-creep guard.
  2. **Choose the archetype** by cheapest-path-to-learning (video / concierge / Wizard-of-Oz / functional single-interaction — non-code is a feature, not a gap).
  3. **Build** — if functional, drive Claude Code to build *just* the single core interaction.
  4. **Release to the 5** validated-profile users + a reaction rubric.
  5. **Synthesize** the 5 reactions → a **direction decision** (keep-building / pivot / back-to-drawing-board — the BML loop-back) **+** an **MVP-scope-input handoff** the next layer consumes to lock the MVP scope. build-poc produces the *input*; it does NOT lock the MVP.
- **Execution (phase-aware, multi-session — one skill, resumes by detecting artifacts):** **scope phase** (no `poc-brief.md` → list what-to-build/non-goals + archetype, scaffold a build session) → **build phase externalized to its OWN focused coding session + worktree** (a clean Claude Code build of *only* the single core interaction from `poc-brief.md` — no validation-reasoning noise; **non-code archetypes skip this**) → *[days: the 5-user test, off-tool]* → **synthesize phase** (reactions exist → decision + handoff). The heavy code build stays isolated; validation reasoning stays in build-poc. Mirrors the `customer-discovery` design/synthesis seam.
- **Out:** `ideas/<slug>/poc/{poc-brief.md (scope + non-goals), reactions.md (5-user synthesis + direction), mvp-input.md (handoff to the MVP layer), …prototype}`. **Ends the Idea Stage.**

### Loop-backs (BML is a loop, not a pipeline)
- synthesis **PIVOT** → re-enter `sharpen-hypothesis` (or `generate-ideas` for a segment pivot); log the pivot type + decrement runway in `learning-log.md`.
- synthesis **KILL/INVALIDATED** → drop or pick another slate idea.
- PoC reactions negative → back to the drawing board (pivot or reconsider).
- The `idea-stage` index records the validated-learning + pivot history.

---

## 4. The disconfirm persona panel (resolved)

**Advisory-board model — bounded roster, deliberate curation:**
- **Fixed core-3 always fire**, covering the 3 universal disconfirming axes with zero overlap: **edge/monopoly → Thiel**, **inversion/failure → Munger**, **customer/demand → Bezos**.
- **+ competitor-steelman** always.
- **+ the doctrine angles always** (forward-deployed-founder "no-distribution/SaaS-dead"; lean-startup "riskiest-assumption") — so disconfirmation is anchored even if the roster is never touched.
- **+ ≤1 auto-suggested idea-type specialist** (Taleb=risk/fintech, Eisenmann=services/ops & failure-pattern, Naval=leverage/content, …). The founder may swap any seat, but **defaults run unprompted**.
- **Output contract:** each lens fires **one sharpest objection** → 1 falsifiable assumption + 1 Mom-Test question (+ optional fatal-flaw *flag to the judge*, not into the brief). The judge dedupes + risk-ranks into **~5–8 OPEN assumptions**. The cap is a feature — a *testable* brief, not a 30-item wall.
- **Epistemic limit:** founder-blind; can't invent facts; subjective objections stay **OPEN → interview questions**; only hard checkable facts (legality/feasibility) close. Lenses surface risks to test; they never render a verdict.
- **nuwa mints a new specialist only *between* runs**, when a logged coverage-gap recurs. The roster grows slowly and on purpose.

---

## 5. Artifact / output convention (resolved)

- **Format:** every stage writes ONE markdown file = a **thin YAML frontmatter handoff header** (stage · status/verdict · a handful of key scalars · pointers) **+ a human-readable body**. Rich/nested content lives in the body; **genuinely mechanical-scored data is the only `.json`** (`kill-criteria.json`, scoring). The frontmatter is the contract the next stage's **entry-guard** parses; the body explains. *Never cram the whole payload into frontmatter.*
- **Templates:** each stage skill bundles `assets/<artifact>-template.md` (the output scaffold it fills → guaranteed-consistent format), kept **separate from `references/`** (rubrics/doctrine the skill reasons with) so each skill self-documents what it *produces* vs what it *reads*. Migrate the existing `customer-discovery`/`solution-design` templates from `references/` → `assets/` in Phase 2.
- **Provenance:** a same-named subfolder per stage holds worker outputs.
- **Entry-guards:** each stage refuses unless its predecessor artifact exists, and points the founder at the right upstream skill.

---

## 6. Project structure (resolved)

Three zones that never mix: `.claude/` (the machine) · `docs/` (layer meta) · `ideas/` (founder work product).

```
.claude/skills/        # flat (Claude Code discovers <name>/SKILL.md); grouped by naming + the index map
  idea-stage/  generate-ideas/  sharpen-hypothesis/  disconfirm/  market-map/
  customer-discovery-design/  customer-discovery-synthesis/  solution-design/
  idea-stage-exit/  build-poc/
  lean-startup/  forward-deployed-founder/  solo-founder/
  peter-thiel-perspective/  tom-eisenmann-perspective/  …other *-perspective
  create-founder-profile/  nuwa-skill/  …meta
.claude/agents/        # kept workers (see Cleanup)
.claude/workflows/     # phase-2 auto-orchestration lands here later
docs/                  # LAYER META ONLY: founder-profile, founder-dossier, skill-designs/, research/
ideas/                 # FOUNDER WORK PRODUCT
  _exploration/<thesis>/{slate.md, grounding.md}
  <idea-slug>/{hypothesis.md, disconfirmation-brief.md(+disconfirmation/),
               market-research.md(+market-research/),
               customer-discovery/{cowork-runpack.md, kill-criteria.json, interviews/, synthesis/},
               customer-discovery.md, solution-design.md(+solution-design/),
               idea-stage-exit.md, poc/{poc-brief.md, reactions.md}, learning-log.md}
```

---

## 7. Cleanup (resolved: retire funnel + ledger, keep workers)

- **Retire:** `idea-funnel` skill · `idea-funnel-engine.js` · ledger machinery (`ledger-reader`, `ledger-writer`, `ledger-schema.md`) · `fmf-screen` as a kill-gate (fold founder-fit into `generate-ideas`'s recommendation).
- **Keep as workers:** seed-generator, objection-lens, competitor-steelman, disconfirmation-judge, market-researcher, cd-design-gate (→ rename `customer-discovery-design-worker`), customer-discovery-personas-worker, customer-discovery-bias-check, solution-red-team.
- **Absorbed into a skill:** `sharpen-gate` — its sharpening logic moves *inline* into the founder-aware `sharpen-hypothesis` skill (no longer a headless founder-blind worker).
- **Migrate:** `expert-lens-map.md` + `gate-rubrics.md` content → `idea-stage/references/` (the lens-map + a slimmed `stage-pipeline.md`; the v2 fatal-flaw "gate-rubrics" logic is dropped). Existing work product under `docs/ideas-stages/` migrates to `ideas/`.

---

## 8. Build plan

- **Phase 1 — knowledge layer first** (it's deliverable #1, the stages depend on it, and it's where the research feeds): build `lean-startup`, `forward-deployed-founder`, `solo-founder` + enrich `peter-thiel-perspective` & `tom-eisenmann-perspective` + the `doctrine-map` & `failure-patterns` references. Build via `/prompt-architect`.
- **Phase 2 — the stage spine:** the 8 stage skills + `idea-stage` index + `idea-stage-exit`; rename/rewire `customer-discovery` → `customer-discovery-synthesis` and `solution-design`; retire the funnel + ledger; rewire the kept workers.
- **Deferred:** the automatic orchestration workflow (validate the human-gated version first).

## 9. Deferred to `/prompt-architect` (implementation, not design)

Template section-lists per skill; exact frontmatter field sets; the `slate.md` and `learning-log.md` layouts; the generate-ideas pick interaction (AskUserQuestion); per-skill `description`/trigger tuning; eval prompts.
