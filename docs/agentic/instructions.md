---
layer: agentic
---

# Agent Behavioral Instructions

Detailed behavioral standards and operational rules for AI agents in `hy-home.docker`.

## 1. Core Principles

- **Spec-Driven Development**: Never implement complex features without a corresponding specification in `docs/specs/`.
- **Validation-First**: Run `scripts/validate-docker-compose.sh` and `scripts/preflight-compose.sh` before proposing infrastructure changes.
- **Layered Traceability**: Every file must declare its `layer` in YAML frontmatter.
- **Lazy Loading**: Respect the gateway protocol. Load only what is needed for the current task.

## 2. Documentation Standards

- All management artifacts (ADR, ARD, PRD, Spec, Plan, Runbook, Incident, Postmortem) must use repository templates.
- Maintain a flat documentation taxonomy. Avoid nested subdirectories beyond category roots.
- Use relative links for all internal cross-references.
- Mandatory `layer` metadata in every Markdown file.

## 3. Infrastructure & DevOps

- **Secrets**: Use file-backed Docker Secrets under `secrets/`. Never hardcode credentials in `.env` or Compose files.
- **Networks**: Use `infra_net` for internal service communication. External networks (`project_net`, `kind`) are integration points.
- **Port Convention**: Distinguish between `*_PORT` (container) and `*_HOST_PORT` (host).
- **Lifecycle**: Follow the [Discover -> Specify -> Plan -> Implement -> Verify -> Document] chain.

## 4. Responsible AI Collaboration (March 2026 Standards)

- Adhere to community standards for empathy and constructive feedback.
- **Full Skill Autonomy**: Proactively discover and apply ANY purpose-fit skill from your toolkit. There are NO restricted skills in this repository.
- Ensure tool use is efficient and well-documented.
- Never hallucinate requirements or edge cases; stop and ask for clarification.
- Follow the persona matrix to ensure the correct level of authority and expertise.

## 5. Operational Response

- Incident response must follow the corresponding `docs/runbooks/`.
- All SEV-1/2 incidents require a blameless postmortem recorded in `docs/operations/postmortems/`.
- Log anomalies and minor issues via GitHub Issues.
