# Market Research: student-notes-to-study-interface

> **Desk research synthesizing public evidence — competitor sites, reviews, market data,
> trend signals — not customer validation.** A favorable read means the public evidence is
> favorable; it is not proof anyone will pay. Take the wedge and disconfirmation targets into
> customer discovery. Re-run when the hypothesis evolves.
>
> This single doc carries all four workstreams (W1 landscape, W2 review-synthesis, W3 sizing +
> buyer map, W4 trends) plus a top-line Market Read, because the sweep was dispatched as one
> instance. Each workstream below follows its brief's output shape.

---

## Market Read

**reconsider (or hard reposition)** — The core mechanism of the hypothesis ("one app ingests your
notes and renders the same underlying data in multiple student-selectable study interfaces, no
manual reformatting") is *already shipped at scale* by RemNote (1M+ students, free tier, AI
flashcard + spaced-repetition + notes in one tool) and is being commoditized weekly by a dense
field of AI study apps (StudyFetch, Knowt, Mindgrasp, Quizlet, NotebookLM, Notion AI). The
"2–4 hours/week reformatting" pain is real and well-documented, but the gap incumbents have *not*
closed is **trust/accuracy of AI-generated study material** and **format-portability between the
notes app a student already lives in (Notion/Obsidian) and their drill tool** — not "render in
multiple interfaces," which is table stakes. There is a defensible wedge here, but it is narrower
and different from the hypothesis as written, and the build is a crowded consumer-subscription
fight that is GTM-heavy — the founder's stated weakest axis.

---

# W1 — Competitive Landscape

## Direct
| Player | What they do | Who they serve | Pricing | Where they fall short for this segment |
|---|---|---|---|---|
| **RemNote** | Notes + AI-generated flashcards + spaced repetition (FSRS-class) + PDF annotation in ONE tool — explicitly "no switching between Notion, Anki, Quizlet." 1M+ students. [1][8] | Students, esp. med/MCAT/language-exam prep | Free tier (robust); Pro ~$8/mo [3][8] | This IS the hypothesis. Gap = you must adopt RemNote as your home; it does not render *your existing Notion/Obsidian* in multiple interfaces — it wants to be your notes app. |
| **StudyFetch** | Uploads PPT/lecture/notes → flashcards, quizzes, tests, AI tutor ("Spark.e") [9] | College students | ~$4.99–7.99/mo annual; $19/mo monthly [3] | AI accuracy ("minor inaccuracies appear, spot-check"); not anchored to your durable note system; one-way ingest, not a living sync. |
| **Mindgrasp** | Ingest content → notes, summary, flashcards, quizzes, AI tutor [1] | Students + professionals | ~$5.99–14.99/mo; ~$131.88/yr [3] | Same one-shot-generation pattern; quality + accuracy complaints; not a notes-system replacement or sync. |
| **Knowt** | One-click notes → flashcards; lecture-video summaries; positioned as free Quizlet alternative, AI quizzes [1] | High-school + college | Free tier generous; premium exists | "Hallucinates and has no spaced-repetition system… happily generates confidently wrong flashcards" [W2-2]. |
| **Quizlet** | Flashcards, Learn/Test modes, AI "Q-Chat" / Magic Notes | 60M+ MAU, ~50% of US high-schoolers [W3-quizlet] | Quizlet Plus ~$35.99/yr; Learn/Test paywalled since Aug-2022 [W2-1b] | Paywall resentment; requires re-entry of content; not your note home. |
| **NotesXP / Scholarly / Laxu / Turbo AI / Revisely** | Long tail of 2025–26 "upload → flashcards/quiz/mind-map/podcast" apps [1][7] | Students | Mostly freemium $5–15/mo | Undifferentiated; thin moats; same accuracy and "not your durable notes" gaps. |

