---
name: nuwa-skill
description: |
  Distill how anyone thinks into a runnable perspective skill — auto-research, extract a thinking framework (mental models, heuristics, expression DNA), generate the SKILL.md. Use for "create a perspective skill for X", "distill X", "build me a [name] skill", "turn X into a skill", "nuwa".
---

# Nuwa — The Skill That Makes Skills

> "The parts you cannot fit into a SKILL.md are your real moat. But the parts you can fit are already powerful enough."

Nuwa is named after the goddess in Chinese mythology who shaped human beings out of clay. Here the clay is public information — books, talks, interviews, decisions, social posts — and what gets shaped is not a person but a **mirror**: a runnable skill that lets you see your own problem through someone else's eyes.

## Core Philosophy

Nuwa does **not** copy people. It extracts thinking frameworks.

A good perspective skill is a runnable cognitive operating system that captures:

- **Mental models** — the lenses this person uses to see the world
- **Decision heuristics** — the rules of thumb they reach for under uncertainty
- **Expression DNA** — the recognizable fingerprint of how they speak and write
- **Anti-patterns** — what they refuse to do, the value floor
- **Honest limits** — what the skill genuinely cannot do

The key distinction: capture **how** they think, not **what** they said. A skill that only quotes is a parrot. A skill that runs the framework can analyze problems the person has never publicly addressed.

---

## Execution Flow

The pipeline has five phases (0 through 4). Phase 0 routes the request, Phase 1 collects evidence in parallel, Phase 2 synthesizes mental models, Phase 3 builds the deliverable, Phase 4 validates it.

### Phase 0 — Clarify the Request (≈30 seconds)

Two entry paths, picked by how concrete the request is.

**Path A — Direct (the user named someone or something specific)**

Confirm four things, briefly:

1. **Who / what** — name disambiguation if needed (e.g., "Paul Graham the YC essayist, not the philosopher")
2. **Focus** (optional) — full portrait, or zoomed in on one dimension (e.g., "Munger as investor" vs. "Munger as life philosopher")
3. **Intended use** — thinking advisor, decision reference, or full role-play
4. **New or update** — does a skill for this person already exist locally? If yes, run the incremental update flow at the bottom of this file

If the user just says "do X" with no extras, default to: full portrait + thinking advisor + new skill, and proceed.

**Path B — Diagnostic (the user described a problem, not a person)**

Examples: "I want to make better investment decisions", "I'm stuck on how to explain technical stuff", "help me think clearer about risk". In this case, recommend candidates from two sources:

- **Source A — existing local skills.** Scan `.claude/skills/*-perspective/` and read each `SKILL.md` description. Match against the user's stated need.
- **Source B — new distillation candidates.** Suggest 2–4 people whose published thinking frameworks best fit the problem, and explain *which framework of theirs* solves *which part* of the user's problem.

Present recommendations as a short numbered list, mark each as ⚡ Already installed or 🆕 Will need to distill, and let the user pick.

### Phase 0.5 — Create the Skill Directory

**Run this the moment Phase 0 is confirmed, before any research starts.** The skill must be a self-contained directory so the whole thing is portable and inspectable later.

```
[person-name]-perspective/
├── SKILL.md                          # Final deliverable
├── scripts/                          # Helper tools (copied from nuwa-skill)
│   ├── download_subtitles.sh         # YouTube subtitle downloader
│   ├── srt_to_transcript.py          # SRT → clean transcript
│   ├── merge_research.py             # Phase 1.5 checkpoint generator
│   └── quality_check.py              # Phase 4 automated quality gate
└── references/
    ├── research/                     # Raw output of each research agent
    │   ├── 01-writings.md            # Books, essays, newsletters
    │   ├── 02-conversations.md       # Long interviews, podcasts, AMAs
    │   ├── 03-expression-dna.md      # Short-form: tweets, posts, fragments
    │   ├── 04-external-views.md      # What others say about them
    │   ├── 05-decisions.md           # Actual decisions and turning points
    │   └── 06-timeline.md            # Life and thought timeline
    └── sources/                      # Downloaded primary material
        ├── books/
        ├── transcripts/
        └── articles/
```

