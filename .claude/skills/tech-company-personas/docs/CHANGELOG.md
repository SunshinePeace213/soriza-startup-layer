# Changelog

All notable changes to the tech-company-personas skill are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The `version:` field is no longer present in the SKILL.md frontmatter (dropped from the official skill frontmatter spec); semantic version is tracked here instead.

## [Next] — 2026-04-28

### Changed (BREAKING — internal restructure per cc-dev-toolkit Phase B)

- `references/` reorganized into `companies/` and `roles/` subfolders per cc-dev-toolkit redesign spec §17.
- `references/company-engineering-cultures.md` (462-line monolith holding 15 companies) split into 15 per-company files under `references/companies/<co>.md`.
- `references/ic-track.md` (579 lines, exceeded the cc-dev-toolkit ≤250-line target) split into 4 categorized files under `references/roles/`:
  - `ic-generalist.md` — Distinguished/Fellow → Junior (6 roles)
  - `ic-engineering.md` — frontend, backend, fullstack, mobile, devops, SRE, platform, QA/SDET (8 roles)
  - `ic-data-ml.md` — data engineer, ML engineer, AI/ML research engineer (3 roles)
  - `ic-specialty.md` — security, performance, accessibility, design systems, technical writer, UX/UI, UX research (7 roles)
- `references/{executive-level,director-level,management-level,cross-functional}.md` moved into `references/roles/` (each was already under 250 lines and kept as a single file).
- `SKILL.md` rewritten with a Resources table, Loading Guide, and updated Reference Files section pointing at the new directory structure.

### Added

- **10 new company profiles** under `references/companies/` per spec §17: `anthropic.md`, `openai.md`, `nvidia.md`, `github.md`, `cloudflare.md`, `hashicorp.md`, `snowflake.md`, `datadog.md`, `gitlab.md`, `bytedance.md`. Total company count: 15 → 25.
- **`examples/assembled-personas/`** worked examples showing role-card + company-profile composition: `staff-engineer-at-stripe.md`, `principal-engineer-at-anthropic.md`, `sre-at-cloudflare.md`.
- **Tier-1 evals** at `evals/triggers.json` (8 should-trigger + 8 should-NOT-trigger queries) and `evals/smoke.json` (single Staff-Engineer-at-Stripe representative task) — passes the cc-dev-toolkit Tier-1 testing standard per spec §16.
- **`docs/CONTRIBUTING.md`** maintenance guide for adding companies, roles, and assembled-persona examples.
- **`docs/CHANGELOG.md`** — this file.
- **Loading Guide** in SKILL.md naming the agents that should declare this skill in their `skills:` frontmatter list.

### Removed

- `version: 0.1.0` from `SKILL.md` frontmatter (dropped from official skill spec; tracked here in CHANGELOG).
- Description mentions of `meta-agent`, `/meta-prompt`, and `agent-creator` from `SKILL.md` frontmatter (legacy framing — replaced with persona-application + agent-frontmatter-loading triggers per cc-dev-toolkit redesign spec §13).
- `references/company-engineering-cultures.md` (content fully migrated into per-company files; the monolith was moved to `~/.Trash/` per CLAUDE.md "Safe delete").
- `references/ic-track.md` (content fully migrated into 4 ic-\* split files; original moved to `~/.Trash/`).

### Migrated from

- **Phase A (cc-dev-toolkit redesign):** `docs/superpowers/specs/2026-04-27-cc-dev-toolkit-redesign-design.md` (§17 — Phase B preview)
- **Plan reference:** `docs/superpowers/plans/2026-04-27-cc-dev-toolkit-redesign-plan.md` (Task 14.4 — pointer doc that deferred this work)
- The cc-dev-toolkit navigation-aid stub that pointed here from the toolkit side was retired in v2.2.0 of cc-dev-toolkit; consumers now point at this skill at the directory level directly.

## [0.1.0] — 2026-04-27

### Added (initial skill)

- `SKILL.md` with persona selection guide, agent-to-persona mappings, and persona card format
- `references/executive-level.md` — 10 C-suite and VP roles (CEO, CTO, CPO, CFO, COO, CISO, VPs of Eng/Product/Design/Data-AI)
- `references/director-level.md` — 7 director roles (Engineering, Product, QA, DevOps, Security, Data-AI, Developer Experience)
- `references/management-level.md` — 6 management roles (EM, PM, TPM, Program Manager, Scrum Master, QA Manager)
- `references/ic-track.md` — 24 IC roles (Distinguished → Junior + specialty tracks)
- `references/cross-functional.md` — 8 cross-functional roles (Solution Architect, Enterprise Architect, BA, Release Manager, DevRel, EngProd, DBA, Cloud/Infra)
- `references/company-engineering-cultures.md` — 15 company profiles (Mega 7 + Stripe, Airbnb, DoorDash, Uber, Spotify, Salesforce, Databricks, Shopify)
