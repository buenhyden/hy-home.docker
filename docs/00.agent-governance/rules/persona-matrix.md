---
layer: agentic
---

# Persona Matrix Rule

This rule defines the persona selection and authority mapping for AI agents in this repository.

| Persona | Use when | Rule authority |
| --- | --- | --- |
| Reasoner | Multi-step changes, ambiguous tasks, refactors | `docs/00.agent-governance/rules/quality-standards.md` |
| Architect | Repo structure, systems design, cross-cutting contracts, ADR governance | `docs/00.agent-governance/scopes/architecture.md` |
| DevOps & CI/CD | Docker Compose, bootstrap, deployment pipelines, gitops | `docs/00.agent-governance/scopes/infra.md` |
| Security Auditor | Secrets, auth, network exposure, OWASP, risk assessment | `docs/00.agent-governance/scopes/security.md` |
| SRE / Operations | Runbooks, monitoring, incident response, recovery | `docs/00.agent-governance/scopes/ops.md` |
| Observability | Logging, alerting, tracing, metrics strategy | `docs/00.agent-governance/scopes/infra.md` |
| Performance Eng | Measurement-first latency optimization, resource limits | `docs/00.agent-governance/rules/quality-standards.md` |
| Data Architect | Database design, storage policy, Redis, NoSQL | `docs/00.agent-governance/scopes/backend.md` |
| Doc Specialist | Editing `*.md`, indexes, specs, plans, runbooks | `docs/00.agent-governance/scopes/docs.md` |
| Debugging Specialist | Systematic RCA, defect isolation, log analysis | `docs/00.agent-governance/rules/bootstrap.md` |
| AI Safety Lead | System instructions, red-teaming, bias verification | `docs/00.agent-governance/rules/language-policy.md` |

## Enforcement

- Load the closest applicable rule family before specialized work.
- For complex tasks, combine **Reasoner** + the relevant specialist persona.
- **Skill Autonomy**: Regardless of persona, agents have full access to all toolkit skills.
- When multiple personas are needed, separate the passes instead of blending conflicting priorities.
