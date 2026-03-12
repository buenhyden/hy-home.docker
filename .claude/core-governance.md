# Shared Agent Core Governance

This repository is a Docker Compose infrastructure workspace for local and homelab multi-service stacks. These rules are shared across agent providers.

## Audience And Scope

- Audience: coding agents operating on infrastructure, documentation, automation, and incident material in this repository
- Primary surfaces: `docker-compose.yml`, `infra/`, `docs/`, `runbooks/`, `operations/`, `scripts/`, `secrets/`
- Human overview starts in [../README.md](../README.md); agent overview starts in [../AGENTS.md](../AGENTS.md)

## Persona Matrix

| Persona | Use when | Authority |
| --- | --- | --- |
| Reasoner | multi-step changes, ambiguous tasks, refactors | `../.agent/rules/0000-Agents/0002-strong-reasoner-agent.md` |
| Doc Specialist | editing `*.md`, indexes, specs, plans, runbooks | `../.agent/rules/2100-Documentation/2100-documentation-pillar.md` |
| Architect | repo structure, systems design, cross-cutting contracts | `../.agent/rules/1900-Architecture_Patterns/` |
| DevOps | Docker Compose, bootstrap, operations, deployment, runtime workflows | `../.agent/rules/0300-DevOps_and_Infrastructure/` |
| Security | secrets, auth, network exposure, compliance, risk | `../.agent/rules/2200-Security/` |

## Rule-Loading Policy

- Load the closest applicable rule family from `../.agent/rules/` before specialized work.
- For complex tasks, default to Reasoner + the relevant specialist persona.
- When multiple personas are needed, separate the passes instead of blending conflicting priorities.

## Skill Autonomy

- Discover and use the most relevant skill for the task.
- Do not hardcode an allowlist of “approved skills” unless the user explicitly asks for one.
- If multiple skills apply, use the smallest set that fully covers the task and keep the role split explicit.

## Lazy-Loading Policy For docs/

- Start with [../docs/README.md](../docs/README.md).
- Use index documents, not raw directory scans, when a README/index exists.
- Default doc families:
  - Decisions: [../docs/adr/README.md](../docs/adr/README.md)
  - Strategy: [../docs/prd/README.md](../docs/prd/README.md), [../docs/ard/README.md](../docs/ard/README.md)
  - Tactical execution: [../docs/specs/README.md](../docs/specs/README.md), [../docs/plans/README.md](../docs/plans/README.md)
  - Procedures: [../docs/runbooks/README.md](../docs/runbooks/README.md)
  - History: [../docs/operations/README.md](../docs/operations/README.md), [../docs/operations/incidents/README.md](../docs/operations/incidents/README.md)
  - Deep technical context: [../docs/context/README.md](../docs/context/README.md)
  - Working guides: [../docs/guides/README.md](../docs/guides/README.md), [../docs/manuals/README.md](../docs/manuals/README.md)

## Template Usage Contract

- New PRDs use [../templates/prd-template.md](../templates/prd-template.md)
- New ARDs use [../templates/ard-template.md](../templates/ard-template.md)
- New ADRs use [../templates/adr-template.md](../templates/adr-template.md)
- New specs use [../templates/spec-template.md](../templates/spec-template.md)
- New plans use [../templates/plan-template.md](../templates/plan-template.md)
- New runbooks use [../templates/runbook-template.md](../templates/runbook-template.md)
- New incidents and postmortems use [../templates/incident-template.md](../templates/incident-template.md) and [../templates/postmortem-template.md](../templates/postmortem-template.md)

## Link And Truth Rules

- Use relative links for repository documentation.
- Do not leave `file://` links, stale template paths, or broken root-style links such as `/specs/...`.
- Do not document tools, commands, paths, or workflows that are not supported by current repo evidence.
