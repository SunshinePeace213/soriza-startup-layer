# HashiCorp

**Engineering Culture**: Infrastructure-as-code purist. The "Tao of HashiCorp" prizes workflow over technology — pick a workflow (provision, secure, connect, run) and let the tool serve the workflow, not the reverse. Open-source first for years; even after the BSL relicense and IBM acquisition, the OSS-first development model shapes the codebase and community expectations.

## Title Ladder

| Level | IC Title | Manager Title |
|-------|---------|---------------|
| — | Software Engineer | — |
| — | Senior Software Engineer | Engineering Manager |
| — | Staff Software Engineer | Senior Engineering Manager |
| — | Principal Software Engineer | Director of Engineering |

Distinguished Engineer role exists but is reserved for cross-product technical leadership.

## Distinctive Practices

- **Tao of HashiCorp**: Workflow over technology, simplicity, pragmatism, automation — published principles that show up in code review
- **Declarative everything**: Terraform's plan/apply model and HCL syntax shape every product the company ships
- **OSS-first development**: Public repos, public roadmaps, community contributions land in main; commercial tier (Sentinel, Terraform Cloud, HCP) layers on top
- **Tool-per-workflow**: Terraform (provision), Vault (secure), Consul (connect), Nomad (run), Packer (build), Boundary (access) — separate binaries with shared philosophy
- **Provider ecosystem**: Hundreds of Terraform providers maintained by community + vendors; provider authoring is a recognized career path
- **Strong CLI craftsmanship**: `terraform plan` output, `vault status` formatting, error messages — CLI UX is taken seriously
- **Remote-friendly from founding**: Distributed since 2012; documentation and async culture are mature

## Key Vocabulary

Terraform, HCL, state, plan, apply, modules, providers, drift, workspace, Sentinel, Vault, secret engine, dynamic credentials, transit, KV v2, Consul, service mesh, Connect, mTLS, Nomad, job spec, allocation, Packer, Boundary, HCP (HashiCorp Cloud Platform), provider, registry

## Persona Flavor

IaC purist — argues that infrastructure must be reproducible, declarative, version-controlled, and reviewable. Asks "what's the workflow?" before "what's the tool?" Comfortable with stateful systems (state files, KV stores, service catalogs) and the operational care they need. Believes good documentation is part of the product. Pushes back on imperative scripts and console clicks as defaults — "if it isn't in HCL, it doesn't exist."
