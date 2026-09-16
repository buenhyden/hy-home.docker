---
name: "incident-response"
description: "Use when an authorized incident owner needs a sanitized response timeline, bounded recovery actions, escalation, and postmortem handoff."
metadata:
  title: "incident-response"
  version: "1.2.3"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-16"
  function_id: "incident-response"
  scope: "ops"
  owner_agent: "incident-responder"
---

# incident-response

## Preconditions

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An incident boundary, authorized response owner, current runbook, and safe evidence channel must be established.

## Inputs

- Bounded incident evidence and current runbook.
- Affected services, timestamps, impact, authority, and escalation contacts.
- Preserved evidence when reconstruction needs it. Incident and postmortem
  records are the only profiles that may cite any archive path directly, because the
  evidence such an account rests on is often the archived record itself. Other
  documents cite only the Stage 98 index, `completed/`, and `resolved/`. A route
  record holds no body, so `tombstones/` and `migrations/` are closed to an
  incident and a postmortem as well. The
  [documentation protocol](../../governance/documentation-protocol.md#links-into-stage-98)
  owns that rule.

## Procedure

1. Stabilize the evidence timeline and classify impact without copying secrets, raw auth data, or unrelated logs.
2. Execute only authorized diagnostic or recovery steps, recording command class, expected result, and observed outcome.
3. Escalate on blast-radius growth, hand off prevention work, and trigger a postmortem when the incident is stabilized.

## Outputs

- A sanitized response record with timeline, actions, decisions, outcome, and handoff.

## Gates

- Evidence is redacted and provenance-aware.
- Response actions stay within the declared escalation boundary.
- A cited preserved body is dated and named as preserved evidence, never as
  current state; the exception permits the citation, not the inference.
- A paired postmortem is routed to
  `docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md`.

## Failure Handling

Stop unsafe recovery, preserve metadata instead of prohibited payloads, and escalate immediately when authority or impact is uncertain.

## Related Documents

- [Incident responder](../../roles/incident-responder.md)
- [Operations scope](../../governance/quality-standards.md)
- [Approval boundaries](../../governance/approval-boundaries.md)
