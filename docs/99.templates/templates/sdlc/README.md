---
layer: agentic
---

# SDLC Templates

> requirements, architecture, specification, planning, and task-evidence templates

## Overview

`docs/99.templates/templates/sdlc` contains copyable templates for the
repository SDLC path from product intent to implementation evidence. Use these
templates when the target document belongs to Stage 01 through Stage 04 and
needs traceability across requirements, architecture, specs, plans, and tasks.

## Templates

| Need | Template |
| --- | --- |
| Capture product need, users, requirements, and success criteria | [prd.template.md](./prd.template.md) |
| Describe system or domain architecture and quality attributes | [ard.template.md](./ard.template.md) |
| Record an architectural decision and its consequences | [adr.template.md](./adr.template.md) |
| Define the technical design for a feature or workspace change | [spec.template.md](./spec.template.md) |
| Plan an approved implementation stream | [plan.template.md](./plan.template.md) |
| Track task execution, evidence, validation, and gaps | [task.template.md](./task.template.md) |

## Target Rules

- `prd.template.md` targets
  `docs/01.requirements/YYYY-MM-DD-<feature-or-system>.md`.
- `ard.template.md` targets
  `docs/02.architecture/requirements/####-<system-or-domain>.md`.
- `adr.template.md` targets
  `docs/02.architecture/decisions/####-<short-title>.md`.
- `spec.template.md` targets `docs/03.specs/<feature-id>/spec.md`.
- `plan.template.md` targets
  `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
- `task.template.md` targets
  `docs/04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md`.
- Calculate target-relative links from the copied document path.

## Related Documents

- [templates catalog](../README.md)
- [template contract](../../support/template-contract.md)
- [template governance](../../support/template-governance.md)
- [lifecycle status](../../support/lifecycle-status.md)
