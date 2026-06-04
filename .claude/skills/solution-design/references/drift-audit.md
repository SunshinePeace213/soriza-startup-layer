# Drift Audit — reconstructing the validated baseline and measuring drift

The drift audit is the spine of `/solution-design`. It answers the Playbook's reality checkpoint: *does
the design address the problem the validation revealed, not the problem you assumed going in?* This
founder's documented failure mode — *"concede the diagnosis, keep the prescription"* — IS drift, so this
audit is the load-bearing anti-self-deception device. Read this in Step 3 (baseline) and Step 5 (audit).

## Why you can't just read `hypothesis.md`

`hypothesis.md` is the **assumed** problem — what the founder believed before any validation. Every
downstream stage then emitted corrections in a *"Hypothesis Updates Flagged"* block, but **only
`/idea-funnel` is allowed to fold those back into `hypothesis.md`.** Mid-pipeline the founder
usually hasn't re-run it, so `hypothesis.md` is **stale**. Measuring the concept against the stale file
would let real, evidence-based corrections silently disappear — which is exactly the drift you're hunting.

So the audit has two inputs:
- **The assumed problem** = `hypothesis.md` as written (the "before").
- **The validated baseline** = assumed problem **+ every accumulated delta applied** (the "after").

## Step 1 — Assemble the delta ledger (script)

`scripts/build_delta_ledger.py` scans `disconfirmation-brief.md`, `market-research.md`, and
`customer-discovery.md` for every *"Hypothesis Updates Flagged"* block + the Discovery Read verdict + the
TRIPPED criteria + any override, and prints them **verbatim**. Run it and write the output to
`solution-design/delta-ledger.md`. Trust the `warnings` field — when a doc's header deviated from the
convention, the script lists that doc's `##` sections so you can find the delta by hand rather than
assuming there was none. It also reports `unsettled_criteria` — any latest-round criterion whose Status
is neither TRIPPED nor CLEARED (INCONCLUSIVE / MANUAL / ERROR). Treat a non-empty `unsettled_criteria`
as a flag that the concept may be getting designed on still-unsettled evidence; name those criteria in
the drift audit rather than designing past them.

## Step 2 — Reconstruct the validated baseline

Take the four hypothesis dimensions (plus an optional Why-now/wedge row) and apply each delta. Write `solution-design/validated-baseline.md`:

```markdown
# Validated baseline — <slug>
*(Assumed problem from hypothesis.md + accumulated deltas applied. This — not hypothesis.md — is what the
drift audit measures the concept against.)*

| Dimension | Originally assumed | Delta(s) applied (source) | Validated version |
|---|---|---|---|
| Who has it | <hypothesis> | <e.g. "narrow to staff+ engineers" — customer-discovery.md> | <after> |
| How often | ... | ... | ... |
| How severe | ... | ... | ... |
| What they do now | ... | ... | ... |
| Why-now / wedge | ... | <e.g. "native assistant suffices for majority" — customer-discovery.md TRIPPED> | <after> |
```

A TRIPPED kill criterion is a delta too: it tells you a part of the assumed problem failed validation.
Fold its implication into the relevant dimension.

## Step 3 — Build the assumed→validated table

For each validated dimension, ask: **does the crystallized concept serve the validated version, or is it
still built for the assumed one?** Mark each row:
- **✅ serves it** — the concept's wedge/who/job matches the validated dimension.
- **⚠️ drifting** — partially serves it; the concept leans on an assumed element the evidence weakened.
- **❌ still solving the old problem** — the concept serves the assumed dimension that validation overturned.

## What counts as drift (the patterns to catch)

- **Persona drift** — concept targets the wide hypothesis net when discovery narrowed the validated who to a slice (e.g. designing for "all PMs" when only staff+ engineers showed the pain/WTP).
- **Job drift** — concept owns the job the founder assumed mattered, when discovery showed a *different* job is the real one (e.g. "abandon the channel" vs the validated "filter it better").
- **Why-now drift** — concept's premise relies on a gap discovery showed is already closing (e.g. "the assistant doesn't do this yet" when a majority said native suffices).
- **Severity drift** — concept is priced/scoped for a severe daily pain that validation never confirmed (the "60–120 min/day" claim that wasn't in the behaviour).
- **Prescription-keeping** — the most dangerous: the founder concedes a diagnosis delta in words ("yes, native is good enough for most") but the concept is unchanged ("…but I'll build the digest anyway"). Flag the contradiction explicitly; it is the failure mode this stage exists to stop.

The blind `solution-red-team` produces its own drift findings independently (Step 5). Reconcile: any drift
it caught that your audit missed goes into the card's Challenge section as a reconciliation gap.
