# Soriza Startup Layer — task runner
# Run `just` (no args) to list recipes. Docs: https://just.systems
#
# This repo is a Claude Code agentic layer: skills (.claude/skills/*/SKILL.md),
# subagents (.claude/agents/*.md), JS workflows, memory, and Python factory
# tooling under prompt-architect. The recipes below wrap the repeatable chores:
# validating artifact frontmatter, enforcing the <300-char description budget,
# packaging skills, the nuwa transcript pipeline, and housekeeping — plus
# preset Claude Code session launchers.

# ---- Settings -------------------------------------------------------------
set shell := ["bash", "-eu", "-o", "pipefail", "-c"]
# Expose recipe args as $@/$1/... so launchers can pass-through quoted prompts.
set positional-arguments

# ---- Variables ------------------------------------------------------------
python        := "python3"
skills_dir    := ".claude/skills"
agents_dir    := ".claude/agents"
pa            := ".claude/skills/prompt-architect/scripts"
desc_max      := "300"
claude_effort := "xhigh"

# ---- Meta -----------------------------------------------------------------

# List all recipes (default when you run bare `just`)
default:
    @just --list --unsorted

# Print resolved tool versions / environment
doctor:
    @echo "just     : $(just --version)"
    @echo "claude   : $(command -v claude >/dev/null && claude --version || echo 'NOT on PATH')"
    @echo "python   : $({{python}} --version 2>&1)  ($(command -v {{python}}))"
    @echo "uv       : $(command -v uv || echo 'NOT installed — nuwa scripts fall back to {{python}}')"
    @echo "yt-dlp   : $(command -v yt-dlp || echo 'NOT installed — needed by `just subs`')"
    @echo "skills   : $(ls -1d {{skills_dir}}/*/ 2>/dev/null | wc -l)"
    @echo "agents   : $(ls -1 {{agents_dir}}/*.md 2>/dev/null | wc -l)"

# ---- Claude Code session launchers ----------------------------------------
# Open an interactive Claude Code session with a preset flag combo. Extra args
# pass straight through (quoted), so:  just ca -c   |   just ca "review this repo"
# Flags (see `claude --help`):
#   --permission-mode {auto|acceptEdits|plan|dontAsk|bypassPermissions|default}
#   --effort {low|medium|high|xhigh|max}      --model {opus|sonnet|haiku}
# Fast mode has NO CLI flag — toggle it in-session with /fast.

# ca: default driver — auto permission mode + xhigh effort
ca *args:
    @claude --permission-mode auto --effort {{claude_effort}} "$@"

# cc: continue the most recent conversation in this dir (auto + xhigh)
cc *args:
    @claude --permission-mode auto --effort {{claude_effort}} --continue "$@"

# cr: resume a past conversation via picker (auto + xhigh)
cr *args:
    @claude --permission-mode auto --effort {{claude_effort}} --resume "$@"

# cap: plan-first — planning mode, nothing changes until you approve (xhigh)
cap *args:
    @claude --permission-mode plan --effort {{claude_effort}} "$@"

# cf: fast/cheap driver — Sonnet, auto mode, high effort
cf *args:
    @claude --permission-mode auto --effort high --model sonnet "$@"

# cyolo: bypass ALL permission checks + max effort — sandbox/throwaway only
cyolo *args:
    @claude --permission-mode bypassPermissions --effort max "$@"

# ---- Validation (the core quality gate) -----------------------------------

# Validate every skill AND subagent's frontmatter; non-zero exit if any fail
validate: validate-skills validate-agents
    @echo "✓ all artifacts valid"

