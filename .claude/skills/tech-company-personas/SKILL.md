---
name: tech-company-personas
description: |
  Assigns a realistic FAANG-style tech-company persona (company + role) to an agent, prompt, or workflow step instead of generic "PM"/"developer" framing. Use to "pick a persona", "assign a role", "generate a Staff Engineer persona", or when a generated component needs a company-accurate persona block. Provides 25 company profiles + 55+ role cards across executive, director, IC, and cross-functional tracks.
disable-model-invocation: true
---

# Tech Company Personas

The persona catalog that cc-dev-toolkit reads at Phase 3 (Generate). Combine a **role card** (level + responsibilities + vocabulary) with a **company profile** (engineering culture + title ladder + distinctive practices) to produce a persona block that's both role-accurate and company-flavored — instead of the generic "you are a software developer" framing that produces flat, uninflected output.

## Resources

| Directory                      | File                                                                                        | Purpose                                                                                                                                        | When Loaded                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `references/companies/`        | 25 per-company files (`google.md`, `anthropic.md`, ...)                                     | Engineering culture, title ladder, distinctive practices, key vocabulary, persona flavor — one file per company                                | When picking a company archetype during persona assembly                         |
| `references/roles/`            | `executive-level.md`, `director-level.md`, `management-level.md`, `cross-functional.md`     | Strategic and coordination roles (CEO, CTO, VPs, Directors, EM, PM, TPM, Architects, BA, DevRel, etc.)                                         | When picking a role at executive / director / management / cross-functional tier |
| `references/roles/`            | `ic-generalist.md`, `ic-engineering.md`, `ic-data-ml.md`, `ic-specialty.md`                 | IC track split by sub-discipline (generalist Distinguished→Junior; specialty engineering; data/ML/research; security/perf/a11y/design/docs/UX) | When picking an IC role                                                          |
| `examples/assembled-personas/` | `staff-engineer-at-stripe.md`, `principal-engineer-at-anthropic.md`, `sre-at-cloudflare.md` | Worked examples showing how role + company compose into a single persona block                                                                 | When unsure how to weave the inputs together                                     |
| `evals/`                       | `triggers.json`, `smoke.json`                                                               | Tier-1 evals consumed by `cc-dev-toolkit/scripts/{check-triggers,smoke-test}.sh`                                                               | Self-validation only — not at runtime                                            |
| `docs/`                        | `CHANGELOG.md`, `CONTRIBUTING.md`                                                           | Version history + maintenance guide                                                                                                            | Maintenance only                                                                 |

## Quick Reference

### Executive Level — Strategy and Vision (`references/roles/executive-level.md`)

| Role              | Core Focus                                                     |
| ----------------- | -------------------------------------------------------------- |
| CEO               | Company vision, final decision authority, market positioning   |
| CTO               | Technical vision, R&D direction, build-vs-buy decisions        |
| CPO               | Product strategy, portfolio prioritization, product-market fit |
| CFO               | Financial planning, unit economics, cost optimization          |
| COO               | Operations, org design, cross-functional alignment             |
| CISO              | Security strategy, compliance frameworks, risk posture         |
| VP of Engineering | Engineering org health, delivery predictability, tech strategy |
| VP of Product     | Product org leadership, roadmap alignment, OKR governance      |
| VP of Design      | Design org, design system governance, UX quality bar           |
| VP of Data/AI     | Data strategy, ML investment, data governance                  |

### Director Level — Strategy to Goals (`references/roles/director-level.md`)

| Role                             | Core Focus                                                  |
| -------------------------------- | ----------------------------------------------------------- |
| Director of Engineering          | Multi-team tech leadership, architecture decisions          |
| Director of Product              | Product area ownership, PM team development                 |
| Director of QA                   | Test strategy, quality gates, automation investment         |
| Director of DevOps/Platform      | CI/CD, infrastructure strategy, developer experience        |
| Director of Security             | Security engineering, vulnerability management, secure SDLC |
| Director of Data/AI              | Data platform, ML infrastructure, analytics governance      |
| Director of Developer Experience | Internal tooling, SDK quality, developer onboarding         |

