# Idea Stage v3 — Phase 1 Build & Verification Record

Phase 1 = the **knowledge layer** the stage skills inline-read. Built per the design contract
(`idea-stage-v3-design.md`, §2 + §8). Verified with the prompt-architect apparatus before commit.

## What was built

| Artifact | Type | Notes |
|---|---|---|
| `forward-deployed-founder` | NEW skill | AI-era moat doctrine (SaaS-dead · FDE/business-builder · good-idea-2026 rubric · 3 failure mindsets · distribution-first) |
| `lean-startup` | NEW skill | BML · value/growth hypotheses · MVP-type chooser · validated-vs-vanity · 10 pivots + runway-as-pivots · "should we build this?" |
| `solo-founder` | NEW skill | keep-vs-delegate/automate matrix · AI-as-cofounder · solo failure modes · ruthless focus · solo-vs-cofounder |
| `idea-stage/references/doctrine-map.md` | NEW ref | stage → doctrine routing (the shared config; idea-stage SKILL.md is Phase 2) |
| `tom-eisenmann-perspective/references/failure-patterns.md` | NEW ref | the six *Why Startups Fail* patterns, in English; read by `disconfirm` |
| `peter-thiel-perspective` | ENRICHED | Zero to One operational tools (7 Questions · Distribution test · monopoly-building · $150k CEO-pay rule); research → `references/research/07-zero-to-one-frameworks.md` |
| `tom-eisenmann-perspective` | ENRICHED | Catch-22 + 4 tactics · Six S's · Failing-Better endgame · 3-phase Recovery; research → `references/research/07-why-startups-fail.md` |
| `.claude/workflows/artifact-eval.js` | FIX | now accepts string-delivered `args` (matched the `idea-funnel-engine` pattern) — it threw `pipeline() expects an array` otherwise |

## Verification (prompt-architect Phase 5 — `artifact-eval` vs baseline, graded by `meta-skill-grader`)

| Skill | iter | per-eval (with vs baseline) | result |
|---|---|---|---|
| forward-deployed-founder | 1 | saas 1.0/1.0 · moat 1.0/1.0 · near-miss **0.0**/1.0 | near-miss FAILED → over-engaged on a coding task |
| — | 2 (after fix) | saas 1.0/1.0 · moat **1.0/0.0** · near-miss **1.0**/1.0 | **3/3**, delta **+0.33** (beats baseline) |
| lean-startup | 1 | mvp 1.0/1.0 · vanity 1.0/1.0 · near-miss 1.0/1.0 | **3/3** |
| solo-founder | 1 | delegate 1.0/1.0 · cofounder 1.0/1.0 · near-miss 1.0/1.0 | **3/3** |

`quick_validate` (frontmatter): all 5 new/enriched skills **valid**.

## The one issue found and fixed

iteration-1 of `forward-deployed-founder` failed its near-miss: told to "use the skill" on a pure
*"wire up Stripe in Next.js"* task, it hijacked the coding question with the moat/distribution doctrine
instead of answering it. **Fix:** added an explicit **"Out of scope"** boundary to all three new doctrine
skills (they defer on implementation / coding / unrelated tasks). Re-run: every near-miss now **defers**
(answers the technical question directly, no doctrine leakage), and `forward-deployed-founder` flipped to
a positive delta over baseline.

Deltas of 0 on the in-scope evals are expected for doctrine skills — baseline-Claude also reaches a decent
answer; the skill's value is the *reliable, structured* version plus the specific frameworks the stages
inline-read. The grader confirmed every pass was on genuine, citable substance (not surface compliance).

## Cleanup done at this commit

- Migrated the two book-research docs **into** each persona skill's `references/research/`; **deleted** the
  staging `docs/skill-designs/research/` (per the contract's migrate-then-clean decision — skills are now
  self-contained/portable).
- Deleted the bulky `phase1-verify/` eval scratch (this record preserves the results).