# Validate every skill directory (SKILL.md frontmatter)
validate-skills:
    #!/usr/bin/env bash
    fail=0
    for d in {{skills_dir}}/*/; do
        name=$(basename "$d")
        if ! out=$({{python}} {{pa}}/quick_validate.py "$d" 2>&1); then
            echo "✗ skill  $name"; echo "$out" | sed 's/^/    /'; fail=1
        else
            echo "✓ skill  $name"
        fi
    done
    exit $fail

# Validate every subagent .md (frontmatter as artifact-type subagent)
validate-agents:
    #!/usr/bin/env bash
    fail=0
    for f in {{agents_dir}}/*.md; do
        name=$(basename "$f" .md)
        if ! out=$({{python}} {{pa}}/quick_validate.py "$f" --artifact-type subagent 2>&1); then
            echo "✗ agent  $name"; echo "$out" | sed 's/^/    /'; fail=1
        else
            echo "✓ agent  $name"
        fi
    done
    exit $fail

# Validate ONE skill by name, e.g. `just validate-one grill-me`
validate-one name:
    {{python}} {{pa}}/quick_validate.py {{skills_dir}}/{{name}}

# ---- Description budget ----------------------------------------------------
# Layer standard: every SKILL.md `description:` stays < 300 chars so the
# skill-listing stays inside Claude Code's per-entry + global budget.
# NOTE: subagents (.claude/agents/*.md) are deliberately excluded — they live
# in the Agent-tool type list (a larger, separate per-entry cap) and carry
# longer delegation-trigger descriptions on purpose.

# Flag any skill whose description exceeds the char budget
check-desc:
    #!/usr/bin/env python3
    import sys, pathlib, re
    MAX = {{desc_max}}
    roots = sorted(pathlib.Path("{{skills_dir}}").glob("*/SKILL.md"))
    bad = []
    for p in sorted(roots):
        text = p.read_text(encoding="utf-8")
        m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        if not m:
            continue
        fm = m.group(1)
        dm = re.search(r"^description:\s*(.*(?:\n[ \t]+.*)*)", fm, re.M)
        if not dm:
            continue
        desc = " ".join(line.strip() for line in dm.group(1).splitlines()).strip().strip('"\'')
        n = len(desc)
        flag = "✗" if n >= MAX else "✓"
        label = p.parent.name if p.name == "SKILL.md" else p.stem
        print(f"{flag} {n:4d}  {label}")
        if n >= MAX:
            bad.append(label)
    if bad:
        print(f"\n{len(bad)} over the {MAX}-char budget: {', '.join(bad)}", file=sys.stderr)
        sys.exit(1)
    print(f"\nall descriptions < {MAX} chars")

# ---- Packaging ------------------------------------------------------------

# Package one skill into a distributable .skill file under dist/
package name:
    @mkdir -p dist
    {{python}} {{pa}}/package_skill.py {{skills_dir}}/{{name}} dist/

# Package every skill into dist/
package-all:
    #!/usr/bin/env bash
    mkdir -p dist
    for d in {{skills_dir}}/*/; do
        {{python}} {{pa}}/package_skill.py "$d" dist/
    done
    echo "✓ packaged $(ls dist/*.skill 2>/dev/null | wc -l) skills into dist/"

# ---- Nuwa / perspective-skill pipeline ------------------------------------

# Download YouTube subtitles for distillation, e.g. `just subs <url> subs/`
subs url out_dir="subs":
    bash {{skills_dir}}/nuwa-skill/scripts/download_subtitles.sh {{url}} {{out_dir}}

# Convert an .srt/.vtt into a clean transcript on stdout
srt file:
    {{python}} {{skills_dir}}/nuwa-skill/scripts/srt_to_transcript.py {{file}}

# Quality-check a generated SKILL.md against the nuwa pass criteria
nuwa-check file:
    {{python}} {{skills_dir}}/nuwa-skill/scripts/quality_check.py {{file}}

# ---- Housekeeping ---------------------------------------------------------

# Remove macOS cruft and Python caches
clean:
    #!/usr/bin/env bash
    find . -name '.DS_Store' -not -path './.git/*' -delete -print
    find . -name '__pycache__' -type d -not -path './.git/*' -prune -exec rm -rf {} + -print
    find . -name '*.pyc' -not -path './.git/*' -delete
    echo "✓ cleaned"

# Prune stale git worktrees (the layer spawns these for bg/idea-funnel jobs)
prune-worktrees:
    git worktree prune -v
    @echo "--- remaining worktrees ---"
    @git worktree list

# Quick repo inventory
stats:
    @echo "skills    : $(ls -1d {{skills_dir}}/*/ 2>/dev/null | wc -l)"
    @echo "agents    : $(ls -1 {{agents_dir}}/*.md 2>/dev/null | wc -l)"
    @echo "workflows : $(ls -1 .claude/workflows/*.js 2>/dev/null | wc -l)"
    @echo "memory    : $(ls -1 .claude/memory/*.md 2>/dev/null | grep -v MEMORY.md | wc -l)"
    @echo "py scripts: $(find {{skills_dir}} -name '*.py' | wc -l)"

# ---- Composite gate -------------------------------------------------------

# Run the full local quality gate before committing
precommit: clean validate check-desc
    @echo "✓ precommit passed"
