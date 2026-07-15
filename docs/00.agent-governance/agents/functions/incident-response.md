---
layer: agentic
artifact_type: agent-function
function_id: incident-response
scope: ops
status: active
---

# incident-response

## Preconditions

An incident boundary, authorized response owner, current runbook, and safe evidence channel must be established.

## Inputs

- Bounded incident evidence and current runbook.
- Affected services, timestamps, impact, authority, and escalation contacts.

## Procedure

1. Stabilize the evidence timeline and classify impact without copying secrets, raw auth data, or unrelated logs.
2. Execute only authorized diagnostic or recovery steps, recording command class, expected result, and observed outcome.
3. Escalate on blast-radius growth, hand off prevention work, and trigger a postmortem when the incident is stabilized.

## Outputs

- A sanitized response record with timeline, actions, decisions, outcome, and handoff.

## Gates

- Evidence is redacted and provenance-aware.
- Response actions stay within the declared escalation boundary.
- A paired postmortem is routed to
  `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md`.

## Failure Handling

Stop unsafe recovery, preserve metadata instead of prohibited payloads, and escalate immediately when authority or impact is uncertain.

## Related Documents

- [Incident responder](../agents/incident-responder.md)
- [Operations scope](../../scopes/ops.md)
- [Approval boundaries](../../rules/approval-boundaries.md)
