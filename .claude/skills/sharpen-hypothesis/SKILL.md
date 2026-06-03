---
name: sharpen-hypothesis
description: First step in the Idea Stage of Soriza Startup Layer — the entry point for any new startup idea. Interviews the founder about a vague problem and sharpens it into a testable hypothesis along four dimensions (who has it, how often, how severely, what they do now), or refuses the idea when it fails hard criteria. Produces a structured hypothesis.md that the /pressure-test skill consumes next.
when_to_use: |
  Use when the user says "sharpen my hypothesis", "sharpen this idea", "is this testable",
  "I have a startup idea", "validate this problem", "problem hypothesis", "testable hypothesis",
  "who has this problem", "start a new idea", "begin Idea Stage", "new startup idea",
  "first step of Idea Stage", or pastes a vague problem statement and asks what to do next.
  Also trigger on phrasings like "sharpen until testable" or "problem hypothesis stage".
  Do NOT use to turn open-ended research/trends into ideas (that is /generate-ideas), to stress-test
  an existing hypothesis (that is /pressure-test), or for a bare "what's next" once a hypothesis.md
  already exists in the idea's docs/ideas-stages folder (that hands off to /pressure-test).
allowed-tools: AskUserQuestion, Read, Write, Bash
---

# Sharpen Hypothesis

First step in the **Idea Stage** of the Soriza Startup Layer — the entry door any new startup idea passes through. Take a vague problem statement and produce one testable hypothesis (plus four supporting dimensions), or refuse the idea if it fails hard criteria. Output goes to `docs/ideas-stages/<slug>/hypothesis.md` for the next skill (`/pressure-test`) to consume.

## When this skill applies

- "I have a startup idea — help me sharpen it"
- "Sharpen my hypothesis" / "is this testable yet?"
- "Start a new idea" / "begin Idea Stage" / "first step of Idea Stage"
- "Validate this problem" / "who has this problem"
- User pastes a vague problem statement and asks what's next

## Gotchas

- **Judge the `notes`/Other text, never the option label.** A founder can click a valid-looking button (e.g. "Industry + company size + role") and leave `notes` empty — that is a non-answer and a rejection trigger, not a pass. Every advance/reject decision reads the free text, not the choice.
- **Round 0 is the pasted idea, not a question.** The founder's initial idea is round 0; the first `AskUserQuestion` follow-up is round 1. The two-round rejection clock counts question cycles only — don't burn a round on the idea they already handed you.
- **`AskUserQuestion` forces 2–4 options even when the question is open-ended.** That is why bare invocation uses the "Where are you starting from?" shape framing — you cannot ask a raw free-text question through the tool. The real answer always arrives via `notes` or the auto-provided "Other", so the option labels are scaffolding, not the data.

## Interaction model

**All grilling goes through `AskUserQuestion`.** Plain-chat free-text input is embedded inside `AskUserQuestion` via the auto-provided "Other" option and the `notes` field on every choice — the founder can always type a custom answer, just routed through the tool. Do not ask free-text questions in plain chat during grilling; every round is an `AskUserQuestion` call.

For each dimension, work in two beats inside a single assistant message:

1. **Ideas-first context** — 1–3 sentences surfacing possibilities from what the founder pasted, without naming the answer for them. Scaffolds the founder's thinking and shows what good answers look like.
2. **`AskUserQuestion`** — the founder commits by picking an option (and elaborating in `notes`) or picking the auto-provided "Other" and typing their full answer. In the question prompt, explicitly invite the founder to add specifics in the notes field.

The founder still owns the facts; Claude provides shape templates and perspective. The skill uses a generic founder-coaching lens at this stage — distilled-persona advisors (Thiel, Bezos, Eisenmann, etc.) live exclusively at `/pressure-test`, the next pipeline step.

Grilling and option-derivation are reasoning-sensitive — run this skill at high effort or above for sharper ideas-first context paragraphs and refinement rounds.

## Workflow

