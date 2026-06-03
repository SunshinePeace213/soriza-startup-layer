# Gate rubrics — the tunable kill thresholds

The bars each gate kills against. These are the knobs you tune in the eval loop (Phase 7). Every gate
scores 0–100 and kills below its **bar**; the bar is deliberately conservative early (kill cheaply,
keep the survivor pool honest) and the **cap** (not a bar) trims the final survivors to K.

Principle (ADR-0001): a gate kills on a **checkable** criterion — a rubric or external evidence —
never on a debate the agent stages with itself. When uncertain, a desk gate should prefer to **advance**
(a false kill is cheaper than a false pass — but only at the cheap gates; Gate 2 is allowed to be harsh
because it has evidence in hand).

---

## Gate 0 — Founder-Market-Fit  (bar: score ≥ 55)

Reads `docs/founder-profile.md`. Score = how well the idea fits THIS founder. Kill below 55, OR on any
single **hard fail** regardless of score.

| Dimension | Hard fail (instant kill) | Soft signal (lowers score) |
|---|---|---|
| Geography / market | Requires a market the founder cannot credibly serve | Weak language/cultural fit |
| Risk & regulatory | Needs a licence / regulated activity / heavy compliance | Adjacent to regulation |
| Capital | Needs significant up-front capital / inventory / hardware | Modest but non-trivial spend |
| Capacity | Cannot be moved at all part-time / needs a full team day-one | Demanding for part-time |
| Skill / unfair advantage | Outside the founder's buildable surface, no agentic-coding edge | Stretch but learnable |

Output: `{ verdict, score, reason, hard_fail | null, fit_flags }`.

## Gate 1 — Testability  (bar: score ≥ 50)

Runs the sharpen rubric. A seed advances only if it can be made into a testable hypothesis naming all
four dimensions **specifically** after one sharpening pass.

| Dimension | Specific (pass) | Vague (fail) |
|---|---|---|
| WHO | named role + context + segment | "businesses", "people" |
| HOW OFTEN | a frequency | "sometimes" |
| HOW SEVERE | a cost/pain magnitude | "it's annoying" |
| STATUS QUO | what they do now | "nothing" / unknown |

Kill if any dimension stays vague after one pass, or the resulting hypothesis is unfalsifiable. On
advance, write `hypothesis.md` (sharpened sentence + the four dimensions) for the candidate.
Output: `{ verdict, score, reason, testable, hypothesis }`.

## Gate 2 — Disconfirmation pass  (bar: score ≥ 50)  ← the expensive evidence tier

One research sweep produces both (a) evidence adjudicating the experts' objections and (b) the market
read. Kill if EITHER:
- the **strongest objection stands unrebutted by evidence** (no public evidence answers it), OR
- the **market read fails**: SOM too small to matter, market closed/consolidated with no wedge, or a
  decisive timing **headwind**.

Score blends objection-survival and market strength. Always record `strongest_unrebutted` and (per
ADR-0004) any `coverage_gap` (an ideal-but-missing lens). Harsh-by-design: this gate has evidence in
hand, so it may kill confidently.
Output: `{ verdict, score, reason, strongest_unrebutted, objection_ledger, market, coverage_gap }`.

## Gate 3 — Customer-discovery DESIGN  (soft gate: reachability only)

Not a quality kill — the idea already survived the desk funnel. Soft-kill ONLY if there is **no
reachable audience** to interview (no identifiable community/channel where the target congregates).
Otherwise produce the sealed run-pack.
Output: `{ verdict, reachable, runpack_path, reason }`.

---

## Tuning notes

- Start with the bars above; in Phase 7, run the fixtures and move a bar only if a known should-advance
  is killed or a known should-kill survives.
- The bars are absolute (bar-to-kill); the **cap K** is separate (cap-to-advance) and is set from the
  founder profile, not here.
- Log every cut with its one-line reason — no silent kills.