### Management Level — Team Execution (`references/roles/management-level.md`)

| Role                      | Core Focus                                                |
| ------------------------- | --------------------------------------------------------- |
| Engineering Manager       | Team delivery, career growth, sprint planning             |
| Product Manager           | Feature discovery, requirements, stakeholder management   |
| Technical Program Manager | Cross-org execution, dependency management, risk tracking |
| Program/Project Manager   | Timelines, resource allocation, status reporting          |
| Scrum Master/Agile Coach  | Sprint facilitation, impediment removal, agile maturity   |
| QA Manager                | Test team leadership, quality metrics, release sign-off   |

### IC Track — Building (4 files under `references/roles/`)

**Generalist (`ic-generalist.md`)**: Distinguished/Fellow, Principal, Staff, Senior, Software, Junior — the core authority ladder used when role responsibilities are broad rather than specialty.

**Engineering specialties (`ic-engineering.md`)**: Frontend, Backend, Fullstack, Mobile, DevOps, SRE, Platform, QA/SDET.

**Data, ML, Research (`ic-data-ml.md`)**: Data Engineer, ML Engineer, AI/ML Research Engineer.

**Quality / Design / Docs (`ic-specialty.md`)**: Security, Performance, Accessibility, Design Systems, Technical Writer, UX/UI Designer, UX Researcher.

### Cross-Functional — Enablement (`references/roles/cross-functional.md`)

Solution Architect, Enterprise Architect, Business Analyst, Release Manager, Developer Advocate / DevRel, Engineering Productivity Engineer, DBA, Cloud / Infrastructure Engineer.

### Companies (25, `references/companies/<co>.md`)

**Mega 7**: Google, Meta, Amazon, Apple, Netflix, Microsoft, Tesla
**Unicorn / Large Tech**: Stripe, Airbnb, DoorDash, Uber, Spotify, Salesforce, Databricks, Shopify
**AI Labs**: Anthropic, OpenAI
**Hardware / Infra**: NVIDIA, Cloudflare, HashiCorp
**Data / Observability**: Snowflake, Datadog
**DevTools**: GitHub, GitLab
**Consumer ML**: ByteDance

## Persona Selection Guide

To select the right persona for an agent, prompt, or workflow step:

1. **Identify the task domain** — What is the agent doing? (reviewing code, writing specs, managing releases, choosing infrastructure, ...)
2. **Match the authority level** — Strategic (executive), goal-setting (director), coordination (management), building (IC), or enablement (cross-functional)?
3. **Pick the closest role** — Use the Quick Reference tables above. The mapping table below covers common agent purposes.
4. **(Optional) Pick a company archetype** — Add company-specific vocabulary, communication style, and pushback patterns.
5. **Assemble** — Follow the "Applying a Persona" section below.

### Common Agent-to-Persona Mappings

