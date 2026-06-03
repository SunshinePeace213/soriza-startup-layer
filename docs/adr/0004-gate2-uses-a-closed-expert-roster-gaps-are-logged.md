# Gate 2 uses a closed expert roster at runtime; coverage gaps are logged, not auto-filled

**Status:** accepted

Gate 2's lens-selector picks 3–4 lenses from the distilled `*-perspective` roster. When the ideal
lens for a Candidate's domain hasn't been distilled, the funnel must do *something* — auto-mint it,
block, or proceed with what it has.

**Decision.** The funnel uses a **closed roster** at runtime. It picks the best available lenses AND
records the **ideal-but-missing** expert as a coverage-gap note in the ledger — never a silent miss.
It does **not** auto-mint experts mid-run. Minting a new lens (via `nuwa-skill`) + adding its
lens-card to `expert-lens-map.md` is a deliberate, human-gated **curation step between runs**, not
part of a run.

**Rationale.** Disconfirmation needs *diverse failure lenses*, not a perfect domain specialist. The
generalist roster (Thiel/Munger/Taleb/Bezos/Eisenmann/…) already covers most failure modes, so a
missing specialist sharpens an edge case rather than blocking a kill decision. Over time the roster
**grows to fit the founder's idea-space**, driven by the gaps runs actually hit.

## Considered Options

- **Auto-mint mid-funnel via nuwa.** Rejected: nuwa is heavy and interactive (the funnel can't pause —
  [ADR-0002](0002-validator-runtime-is-a-dynamic-workflow.md)), a workflow orchestrates subagents not
  skills, and a freshly auto-distilled lens is unverified — killing real ideas on an untrusted lens.
- **Block the Candidate on a gap.** Rejected: a missing specialist is a nice-to-have, not a blocker.
- **Proceed silently with best-effort lenses.** Rejected: violates no-silent-caps — the gap must be
  logged so the founder can curate.

## Consequences

- The ledger carries a **coverage-gap** field (the per-Candidate "ideal-but-missing" note).
- The founder periodically curates the roster from those notes; `nuwa-skill` is a curation tool, never
  a funnel-runtime dependency.
- v1 ships with the existing ~11 generalist `*-perspective` lenses.