## Indirect
| Player | Approach to the same job | Why a customer settles for it | Where it fails |
|---|---|---|---|
| **Notion + Notion AI** | Home for notes; AI summarizes/rewrites; SM-2 flashcard *templates* exist; "AI Study Guide" template [W1-notion] | They already live in Notion; one less app | "Does NOT include true flashcard or quiz modes" natively — templates are clunky; no real drill UX. This is the *source* the hypothesis ingests from. |
| **Obsidian + Spaced Repetition / Flashcard plugins** | Local notes → community plugins turn notes into decks; 2,700+ plugins [W1-notion] | Power users own their data, want local + free | Plugin assembly is DIY/technical; fragmented; no clean multi-interface render out of the box. |
| **Notion→Anki bridges (2anki.net, Notion2Anki, Notes2Flash)** | One-way/sync export of Notion (and limited Obsidian) into Anki cards [6] | Cheapest path keeping Anki's FSRS | "If you change something in Notion, Anki cards don't update… many give up after a few weeks" [W2-3]. Setup friction; brittle. |
| **Anki (manual)** | Gold-standard SRS; 86% of US med students, 66% daily [W3] | Best retention algorithm, free, trusted | "Making good cards by hand is slow, tedious work"; "interface dated, learning curve steep" [W2-1]. THIS manual labor is the pain the hypothesis targets. |
| **NotebookLM (Google)** | Upload sources → grounded summaries, Q&A, audio overview, recently study guides/flashcards | Free, Google-trusted, source-grounded (low hallucination) | "Lacks a flashcard or spaced-repetition layer"; source caps on free tier [W2-1]. Closing fast. |
| **ChatGPT (manual prompting)** | "Make 30 flashcards from these notes" → paste into Anki | Already paying for it; flexible | Re-entry friction; "happily generates confidently wrong flashcards" [W2-1]; no persistence/SRS. |

## Potential acquirers
- **Quizlet / Chegg / Course Hero (Learneo)** — distressed-but-distribution-rich incumbents that would buy a slick AI ingest-and-drill layer to defend declining engagement; implies an exit is *possible* but the founder's bootstrap posture (no raise, wants to own Soriza) makes acquisition-as-strategy a poor fit.
- **Notion / Obsidian** — would buy a study layer to deepen student stickiness; Notion is already shipping agentic workflows (2025). For a solo bootstrapper this is "build a feature a platform can absorb," not a moat.
- **Duolingo** — cash-rich, consumer-learning, acquisitive (bought Hobbes 2024); could bolt on exam-prep drill. Again, validates the space more than it helps a bootstrapper.

## Adjacent (could move in)
- **Notion** — already has notes + AI + templates + agentic workflows; adding native flashcard/quiz *modes* is a quarter of roadmap, not a moonshot. Fastest, most dangerous mover — it owns the data the hypothesis depends on.
- **Google (NotebookLM)** — source-grounded (its hallucination story is *better* than the field), free, and explicitly adding study-guide/flashcard surfaces in 2025–26. Could erase the wedge for English-market students at zero price.
- **Anthropic / OpenAI (Claude/ChatGPT) "Study" modes** — both shipping education-tuned modes; "render my notes as flashcards/quiz/concept map" is one feature away and bundled into a subscription the student already pays.

---

# W2 — Review Synthesis

