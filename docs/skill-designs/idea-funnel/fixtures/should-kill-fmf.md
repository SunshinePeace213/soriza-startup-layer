# Fixture — should KILL at Gate 0 (Founder-Market-Fit)

Expected: hard-fail at Gate 0. The idea may be perfectly good in the abstract, but it does not fit THIS
founder (part-time, solo, low risk/regulatory appetite, low capital, HK/APAC + global-English). If it
survives Gate 0, the FMF hard-fails aren't firing.

```json
{
  "id": "cand-neobank-for-smes",
  "title": "Licensed neobank for Hong Kong SMEs",
  "problem": "HK SMEs get poor service and slow onboarding from incumbent banks for multi-currency accounts and lending.",
  "who": "Finance managers at HK SMEs with cross-border suppliers",
  "why_now": "Virtual-bank licences exist in HK and SMEs are underserved",
  "idea_type": "regulated-adjacent"
}
```

Checks:
- **Gate 0 (FMF):** **kill** — hard fails on *risk & regulatory* (requires a banking/virtual-bank
  licence) and *capital* (deposits, compliance, capital reserves), and likely *capacity* (cannot be run
  part-time solo). `hard_fail` should name the licence requirement. Should never reach Gate 1.
