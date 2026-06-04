# Competitor Steelman — ecommerce-ops-dashboard-per-role

*Written in the voice of the incumbent's strategist. Adversarial by design. The job here is to make the strongest case that the founder loses, not a balanced read.*

The founder's pitch is "each team member gets their own AI-generated operations dashboard from shared store data." The uncomfortable truth: that is not a product, it is a feature — and it is a feature the platform that owns the data is already shipping, for free, to the exact merchants you'd sell to. You are building a wrapper around an API whose owner has decided to absorb your entire value proposition.

## Per-tier threat

- **Direct — Shopify itself (Sidekick + native Saved Views + custom roles).** This is not a fair fight. Shopify already ships three of your four pillars natively and free: (1) **Saved Views** on Orders/Inventory/Transfers — every staff member can build a view with custom filters, custom columns, custom sort order and save it by name ("pending orders that need packing, sorted by courier cutoff," "today's refund queue") — *exactly* your headline use case, shipped, in the admin, at zero marginal cost. (2) **Custom roles** (Merchandiser, Customer support, or fully bespoke permission sets) scoped to Products/Orders/Customers/Reports/Apps/Settings — your "per-role" framing, native. (3) **Sidekick**, the in-admin AI assistant that as of Winter '26 *generates custom admin applications from natural language with "no programming expertise required,"* respects each staff member's permissions automatically, and is included in the plan. Your differentiated demo — "I want to see X, render me a dashboard" — is a Sidekick prompt. You are selling, as a paid third-party app, the thing the merchant gets in the box.

- **Indirect — "good enough" is the saved view they already use plus a $9.99 app.** Small e-commerce teams do not have an unmet dashboarding crisis; they have a saved filter and a column layout, and for the 10% of cases that need more, a purpose-built single-job app (Order Picking App, returns apps, order managers) at $9.99–$19.99/mo that does *one* job deeply — barcode-scanned picking, return rules, restocking fees. A focused $10 app that nails warehouse picking will out-convert a generalist "AI renders any view" tool every time, because the buyer's actual pain is "packing errors," not "interface personalization." Horizontal flexibility is a liability against vertical depth here. Good-enough wins because the problem the founder describes is friction, not fire.

- **Potential acquirer — Shopify has no reason to buy you; they'll out-ship you.** Normally this tier is a threat *and* an exit. Here it's only a threat: the natural acquirer already built it. Shopify is pouring AI into Sidekick (Pulse, Skills, Flow-from-natural-language, custom app generation) as the centerpiece of its merchant strategy. They will not pay for a wrapper around their own API when the capability is core roadmap. The acquirer who'd have rescued you is the one erasing you.

- **Adjacent — Retool / Glide can render an internal e-commerce ops tool today.** The "AG-UI commoditizes agent-to-frontend plumbing" tailwind the founder leans on cuts *against* him: it lowers the barrier for everyone, including incumbents with AI-native builders already live. Retool is AI-native ("describe what you need, it generates a working app connected to your data"), reads and writes Shopify via REST/GraphQL, has a published Shopify dashboard template and a "build internal apps on top of Shopify" use case, and is **free for up to 5 users** — the founder's exact team-size sweet spot (2–15 staff). A 3-person shop that wants role-specific views can get them from Retool's free tier today, with write-back, which the founder may not even offer.

## The one that kills you

**Shopify Sidekick** (the platform-native incumbent). Not a separate company — the platform under the founder's feet, which is worse, because he can't out-distribute or out-integrate the entity that *owns the data, the buyer relationship, the billing, and the admin surface he renders into.*

**Why their approach is better for the customer, not just cheaper:**
- **Zero integration, zero new login, zero new vendor.** Sidekick lives inside the admin the staff already use all day. The founder's product requires a merchant to install an app, grant API/data-access scopes, onboard staff into a second surface, and trust a solo HK developer with their order and customer data. Sidekick is one click and already trusted with everything.
- **It already respects roles.** Sidekick automatically honors each staff member's existing permissions — the picker sees picker data, the CS rep sees CS data — with no per-role setup. The founder has to rebuild Shopify's entire permission model on the outside and keep it in sync, or risk leaking data across roles. That's a liability he carries and Shopify doesn't.
- **It writes back and acts.** Sidekick builds Flow automations ("when inventory < 10, Slack alert + tag"), generates apps, and takes actions in the admin. A render-only dashboard that shows the refund queue but can't *process* the refund is a strictly worse tool than the place the work actually happens.
- **It's free and improving monthly.** Included in the plan, on the fastest-shipping AI roadmap in commerce. The founder is charging for a snapshot of a capability that gets better, for free, every release.

