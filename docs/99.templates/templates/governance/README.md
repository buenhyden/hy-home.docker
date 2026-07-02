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

## Use When

| Need | Template |
| --- | --- |
| Record a durable problem, context, resolution, prevention, and evidence note | [memory.template.md](./memory.template.md) |
| Seed or repair the Stage 00 agent progress log structure | [progress.template.md](./progress.template.md) |
| Define allowed paths, approvals, validation, secret handling, and rollback for harness work | [harness-task-contract.template.md](./harness-task-contract.template.md) |

## Do Not Use For

- Ordinary feature planning or task execution records; use
  [SDLC templates](../sdlc/README.md).
- Operational guide, policy, runbook, incident, or postmortem records; use
  [operations](../operations/README.md).
- Copying support rules into README files; rules live in
  [support documents](../../support/README.md).

## Target Rules

- Keep Stage 00 governance records concise and evidence-oriented.
- Do not store secrets, credentials, or unredacted sensitive values in memory or
  progress records.
- Harness task contracts must name allowed and forbidden paths before state
  changes begin.
- Broad governance changes must update validation or support documents when
  repository behavior changes.

## Related Documents

- [templates catalog](../README.md)
- [template governance](../../support/template-governance.md)
- [frontmatter contract](../../support/frontmatter-contract.md)
- [template selection](../../support/template-selection.md)