Produce a ≤300-word `hypothesis.md` the `/pressure-test` skill can consume, or refuse and explain why. Steps are ordered (slug → resume → grill → synthesize → confirm → write); within each step the work is goal-oriented, not scripted.

### 1. Capture the initial idea (if not already provided)

If the founder invoked the skill bare (e.g. `/sharpen-hypothesis` with no pasted idea), fire `AskUserQuestion` to capture a starting point. `AskUserQuestion` requires 2–4 options, so frame it as "Where are you starting from?" with these shape options (the founder types the actual idea in `notes` or Other):

- **A. I have a concrete problem I want to solve** — founder describes the problem in `notes`
- **B. I have a target user / market in mind** — founder names the segment in `notes`
- **C. I have a solution looking for a problem** — founder describes the solution in `notes`
- (auto) **Other** — fully describe a different starting point

The founder's text in `notes`/Other becomes the input the rest of the workflow consumes — the option label only signals which dimension is already strongest.

If the founder already pasted an idea in the same turn as the invocation, skip this step.

### 2. Ask for a project slug

Use `AskUserQuestion`. Propose a slug derived from the founder's idea (e.g. `contract-redline-tool`) as the recommended option, with 2–3 alternates. The chosen slug becomes the folder name `docs/ideas-stages/<slug>/`.

The slug is provisional — no folder is created until Step 8, and it's discarded if any rejection criterion fires in Step 5. Mention this in the question prompt so the founder knows naming isn't a commitment.

### 3. Resume if there's prior work

If `docs/ideas-stages/<slug>/hypothesis.md` already exists, read it. Treat each of the five sections as filled or empty/weak; only grill on the empty or weak ones. This lets the founder iterate without losing prior answers.

**If all five sections are already filled**, skip Step 4 (grilling) entirely and jump to Step 7 (show the draft and confirm). The founder is revisiting a complete hypothesis and just wants to confirm or refine.

### 4. Grill on the four dimensions

Order: **Who → How Often → How Severely → Status Quo**. One dimension at a time. For each dimension:

- Write the ideas-first context paragraph (per the interaction model above).
- Fire `AskUserQuestion` with the options defined for that dimension.
- Read the founder's choice **plus the text in `notes`/Other**. If specific enough, advance to the next dimension. If still vague, fire one refinement round — a narrower `AskUserQuestion` whose options are derived from what they said.
- If still vague after **2 rounds on the same dimension**, trigger rejection (Step 5).

A "round" is one `AskUserQuestion` + answer cycle on the same dimension. The founder's initial pasted idea is round 0; the first follow-up question is round 1.

Push for specificity only — don't second-guess truth claims. The `/pressure-test` skill handles adversarial review of whether claims are accurate. Your job here is to make the claims precise enough to be falsifiable.

**Who**

Options are *shape templates* — they communicate what a good answer looks like. The auto-provided "Other" is the expected primary path for founders who already know their exact segment.

- **A. Industry + company size + role** — example to mention in the description: "in-house counsel at 100–500 person SaaS"
- **B. Consumer demographic + behaviour** — example: "macro-tracking gym-goers, 25–35"
- **C. Geography + occupation** — example: "HVAC contractors in Texas"
- (auto) **Other** — founder types their full segment

"Everyone" / "all small businesses" / "consumers" is **not** a valid answer regardless of which button is clicked. Inspect the text in `notes`/Other, not the option label.

**How Often**

Closed buckets — pick one. Distinguishes painkiller from vitamin.

- **A. Per-event or daily**
- **B. Weekly**
- **C. Monthly**
- **D. Less often (quarterly, annual, one-time)**

Frequency lower than monthly is a vitamin signal — combine with severity check in Step 5.

**How Severely**

Closed ranges. Pick the dominant cost type; founder quantifies in `notes`.

- **A. Time cost — hours per occurrence**
- **B. Time cost — days per occurrence**
- **C. Dollar cost per occurrence** (founder specifies a range in `notes`)
- **D. Risk / consequence cost** (compliance, reputation, lost deals — founder specifies in `notes`)

