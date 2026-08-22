---
profile_id: governance-policy
layer: agentic
---

# JIT Markers

Just-In-Time markers used to trigger the loading of specific policy or stage documents into the agent's context.

## Stage Markers

| Marker               | Target                          | Purpose                         |
| :------------------- | :------------------------------ | :------------------------------ |
| `[LOAD:PRD]`         | `docs/01.requirements/README.md`         | Product intent and requirements |
| `[LOAD:ARCHITECTURE]` | `docs/02.architecture/descriptions/README.md`        | Architecture Description        |
| `[LOAD:ADR]`         | `docs/02.architecture/decisions/README.md`         | Decision history                |
| `[LOAD:SPECS]`       | `docs/03.specs/README.md`       | Technical source of truth       |
| `[LOAD:PLANS]`       | `docs/03.specs/README.md`                 | Co-located implementation plans |
| `[LOAD:TASKS]`       | `docs/03.specs/README.md`                 | Co-located execution evidence   |
| `[LOAD:OPERATIONS]`  | `docs/05.operations/README.md`   | Operations knowledge base        |
| `[LOAD:INCIDENTS]`   | `docs/05.operations/incidents/README.md`   | Incident records and postmortems |
| `[LOAD:REFERENCES]`  | `docs/90.references/README.md`  | Stable references               |
| `[LOAD:TEMPLATES]`   | `docs/99.templates/README.md`   | Document templates              |

## Rule Markers

| Marker                      | Rule                              |
| :-------------------------- | :-------------------------------- |
| `[LOAD:RULES:BOOTSTRAP]`    | `policies/bootstrap.md`              |
| `[LOAD:RULES:PERSONA]`      | `policies/persona.md`                |
| `[LOAD:RULES:CHECKLISTS]`   | `policies/task-checklists.md`        |
| `[LOAD:RULES:STAGE-MATRIX]` | `policies/stage-authoring-matrix.md` |
| `[LOAD:RULES:STANDARDS]`    | `policies/standards.md`              |
| `[LOAD:RULES:DOCS]`         | `policies/documentation-protocol.md` |
| `[LOAD:RULES:QUALITY]`      | `policies/quality-standards.md`      |
| `[LOAD:RULES:AGENTIC]`      | `policies/agentic.md`                |
| `[LOAD:RULES:GIT]`          | `policies/git-workflow.md`           |
| `[LOAD:RULES:GITHUB]`       | `policies/github-governance.md`      |

## Related Documents

- `../README.md`
