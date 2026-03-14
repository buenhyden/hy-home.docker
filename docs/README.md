---
layer: core
---

# Project Documentation Index (Lazy Loading Gateway)

Master entry point for spec-driven documentation discovery.

Read this file first, then load only the relevant index document for the task.

## Discovery Protocol

- `[GATE-DISC-01]` Start here before opening a doc family.
- `[GATE-DISC-02]` Prefer README/index files over blind directory scans.
- `[GATE-DISC-03]` Use relative links only.

## Lazy-Loading Map

| Marker | Entry Point | Use when |
| --- | --- | --- |
| `[LOAD:INDEX]` | [README.md](README.md) | Session start or repo-wide orientation |
| `[LOAD:DECISION]` | [adr/README.md](adr/README.md) | Architecture decisions and rationale |
| `[LOAD:STRATEGIC]` | [prd/README.md](prd/README.md), [ard/README.md](ard/README.md) | Product scope, architecture boundaries |
| `[LOAD:TACTICAL]` | [plan/README.md](plan/README.md) | Active implementation and refactor work |
| `[LOAD:RUNBOOK]` | [runbooks/README.md](runbooks/README.md) | Executable operational procedures |
| `[LOAD:HISTORY]` | [operations/incidents/README.md](operations/incidents/README.md) | Incidents, RCA, historical records |
| `[LOAD:CONTEXT]` | [context/README.md](context/README.md) | Deep service and platform blueprints |
| `[LOAD:GUIDE]` | [guides/README.md](guides/README.md), [manuals/README.md](manuals/README.md) | Lifecycle guides and team manuals |

## Templates

Use the repository templates at the project root when creating new artifacts:

- [PRD Template](../templates/prd-template.md)
- [ARD Template](../templates/ard-template.md)
- [ADR Template](../templates/adr-template.md)
- [Spec Template](../templates/spec-template.md)
- [Plan Template](../templates/plan-template.md)
- [Runbook Template](../templates/runbook-template.md)
- [Incident Template](../templates/incident-template.md)

## Related Policy

- [Agent Instructions Gateway](agentic/gateway.md) — Agent-specific session entrypoint
- [AGENTS.md](../AGENTS.md) — Canonical cross-agent entrypoint
- [CLAUDE.md](../CLAUDE.md) — Claude-specific shim
- [GEMINI.md](../GEMINI.md) — Gemini-specific shim
