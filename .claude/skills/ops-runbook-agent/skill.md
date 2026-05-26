---
name: ops-runbook-agent
description: >
  Author and maintain Stage 05 runbook documents in docs/05.operations/runbooks/.
  Runbooks define ordered procedures, expected output, failure-stop criteria,
  rollback steps, and escalation paths for hy-home.docker services.
---

# ops-runbook-agent

Creates and updates operational runbooks in `docs/05.operations/runbooks/`.

## Trigger Examples

- "Write a runbook for rotating Vault secrets"
- "Create a recovery runbook for the PostgreSQL tier"
- "Update the Traefik TLS rotation runbook with new cert paths"

## Purpose

Produce runbook documents that an operator can follow step-by-step during
incidents or routine operations. Runbooks must include expected output per
step and explicit stop criteria for failures.

## Bootstrap

1. Read `AGENTS.md` and `docs/05.operations/README.md`.
2. Read `docs/99.templates/operation.template.md` for the operations template.
3. Check `docs/05.operations/runbooks/` for any existing runbook on the topic.
4. Read the relevant spec at `docs/03.specs/<tier>/spec.md` for service context.

## Working Rules

- Runbook filename: `docs/05.operations/runbooks/<tier>/<topic>.md`.
- Required sections: When to Use, Procedure, Evidence, Rollback or Recovery, Escalation.
- Every procedure step must include: command, expected output, failure action.
- Never include secret values, tokens, or credential content.
- Link to the related spec, guide, and policy documents in Related Documents.
- Update `docs/05.operations/runbooks/README.md` after adding a new runbook.

## Inputs

| Input | Source |
| ----- | ------ |
| Service spec | `docs/03.specs/<tier>/spec.md` |
| Operations template | `docs/99.templates/operation.template.md` |
| Existing runbooks | `docs/05.operations/runbooks/<tier>/` |

## Outputs

- New or updated runbook at `docs/05.operations/runbooks/<tier>/<topic>.md`
- Updated `docs/05.operations/runbooks/README.md` index entry

## Related Skills

- `task-breakdown-agent` — task evidence that may graduate to runbook
- `incident-response` — incident response workflow
