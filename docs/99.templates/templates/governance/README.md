---
layer: agentic
---

# Governance Templates

> Stage 00 memory, progress, and harness task contract templates

## Overview

`docs/99.templates/templates/governance` contains copyable templates for
agent-facing governance records. Use these templates when the target document
records durable agent memory, active progress, or the allowed surface for a
harness-engineering task.

## Templates

| Need | Template |
| --- | --- |
| Record a durable problem, context, resolution, prevention, and evidence note | [memory.template.md](./memory.template.md) |
| Seed or repair the Stage 00 agent progress log structure | [progress.template.md](./progress.template.md) |
| Define allowed paths, approvals, validation, secret handling, and rollback for harness work | [harness-task-contract.template.md](./harness-task-contract.template.md) |

## Target Rules

- `memory.template.md` targets
  `docs/00.agent-governance/memory/{short-title}.md`.
- `progress.template.md` targets
  `docs/00.agent-governance/memory/progress.md`.
- `harness-task-contract.template.md` targets
  `docs/04.execution/tasks/YYYY-MM-DD-<harness-stream>.md`.
- Calculate target-relative links from the copied document path.

## Related Documents

- [templates catalog](../README.md)
- [template governance](../../support/template-governance.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
- [template selection](../../support/template-selection.md)
