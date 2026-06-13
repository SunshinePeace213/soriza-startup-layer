# Retired skills (archived)

These skills are **retired** under the 9-step pipeline canon (`docs/loop-engineering-reference-en.md`
§2 / migration table §2.11). They live here, out of `.claude/skills/`, so Claude no longer discovers
or fires them — but they are kept (not deleted) as reference for building their replacements.

Redirect map (old → new step skill):

| Retired skill | Replaced by | Step(s) |
|---|---|---|
| `disconfirm` | `pressure-test` (α + β) | 4, 6 |
| `market-map` | `kill-scan` (demand/complaint mining) **+** `market-sizing` (TAM/SAM/SOM, buyer, trends) | 3, 7 |
| `solution-design` | `startup-brief` (drift audit + red-team + premortem) | 8 |
| `idea-stage-exit` | `startup-brief` (exit criteria + GO/NO-GO + override stamping) | 8 |

**Status note:** the replacement skills (`kill-scan`, `pressure-test`, `market-sizing`, `startup-brief`)
are not built yet — they are scheduled W2–W8 in the build plan (§12). Until then, pipeline steps 3/4/6/7/8
have no live skill. The doc's plan archived these in W11 *after* the replacements existed; this archival
ran earlier by request.

**Follow-up (W11 reference cleanup, not yet done):** kept skills still name the retired stages and now
have dangling references — `generate-ideas` is fixed; still stale: `sharpen-hypothesis`,
`customer-discovery-design`, `customer-discovery-synthesis`, `build-poc`, `create-founder-profile`, and the
`idea-stage` router refs (`expert-lens-map.md`, `doctrine-map.md`). The §7.6 `UserPromptExpansion`
deprecation guard (redirects `/disconfirm` etc.) is also not wired.
