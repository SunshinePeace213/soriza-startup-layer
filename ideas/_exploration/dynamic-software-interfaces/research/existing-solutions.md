# Existing Solutions & Competitors — Findings

## Key findings

- **Lovable hit $400M ARR by Feb 2026 with ~8M users building ~100k apps/day** — confirming massive demand for AI-generated interfaces, but all output is developer-owned greenfield apps. Zero provision for an end user modifying an *existing* app's interface on their own. These tools serve app creators, not app *users* who want to reshape what they already use.

- **v0 (Vercel) has 4M users, generated 5M UI components since Oct 2024; 20% of Fortune 500 dev teams use it** — but v0 is entirely developer-facing (component generation → handoff to engineers). It produces a static artifact; there is no runtime adaptation, no mechanism for the final user to tweak the interface to their context. It is a better Figma-to-code bridge, not a "user-owned interface" primitive.

- **Vercel AI SDK's generative-UI RSC path (streamUI / useUIState) is officially paused** — Vercel's own docs say "Development of AI SDK RSC is currently paused; migrate to AI SDK UI." The developer infra layer for *runtime* UI generation remains genuinely unsettled — a window for a focused product to own the runtime-adaptive-UI category.

- **Thesys (C1 API, 300+ teams) and Tambo (open-source React SDK) are the clearest bets on runtime generative UI** — Thesys augments LLM responses to output structured UI components via an OpenAI-compatible endpoint; Tambo lets agents pick and stream components from a developer-registered kit. Both are pure developer SDKs: they let *developers* build apps where the AI picks components. Neither gives the end user agency to define, save, or share their own interface variant — the user-agency layer sits entirely above their abstraction level.

- **CopilotKit raised $27M Series A (May 2026) for app-native agents with generative UI** — their AG-UI protocol and "pixel-perfect vs. broad building blocks" toggle shows the dev-infra tension is real. But the product is an SDK sold to app developers, not a layer that sits on top of any existing app to let end users customise it. The $27M raise confirms investor appetite in this adjacent space.

- **Arc Boosts (user-owned CSS/JS per site) proved real demand for per-user interface personalisation — then died** — The Browser Company stopped active Arc development in May 2025 and sold to Atlassian for $610M (Oct 2025), pivoting Dia toward enterprise Jira/Confluence workflows. The consumer/prosumer "personalise any web surface" use-case is now effectively unserved — no serious inheritor owns it. This is the clearest signal that the demand was real but the business model was not.

- **Retool / Airtable Interfaces / Notion all assume one canonical interface built by IT, consumed passively by everyone else** — Retool requires developer involvement; Airtable Interfaces are shallow and walled-garden; Notion is document-first. None supports "user A gets their own layout derived from shared primitives." These incumbents have no incentive to fix this: personalised interfaces erode the admin's control they are selling.

- **Figma Make (GA Aug 2025, Claude 3.7-powered) deepens the design-to-dev handoff but does not touch the end-user customisation problem** — output is a deployed app, not a personalisable shell. It reinforces the design-team → developer → end-user waterfall rather than collapsing it.

- **Ink & Switch's "Malleable Software" research programme names the exact unsolved stack** — the essay identifies that settings/plugins only allow "specifically authorized" modifications; siloed apps cannot be composed; and there are no sustainable business models for tools-vs-apps hybrids. These gaps (persistence of user modifications, sharing, sandboxing, auth, business model) are named but **no funded startup has closed them**. The most-cited projects (PushPin, Potluck, Cambria) remain research artefacts, not products.

- **shadcn/ui (75k+ GitHub stars) normalises "UI components as owned source code, not rented dependency"** — the CLI copies components directly into your repo. The shadcn + Radix + Base UI + Tailwind ecosystem is the emerging primitive standard. The first product that wires AI-directed modification of these primitives to a persistence/sharing layer for end users inherits an already-accepted component standard rather than fighting for adoption of a new one.

## Sources
1. https://techcrunch.com/2025/11/10/lovable-says-its-nearing-8-million-users-as-the-year-old-ai-coding-startup-eyes-more-corporate-employees/ — Lovable 8M users
2. https://shipper.now/lovable-stats/ — Lovable 100k apps/day, $400M ARR Feb 2026
3. https://www.saastr.com/saastr-ai-app-of-the-week-v0-by-vercel-the-vibe-coding-tool-that-4-million-people-use-to-ship-real-software-not-just-demos/ — v0 4M users, Fortune 500 adoption
4. https://www.linkedin.com/posts/nicbaird_vercel-had-4-million-developers-ship-96-activity-7447289351639646212-4A3r — v0 9.6M projects shipped 2025
5. https://ai-sdk.dev/docs/ai-sdk-rsc/generative-ui-state — Vercel AI SDK RSC paused notice (primary source)
6. https://www.thesys.dev/report/gen-ui-2025 — Thesys Gen UI 2025 report, 300+ teams using Thesys
7. https://github.com/tambo-ai/tambo — Tambo open-source generative UI SDK for React
8. https://techcrunch.com/2026/05/05/copilotkit-raises-27m-to-help-devs-deploy-app-native-ai-agents/ — CopilotKit $27M Series A, May 2026
9. https://www.atlassian.com/blog/announcements/atlassian-acquires-the-browser-company — Atlassian $610M acquisition of The Browser Company / Dia, Oct 2025
10. https://www.superchargebrowser.com/library/arc-browser-dead-get-features-in-chrome/ — Arc in maintenance mode since May 2025
11. https://resources.arc.net/hc/en-us/articles/19212718608151-Boosts-Customize-Any-Website — Arc Boosts: user CSS/JS per site feature
12. https://www.inkandswitch.com/essay/malleable-software/ — Ink & Switch malleable software: named gaps in persistence, sharing, sandboxing, business model
13. https://www.figma.com/blog/figma-make-general-availability/ — Figma Make GA August 2025
14. https://ui.shadcn.com/ — shadcn/ui primitive ecosystem
15. https://zenriotech.com/blog/shadcn-radix-ui-headless-component-architectures-standard — shadcn 75k+ stars, headless architecture as industry standard
