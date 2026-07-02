---
layer: agentic
---

# SDLC Templates

> requirements, architecture, specification, planning, and task-evidence templates

## Overview

`docs/99.templates/templates/sdlc` contains copyable templates for the
repository SDLC path from product intent to implementation evidence. Use these
templates when the target document belongs to Stage 01 through Stage 04 and
must preserve traceability across requirements, architecture, specs, plans, and
tasks.

## Use When

| Need | Template |
| --- | --- |
| Capture product need, users, requirements, and success criteria | [prd.template.md](./prd.template.md) |
| Describe system or domain architecture and quality attributes | [ard.template.md](./ard.template.md) |
| Record an architectural decision and its consequences | [adr.template.md](./adr.template.md) |
| Define the technical design for a feature or workspace change | [spec.template.md](./spec.template.md) |
| Plan an approved implementation stream | [plan.template.md](./plan.template.md) |
| Track task execution, evidence, validation, and gaps | [task.template.md](./task.template.md) |

## Do Not Use For

- API, data, agent, service, or machine-readable contracts inside a feature
  spec; use [spec-contracts](../spec-contracts/README.md).
- Operational procedures, policies, incidents, or postmortems; use
  [operations](../operations/README.md).
- Stage 00 memory, progress, or harness task contract surfaces; use
  [governance](../governance/README.md).

## Target Rules

- Use one primary SDLC template per target document.
- Keep target paths aligned with
  [template selection](../../support/template-selection.md).
- Replace template placeholders and examples with topic-specific content before
  saving the target document.
- Target document frontmatter follows
  [frontmatter contract](../../support/frontmatter-contract.md), not template
  source frontmatter.

## Related Documents

- [templates catalog](../README.md)
- [template contract](../../support/template-contract.md)
- [template governance](../../support/template-governance.md)
- [lifecycle status](../../support/lifecycle-status.md)