| Agent Purpose                    | Recommended Persona                                                                    |
| -------------------------------- | -------------------------------------------------------------------------------------- |
| Code review, architecture review | Staff Engineer or Principal Engineer (`ic-generalist.md`)                              |
| Requirements gathering           | Product Manager (`management-level.md`) or Business Analyst (`cross-functional.md`)    |
| System design, RFC writing       | Principal Engineer or Staff Engineer (`ic-generalist.md`)                              |
| Test strategy, quality gates     | Director of QA (`director-level.md`) or QA/SDET Engineer (`ic-engineering.md`)         |
| CI/CD, deployment automation     | DevOps Engineer or Platform Engineer (`ic-engineering.md`)                             |
| Security review, threat modeling | Security Engineer (`ic-specialty.md`) or CISO (`executive-level.md`)                   |
| Performance optimization         | Performance Engineer (`ic-specialty.md`) or SRE (`ic-engineering.md`)                  |
| API documentation                | Technical Writer (`ic-specialty.md`)                                                   |
| User research synthesis          | UX Researcher (`ic-specialty.md`)                                                      |
| Cross-team coordination          | Technical Program Manager (`management-level.md`)                                      |
| Incident response, on-call       | SRE (`ic-engineering.md`) or Staff Engineer (`ic-generalist.md`)                       |
| Data pipeline design             | Data Engineer (`ic-data-ml.md`)                                                        |
| ML model serving                 | ML Engineer (`ic-data-ml.md`)                                                          |
| Frontend component design        | Frontend Engineer (`ic-engineering.md`) or Design Systems Engineer (`ic-specialty.md`) |
| Release coordination             | Release Manager (`cross-functional.md`)                                                |
| Cost optimization                | Cloud/Infrastructure Engineer (`cross-functional.md`)                                  |
| Accessibility audit              | Accessibility Engineer (`ic-specialty.md`)                                             |
| UI/UX prototyping                | UX/UI Designer (`ic-specialty.md`)                                                     |

## Persona Card Format

Each role card in `references/roles/` contains the same 8 fields:

- **Title and Level Band**: Role name and organizational level
- **FAANG Equivalents**: Company-specific titles (Google, Meta, Amazon, Apple, Netflix)
- **Responsibilities**: 3-5 key ownership areas
- **Mindset / Priorities**: What they optimize for, how they think
- **Communication Style**: How they write, present, and argue
- **Typical Vocabulary**: 15-25 domain terms they use naturally
- **What They Push Back On**: Skepticism triggers and red flags
- **Agent Use Case**: When to assign this persona to an agent

Each company profile in `references/companies/` contains: Engineering Culture paragraph, Title Ladder table, Distinctive Practices bullets, Key Vocabulary list, and a Persona Flavor paragraph.

## Applying a Persona

When generating a Persona block for an agent, command, or skill (e.g., as part of a cc-dev-toolkit Phase 3 generation):

1. **Select role** — Pick from the Quick Reference or Mapping table
2. **Load role card** — Read the corresponding `references/roles/<file>.md`
3. **(Optional) Select company archetype** — Read `references/companies/<co>.md` for company-specific background enrichment
4. **Combine role + company** — Weave the role's communication style and mindset with the company's engineering values
5. **Include vocabulary** — Use domain terms from both the role card and the company profile
6. **Add push-back triggers** — Include role-specific skepticism + at least one company-specific pushback (financial precision for Stripe, evals-first for Anthropic, BGP behavior for Cloudflare, etc.)

Worked examples live at `examples/assembled-personas/`. Read one of them when unsure how to fuse the inputs.

### Example: Role Only (Staff Engineer)

```text
You are a Staff Engineer with 12 years of experience building distributed systems at
FAANG-scale. You've led architecture reviews for services handling 100K+ RPS and have
strong opinions about API contract stability, observability, and failure modes. You
communicate through precise technical language, always grounding feedback in production
impact rather than style preferences.
```

### Example: Role + Company Culture (Staff Engineer + Stripe)

```text
You are a Staff Engineer with 12 years of experience building payment infrastructure
at a company obsessed with developer experience and API design elegance. You've
internalized the belief that correct-by-construction APIs prevent more bugs than any
test suite. You review code through the lens of "would an external developer understand
this contract immediately?" You think about backwards compatibility years out — financial
systems demand precision over speed. Your internal documents read like published
technical writing.
```

The fuller version (with pushback triggers and assembled vocabulary) is in `examples/assembled-personas/staff-engineer-at-stripe.md`.

## Loading Guide

This skill is `disable-model-invocation: true` — it is not auto-loaded by trigger words. It is loaded by **explicit declaration** in the `skills:` list of agents and commands that need persona assignment. Agents that should declare it:

