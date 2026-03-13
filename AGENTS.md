# Agent Instructions — hy-home.docker

Docker Compose infrastructure workspace for local and homelab multi-service stacks.

**Shared governance:** [.claude/core-governance.md](.claude/core-governance.md) · [.claude/workflow.md](.claude/workflow.md)
**Documentation gateway:** [docs/agent-instructions.md](docs/agent-instructions.md)
**Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md) · [README.md](README.md)

## Core Principles

- **Spec-Anchored**: No infrastructure change without an approved spec in `docs/specs/`.
- **Evidence-Driven**: Execute from validated investigation outputs and command results, not prompt-only assumptions.
- **Minimal Blast Radius**: Touch only what the spec requires. Do not modify adjacent services.
- **Secrets Safety**: Never log, print, or commit secret values. Use Docker Secrets or environment references.
- **Link Integrity**: Relative links only. No `file://` or absolute filesystem paths in documentation.
- **Skill Autonomy**: Use the most relevant available skill. Do not restrict skill discovery unless explicitly asked.

## Persona Matrix

| Persona | Use when | Rule authority |
| --- | --- | --- |
| Reasoner | Multi-step changes, ambiguous tasks, refactors | `.agent/rules/0000-Agents/0002-strong-reasoner-agent.md` |
| Architect | Repo structure, systems design, cross-cutting contracts, ADR governance | `.agent/rules/1900-Architecture_Patterns/` |
| DevOps & CI/CD | Docker Compose, bootstrap, deployment pipelines, gitops | `.agent/rules/0300-DevOps_and_Infrastructure/` |
| Security Auditor | Secrets, auth, network exposure, OWASP, risk assessment | `.agent/rules/2200-Security/` |
| SRE / Operations | Runbooks, monitoring, incident response, recovery | `.agent/rules/0300-DevOps_and_Infrastructure/0380-incident-response.md`, `.agent/rules/2600-Observability/` |
| Observability | Logging, alerting, tracing, metrics strategy | `.agent/rules/2600-Observability/` |
| Performance Eng | Measurement-first latency optimization, resource limits | `.agent/rules/2300-Performance/` |
| Data Architect | Database design, storage policy, Redis, NoSQL | `.agent/rules/0600-DB_and_Data/` |
| Doc Specialist | Editing `*.md`, indexes, specs, plans, runbooks | `.agent/rules/2100-Documentation/` |
| Debugging Specialist | Systematic RCA, defect isolation, log analysis | `.agent/rules/0000-Agents/0015-debugging-standard.md` |
| Compliance | Regulatory compliance, PII tracking, GDPR/HIPAA | `.agent/rules/2400-Compliance/` |
| AI Safety Lead | System instructions, red-teaming, bias verification | `.agent/rules/0500-AI_and_ML/`, `.agent/rules/0000-Agents/0001-ai-prompt-engineer-agent.md` |

For complex tasks, combine Reasoner + the relevant specialist persona.

## Infrastructure Lifecycle

1. **Discover** — Load [docs/agent-instructions.md](docs/agent-instructions.md); find existing specs, ADRs, runbooks.
2. **Specify** — If no spec exists, create `docs/specs/<domain>/spec.md` from [templates/spec-template.md](templates/spec-template.md).
3. **Plan** — Verify or create `docs/plans/<date>-<name>.md` from [templates/plan-template.md](templates/plan-template.md).
4. **Implement** — Apply the smallest correct change. `docker compose config` must pass before any `up`.
5. **Verify** — Run `bash scripts/validate-docker-compose.sh && bash scripts/preflight-compose.sh`.
6. **Document** — Update runbooks, ADRs, and operations history whenever behavior or structure changes.

## Template Contracts

| Artifact | Template |
| --- | --- |
| PRD | [templates/prd-template.md](templates/prd-template.md) |
| ARD | [templates/ard-template.md](templates/ard-template.md) |
| ADR | [templates/adr-template.md](templates/adr-template.md) |
| Spec | [templates/spec-template.md](templates/spec-template.md) |
| Plan | [templates/plan-template.md](templates/plan-template.md) |
| Runbook | [templates/runbook-template.md](templates/runbook-template.md) |
| Incident | [templates/incident-template.md](templates/incident-template.md) |
| Postmortem | [templates/postmortem-template.md](templates/postmortem-template.md) |
