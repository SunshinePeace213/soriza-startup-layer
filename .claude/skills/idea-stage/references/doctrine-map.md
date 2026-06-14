# Doctrine map — which doctrine each Idea-Stage stage reads

The shared routing config. Each stage **inline-reads** the named doctrine skill's `SKILL.md` (+ its
`references/`) — a cheap, deterministic reference read, **not** a `Skill`-tool invocation and **not** a
subagent. The doctrine skills are also standalone-invocable by the founder.

> The `idea-stage` index skill (Phase 2) owns this file as part of its spine config, alongside
> `expert-lens-map.md` (the pressure-test persona roster) and `stage-pipeline.md` (order + entry-guards).

| Stage | Reads (doctrine) | For |
|---|---|---|
| **generate-ideas** | `forward-deployed-founder` + `lean-startup` | bias the slate toward reachable-niche / distribution-first / business-builder wedges; flag undifferentiated-SaaS seeds; weight distribution in the recommendation; (lean) frame value/growth early |
| **sharpen-hypothesis** | `lean-startup` | name the **value** + **growth** hypotheses alongside the four problem dimensions |
| **pressure-test** (α/β) | persona lenses (via `expert-lens-map.md`) **+** `forward-deployed-founder` **+** `lean-startup` | the always-on doctrine angles: the *no-distribution / SaaS-dead* objection (FDF) and the *riskiest-assumption* objection (lean) |
| **market-sizing** | `forward-deployed-founder` | the moat / distribution read alongside sizing + buyer + trends |
| **startup-brief** | `lean-startup` + `forward-deployed-founder` + `solo-founder` | MVP type & pivots; does the concept own a workflow *and* a channel; is the scope a one-person job; the "**should we even build this?**" GO/NO-GO gate against the locked kill-criteria |
| **build-poc** | `lean-startup` + `solo-founder` | the MVP-type chooser (video/concierge/WoZ/functional); scope the build to what a solo founder can run |

## Notes

- **Inline read, not invocation.** A stage opens the doctrine skill's content and applies it; it does not
  spawn an agent or call the `Skill` tool. This mirrors how `pressure-test` reads `expert-lens-map.md`.
- **Persona lenses are routed separately.** The `pressure-test` persona panel (fixed core-3 Thiel/Munger/
  Bezos + competitor-steelman + ≤1 idea-type specialist) lives in `expert-lens-map.md`, not here. This
  file is only the *doctrine* routing.
- **Adding a doctrine** is a one-line edit here plus the new `lean-startup`-style skill; no stage code
  changes.
