---
layer: agentic
---

# Operations Templates

> guide, policy, runbook, incident, postmortem, and release templates

## Overview

`docs/99.templates/templates/operations` contains copyable templates for Stage
05 operational documentation. Use these templates when a document explains how
to operate, govern, respond to, or learn from a workspace service or process.

## Templates

| Need | Template |
| --- | --- |
| Explain usage context, common checks, and runbook handoff | [guide.template.md](./guide.template.md) |
| Define controls, exceptions, verification, and review cadence | [policy.template.md](./policy.template.md) |
| Provide ordered execution steps, evidence, recovery, and escalation | [runbook.template.md](./runbook.template.md) |
| Record an active or resolved incident timeline and response state | [incident.template.md](./incident.template.md) |
| Analyze incident impact, root cause, action items, and prevention | [postmortem.template.md](./postmortem.template.md) |
| Record verified artifacts, approvals, rollout, rollback, and outcome for a real release event | [release.template.md](./release.template.md) |

## Target Rules

- `guide.template.md` targets `docs/05.operations/guides/<tier>/<topic>.md`.
- `policy.template.md` targets `docs/05.operations/policies/<tier>/<topic>.md`.
- `runbook.template.md` targets `docs/05.operations/runbooks/<tier>/<topic>.md`.
- `incident.template.md` targets
  `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/INC-###-<incident-title>.md`.
- `postmortem.template.md` targets
  `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md`.
- `release.template.md` targets
  `docs/05.operations/releases/YYYY-MM-DD-release-name.md` and requires real
  release-event evidence; it does not authorize deployment runtime changes.
- Calculate target-relative links from the copied document path.

## Related Documents

- [templates catalog](../README.md)
- [template selection](../../support/template-selection.md)
- [template contract](../../support/template-contract.md)
- [template governance](../../support/template-governance.md)
