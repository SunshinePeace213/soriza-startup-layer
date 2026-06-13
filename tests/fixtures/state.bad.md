---
slug: bad-state
schema_version: 1
current_step: 5
step_name: customer_discovery
status: halfway
owner: nobody
interview_budget: {total: 10, used: 99}
step_checklist:
  - {item: "missing owner and done"}
deltas_pending: []
gates:
  g4: {result: proceed, date: 2026-07-01}
next_action: ""
updated: 2026-07-08T21:40+08:00
---
Intentionally invalid: schema_version 1, bad status/owner enums, used>total, malformed
checklist item, gate g4 missing criteria+decision, empty next_action, no blocking field.
