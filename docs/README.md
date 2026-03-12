# Project Documentation Index (Lazy Loading Gateway)
>
> Master entry point for spec-driven documentation discovery.

To prevent context window saturation, AI agents MUST follow this gateway protocol for discovering and reading documentation.

## 1. Documentation Discovery Protocols

- **[GATE-DISC-01] Index-First Search**: Always read this README before fetching specific sub-directories.
- **[GATE-DISC-02] Conditional Read**: Only fetch folders relevant to your active layer (see below).
- **[GATE-DISC-03] Link Integrity**: Use the correct relative paths defined below and GFM alerts for emphasis.

## 2. Directory Map (Layered Access)

| Layer | Entry Point | Usage Priority | Lazy Load Marker |
| --- | --- | --- | --- |
| **Index** | `README.md` | Session Start | `[LOAD:INDEX]` |
| **Strategic** | `prd/`, `ard/` | High (Planning) | `[LOAD:STRATEGIC]` |
| **Tactical** | `specs/`, `plans/` | Critical (Execution) | `[LOAD:TACTICAL]` |
| **Decision** | `adr/` | Medium (Rationale) | `[LOAD:DECISION]` |
| **Operational** | `runbooks/`, `operations/` | High (Maintenance) | `[LOAD:OPERATIONAL]` |
| **Procedural** | `guides/`, `manuals/` | Medium (Reference) | `[LOAD:PROCEDURAL]` |

## 3. Latest Templates & Guidelines

For all new document creation, MUST refer to the `templates/` directory at the project root.

- [PRD Template](file:///home/hy/projects/hy-home.docker/templates/prd-template.md)
- [Spec Template](file:///home/hy/projects/hy-home.docker/templates/spec-template.md)
- [ADR Template](file:///home/hy/projects/hy-home.docker/templates/adr-template.md)

---
*For behavioral directives, see [AGENTS.md](file:///home/hy/projects/hy-home.docker/AGENTS.md) at the repository root.*