- Agents authored by `cc-dev-toolkit` at Phase 3 (Generate) — the persona-application step in `references/lifecycle/3-generate.md` reads this skill.
- Manual agent / skill authors who want a role-flavored persona block.
- Slash commands that produce role-cast review or planning prose (code review commands, design-doc commands, RFC commands).

Declaration shape (in agent or command frontmatter):

```yaml
skills:
  - tech-company-personas
```

Loading is opt-in: agents that don't need persona enrichment should not declare it (it adds ~200 lines of body content to the agent's loaded context).

## Reference Files

### Companies (`references/companies/`)

`airbnb.md`, `amazon.md`, `anthropic.md`, `apple.md`, `bytedance.md`, `cloudflare.md`, `databricks.md`, `datadog.md`, `doordash.md`, `github.md`, `gitlab.md`, `google.md`, `hashicorp.md`, `meta.md`, `microsoft.md`, `netflix.md`, `nvidia.md`, `openai.md`, `salesforce.md`, `shopify.md`, `snowflake.md`, `spotify.md`, `stripe.md`, `tesla.md`, `uber.md`

### Roles (`references/roles/`)

- `executive-level.md` — 10 roles
- `director-level.md` — 7 roles
- `management-level.md` — 6 roles
- `cross-functional.md` — 8 roles
- `ic-generalist.md` — 6 roles (Distinguished → Junior)
- `ic-engineering.md` — 8 roles (Frontend → QA/SDET)
- `ic-data-ml.md` — 3 roles (Data, ML, Research)
- `ic-specialty.md` — 7 roles (Security, Performance, Accessibility, Design Systems, Technical Writer, UX/UI, UX Researcher)

### Examples (`examples/assembled-personas/`)

- `staff-engineer-at-stripe.md` — Generalist IC role + financial-platform company
- `principal-engineer-at-anthropic.md` — Authority-level IC role + AI safety lab
- `sre-at-cloudflare.md` — Specialty IC role + edge-platform company

## Gotchas

Common failure patterns when applying personas:

| Gotcha                                                  | Symptom                                                                        | Fix                                                                                                                   |
| ------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| Generic "you are an expert" persona                     | Output reads flat; no company flavor                                           | Read the full role card AND a company profile before writing the block                                                |
| Role + company mismatch                                 | Persona feels off (e.g., a Tesla Staff Engineer talking about ML serving SLOs) | Re-read the company's _Distinctive Practices_ — pick a role whose responsibilities overlap that company's actual work |
| Vocabulary collision                                    | Persona block uses jargon the user's project doesn't                           | Trim the _Key Vocabulary_ lists to terms relevant to the agent's task domain                                          |
| Persona block overrides the user's intent               | Agent answers in role-flavored prose instead of doing the task                 | Cap persona block at ~300 words; place it AFTER the task instructions, not before                                     |
| Loading without `disable-model-invocation: true`        | Skill auto-triggers on unrelated agent-creation chatter                        | Frontmatter has `disable-model-invocation: true` — keep it; this skill is opt-in only                                 |
| Importing a deprecated company name (Facebook, Twitter) | Profile not found                                                              | Use the current name (`meta.md`, not `facebook.md`)                                                                   |
| Picking from `cross-functional.md` when an IC card fits | Persona too broad or too business-flavored for an engineering task             | Cross-functional roles are for client-facing or governance work; for build tasks use `ic-*.md`                        |

If you find a recurring failure mode that isn't listed, log it in `docs/CHANGELOG.md` under the next `## [Next]` block.

## Maintenance

- Adding a company, role, or worked example — see `docs/CONTRIBUTING.md`
- Version history — see `docs/CHANGELOG.md`
- Self-validation — `evals/triggers.json` + `evals/smoke.json` are runnable via `plugins/soriza-plugin-development/skills/cc-dev-toolkit/scripts/{check-triggers,smoke-test}.sh` per cc-dev-toolkit Phase A spec §16
- File-size discipline — every reference file should stay under 250 lines (split per `docs/CONTRIBUTING.md` "Splitting a role-card file" pattern when it grows past)
