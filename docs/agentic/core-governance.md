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
- **Unrestricted usage**: Do not hardcode "approved skills" or restrict the agent's ability to browse and use its full toolkit. Use purpose-fit skills for every task (e.g., `agent-md-refactor` for instructions, `docker-expert` for compose work).
- **Purpose Matching**: Select skills based on their functional purpose rather than list-matching.

## Lazy-Loading Policy For docs/

- Start with [gateway.md](gateway.md) for session-start orientation.
- Use index documents (`README.md`) for discovery within categories.
- Stable doc roots (Flat taxonomy):
  - Decisions: [../docs/adr/README.md](../docs/adr/README.md)
  - Requirements: [../docs/prd/README.md](../docs/prd/README.md), [../docs/ard/README.md](../docs/ard/README.md)
  - Implementation: [../docs/specs/README.md](../docs/specs/README.md), [../docs/plans/README.md](../docs/plans/README.md)
  - Operations: [../docs/runbooks/README.md](../docs/runbooks/README.md), [../docs/operations/README.md](../docs/operations/README.md)
  - Agentic: [README.md](README.md)
  - Deep Context: [../docs/context/README.md](../docs/context/README.md)
  - Methods: [../docs/guides/README.md](../docs/guides/README.md), [../docs/manuals/README.md](../docs/manuals/README.md)

## Template Usage Contract

- New PRDs use [../templates/prd-template.md](../templates/prd-template.md)
- New ARDs use [../templates/ard-template.md](../templates/ard-template.md)
- New ADRs use [../templates/adr-template.md](../templates/adr-template.md)
- New specs use [../templates/spec-template.md](../templates/spec-template.md)
- New plans use [../templates/plan-template.md](../templates/plan-template.md)
- New runbooks use [../templates/runbook-template.md](../templates/runbook-template.md)
- New incidents use [../templates/incident-template.md](../templates/incident-template.md)
- New postmortems use [../templates/postmortem-template.md](../templates/postmortem-template.md)

## Link And Truth Rules

- Use relative links for repository documentation.
- Do not leave `file://` links, stale template paths, or broken root-style links such as `/specs/...`.
- Do not document tools, commands, paths, or workflows that are not supported by current repo evidence.