**Why each claimed differentiator is not defensible:**
- *"Per-role AI-generated dashboards from shared data."* — Already native: Saved Views + custom roles + Sidekick app generation. This is shipped, not roadmap. The core idea is gone before launch.
- *"Removes ops friction for teams with no dev budget / no FDE budget."* — Sidekick *is* the no-budget FDE: "generate custom applications, no programming expertise required," free in-plan. The wedge ("enterprises pay engineers, small shops can't") is exactly the gap Shopify is closing for its own merchants. The premise is being invalidated in real time.
- *"AG-UI / agent-to-frontend plumbing is the why-now."* — Commoditized plumbing is not a moat; it's a moat-eraser. It lets Sidekick, Retool, and Glide do this too. A tailwind everyone rides is no one's edge.
- *"Vertical SaaS commands 2–3x WTP premium."* — Only if the vertical app owns something the horizontal platform doesn't. Here the platform owns the data, the buyer, the interface, and the AI. There is no upstream asset for a third party to capture; the "vertical" layer is rented from the incumbent on revocable API terms.
- *"Founder's Soriza e-commerce background → distribution via a community he understands."* — He built Soriza but, by his own account, never launched it: zero distribution track record, self-identified weakest on GTM/sales. "I understand the community" is not a distribution channel against a platform with the merchant's homepage, app store placement, billing rails, and an AI assistant that greets every merchant on login. Domain familiarity is not an unfair advantage when the incumbent has the relationship.

## Survival bar

For the founder to survive this, **all** of the following must be true — stated as conditions to clear, not reassurance:

1. **He must find a job Sidekick + Saved Views provably cannot do** — likely *cross-platform* (a shop running Shopify *and* WooCommerce *and* a marketplace from one unified ops view), since Sidekick is locked to Shopify and Saved Views can't reach outside it. A single-platform play is dead on arrival.
2. **The job must require write-back and action, not just rendering** — a read-only "view generator" is strictly dominated by the place the work already happens. He must own a workflow (picking, returns adjudication, courier-cutoff dispatch) end to end, not display it.
3. **He must defend a data or workflow asset the platform doesn't own** — e.g., normalized multi-channel order state, courier-cutoff logic per HK/Greater-China carrier, or Chinese-language CS sentiment tuned for the region. Differentiation has to live in something Shopify can't trivially absorb on its next release.
4. **He must solve distribution without relying on "community I understand"** — a concrete, repeatable acquisition channel (HK/Greater-China Shopify-partner agencies, WooCommerce dev shops, a wedge integration), given a documented zero-launch, weakest-on-GTM starting point and a 1–2 month runway.
5. **He must out-run a free, monthly-improving incumbent feature on a part-time schedule** — 15–25 hrs/week, solo, bootstrapped, against the fastest AI shipper in commerce. The timeline math has to close before Sidekick's next release closes the gap further.

If even one of these fails, the incumbent wins by default — because for the single-platform, read-only, "AI renders my view" version of this idea, the incumbent has *already* won.

## Sources

1. https://www.shopify.com/sidekick — Sidekick included in plan; respects each staff member's admin permissions automatically.
2. https://thelettertwo.com/2025/12/10/shopify-ai-growth-tools-sidekick-tinker-agentic-storefronts/ — Winter '26: Sidekick generates custom admin applications via natural language, "no programming expertise required"; Skills; Flow automation from plain language.
3. https://www.retailbrew.com/stories/2025/12/11/shopify-plugs-in-more-ai-power-to-merchant-assistant — Sidekick Pulse proactive monitoring; expanded agentic capabilities as core merchant strategy.
4. https://changelog.shopify.com/posts/search-filter-and-saved-views-for-orders-products-and-more — Native Saved Views with saved filters, custom columns, column order, and sort — the founder's headline use case, shipped free.
5. https://help.shopify.com/en/manual/shopify-admin/productivity-tools/searching-filtering-views — Saved views available on Orders, Inventory, Transfers, Metaobjects; custom columns hide/reorder per view.
6. https://help.shopify.com/en/manual/your-account/users/roles/manage-roles — Native custom roles (e.g., Merchandiser, Customer support) scoped per permission category.
7. https://retool.com/use-case/internal-apps-on-shopify — Retool builds internal apps on Shopify data (REST/GraphQL), AI-native generation, read + write-back.
8. https://retool.com/pricing — Retool free for up to 5 users; team plan $10/standard user/mo — fits the founder's 2–15-staff target.
9. https://apps.shopify.com/order-picking-app — Focused single-job picking app (barcode, custom pick types) — the "good enough" vertical depth that beats a generalist view tool.
10. https://www.logbase.io/blog/shopify-order-management-apps — Order/returns app pricing benchmarks ($9.99–$49.99/mo) the founder must price against.
