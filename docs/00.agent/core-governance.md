---
layer: agentic
---

# Shared Agent Core Governance

This repository is a Docker Compose infrastructure workspace for local and homelab multi-service stacks. These rules are shared across agent providers.

## Audience And Scope

- Audience: coding agents operating on infrastructure, documentation, automation, and incident material in this repository
- Primary surfaces: `docker-compose.yml`, `infra/`, `docs/`, `runbooks/`, `operations/`, `scripts/`, `secrets/`
- Human overview starts in [../README.md](../README.md); agent overview starts in [../AGENTS.md](../AGENTS.md)

## Persona Matrix

| Persona | Use when | Authority |
| --- | --- | --- |
| Reasoner | Multi-step changes, ambiguous tasks, refactors | `../.agent/rules/0000-Agents/0002-strong-reasoner-agent.md` |
| Architect | Repo structure, systems design, cross-cutting contracts, ADR governance | `../.agent/rules/1900-Architecture_Patterns/` |
| DevOps & CI/CD | Docker Compose, bootstrap, deployment pipelines, CI/CD, gitops | `../.agent/rules/0300-DevOps_and_Infrastructure/` |
| Security Auditor | Secrets, auth, network exposure, OWASP compliance, risk assessment | `../.agent/rules/2200-Security/` |
| SRE / Operations | Runbooks, monitoring, incident response, recovery, on-call procedures | `../.agent/rules/0300-DevOps_and_Infrastructure/0380-incident-response.md`, `../.agent/rules/0300-DevOps_and_Infrastructure/0381-runbooks-oncall.md` |
| Observability | Logging, alerting, distributed tracing, metrics strategy, SLO implementation | `../.agent/rules/2600-Observability/` |
| Performance Eng | Measurement-first latency optimization, resource limits, profiling | `../.agent/rules/2300-Performance/` |
| Data Architect | Database design, 3NF normalization, storage policy, Redis, NoSQL | `../.agent/rules/0600-DB_and_Data/` |
| Doc Specialist | Editing `*.md`, indexes, specs, plans, runbooks (Diátaxis framework) | `../.agent/rules/2100-Documentation/2100-documentation-pillar.md` |
| Debugging Specialist | Systematic RCA, defect isolation, log analysis | `../.agent/rules/0000-Agents/0015-debugging-standard.md` |
| Compliance | Regulatory compliance, PII tracking, GDPR/HIPAA standards | `../.agent/rules/2400-Compliance/` |
| AI Safety Lead | Structured system instructions, red-teaming, bias verification | `../.agent/rules/0500-AI_and_ML/`, `../.agent/rules/0000-Agents/0001-ai-prompt-engineer-agent.md` |

## Rule-Loading Policy

- Load the closest applicable rule family from `../.agent/rules/` before specialized work.
- For complex tasks, default to Reasoner + the relevant specialist persona.
- When multiple personas are needed, separate the passes instead of blending conflicting priorities.

## Skill Autonomy

- **Discover and apply**: Choose the best-fit skill for the current task context proactively.
- **Unrestricted usage**: AI agents have full autonomy to use any available skill in their toolkit. No skills are restricted.
- **2026-03 Compliance**: Always check root triggers `[LOAD:RULES:*]` before starting a task.

## Lazy-Loading Policy For docs/

- Start with [gateway.md](gateway.md) for session-start orientation.
- Stable doc roots:
  - Decisions: [../adr/README.md](../adr/README.md)
  - Requirements: [../prd/README.md](../prd/README.md), [../ard/README.md](../ard/README.md)
  - Implementation: [../specs/README.md](../specs/README.md), [../plans/README.md](../plans/README.md)
  - Operations: [../runbooks/README.md](../runbooks/README.md), [../operations/incidents/README.md](../operations/incidents/README.md)
  - Agentic: [README.md](README.md)
  - Guides: [../guides/README.md](../guides/README.md)
  - Global: [../../AGENTS.md](../../AGENTS.md)

## Template Usage Contract

- [ADR 0017: Flat Documentation Taxonomy](../adr/2026-02-27-0017-flat-documentation-taxonomy.md)
- [PRD Specification](../docs/templates/prd.md)
- [ARD Specification](../docs/templates/ard.md)
- [ADR Recommendation](../docs/templates/adr.md)
- [Technical Spec](../docs/templates/spec.md)
- [Implementation Plan](../docs/templates/plan.md)
- [Runbook Guide](../docs/templates/runbook.md)
- [Incident Report](../docs/templates/incident.md)
- [Postmortem Guide](../docs/templates/postmortem.md)

## Link And Truth Rules

- Use relative links for repository documentation.
- Do not leave `file://` links, stale template paths, or broken root-style links such as `/specs/...`.
- Do not document tools, commands, paths, or workflows that are not supported by current repo evidence.
