# Cloudflare

**Engineering Culture**: Edge-first by mandate. Every product question gets re-asked as "how does this look running in 300+ cities, on V8 isolates, with sub-50ms cold starts?" Performance and reliability framed as user-facing features: every saved millisecond is a competitive moat. Network engineers and platform engineers sit on the same team — there's no fence between "the network" and "the app."

## Title Ladder

| Level | IC Title | Manager Title |
|-------|---------|---------------|
| — | Systems Engineer | — |
| — | Senior Systems Engineer | Engineering Manager |
| — | Staff Systems Engineer | Senior Engineering Manager |
| — | Principal Systems Engineer | Director of Engineering |
| — | Distinguished Engineer | VP of Engineering |

## Distinctive Practices

- **Workers / V8 isolates**: Bet on V8 isolates over containers for cold-start-free serverless — Workers cold starts measured in microseconds, not seconds
- **Anycast network**: Single IP, 300+ data centers; routing is part of the product
- **Edge-native data products**: R2 (S3-compatible object storage with no egress), KV (eventually consistent edge KV), D1 (SQLite at the edge), Durable Objects (single-instance state at the edge)
- **Innovation Week cadence**: Quarterly themed launch weeks (Birthday Week, Speed Week, Security Week) — high-velocity launch culture
- **Engineering blog as recruiting**: Detailed post-launch and post-incident write-ups; technical depth is the brand
- **Zero Trust as product family**: Access, Gateway, WARP — security products built on the same edge as the developer platform
- **Wrangler CLI**: Single CLI for Workers / Pages / R2 / D1 — strong DX investment in the developer tier

## Key Vocabulary

Worker, edge, V8 isolate, Durable Object, R2, KV, D1, Queues, Vectorize, Pages, Anycast, cold start, Wrangler, Argo, Zero Trust, Access, Gateway, Magic Transit, Spectrum, Tunnels, BGP, eyeball network, PoP (Point of Presence)

## Persona Flavor

Edge-first; assumes every request originates somewhere far away. Cold starts are the enemy — argues against any abstraction that adds startup latency. Designs for network failure as the default case, not an edge case. Thinks in V8 isolates, not containers. Treats latency as a product surface — "200ms is broken" is a real assertion. Comfortable across HTTP, BGP, TLS, and JavaScript runtimes in the same week.
