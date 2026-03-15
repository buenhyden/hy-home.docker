---
layer: agentic
---

# Persona Matrix Rule

This rule defines the persona selection and authority mapping for AI agents in this repository.

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

## Enforcement

- Load the closest applicable rule family before specialized work.
- For complex tasks, combine **Reasoner** + the relevant specialist persona.
- **Skill Autonomy**: Regardless of persona, agents have full access to all toolkit skills.
- When multiple personas are needed, separate the passes instead of blending conflicting priorities.
