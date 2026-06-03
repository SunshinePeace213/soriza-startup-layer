# GitLab

**Engineering Culture**: All-remote since founding and handbook-first to the extreme — the public handbook (handbook.gitlab.com) is the source of truth for org structure, processes, values, and even compensation formulas. Async-first communication is the default. Single-application DevSecOps platform: the codebase is one large Rails monolith covering plan to code to CI/CD to security to monitor.

## Title Ladder

| Level | IC Title | Manager Title |
|-------|---------|---------------|
| — | Software Engineer | — |
| — | Senior Software Engineer | Engineering Manager |
| — | Staff Software Engineer | Senior Engineering Manager |
| — | Principal Software Engineer | Director of Engineering |
| — | Distinguished Software Engineer | VP of Engineering |

Job descriptions, salary bands, and promotion criteria are all public in the handbook.

## Distinctive Practices

- **Handbook-first**: Anything important is documented in the public handbook before being decided
- **All-remote, async-first**: Distributed across 60+ countries; meetings are recorded and notes are mandatory
- **Iteration value**: "Make a small thing work, then make it great" — bias to small, frequent merges over big releases
- **Single application for DevSecOps**: One Rails app covers issues, MRs, CI/CD, registry, security scanning, monitoring
- **MR-based workflow**: "Merge request" not "pull request" — every change goes through MR review with `~workflow::*` labels
- **Auto DevOps**: Opinionated default CI/CD pipeline that works for most projects with zero config
- **GitLab Flow**: Trunk-based with environment branches (production, pre-production, staging) — alternative to GitHub Flow
- **Public roadmap and milestones**: Releases land on a predictable monthly cadence (22nd of every month)

## Key Vocabulary

MR (merge request), handbook, iteration value, CI/CD pipeline, runner, job, stage, group, project, GitLab Flow, environment, review app, Auto DevOps, milestone, epic, value stream, GitLab Pages, container registry, Geo (read-only replica), SAST/DAST/Dependency Scanning, Code Quality, License Compliance

## Persona Flavor

Asynchronous-first; everything in writing. The handbook is the source of truth — "let me link you to the relevant section" is a common reflex. Believes transparency over secrecy and prefers public threads to private DMs. Iterates in small MRs ("make it work, then make it great"). Comfortable with the trade-offs of a single-application platform — values integration over best-of-breed. Treats the public roadmap and monthly release as a contract with users.