**Iron rule:** every sub-agent in Phase 1 MUST write its findings into the matching `references/research/0X-*.md` file. Research that doesn't get saved to a file never happened. Copying the skill directory to another machine must reproduce the same result.

---

### Phase 1 — Parallel Research Swarm (6 Agents)

Spawn six sub-agents in parallel. Each owns one slice of the evidence space.

#### Agent Assignments

| Agent | Sources to mine | What to extract | Output file |
|-------|-----------------|-----------------|-------------|
| **1. Writings** | Books, essays, papers, newsletters | Core arguments that recur ≥3 times = real beliefs. Coined terms. Reading lists. | `01-writings.md` |
| **2. Conversations** | Podcasts, long videos, AMAs, deep interviews | Responses under pressure, off-the-cuff analogies, changed positions, refused questions. | `02-conversations.md` |
| **3. Expression** | X/Twitter, short posts, fragments | High-frequency sentence patterns, controversial stances, humor style, public debates. | `03-expression-dna.md` |
| **4. External views** | Critic analyses, book reviews, biographies | Patterns observed by outsiders, criticisms, peer comparisons, blind spots. | `04-external-views.md` |
| **5. Decisions** | Major decisions, turning points, controversial actions | Decision context and logic, post-hoc reflections, gap between words and actions. | `05-decisions.md` |
| **6. Timeline** | Birth/debut → today | Key milestones, thought turning points. **Always include the last 12 months** to prevent staleness. | `06-timeline.md` |

#### Hard Rules for Every Agent

- Save results to `references/research/0X-*.md`. No exceptions.
- Tag every claim with source and credibility (primary > secondary > inference).
- Distinguish "they said" vs. "others said about them" vs. "I inferred from pattern".
- When you find contradictions, **preserve them**. Don't smooth them away.

#### Source Priority

| Source type | What it reveals | Weight |
|-------------|-----------------|--------|
| Their own long-form writings | Systematic thinking | Highest |
| Long interviews / podcasts | Improvisational thinking process | Highest |
| Actual decision records | Real behavior vs. claims | Highest |
| Social media | Expression style, instant reactions | Medium |
| Others' evaluations | External perspective, blind spots | Medium |
| Second-hand accounts | Reference only, needs verification | Low |

#### Source Blocklist

Skip aggregator and SEO-content sites that are unreliable. For figures whose primary material is in Chinese, exclude Zhihu (知乎), WeChat public-account articles (微信公众号), and Baidu Baike/Zhidao. Accept only authoritative outlets such as 36Kr, GeekPark, LatePost, Caixin, Yicai, Huxiu, SSPAI.

#### Local Corpus Mode

If the user supplies their own files (PDFs of books, transcript dumps, internal documents) for the subject, the agents prioritize those primary sources over web searches. Save copies into `references/sources/`.

#### Failure Handling

- **Agent times out or finds nothing**: do not wait. Move on. Mark "insufficient information" for that dimension in Phase 2.
- **Source scarcity (<10 usable items overall)**: alert the user at Phase 0.5. Lower the quality expectations. Expand the "Honest limits" section in the final skill.
- **Agents return conflicting findings**: keep both. Contradictions are signal, not noise.

**Principle:** an honest 60-point skill with clearly marked gaps is more useful than a fake 90-point skill that hallucinated to fill them.

#### Helper Scripts

Four scripts in `scripts/` automate the repetitive parts of Phase 1, Phase 1.5 and Phase 4. Use them; don't reimplement.

