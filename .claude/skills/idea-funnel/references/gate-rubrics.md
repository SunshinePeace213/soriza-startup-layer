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

Reads `docs/founder-profile.md` (the summary; read `docs/founder-dossier.md` for depth if a factor is
ambiguous). Score = how well the idea fits THIS founder. The rubric below is the **general standard**;
the founder's specifics are **data read from the profile**, never hard-coded here — so the same rubric
scores any founder fairly (a different founder's regulatory appetite, capital, capacity, and skills
yield a different verdict on the same idea). Each factor compares the idea's *requirement* to the
founder's *stated value* from the named profile section. Kill below 55, OR on any single **hard fail**
regardless of score.

| Dimension | Reads from profile | Hard fail (instant kill) | Soft signal (lowers score) |
|---|---|---|---|
| Geography / market | Location & serviceable geography | Requires a market/language the profile says the founder cannot credibly serve | Weak language/cultural fit for the target |
| Risk & regulatory | Risk & regulatory appetite | Requires regulated activity / a licence / heavy compliance beyond the founder's stated appetite | Adjacent to regulation, within stated tolerance |
| Capital | Capital & runway | Needs up-front capital / inventory / hardware beyond the founder's stated capital & runway | Modest spend, non-trivial against the stated runway |
| Capacity | Time commitment | Needs more sustained time, or a larger day-one team, than the founder's stated commitment allows | Demanding for the founder's stated capacity |
| Skill / unfair advantage | Skills & unfair advantage | Outside the founder's stated buildable surface — no relevant skill and no declared unfair advantage | Stretch beyond current level but learnable |

A missing or declined value (e.g. runway not shared) is scored **conservatively** — treat the
constraint as tight, not absent, so a blank never flatters. Output:
`{ verdict, score, reason, hard_fail | null, fit_flags }`.

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
