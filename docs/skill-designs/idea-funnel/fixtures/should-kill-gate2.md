# Fixture — should KILL at Gate 2 (Disconfirmation)

Expected: passes Gate 0 (founder fit) and Gate 1 (it IS testable), but dies at Gate 2 because the
strongest expert objection — a crowded, zero-moat market dominated by free incumbents — stands
unrebutted by evidence, and the SOM is negligible. This tests that the evidence-screen actually kills a
testable-but-doomed idea (the false-positive the funnel exists to catch). If it survives Gate 2, the
judge is being too lenient about unrebutted objections.

```json
{
  "id": "cand-another-todo-app",
  "title": "A to-do list app with AI task suggestions",
  "problem": "Solo freelancers forget tasks and want reminders with smart AI suggestions for what to do next.",
  "who": "Solo freelancers who manage their own workload",
  "why_now": "LLMs can suggest next actions",
  "idea_type": "ai-agent"
}
```

Checks:
- **Gate 0 (FMF):** advance — software, fits the founder.
- **Gate 1 (Testability):** advance — who/how-often/how-severe/status-quo are nameable.
- **Gate 2 (Disconfirmation):** **kill** — Thiel (no moat, red ocean of free todo apps) and the
  competitor-steelman (Todoist/TickTick/Notion/Apple Reminders already do this, many with AI) raise
  objections that public evidence *confirms* rather than rebuts; market read shows a saturated category
  with negligible reachable SOM. `strongest_unrebutted` should name the no-moat / incumbent objection.
