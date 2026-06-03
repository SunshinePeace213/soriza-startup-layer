# The Idea-Stage Validator kills on evidence, not on a simulated debate

**Status:** accepted

The Idea-Stage Validator runs many Candidates through the pipeline with no human in the chair.
Pressure-test's verdict normally derives its meaning from a *real founder* committing substantive
responses that the expert panel then judges. Automating that would force the agent to fabricate the
founder's defense and then grade it — the agent marking its own homework, which manufactures
false-positives at scale (the exact failure the human-gated pipeline exists to prevent).

**Decision.** In a Funnel run, pressure-test runs as an **objection screen**, not a debate: experts
(plus the competitor-steelman) generate their strongest disconfirming objections, and the engine
kills a Candidate only when its strongest objection stands **unrebutted by external evidence**
gathered the same pass. No fabricated founder voice; no multi-round rebuttal loop. The **full
debate** — 4 rounds, multiple personas, the founder actually defending — is preserved unchanged and
runs later, by a human, only on the ≤K survivors on the Shortlist.

**Why this is faithful to the source.** The Founder's Playbook asks the founder to "argue against
your idea and find disconfirming evidence that refutes your hypothesis" — it never asks anyone to
*win a debate*. An evidence-screen is the Playbook's actual instruction; a simulated debate would be
a drift away from it.

## Considered Options

- **Agent defends, flagged low-trust** — keep the full debate, agent plays the founder, verdict
  marked provisional. Rejected: the agent is still partly grading itself; the verdict carries little
  signal and every pass needs human review anyway.
- **Cut pressure-test from the funnel** — only sharpen + market-research + review-synthesis run
  automatically. Rejected: loses cheap adversarial filtering exactly where it is cheapest.

## Consequences

- The funnel will produce **false kills** (ideas a real founder could have rebutted). Accepted
  because a false kill is far cheaper than a false pass, which would burn a scarce human
  customer-discovery slot. Mitigated by the **Funnel ledger**: every killed Candidate keeps its
  kill-reason and can be **appealed/resurrected** by the founder.
- Pressure-test and market-research couple into a single **disconfirmation pass** in batch mode
  (personas generate objections; research gathers the adjudicating evidence).
