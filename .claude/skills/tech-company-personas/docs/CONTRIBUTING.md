# Contributing to tech-company-personas

This skill is the persona catalog that cc-dev-toolkit pulls from at Phase 3 (Generate). Changes here ripple through every command, agent, and skill that declares `plugins/soriza-plugin-development/skills/tech-company-personas` in its `skills:` frontmatter list. Read the cc-dev-toolkit redesign spec (`docs/superpowers/specs/2026-04-27-cc-dev-toolkit-redesign-design.md` §17) before making structural changes.

## Adding a new company profile

Company profiles live at `references/companies/<co>.md`, one file per company. Use the lowercase, hyphen-free filename (`anthropic.md`, `bytedance.md`, `databricks.md`).

1. **Mirror the established structure** (set by the existing 25 profiles):
   - H1 = company display name (parent company in parentheses if relevant: `Google (Alphabet)`)
   - `**Engineering Culture**:` paragraph — 2-4 sentences capturing identity
   - `## Title Ladder` — markdown table. Use the company's actual ladder (E3/E4/...; L4/L5/...; ICT2/ICT3/...; or numeric like ByteDance's 1-1, 2-1). Add a `Manager Title` column when the manager track is named distinctly; omit it when the IC ladder is dominant.
   - `## Distinctive Practices` — 5-8 bullets, each one bolded term + colon + one-sentence description
   - `## Key Vocabulary` — comma-separated single-paragraph list (15-25 terms)
   - `## Persona Flavor` — 2-4 sentence paragraph that captures the _texture_ of how an engineer at this company thinks
2. **Anti-bloat**: stay under ~50 lines. If you find yourself writing more, the company's nuance probably belongs in role cards.
3. **Update SKILL.md**: add a row to the Reference Files / Companies table.
4. **Update `docs/CHANGELOG.md`**: log the new profile in the next `## [Next]` block under Added.
5. **Optional**: add a worked example at `examples/assembled-personas/<role>-at-<co>.md` (one is enough; total examples should stay in the 3-7 range).

## Adding a new role card

Role cards live at `references/roles/<level>.md`. The current set:

- `executive-level.md` — C-suite, VPs (243 lines, single file)
- `director-level.md` — Director track (171 lines, single file)
- `management-level.md` — EM/PM/TPM/Program Manager/Scrum Master/QA Manager (147 lines, single file)
- `cross-functional.md` — Architects, BA, Release Manager, DevRel, EngProd, DBA, Cloud/Infra (195 lines, single file)
- `ic-generalist.md` — Distinguished → Junior (6 roles, ~150 lines)
- `ic-engineering.md` — frontend/backend/fullstack/mobile/devops/SRE/platform/QA-SDET (8 roles, ~200 lines)
- `ic-data-ml.md` — Data/ML/Research engineer (3 roles, ~75 lines)
- `ic-specialty.md` — security/performance/accessibility/design-sys/tech-writer/UX-UI/UX-research (7 roles, ~170 lines)

To add a new role:

1. **Pick the right file**. If the role is a new specialty, add it to the closest `ic-*` file. If the file is already at ~225+ lines, split it instead of extending it (cc-dev-toolkit ≤250-line target).
2. **Mirror the 8-field shape** that every existing role uses:
   - H2 = role name
   - `**Level Band**:` — internal tier and IC range
   - `**FAANG Equivalents**:` — pipe-separated `Company: Title (level)` list
   - `**Responsibilities**:` — 4-5 bullet list
   - `**Mindset / Priorities**:` — paragraph
   - `**Communication Style**:` — paragraph
   - `**Typical Vocabulary**:` — comma-separated paragraph (15-25 terms)
   - `**What They Push Back On**:` — paragraph or bullets
   - `**Agent Use Case**:` — single sentence
3. **Update SKILL.md**: add the role to the Quick Reference table.
4. **Update `docs/CHANGELOG.md`**.

## Splitting a role-card file

Trigger: file approaches or exceeds 250 lines. Pattern set by the `ic-track.md` → 4-file split (see `docs/CHANGELOG.md` 2026-04-28 entry):

1. Group roles by sub-discipline (generalist / engineering / data-ML / specialty / etc.).
2. Create `references/roles/<group>.md` per group with a top-level "what's here / where the rest lives" header that cross-links the siblings.
3. Update SKILL.md Reference Files table to list the new files.
4. Move the original file to `~/.Trash/<file>.<timestamp>.bak` (per CLAUDE.md "Safe delete" — never `rm -rf`).
5. Update `docs/CHANGELOG.md` under Changed (BREAKING — internal restructure).

## Adding an assembled-persona example

Worked examples live at `examples/assembled-personas/<role>-at-<co>.md`. Cap the total at 3-7; more than that becomes maintenance noise rather than helpful reference. Each example must:

1. Cite the **role card** (`references/roles/<file>.md`) and **company profile** (`references/companies/<co>.md`) it composes.
2. Show a **Method** section summarizing how the role-card and company-profile fields fuse.
3. Provide an **Assembled Persona block** in a fenced code block, ~200-400 words.
4. Include **Notes** — what the company profile uniquely contributes vs. the bare role card; where to swap fields for a different company.

## Anti-bloat guidelines (per cc-dev-toolkit standards)

- Reference files target ≤250 lines.
- SKILL.md target ≤2,000 words (this skill's body should stay leaner — closer to ~1,200 words — because most content lives in references).
- One topic per file.
- No duplication — POINT to the canonical source rather than restate it.

## Self-validation (Tier-1)

This skill ships with `evals/triggers.json` and `evals/smoke.json` per cc-dev-toolkit Phase A spec §16:

```bash
# Triggering test (target ≥90%)
bash plugins/soriza-plugin-development/skills/cc-dev-toolkit/scripts/check-triggers.sh plugins/soriza-plugin-development/skills/tech-company-personas \
  --skill-name tech-company-personas --workspace /tmp/personas-tier1

# Smoke functional test
bash plugins/soriza-plugin-development/skills/cc-dev-toolkit/scripts/smoke-test.sh plugins/soriza-plugin-development/skills/tech-company-personas \
  --workspace /tmp/personas-tier1
```

Run these locally after any structural change before opening a PR.

## Pre-PR checklist

- [ ] Files cited in `SKILL.md` resolve on disk (no broken `references/...` paths)
- [ ] No file in `references/` exceeds 250 lines (`wc -l references/**/*.md`)
- [ ] No `meta-prompt` / `meta-agent` / `meta-skill` / `agent-creator` mentions reintroduced (`grep -rniE 'meta-(prompt|agent|skill)|agent-creator' SKILL.md references/ examples/ docs/`) — historical CHANGELOG entries are exempt
- [ ] No `version:` field reintroduced in `SKILL.md` frontmatter (dropped per official spec)
- [ ] No `<` or `>` in any frontmatter value of `SKILL.md` (cc-dev-toolkit Frontmatter Security check)
- [ ] Skill name does not contain `claude` or `anthropic` (cc-dev-toolkit reserved-name check)
- [ ] Tier-1 evals pass per the Self-validation block above
- [ ] `docs/CHANGELOG.md` updated with a `## [Next]` entry under the appropriate Added/Changed/Removed section
- [ ] Single-purpose commits with conventional commit messages (`feat(tech-company-personas): ...`, `chore(tech-company-personas): ...`, etc.)
