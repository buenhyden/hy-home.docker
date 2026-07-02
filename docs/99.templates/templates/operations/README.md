---
layer: agentic
---

# Operations Templates

> guide, policy, runbook, incident, and postmortem templates

## Overview

`docs/99.templates/templates/operations` contains copyable templates for Stage
05 operational documentation. Use these templates when a document explains how
to operate, govern, respond to, or learn from a workspace service or process.

## Use When

| Need | Template |
| --- | --- |
| Explain usage context, common checks, and runbook handoff | [guide.template.md](./guide.template.md) |
| Define controls, exceptions, verification, and review cadence | [policy.template.md](./policy.template.md) |
| Provide ordered execution steps, evidence, recovery, and escalation | [runbook.template.md](./runbook.template.md) |
| Record an active or resolved incident timeline and response state | [incident.template.md](./incident.template.md) |
| Analyze incident impact, root cause, action items, and prevention | [postmortem.template.md](./postmortem.template.md) |

## Do Not Use For

- Product, architecture, spec, plan, or task records; use
  [SDLC templates](../sdlc/README.md).
- Stable external facts or research notes; use
  [common/reference.template.md](../common/reference.template.md).
- Harness approval contracts; use
  [governance/harness-task-contract.template.md](../governance/harness-task-contract.template.md).

## Target Rules

- Guides provide context and handoff; they are not ordered emergency procedures.
- Policies define controls and exceptions; they are not runbooks.
- Runbooks provide executable procedures and evidence; they are not tutorials.
- Incidents record event state; postmortems record analysis and follow-up.
- Preserve command names, service names, profiles, secret IDs, and evidence
  labels exactly when copying from verified sources.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [template governance](../../support/template-governance.md)
