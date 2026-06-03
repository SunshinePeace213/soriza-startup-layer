# Thinking-Framework Extraction Methodology

> From raw information to a runnable mental model — the core methodology.

This document is the depth reference for Phase 2 of Nuwa. Read it whenever you need to decide whether a candidate idea is a real mental model, how to quantify expression DNA, how to handle contradictions in the evidence, and how to self-check the final skill.

## 1. Triple Verification for Mental Models

For a candidate idea to count as a **mental model** and not just "something this person once said", it must pass all three checks below.

### Check 1: Cross-Domain Recurrence

The same thinking pattern shows up in at least two distinct domains the person discusses.

*Example — Naval's concept of "leverage":*
- In **wealth creation**: code, media, capital, labor are forms of leverage
- In **personal growth**: specific knowledge + leverage = compound returns
- In **career choice**: pick work that has leverage
- → recurs across three domains → real mental model

### Check 2: Generative Power

Using this model, you can predict the person's likely stance on a new question they have never publicly addressed.

*Example — if Munger's "invert, always invert" is a real mental model:*
- For "how do I succeed?" → he would start with "how do I guarantee failure?"
- For "how do I invest?" → he would start with "how do I lose every dollar?"
- → generates new inferences → real mental model

### Check 3: Exclusivity

Not every smart person would arrive at this framing. The model reflects this person's distinctive angle on the world.

*Example — "antifragile" is Taleb's frame. Not everyone sees the world in fragility/robustness/antifragility terms.*
- → has differentiation → worth extracting

### Downgrade Rules

- **Passes only 1 of the 3 checks** → demote to "decision heuristic", not a mental model.
- **Passes 0 of the 3 checks** → it's probably a situational remark. Don't include.

---

## 2. Quantifying Expression DNA

### 2.1 Sentence-Structure Fingerprint

Pull 20 random paragraphs from this person's long-form writing or transcribed talks, then measure:

| Dimension | How to measure |
|-----------|----------------|
| Average sentence length | Total words ÷ total sentences |
| Question-sentence ratio | Question sentences ÷ total sentences |
| Analogy density | Number of analogies per 1,000 words |
| First-person frequency | How often "I" appears |
| Certainty register | Frequency of "obviously" / "definitely" vs. "perhaps" / "maybe" |
| Transition frequency | "but" / "however" / "yet" per 1,000 words |

### 2.2 Style Tags

Place the person somewhere along each axis:

```
formal       ←→ conversational
abstract     ←→ concrete
cautious     ←→ assertive
academic     ←→ accessible
long-sentence ←→ short-sentence
setup-first  ←→ conclusion-first
data-driven  ←→ narrative-driven
```

### 2.3 Forbidden Words and Verbal Tics

- **Words this person never uses** → the generated skill should not use them either.
- **Words/phrases this person uses constantly** (verbal tics) → use sparingly. Overuse turns the skill into caricature.

---

## 3. Handling Contradictions

Contradictions are core features of a personality, not bugs to be fixed.

### Three Kinds of Contradiction

1. **Temporal contradiction** (views evolved)
   - The person said A early in their career, B later.
   - **How to handle**: log the evolution and label "early view" vs. "recent view". In the skill, default to the recent view but mention the evolution.

2. **Domain contradiction** (different rules for different arenas)
   - The person advocates X at work and Y in personal life.
   - **How to handle**: record both, scoped to their domain. Do not force them into a single rule. This separation is often a source of depth.

3. **Essential tension** (genuine internal conflict in values)
   - Example: simultaneously prizes freedom and discipline.
   - **How to handle**: record explicitly as a "core tension". This is usually the most interesting part of the person.

### What Not to Do

- ❌ Pick one side, ignore the other.
- ❌ Invent a tidy explanation that smooths the contradiction away.
- ❌ Pretend the contradiction doesn't exist.

---

## 4. When Information Is Insufficient

| Situation | How to handle |
|-----------|---------------|
| One dimension has very little public material | Mark "insufficient information; this dimension is inferred" in the skill |
| Only secondhand reporting is available | Lower confidence; tag as "per [source's] reporting" |
| Sources contradict and you cannot judge which is right | Present both side by side, let the user decide |
| The person deliberately stays silent on a topic | Respect that. Note in the skill: "the subject does not publicly address this topic" |

---

## 5. Person Skill vs. Topic Skill

| Dimension | Person skill | Topic skill |
|-----------|--------------|-------------|
| Center of gravity | One person's way of thinking | One field's toolbox of thinking |
| Source of mental models | Mainly one person | Synthesized across many |
| Expression style | Mimic that person's voice | Neutral but expert |
| How to handle contradiction | Preserve the person's internal tensions | Show the disagreements between schools |
| How to validate | Compare to the person's known stances | Compare to consensus and accepted divergence in the field |

---

## 6. Quality Self-Check List

After generating the skill, walk through this checklist. Any item that fails sends you back to the relevant phase.

### Mental Models

- Does each model have evidence from at least 2 different domains?
- Is the model count between 3 and 7? (Fewer → too shallow. More → not actually distilled.)
- Does each model have an explicit application context and an explicit limit?
- Are the models in some tension with one another without being outright contradictory?

### Expression DNA

- Does it read with a recognizable voice, not generic AI?
- Is it short of caricature? (Verbal tics used in moderation.)
- Does it capture the core characteristic and not just surface imitation?

### Decision Heuristics

- Does every rule have a concrete case behind it?
- Can the rule be triggered by new situations, not just the original case it came from?

### Honest Limits

- Is what the skill cannot do stated clearly?
- Are the source list and research date documented?
- Are dimensions with insufficient information called out?

### Overall

- If you look at a new problem through this skill's eyes, do you get a perspective that has value?
- Is the output more than a pastiche of original quotes — is it the framework actually running?
- If you stripped the person's name out, would a reader still recognize whose thinking this is?