"A lot" / "really annoying" is not quantified — push for hours, dollars, or a named risk.

**Status Quo**

Workaround shapes. "Other" is the expected primary path when the workaround is hybrid or unusual.

- **A. Manual workaround** — spreadsheets, email threads, paper, ad-hoc Slack
- **B. Existing tool / named competitor** — founder names it in `notes`
- **C. Nothing — they tolerate the pain** — no organized workaround exists today
- (auto) **Other** — founder describes a hybrid or unusual workaround

### 5. Reject and stop if any of these fire

Refuse to write the file. State the reason concretely in chat. No `rejected.md` artifact, no override option.

- **No identifiable user** after two `AskUserQuestion` rounds on Who — founder's `notes`/Other text stayed at "everyone", "all small businesses", "any company", or never committed to a single segment
- **Vitamin not painkiller** — frequency bucket is "Less often than monthly" AND severity remains unquantified or framed as "mild annoyance" in `notes`
- **Founder dodges specificity** after two rounds on any dimension — picks Other but types nothing concrete, or picks A/B/C/D without supplying the requested elaboration in `notes`
- **Illegal, unethical, or clearly harmful** — surveillance of minors, fraud enablement, etc.

Example rejection message: *"Rejected: Who stayed at 'all small businesses' after two rounds. Come back with a single segment you can name (industry + size + role) and I'll sharpen from there."*

### 6. Synthesize the testable hypothesis

Once all four dimensions are sharp, compose one testable sentence in this shape: **segment + frequency + severity + cause-attribution-to-status-quo**. The founder owns the facts; you own the shape.

**Internal shape reference — model the testable sentence on this contrast. Do not show this contrast to the founder:**

> *Vague:* "Contract review takes too long."
>
> *Testable:* "In-house legal teams at mid-market companies spend 3+ days per contract review cycle because redlines are managed across email threads rather than a single version-controlled document."

The Testable form names the segment, quantifies the cost in concrete units, and attributes the cost to a specific status-quo mechanism. Mimic this shape when composing.

### 7. Show the draft and confirm

Print the full draft in chat using exactly this 5-section structure:

```markdown
# Hypothesis: <idea-name>

## Hypothesis
<one testable sentence>

## Who
<exact segment>

## How Often
<frequency>

## How Severely
<quantified cost in time / $ / risk>

## Status Quo
<current workaround / competing solution>
```

Then `AskUserQuestion` with three options: Ship it / Refine more / Abort.

- **Ship it** → proceed to step 8.
- **Refine more** → ask which section via a follow-up `AskUserQuestion`, then return to grilling on that section only.
- **Abort** → no file written, exit cleanly.

### 8. Write the file (only after Ship)

- `mkdir -p docs/ideas-stages/<slug>/` via Bash
- Write `docs/ideas-stages/<slug>/hypothesis.md` with the confirmed content
- In chat (not in the file): `Next: run /pressure-test to stress-test this hypothesis.`

## Output constraints

- Path: `docs/ideas-stages/<slug>/hypothesis.md` — exact, no variations. `<slug>` is the folder chosen in Step 2; the `# Hypothesis: <idea-name>` title is a human-readable name, not the folder name.
- Word count: ≤300 words for the entire file
- Format: five `##` sections in the order Hypothesis / Who / How Often / How Severely / Status Quo, under a `# Hypothesis: <idea-name>` title
- No YAML frontmatter, no "next step" line inside the file, no version metadata, no prose outside the five sections

## Scope

- In: sharpening one problem hypothesis to testable shape, refusing unsalvageable ideas, writing the handoff file
- Out: market sizing, competitor landscape, solution design, business model — those belong to later pipeline steps
- Out: pushing back on whether the founder's claims are accurate — that's `/pressure-test`'s job
- Out: adversarial persona review — this skill uses a generic founder-coaching lens; full distilled-persona stress-testing happens at `/pressure-test`
