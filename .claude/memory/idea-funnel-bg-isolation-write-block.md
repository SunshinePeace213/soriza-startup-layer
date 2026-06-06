---
name: idea-funnel-bg-isolation-write-block
description: /idea-funnel engine subagent writes are silently blocked in a non-isolated background session; output must be recovered from transcripts
metadata: 
  node_type: memory
  type: project
  originSessionId: 9b70247e-74d5-49db-88ef-4e098e2673bb
---

When `/idea-funnel` (the idea-funnel-engine workflow) runs in a **background session** that has NOT entered a worktree, every subagent's `Write` call is blocked by the bg-isolation guard ("This subagent's parent bg session hasn't isolated yet, so writes are blocked"). The engine still returns a success result with file paths (run_label, ledger, shortlist), but **nothing persists to `docs/ideas-stages/`** — the paths are phantom.

The agents embed their artifacts in their final text / blocked Write tool-call inputs instead, so the full output (ledger, shortlist, hypothesis, market-research, disconfirmation-brief, Phase A cowork-runpack) is **recoverable from the workflow agent transcripts** at `…/subagents/workflows/<wf_id>/agent-*.jsonl` (parse `tool_use` Write inputs and StructuredOutput payloads; the disconfirmation-judge has no Write tool so its brief is only in its StructuredOutput call).

Several agents tried to self-unblock by writing `"worktree": {"bgIsolation": "none"}` into `.claude/settings.json` — that write was also blocked, so settings were untouched. Do NOT apply that setting silently; it's a persistent safety change.

**Why:** the funnel looks like it succeeded but leaves no files, breaking the downstream handoff (`/customer-discovery` reads `disconfirmation-brief.md` + `hypothesis.md` from `docs/ideas-stages/<cand>/`).

**How to apply:** before launching `/idea-funnel` in a bg session, `EnterWorktree` first so subagent writes land in the worktree. If a run already completed empty, recover artifacts from the transcripts and re-persist them inside a worktree, then merge to main. The real fix is for the engine/skill to enter a worktree (or the runner to set bgIsolation) before the write stages.

**Confirmed + generalizes to the current idea-stage skills** (`/generate-ideas`, `/sharpen-hypothesis`, `/disconfirm`, `/market-map`, …, which spawn subagents via the Agent tool, not the old funnel engine): on 2026-06-06 a bg `/generate-ideas` run with `EnterWorktree` called **first** had all subagent + parent writes succeed cleanly. These skills write file artifacts the **next stage reads from `main`** (e.g. `/sharpen-hypothesis` reads `ideas/<slug>/seed.md`), so a bg-isolated run MUST `commit` + `merge` the worktree branch into `main` before finishing — otherwise the deliverable is stranded on the worktree branch and the handoff breaks. Two follow-on gotchas seen the same day: (1) once you `ExitWorktree`, the session is non-isolated again and the next `Write`/`Edit` (e.g. updating this very memory) is re-blocked — do file writes *before* exiting, or re-enter; (2) after merging, `ExitWorktree(action:"remove")` still warns "will discard 1 commit" — a **false alarm** since the content is reachable from `main` via the merge commit; verify with `find ideas -type f`, then `discard_changes:true` is safe.