## Top unresolved complaints (ranked)
1. **AI-generated study material is "confidently wrong" / hallucinates, and errors are subtle, not obvious** — high intensity; the #1 dealbreaker for high-stakes exam-prep (med, licensing) where a wrong card costs marks. Sources: Scholarly Reddit roundup of r/medicalschool + r/GetStudying [W2-1]; NCBI/medical-education literature on ChatGPT hallucination in flashcards [W2-3]; practitioner Substack "When AI Flashcards Pollute Your Anki Deck" [W2-3]. — **verified (≥3 independent)**.
2. **Notes and flashcards live in separate apps that don't sync; changing the note doesn't update the card** — high frequency; "many give up on the Notion+Anki combo after a few weeks." Sources: FlashRecall blog + Anki forum threads [W2-3]; "none of them talk to each other… notes don't connect to subjects" app-overload pieces [W2-4]. — **verified (≥2 independent)**.
3. **Manual flashcard creation / reformatting is "slow, tedious work"** (the hypothesis's core pain) — high frequency. Sources: r/GetStudying via Scholarly [W2-1]; Medium "converting Notion notes to Anki" + voovostudy AI-vs-manual [W2-conv]. — **verified (≥2 independent)**.
4. **App fragmentation / tool-switching tax** — average student tries 8–12 study apps before settling; each switch costs 15–25 min of refocus. Sources: imago.us "App Overload" [W2-4]; Medium student-productivity pieces [W2-4]; LuminPDF "Too many apps" [W2-4]. — **verified (≥2 independent), but the 8–12 / 15–25-min figures are blog-sourced, not peer-reviewed — treat as directional.**
5. **Paywall resentment** — Quizlet locked Learn/Test behind ~$35.99/yr Plus (Aug-2022); students "resent it." Sources: two independent student-press op-eds [W2-1b]; Scholarly roundup [W2-1]. — **verified (≥2 independent)**.
6. **No spaced-repetition layer in newer AI tools / SRS distrust** — Knowt and NotebookLM called out for lacking SRS; power users skeptical of non-FSRS schedulers. Source: Scholarly Reddit roundup [W2-1] (single roundup citing multiple subs). — **single-source roundup — corroborated indirectly by RemNote/Anki positioning, but flag as not independently re-verified.**

## Does this idea address them?
- **#1 Hallucination/accuracy** — **Partially / Not.** Re-rendering *existing* notes is *safer* than generating from scratch (the student's own notes are the source) — a genuine advantage IF the product transforms rather than invents. But the moment it "creates flashcards/concept maps," it inherits the same accuracy risk. Not addressed unless trust/traceability is a first-class feature.
- **#2 Sync / single-source-of-truth** — **Addressed (strongest fit).** "One app, same underlying data rendered many ways" directly kills the no-sync problem — IF it owns the data. But that's exactly RemNote's pitch.
- **#3 Manual reformatting** — **Addressed.** This is the headline promise and a real pain.
- **#4 Fragmentation** — **Partially.** Only if it *ingests existing Notion/Obsidian* rather than asking the student to migrate — otherwise it adds a 9th app.
- **#5 Paywall** — **Not inherently** — a paid subscription competing with a free RemNote tier and free NotebookLM inherits this resentment.
- **#6 SRS** — **Partially** — only if it ships a credible (ideally FSRS-class) scheduler, not just static renders.

## Problem–Solution-Fit signal
**weak.** The pains are real and well-documented, but the hypothesis's headline mechanism (multi-interface render of one data source) is the *least* unresolved of them — RemNote ships it, Notion/Anki bridges attempt it, and NotebookLM is converging on it. The genuinely *unresolved* pains (trustworthy/traceable AI cards; living sync from the notes app the student already uses) are addressable only if the hypothesis is repositioned around **"ingest your *existing* Notion/Obsidian and keep it living-synced, with source-traceable transforms"** rather than "be a new multi-mode study app."

---

# W3 — Market Sizing + Buyer Map

## TAM / SAM / SOM
| Layer | Range | Key assumptions (tagged with source) |
|---|---|---|
| **TAM** | **~$7–9B (2025–26), → $30–41B by 2030** | "AI in education" market: $6.9–7.05B (2025), $9.58B (2026), CAGR 31–43% to 2030 [W3-1, W3-2]. This is the whole AI-in-ed category; the notes→study-tool slice is a fraction. |
| **SAM** | **~$200–600M/yr** | Self-directed exam-prep students who store notes digitally (Notion/Obsidian/Drive/Apple Notes) in English + Greater China markets, willing to pay $5–15/mo for AI study tools. Anchored to: 269M global higher-ed students [W3-3]; ~50% of US high-schoolers on Quizlet [W3-quizlet]; Gen Z 97% AI-tool adoption, 51% of college students use genAI to study [W3-genz]. Assume 1–5% of the digital-notes exam-prep cohort is addressable + paying. |
| **SOM (bootstrap, 12–24 mo)** | **~$20K–250K ARR** | A solo bootstrapper with weak GTM realistically reaches low-thousands of paying users. See bottom-up below. |

## Bottom-up SOM
**reachable users × price × conversion:**
- *Reachable users:* Founder's serviceable wedge = English-market + Greater China exam-prep students who already use Notion/Obsidian. HK DSE alone: ~53,000–55,000 candidates/yr [W3-HK] — but most DSE students are NOT Notion/Obsidian users (a niche-within-niche; Notion/Obsidian skew university + Western). Realistic top-of-funnel for a solo founder with no distribution: **5,000–50,000 aware users/yr** across blended channels (Reddit, YouTube, organic).
- *Conversion:* Freemium consumer study apps convert ~1–3% free→paid (RemNote/Quizlet-class freemium norm; **assumption, not a primary-sourced figure — flag**).
- *Price:* $5–10/mo blended (field benchmark: StudyFetch $4.99–7.99, Mindgrasp $5.99–14.99, RemNote ~$8, Quizlet ~$3/mo-equiv) [3].
- **Math:** 10,000 reachable × 2% paid × $7/mo × 12 = **~$17K ARR**; optimistic 50,000 × 3% × $9 × 12 = **~$160K ARR**. → **SOM ≈ $20K–160K ARR in years 1–2** — an indie-business range, not a venture one. Matches the founder's bootstrap goal *only if* CAC is near-zero (organic/content), the binding constraint given the founder's stated GTM weakness.

## Buyer landscape
- **Budget holder:** the student (or a parent for high-schoolers/DSE). · **Influencer:** peers, Reddit/YouTube "study-with-me" creators, subreddit consensus. · **Decider:** the student. · **Same person?** Yes (self-serve consumer) — except high-school/DSE where a parent pays. A *low-ACV, high-volume, trust-and-word-of-mouth-driven* consumer sale — the hardest GTM for a solo founder weak on distribution.

## Market maturity
**Expanding but rapidly commoditizing / early-consolidating.** Signal: AI-in-ed funding and CAGR are high (31–43%) [W3-1,2] AND a long tail of near-identical "upload→flashcards" apps launched 2025–26 [W1-1] while incumbents (Notion, Google/NotebookLM, ChatGPT/Claude study modes) absorb the feature. Fast money + feature commoditization + platform encroachment = the classic "expanding category, collapsing margins for thin wrappers" pattern.

## Sensitivity
The answer hinges most on **CAC / organic-reach.** The SOM math only works at near-zero CAC (content/community-led). If the founder must pay to acquire (CAC > ~$15 for a $7/mo product with consumer churn), unit economics invert and SOM collapses toward **$0 viable ARR**. Secondary hinge: free→paid conversion — if it's 0.5% not 2%, SOM drops ~4×. Both sit on the founder's *weakest* axis (GTM), making the bootstrap path materially riskier than the figures alone suggest.

---

# W4 — Trends

## Three trends
| Trend | Type | Tailwind / headwind | Mechanism for THIS idea | Source |
|---|---|---|---|---|
| **97% Gen-Z AI-tool adoption; 51% of college students use genAI to study; teen ChatGPT homework use doubled 13%→26% '23→'25** | Demographic | **Tailwind** | The behavior ("ask AI to turn my notes into study material") is now mainstream — no market education needed. But it also means the *baseline competitor is the ChatGPT/Claude the student already pays for*, compressing willingness-to-pay for a standalone app. | [W3-genz] |
| **Commoditization of "upload→flashcards/quiz/mind-map" via cheap LLM APIs; dense 2025–26 entrant field + platform encroachment (Notion AI, NotebookLM, study modes)** | Technological | **Headwind** | The exact transform the hypothesis sells is now a weekend-buildable wrapper; differentiation collapses to data-ownership/sync, accuracy/trust, and distribution — not the render itself. NotebookLM's *source-grounded* generation specifically undercuts the accuracy wedge for free. | [W1-1], [W1-notion] |
| **EU AI Act high-risk obligations for educational AI from Aug 2 2026 + GDPR; AI-in-ed ethics/privacy scrutiny rising** | Regulatory | **Mild headwind for some uses, ~neutral for this wedge** | "Exam scoring / steering the learning process / cheating detection" are high-risk; a *self-directed study-reformatting* tool that doesn't grade or gate access likely sits *outside* high-risk — a relative advantage vs. proctoring/grading edtech. But ingesting students' notes raises data-handling duties in EU markets, and "AI that exploits learners' vulnerabilities" is banned. | [W4-eu] |

## Community language
- "I make my notes in Notion but my flashcards in Anki and **nothing talks to each other**" — Anki forums / FlashRecall [W2-3]
- "**Making good cards by hand is slow, tedious work**" — r/GetStudying via Scholarly [W2-1]
- "It'll **happily generate confidently wrong flashcards** if you don't check them" — r/medicalschool via Scholarly [W2-1]
- "I **gave up on the Notion + Anki combo after a few weeks**" — FlashRecall / Anki forum [W2-3]
- "**Too many apps** … my brain constantly jumping between tabs" — app-overload pieces [W2-4]
- "I need to **trace the card back to a source**" (med students) — Scholarly [W2-1]

## Analogous markets
| Market | Similar problem | What worked | What didn't | Transplant |
|---|---|---|---|---|
| **Notion→Anki bridge tools (2anki, Notion2Anki, Notes2Flash)** | Same job: reuse existing notes as drillable cards | One-way conversion got modest adoption; clean cloze/atomic cards praised | *Living sync* failed — stale cards, setup friction, "gave up after weeks" | Sync (not one-shot export) is the unmet need; whoever nails living, traceable sync wins this micro-segment. |
| **RemNote (all-in-one notes+SRS)** | Identical thesis: one tool, notes + multi-mode study | 1M+ students, free tier, real retention story | Asks student to *abandon* their existing notes home (Notion/Obsidian) | The all-in-one is taken. Open seam = "stay in your existing notes app, we add the study layer." |
| **Quizlet (consumer study SaaS)** | Mass-market drill at low ACV | 60M MAU via SEO + school virality | Paywalling free features bred resentment + churn | Free-tier-or-die dynamic; hard to monetize against free RemNote/NotebookLM. |
| **NotebookLM (source-grounded AI study)** | Generate study aids without hallucinating | Source-grounding = trust; free; Google distribution | Lacks SRS/flashcard depth (closing) | The trust bar is being set by a free Google product — the accuracy wedge is shrinking fast. |

---

## Load-bearing claims & verification
| Claim | Sources | Status |
|---|---|---|
| RemNote already ships "one tool, notes+AI flashcards+SRS, no switching to Notion/Anki/Quizlet," 1M+ students, ~$8/mo + free tier | remnote.com [1]; ToolsVerse review [8]; aihungry/pricing [3] | **Verified ≥2** |
| AI-generated flashcards hallucinate / are "confidently wrong," subtle errors — #1 dealbreaker for high-stakes prep | Scholarly Reddit roundup [W2-1]; NCBI med-ed literature [W2-3]; practitioner Substack [W2-3] | **Verified ≥3** |
| Notes↔flashcards don't sync; "gave up on Notion+Anki after a few weeks" | FlashRecall/Anki forums [W2-3]; app-overload pieces [W2-4] | **Verified ≥2** |
| Manual flashcard creation is slow/tedious (the hypothesis's pain) | r/GetStudying via Scholarly [W2-1]; Medium + voovostudy [W2-conv] | **Verified ≥2** |
| AI-in-education TAM ~$7B (2025) → $30–41B (2030), CAGR 31–43% | Precedence [W3-1]; Grand View [W3-2]; Mordor [W3-2] | **Verified ≥3 (firms disagree on magnitude — ranged accordingly)** |
| HK DSE candidates ~53,000–55,000 (2025) | YoungPost/HKEAA [W3-HK]; People's Daily [W3-HK] | **Verified ≥2** |
| Quizlet ~60M MAU; ~50% of US high-schoolers | Memrizz/Notigo aggregations [W3-quizlet]; cited to a 2021 Quizlet figure | **Single-source-vintage — 60M is a 2021 figure repeated downstream; treat as directional, not current.** |
| Free→paid conversion ~1–3% for consumer study freemium | No primary source — industry assumption | **Single-source / assumption — explicitly unverified; SOM sensitivity flags this.** |
| 8–12 apps tried / 15–25 min refocus per switch | imago + Medium blogs [W2-4] | **Single-genre (blog) — directional only, not peer-reviewed.** |
| Gen Z 97% AI adoption; 51% college students use genAI to study; teen ChatGPT homework 13%→26% | ScholarshipOwl survey [W3-genz]; College Board / NPR [W3-genz] | **Verified ≥2** |
| EU AI Act high-risk ed obligations from Aug 2 2026 | euaicompass [W4-eu]; Digital Education Council [W4-eu]; artificialintelligenceact.eu Annex III [W4-eu] | **Verified ≥3** |

---

## Synthesis read-outs (for the action card)

**Positioning & Wedge (from W2):** The one unresolved complaint this idea is uniquely placed to own is **"my notes live in Notion/Obsidian, my drill lives in Anki, and nothing stays in sync"** — reframed as *living, source-traceable sync that leaves the student in the notes app they already use.* NOT "render in multiple interfaces" (RemNote owns that). Angle of attack: a thin layer *on top of* existing notes, with traceability that answers the med-student "I must trace the card to a source" objection.

**Strongest Threat (→ steelman):** **RemNote** — it has already built and scaled the literal hypothesis (1M+ students, free, notes+SRS+AI in one). Survival bar: the founder must serve a job RemNote structurally won't — *keep me in my existing Notion/Obsidian instead of migrating me* — and ship living sync + accuracy/traceability that RemNote and the Notion→Anki bridges have not. If the founder can't beat "just use RemNote (free)" in one sentence, there is no business.

**Sizing Reality:** SOM ≈ **$20K–160K ARR (yrs 1–2)**, a legitimate indie range matching the founder's bootstrap goal — but *only at near-zero CAC*. Buyer = the student (self-serve, low ACV), the founder's weakest GTM terrain. WTP is compressed by free RemNote, free NotebookLM, and the ChatGPT/Claude the student already pays for.

**Timing:** Net **mildly negative.** Demographic tailwind (mainstream AI-study behavior) is outweighed by the technological headwind (the transform is commoditized and platform-encroached, with source-grounded NotebookLM erasing the accuracy wedge for free). Dominant driver: **commoditization + platform absorption.**

**Problem–Solution-Fit:** **weak** — real pains, but the hypothesis's headline mechanism is the least-unresolved of them.

**Hypothesis updates to flag (route to /sharpen-hypothesis — NOT edited here):**
- The wedge is **living source-traceable sync from the student's *existing* Notion/Obsidian**, not "multi-interface render" (which is shipped/commoditized).
- **Accuracy/traceability of transforms** must be a first-class feature or the high-stakes-exam segment won't trust it (their #1 complaint).
- Reconsider the **DSE / high-school segment**: Notion/Obsidian usage skews university + Western; the hypothesis's stated who (DSE students on Notion/Obsidian) may be a thin intersection. Validate the Notion/Obsidian-using exam-prep cohort exists at reachable size.
- **Monetization vs. free incumbents** (RemNote free, NotebookLM free) is unresolved — the price hypothesis competes with $0.
- **GTM/CAC is the binding constraint**, and it is the founder's weakest axis — the whole SOM hinges on near-zero-CAC organic reach.

---

## Sources
1. RemNote (homepage — single-tool notes+AI flashcards+SRS positioning) — https://www.remnote.com/
2. Knowt (free Quizlet alternative, AI study tools) — https://knowt.com/
3. Mindgrasp pricing — https://aihungry.com/tools/mindgrasp/pricing ; StudyFetch review/pricing — https://dupple.com/tools/study-fetch
4. StudyFetch (AI study tools from notes/PPT) — https://www.studyfetch.com/
5. Laxu AI "Best AI study tools / flashcard generators 2026" (entrant-field map) — https://laxuai.com/blog/best-ai-study-tools-2026 ; https://laxuai.com/blog/ai-flashcard-generators-comparison
6. Notes2Flash (Notion/Obsidian/GDocs → Anki) — https://github.com/Colmmm/notes2flash ; 2anki.net — https://2anki.net/ ; Notion2Anki — https://www.notion2anki.com/en
7. Mindgrasp / NotesXP / Scholarly (entrant field) — https://www.mindgrasp.ai/ ; https://notesxp.app/ ; https://scholarly.so/
8. RemNote review (1M+ students, $8/mo, single-tool advantage) — https://thetoolsverse.com/tools/remnote ; App Store listing — https://apps.apple.com/us/app/remnote-notes-flashcards/id1545429784
9. StudyFetch (Spark.e tutor) — https://www.studyfetch.com/
W2-1. Scholarly "Best AI for studying according to Reddit 2026" (r/medicalschool, r/GetStudying, r/Anki complaints) — https://scholarly.so/blog/best-ai-for-studying-reddit-2026
W2-1b. Quizlet paywall student op-eds — https://pawebpage.com/3269/opinions/quizlets-paywall-proves-that-students-are-its-last-priority/ ; https://www.bloomingtonsouthoptimist.org/17407/opinion/quizlets-paywall-hurts-the-students-it-claims-to-help/
W2-2. Knowt/NotebookLM "no SRS, hallucinates" + AI flashcard accuracy comparison — https://laxuai.com/blog/ai-flashcard-generators-comparison ; https://www.mindomax.com/flashcard-app-with-ai-2026
W2-3. Notes↔card no-sync / "gave up after weeks" — https://flashrecall.app/blog/notion-anki ; https://flashrecall.app/blog/anki-to-notion ; Anki forum threads — https://forums.ankiweb.net/t/is-there-a-way-to-convert-my-notion-notes-into-anki-notes/50053 ; NCBI hallucination in med-ed flashcards — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11185278/ ; practitioner "When AI Flashcards Pollute Your Anki Deck" — https://evakeiffenheim.substack.com/p/when-ai-flashcards-pollute-your-anki
W2-conv. Manual-vs-AI / Notion→Anki conversion friction — https://medium.com/@rshlsc/converting-notion-notes-to-anki-7c0491acc7b5 ; https://www.voovostudy.com/study-blog/ai-vs-manual-flashcard-creation
W2-4. App overload / fragmentation — https://blog.imago.us/reclaiming-focus-in-education-how-app-overload-is-stealing-learning-time/ ; https://www.luminpdf.com/blog/too-many-apps-how-online-learning ; https://medium.com/@suupriyahpradhan/why-students-are-still-struggling-with-productivity-apps-ff50bd46b7c4
W3-1. AI-in-education market size (Precedence) — https://www.precedenceresearch.com/ai-in-education-market
W3-2. AI-in-education market size (Grand View; Mordor) — https://www.grandviewresearch.com/industry-analysis/artificial-intelligence-ai-education-market-report ; https://www.mordorintelligence.com/industry-reports/ai-in-education-market
W3-3. Global higher-ed enrollment 269M (UNESCO); China 48M (Wikipedia/MOE) — https://www.unesco.org/en/articles/record-number-higher-education-students-highlights-global-need-recognition-qualifications ; https://en.wikipedia.org/wiki/Higher_education_in_China
W3-HK. HK DSE candidates ~53–55k (2025) — https://www.youngpostclub.com/yp/news/hong-kong/article/3326019/deep-dive-hong-kongs-dse-exam-becoming-more-popular-mainland-students ; https://en.people.cn/n3/2025/0717/c90000-20341319.html
W3-genz. Gen Z AI adoption — https://scholarshipowl.com/blog/gen-z-research/how-gen-z-uses-ai-scholarshipowl-survey-reveals-how-students-are-hacking-their-education-and-their-future/ ; https://newsroom.collegeboard.org/new-research-majority-high-school-students-use-generative-ai-schoolwork ; https://www.npr.org/2025/01/18/g-s1-43115/chatgpt-teen-school-homework-classroom-ai
W3-quizlet. Quizlet 60M MAU / ~50% US high-schoolers (2021 vintage, directional) — https://www.memrizz.com/blogs/the-ultimate-flashcard-showdown-anki-vs-quizlet-which-one-wins
W1-notion. Notion AI / Obsidian study-tool capabilities — https://aloa.co/ai/comparisons/ai-note-taker-comparison/notion-ai-vs-obsidian-ai ; https://www.obsidianstats.com/plugins/flashcards-obsidian
W4-eu. EU AI Act high-risk ed obligations (Aug 2 2026) — https://euaicompass.com/eu-ai-act-for-education.html ; https://www.digitaleducationcouncil.com/post/eu-ai-act-what-it-means-for-universities ; https://artificialintelligenceact.eu/annex/3/
