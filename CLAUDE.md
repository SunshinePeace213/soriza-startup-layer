## Soriza Startup Layer

### Pipeline Constitution

#### 1. Pipeline Canon
- **Stages**: Idea Stage = 9 steps: generate -> hypothesis -> kill-scan -> pressure-a ->
  discovery (design / human interviews / synthesis) -> pressure-b -> sizing -> startup-brief -> PoC
- **Spec**: step cards in `docs/loop-engineering-reference-en.md` SS2. The legacy stage order (disconfirm / market-map / solution-design / idea-stage-exit as standalone stages) is RETIRED -- see the migration table SS2.11

#### 2. Write Rules (hook-enforced)
- **Write path**: ONLY write inside `ideas/<ACTIVE>/` and `ideas/_exploration/`;
  ACTIVE = contents of `ideas/ACTIVE` (hook-enforced)
- **Gates**: NEVER edit the `gates:` block of STATE.md -> run
  `uv run scripts/advance_gate.py` instead (hook-enforced)
- **Agent-writable STATE fields**: `status`, `next_action`, `step_checklist`, `deltas_pending` only
- **Hypothesis**: NEVER edit `hypothesis.md` outside `sharpen-hypothesis` -> emit a
  "Hypothesis Updates Flagged" block; folding is that skill's exclusive right
- **Validation feedback**: every artifact write is schema-checked (hook-enforced); on stderr feedback, fix and rewrite -- do not argue, do not bypass

#### 3. Evidence Rules
- **Web ingress**: web content enters artifacts ONLY via `evidence-ledger.jsonl`; the research
  agent is the single web entry point
- **Grading**: 1=first-party commitment (money/time/intro) | 2=interview quote |
  3=persona opinion | 4=web source (URL required) | 5=founder belief
- **Citations**: ALWAYS cite external facts as `E-xxx`; interview claims cite grade <=2 only

#### 4. Kill Authority
- **Desk kills**: hard, checkable facts ONLY (kill-scan: legality / technical impossibility).
  Subjective merit dies only to real users + the founder's signature
- **p_success**: a calibration prediction, NEVER a verdict

#### 5. Tooling & Runtime
- **Python**: Always `uv` (`uv run scripts/...`, `uv run pytest`) -- inherits global CLAUDE.md; never restated here beyond this pointer
- **Paths**: schemas `tests/schemas/` | gate script `scripts/advance_gate.py` |
  agents `.claude/agents/` | reference `docs/loop-engineering-reference-en.md`

<!-- W2 insert: ## 6. Two-Round Protocol -- independent round blind; cross-exam p-changes need revision_note (ref SS6.3) -->
<!-- W5 insert: ## 7. Hook Behaviour -- Stop blocks until agent-owned checklist items clear; schema failures arrive as stderr -->
<!-- W11: update SS1 pipeline table; remove legacy names -->

<!-- ### Founder Background
@docs/founder-profile.md -->