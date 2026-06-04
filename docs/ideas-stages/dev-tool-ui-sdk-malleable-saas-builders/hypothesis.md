# Hypothesis: SDK for Per-User Malleable Interfaces

**Status:** Provisional, to-be-tested (Gate 1)

---

## Sharpened Hypothesis Sentence

Indie SaaS developers building vertical products on Next.js/React will adopt an SDK that drops into existing apps and lets end-users describe their preferred interface (returning persisted layout configs) if it reduces per-feature rebuild time from ~3 months to less than 1 week.

---

## Four Dimensions (Provisional)

### WHO
Indie SaaS developers and small engineering teams (1–5 engineers) building vertical SaaS products on Next.js/React stacks who need to ship user-customizable interface features.

### HOW OFTEN
When designing a new user-customizable interface feature — typically once per quarter or as part of a new product initiative.

### HOW SEVERE
Faces a ~3-month engineering rebuild (full frontend refactor) to safely expose user-driven layout changes, often deferring the personalization feature entirely rather than paying the rebuild cost. Measured in engineering person-weeks (≈ 1 FTE × 12 weeks for a 5-person team) and delayed revenue from deferred features.

### STATUS QUO
Today they either:
- Ship hard-coded layouts with no user customization;
- Build bespoke, unsafe UI mutation logic on top of raw LLM outputs (reinventing sandboxing + persistence each time);
- Defer personalization features indefinitely to avoid the rebuild cost.

---

## Falsifiability

This hypothesis is testable via:
1. **Adoption:** Do indie SaaS devs install and use the SDK in their existing Next.js/React apps?
2. **Time-to-ship:** Does adoption actually reduce per-feature rebuild from ~3 months to < 1 week?
3. **Feature velocity:** Do teams ship more customization features after adopting the SDK?
4. **Willingness-to-pay:** Do they pay for the SDK (or use it if free), and would they renew/upgrade?

Can be disproven by evidence that:
- The SDK doesn't integrate cleanly with existing Next.js/React apps.
- It doesn't materially reduce rebuild time below the 3-month baseline.
- Indie SaaS devs don't prioritize per-user customization (market doesn't want it).
- The SDK doesn't persist user configs reliably or safely.

---

**Next steps:** Customer discovery interview with indie SaaS developers to validate the pain (Gate 2 disconfirmation pass).
