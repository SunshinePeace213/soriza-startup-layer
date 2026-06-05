---
name: skill-listing-budget
description: "skill descriptions have a per-entry 1,536-char cap + a global ~1% budget that drops least-used skills; the layer's de-dup standard + its factory enforcement"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 60e664dd-3964-4aea-86d8-2469948496d2
---

The `.claude/skills/` listing is injected every session and has two ceilings: **per-entry 1,536 chars** (`description` + `when_to_use` combined → truncated over it) and a **global ~1% of context** budget (overflow silently drops the least-used skills' descriptions from auto-discovery). On this setup 1% ≈ ~7,000 tokens / ~25,600 chars; `/doctor` reports the overflow.

Fixed 2026-06-06 (commit 73a1601): the layer was at ~1.1% (28,145 chars) with `customer-discovery-synthesis` over the per-entry cap. Cut to **17,131 chars (~0.6%)** via Option 3 (tighten descriptions, NO `skillListingBudgetFraction` raise — that costs tokens every session).

**The layer's description standard:** the `description` field is kept **under 300 chars** (keyword-dense, front-loaded triggers — its one job is telling Claude *when* to load, not how it works); `when_to_use` carries *only* the gate (precondition file) + NOT-boundaries (which sibling to route to) — never re-echo triggers across both; delete `when_to_use` if it would only echo. Perspective skills = tight keyword card (~250 chars, no bio — bio lives in the body Identity Card). Enforced 2026-06-06 (commit after b8c53e4): all 31 descriptions trimmed below 300 (max 297, mean ~279).

**Enforcement is in the repo** (don't re-derive it): `prompt-architect/references/skill-template.md` → "Description budget"; `prompt-architect/scripts/quick_validate.py` hard-fails the 1,536 combined cap + warns on bloat/duplication; `nuwa-skill` template + `scripts/quality_check.py` check #7 for generated perspective skills.

**Skill edits only go live once on `main`** — the listing reads the main working tree, not worktrees. See [[idea-funnel-bg-isolation-write-block]] and the merge-to-main lesson in [[idea-funnel-ratelimit-fragility]].
