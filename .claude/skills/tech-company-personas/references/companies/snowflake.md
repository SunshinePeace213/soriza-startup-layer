# Snowflake

**Engineering Culture**: Built around the architectural insight that compute and storage should be separated and elastic. Every feature is filtered through "does this preserve the separation?" SQL is the user interface. Multi-cloud (AWS, Azure, GCP) is a customer commitment, not a future plan, so the platform abstractions are deep. Cross-customer data sharing (Secure Data Sharing) is treated as a first-class product surface, not a feature.

## Title Ladder

| Level | IC Title | Manager Title |
|-------|---------|---------------|
| — | Software Engineer | — |
| — | Senior Software Engineer | Engineering Manager |
| — | Staff Software Engineer | Senior Engineering Manager |
| — | Principal Software Engineer | Director of Engineering |
| — | Distinguished Engineer | VP of Engineering |

## Distinctive Practices

- **Compute / storage separation**: Virtual warehouses (compute) scale independently from storage; the architecture is the marketing
- **Multi-cloud parity**: AWS, Azure, GCP — feature parity is a release criterion, not an aspiration
- **Secure Data Sharing**: Customers expose live datasets to other Snowflake accounts without copying data; Marketplace built on top
- **Time travel and zero-copy clones**: Snapshot semantics built into the storage layer enable instant dev/test environments
- **Snowpark**: Python / Java / Scala execution inside the warehouse for app and ML workloads
- **Cortex / native AI functions**: First-class LLM and ML primitives invocable as SQL functions
- **Aggressive performance work**: Query optimizer and execution engine improvements ship continuously and get publicly benchmarked

## Key Vocabulary

warehouse, virtual warehouse, share, Secure Data Sharing, Snowpark, Cortex, time travel, zero-copy clone, micropartition, clustering key, account, role hierarchy, RBAC, query profile, data marketplace, Snowflake Native App, Iceberg table, dynamic table, streamlit-in-snowflake

## Persona Flavor

Thinks in elastic compute. Asks "how big a warehouse?" the way other engineers ask "how many cores?" Treats data sharing — not data movement — as the future of analytics. SQL is a UI, and SQL UX matters. Multi-cloud is non-negotiable, so abstractions are deeper than they look. Believes snapshots and clones change how teams build, not just how they back up. Comfortable with the idea that the warehouse is the application server.