The three Python scripts use [`uv`](https://docs.astral.sh/uv/) and PEP 723 inline metadata, so they self-execute with no setup — `uv` reads the dependency block from the file itself. If `uv` isn't installed, run `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv`).

| Script | When | Command |
|--------|------|---------|
| `download_subtitles.sh` | Phase 1, when an agent needs a YouTube transcript | `bash scripts/download_subtitles.sh <youtube_url> sources/transcripts/` — auto-prefers manual subtitles, falls back to auto-generated; tries English, then Chinese, then any. Requires `yt-dlp` (install with `uv tool install yt-dlp`). |
| `srt_to_transcript.py` | Right after `download_subtitles.sh` | `uv run --script scripts/srt_to_transcript.py <input.srt>` — strips timestamps, cue indices, HTML tags, sound tags, and de-duplicates consecutive overlapping lines |
| `merge_research.py` | Phase 1.5 checkpoint | `uv run --script scripts/merge_research.py <skill_dir>` — scans `references/research/01-06.md`, counts sources, classifies primary vs. secondary, surfaces contradiction markers, and prints the checkpoint table |
| `quality_check.py` | Phase 4, automated portion | `uv run --script scripts/quality_check.py <SKILL.md>` — verifies all six pass criteria (mental-model count, per-model limits, expression DNA, honest limits, internal tensions, primary-source ratio); exits non-zero on failure |

On a Unix system you can also chmod +x the scripts and invoke them directly (`./scripts/quality_check.py <SKILL.md>`) — the shebang `#!/usr/bin/env -S uv run --script` resolves the same way.

The scripts ship in this repo's `scripts/` directory. When Phase 0.5 creates a new perspective-skill directory, copy `scripts/` into it so the resulting skill is fully self-contained.

### Phase 1.5 — Research Review Checkpoint

After all agents finish, **pause** and show the user a research-quality summary:

```
┌──────────────────┬──────────┬─────────────────────────────┐
│ Agent            │ Sources  │ Key Findings                │
├──────────────────┼──────────┼─────────────────────────────┤
│ 1 Writings       │ 8        │ Core thesis: ...            │
│ 2 Conversations  │ 5        │ Position change on X: ...   │
│ 3 Expression     │ 120      │ High-frequency phrase: ...  │
│ 4 External       │ 6        │ Main criticism: ...         │
│ 5 Decisions      │ 4        │ Pivotal decision: ...       │
│ 6 Timeline       │ Complete │ Latest activity: March 2026 │
├──────────────────┼──────────┼─────────────────────────────┤
│ Contradictions   │ 2        │ A1 says X, A4 observed Y    │
│ Information gaps │ None     │                             │
└──────────────────┴──────────┴─────────────────────────────┘
```

- User says "good, continue" → go to Phase 2.
- User wants more on some dimension → re-run that one agent before moving on.

---

### Phase 2 — Framework Extraction

This phase synthesizes raw research into the building blocks of the skill. The detailed methodology lives in `references/extraction-framework.md` — read it before this phase if depth matters.

#### 2.1 Mental Models (3–7 total)

For a candidate to count as a real mental model — not a one-off quote — it must pass **triple verification**:

1. **Cross-domain recurrence** — the same framework appears in at least two distinct domains this person discusses.
2. **Generative power** — using the model, you can predict their stance on a new problem they have not publicly addressed.
3. **Exclusivity** — it is not a generic "best practice" any smart person would name; it reflects this person's particular angle.

Each surviving model is recorded with: name, one-line description, source evidence (≥2 scenarios), how it is applied, where it fails.

#### 2.2 Decision Heuristics (5–10 total)

These are the "if-then" rules of thumb the person uses when judging fast. Each one needs at least one concrete case behind it.

#### 2.3 Expression DNA

| Dimension | What to capture |
|-----------|-----------------|
| Sentence structure | Long vs. short, statement vs. question, analogy density |
| Vocabulary | High-frequency words, proprietary jargon, words they never use |
| Rhythm | Conclusion-first vs. setup-first, transition style |
| Humor style | Sarcastic, self-deprecating, absurdist, dry, none |
| Certainty register | "I'm not sure" type vs. "obviously" type |
| Citation habits | Whom they cite, what kind of source |

#### 2.4 Values & Anti-patterns

- **Values** — 3–5 core values in rough rank order.
- **Anti-patterns** — behaviors and lines of thinking the person explicitly opposes.
- **Internal tensions** — value pairs that genuinely pull against each other. This is usually the most interesting layer.

#### 2.5 Intellectual Genealogy

Who shaped this person → them → whom they have shaped. Where they sit on the intellectual map.

#### 2.6 Honest Limits

What the finished skill MUST explicitly admit:

- Cannot predict responses to entirely novel problems with full confidence
- Cannot substitute for the person's intuition and creativity
- Public statements ≠ private beliefs
- Information is frozen at the research cutoff date

---

### Phase 3 — Build the Skill File

Read `references/skill-template.md` for the canonical structure. The template defines every section the output `SKILL.md` must contain: frontmatter, role-play rules, agentic response protocol, identity card, mental models, decision heuristics, expression DNA, timeline, values, intellectual genealogy, honest limits, research sources, attribution.

Fill the template section by section from Phase 2 output:

| Template section | Filled from |
|------------------|-------------|
| Frontmatter `description` | Tight routing card only (≤ ~300 chars): `Think like X — <identity>. Use for X's lens. Triggers — …`. No bio — that lives in the Identity Card. See `references/skill-template.md` → description guidance. |
| Role-play rules | Use template defaults; no customization needed |
| Agentic response protocol | Auto-derived from mental models (see the template for the recipe) |
| Identity card | Timeline (06) + Writings (01) → 50-word self-intro in the person's voice |
| Mental models | Phase 2.1 results, each with name / evidence / application / limits |
| Decision heuristics | Phase 2.2 results, each with scenario + case |
| Expression DNA | Phase 2.3 results, translated into style rules for the role-play |
| Timeline | Agent 6 results, condensed to a key-milestone table |
| Values & anti-patterns | Phase 2.4 |
| Intellectual genealogy | Phase 2.5 |
| Honest limits | Phase 2.6 + research cutoff date |
| Research sources | Combined citations from all six agents, split into primary / secondary |
| Attribution | Fixed footer crediting Nuwa and the original creator |

Write the finished file to `.claude/skills/[person-name]-perspective/SKILL.md`.

---

### Phase 4 — Quality Validation

After the skill is written, **spawn a fresh sub-agent** (independent of the main agent, to avoid self-grading bias) and run three tests.

#### 4.1 Known Test (Sanity Check)

Pick three questions this person has publicly answered. Have the sub-agent answer them *with the new skill loaded*. Compare to actual stance.

- Direction matches → the framework is running.
- Significant deviation → trace which mental model misled it and adjust weights.

#### 4.2 Edge Test

Pick one question this person has never publicly discussed but that is adjacent to their interests. Use the skill to infer.

- A good output reads like "Based on models X and Y, the likely view is … but I am uncertain because …"
- A bad output is absolutely certain. Certainty here means the skill is hallucinating.

#### 4.3 Voice Test

Write a 100-word analysis using the skill. Judge:

- Does it carry this person's expression signature?
- Is it free of generic AI platitudes ("It's important to consider multiple perspectives…")?
- Is it more than a patchwork of direct quotes?

#### Pass / Fail Criteria

| Check | Pass | Fail signal |
|-------|------|-------------|
| Mental model count | 3–7, each with source evidence | <3 or >10 |
| Per-model limits | Failure conditions explicitly stated | Only upsides listed |
| Expression DNA | A reader can identify who in 100 words | Reads like generic ChatGPT |
| Honest limits | ≥3 specific limits | Only the boilerplate "can't replace the real person" |
| Internal tensions | ≥2 genuine contradiction pairs | All views suspiciously consistent |
| Primary-source ratio | >50% | Mostly second-hand accounts |

The first, second, third, fourth, fifth, and sixth checks above are all automated by `scripts/quality_check.py`. Run `uv run --script scripts/quality_check.py <SKILL.md>` for a deterministic pass/fail report. The Voice Test (4.3) still requires human judgment.

**Iteration cap:** Phase 2 → Phase 4 loops at most twice. If a check still fails after the second pass, mark the weak dimension in "Honest limits" and deliver the best version available. Don't polish forever.

Show validation results to the user for confirmation before declaring done.

---

## Updating an Existing Skill

When the user says "update X's skill" or "X just published a new book / made a major decision":

1. Read the existing `SKILL.md` and note the previous research cutoff date.
2. Re-run only **Agent 2** (latest interviews), **Agent 5** (recent decisions), and **Agent 6** (timeline update).
3. Diff the new findings against the existing content — strengthen, update, or add.
4. Patch the `SKILL.md` incrementally. Do not rewrite the whole file.

---

## Taste Guidelines

### Good Skill vs. Bad Skill

| Good skill | Bad skill |
|------------|-----------|
| Handles new problems competently | Can only repeat old quotes |
| Has internal contradictions | All views suspiciously consistent |
| Acknowledges uncertainty | Has a confident answer for everything |
| 3–7 deep, sharp models | 20 vague "principles" |
| Recognizable voice | Reads like generic ChatGPT |
| Explicit about limits | Implies it can replace the person |

### Research Taste

1. **Primary > secondary.** Their words beat reports about them.
2. **Long-form > quote.** A 3,000-word essay reveals more structure than 50 tweets.
3. **Controversy > consensus.** Their most-disputed views show the most uniqueness.
4. **Change > fixed.** Positions that shifted carry more information than ones that never moved.
5. **Behavior > words.** Real decisions beat public statements.

### Extraction Taste

1. **Less is more.** Three deep models beat fifteen shallow principles.
2. **Contradictions are features, not bugs.** Preserve internal tension.
3. **Don't beautify.** Blind spots and limits are part of who they are.
4. **Falsifiable.** Each mental model should be verifiable or refutable with specific cases.

### Never Do

- Fabricate things this person never said.
- Package generic wisdom as their "unique insight".
- Hide negative evaluations and controversies.
- Imply the skill equals the person.
- Force-generate when information is insufficient.

---

## Special Scenarios

### Living Person vs. Historical Figure

- **Living**: timeliness matters. Mark the cutoff date clearly. Suggest periodic updates.
- **Historical**: source material is more stable but more likely shaped by biographers. Cross-source verify aggressively.

### Topic Skill vs. Person Skill

When the input is a topic ("value investing", "evolutionary biology", "X/Twitter growth") rather than a person:

- Phase 1 searches for the field's core practitioners and theorists.
- Phase 2 extracts the **domain consensus** plus the **school-of-thought divergences**.
- The output centers on the topic and cites multiple person-perspectives within it.

See `references/extraction-framework.md` Section 5 for the full person-vs-topic comparison.

---

## Reference Files

- `references/extraction-framework.md` — Full methodology: triple verification, expression-DNA quantification, contradiction handling, quality checklist. Read this first when depth matters.
- `references/skill-template.md` — The canonical structure for the output `SKILL.md`. Read this at Phase 3 before populating.
- `scripts/download_subtitles.sh` — Bash wrapper around `yt-dlp` with tiered language fallback. Requires `yt-dlp` on PATH (`uv tool install yt-dlp`).
- `scripts/srt_to_transcript.py` — Self-executing via `uv run --script`. Stdlib-only (no dependencies). Strips SRT/VTT machinery to leave clean readable prose.
- `scripts/merge_research.py` — Self-executing via `uv run --script`. Stdlib-only. Builds the Phase 1.5 checkpoint table from the six per-agent files.
- `scripts/quality_check.py` — Self-executing via `uv run --script`. Stdlib-only. Returns exit 0 if and only if all six Phase 4 criteria pass.

---

## A Note on Attribution

Nuwa is a port-to-English of the original `nuwa-skill` framework by [Huashu / 花叔 (@AlchainHust)](https://x.com/AlchainHust), open-sourced at <https://github.com/alchaincyf/nuwa-skill>. The Chinese name 女娲 refers to the creator goddess in Chinese myth who shaped humans from clay. The methodology, the four-phase pipeline, the triple-verification rule, and the 6-agent research swarm are all his design. This English version preserves the structure verbatim and translates the Chinese text directly into plain English so the framework can be managed by English-speaking teams.

---

## Final Note

Nuwa doesn't create people. It creates mirrors.

A good perspective skill lets you see your own problem through someone else's eyes. The point is not to imitate them — it is to widen your own thinking boundary.
