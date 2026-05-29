---
layer: agentic
---

# JIT Markers

Just-In-Time markers used to trigger the loading of specific policy or stage documents into the agent's context.

## Stage Markers

| Marker               | Target                          | Purpose                         |
| :------------------- | :------------------------------ | :------------------------------ |
| `[LOAD:PRD]`         | `docs/01.requirements/README.md`         | Product intent and requirements |
| `[LOAD:ARD]`         | `docs/02.architecture/requirements/README.md`         | Architecture reference          |
| `[LOAD:ADR]`         | `docs/02.architecture/decisions/README.md`         | Decision history                |
| `[LOAD:SPECS]`       | `docs/03.specs/README.md`       | Technical source of truth       |
| `[LOAD:PLANS]`       | `docs/04.execution/plans/README.md`       | Implementation planning         |
| `[LOAD:TASKS]`       | `docs/04.execution/tasks/README.md`       | Execution evidence              |
| `[LOAD:OPERATIONS]`  | `docs/05.operations/README.md`   | Operations knowledge base        |
| `[LOAD:INCIDENTS]`   | `docs/05.operations/incidents/README.md`   | Incident records and postmortems |
| `[LOAD:REFERENCES]`  | `docs/90.references/README.md`  | Stable references               |
| `[LOAD:TEMPLATES]`   | `docs/99.templates/README.md`   | Document templates              |
| `[LOAD:MEMORY]`      | `docs/00.agent-governance/memory/README.md` | Advisory governance memory       |

## Rule Markers

| Marker                      | Rule                              |
| :-------------------------- | :-------------------------------- |
| `[LOAD:RULES:BOOTSTRAP]`    | `rules/bootstrap.md`              |
| `[LOAD:RULES:PERSONA]`      | `rules/persona.md`                |
| `[LOAD:RULES:CHECKLISTS]`   | `rules/task-checklists.md`        |
| `[LOAD:RULES:STAGE-MATRIX]` | `rules/stage-authoring-matrix.md` |
| `[LOAD:RULES:STANDARDS]`    | `rules/standards.md`              |
| `[LOAD:RULES:DOCS]`         | `rules/documentation-protocol.md` |
| `[LOAD:RULES:QUALITY]`      | `rules/quality-standards.md`      |
| `[LOAD:RULES:AGENTIC]`      | `rules/agentic.md`                |
| `[LOAD:RULES:GIT]`          | `rules/git-workflow.md`           |
| `[LOAD:RULES:GITHUB]`       | `rules/github-governance.md`      |

## Related Documents

- `../README.md`
