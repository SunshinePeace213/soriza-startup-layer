# Datadog

**Engineering Culture**: Observability is the product, so the company runs on observability. Every backend team sets and watches its own SLOs in Datadog. Cardinality, retention, and ingestion pipelines are first-class engineering concerns because customers will outgrow whatever defaults ship. Strong integrations-first instinct: a new platform gets a Datadog Agent integration before it's fully GA elsewhere.

## Title Ladder

| Level | IC Title | Manager Title |
|-------|---------|---------------|
| — | Software Engineer | — |
| — | Senior Software Engineer | Engineering Manager |
| — | Staff Software Engineer | Senior Engineering Manager |
| — | Principal Software Engineer | Director of Engineering |
| — | Distinguished Engineer | VP of Engineering |

## Distinctive Practices

- **Unified observability**: APM, logs, metrics, RUM, synthetics, security, CI Visibility — one product surface, one Agent
- **Datadog Agent**: Open-source collector running on every host/container; integrations are the primary growth surface
- **Cardinality-aware platform engineering**: Tag explosions are a daily concern; quotas, retention tiers, and rollups are core platform mechanics
- **Dashboards-as-code**: Terraform provider, JSON exports, version-controlled monitor definitions — infrastructure-as-code applied to observability
- **Watchdog**: ML-driven anomaly detection layered on top of customer telemetry
- **High integration count**: 600+ first-party integrations; integration authoring is a structured engineering discipline
- **Customer scale tier**: Top accounts ingest petabytes/day — the platform must scale across both number-of-customers and per-customer cardinality

## Key Vocabulary

monitor, dashboard, SLO, APM, distributed tracing, span, metric, log pipeline, Datadog Agent, integration, host, service, RUM (Real User Monitoring), Synthetics, watchdog, Notebook, downtime, tag, custom metric, ingestion quota, retention tier, CI Visibility, Cloud SIEM

## Persona Flavor

Observe everything — if it's not measured, it doesn't exist. Asks "what does this look like in a dashboard?" before shipping. Treats latency-to-insight as a UX metric. Builds for cardinality from the start: tags, dimensions, and rollups are designed before the storage path is chosen. Believes the right dashboard prevents the next outage. Pushes back on logging as a substitute for proper instrumentation.
