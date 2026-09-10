---
name: "incident-response"
description: "Use when an authorized incident owner needs a sanitized response timeline, bounded recovery actions, escalation, and postmortem handoff."
metadata:
  title: "incident-response"
  version: "1.2.0"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-09-10"
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
- Preserved evidence when reconstruction needs it. Outside Stage 98 only
  `docs/98.archive/completed/` may be cited, and an incident or postmortem record
  is the one profile the archive boundary excepts, because reconstructing what
  happened is exactly when a preserved body is the correct citation. The archive
  boundary (`docs/98.archive/README.md`) owns that rule and its limits.

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
