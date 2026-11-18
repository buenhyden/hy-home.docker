---
name: "incident-response"
description: "Use when an authorized incident owner needs a sanitized response timeline, bounded recovery actions, escalation, and postmortem handoff."
metadata:
  title: "incident-response"
  version: "1.5.1"
  type: "governance/skill"
  status: "active"
  owner: "@buenhyden"
  updated: "2026-11-18"
  function_id: "incident-response"
  scope: "ops"
  owner_agent: "incident-responder"
---

# incident-response

## Trigger

### When to Use

Explicit invocation only, under the
[agent execution rules](../../governance/agentic.md#execution-rules).

An incident boundary, authorized response owner, current runbook, and safe evidence channel must be established.

### When Not to Use

None: this skill states no exclusion.

## Procedure

### Steps

1. Stabilize the evidence timeline and classify impact without copying secrets, raw auth data, or unrelated logs.
2. When stateful recovery is proposed, hand the sanitized contract to [stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md) and keep its verdict separate from recovery authorization.
3. Execute only authorized diagnostic or recovery steps, recording command class, expected result, and observed outcome.
4. Escalate on blast-radius growth, hand off prevention work, and trigger a postmortem when the incident is stabilized.

#### Gates

- Evidence is redacted and provenance-aware.
- Response actions stay within the declared escalation boundary.
- Stateful recovery has an independent readiness verdict and separate human approval before execution.
- A cited preserved body is dated and named as preserved evidence, never as
  current state; the exception permits the citation, not the inference.
- A paired postmortem is routed to
  `docs/05.operations/incidents/<year>/inc-####-<slug>/postmortem.md`.

#### Inputs

- Bounded incident evidence and current runbook.
- Affected services, timestamps, impact, authority, and escalation contacts.
- Earlier evidence when reconstruction needs it, read from version history at
  the revision that last carried it; Stage 98 holds no records. The
  [documentation protocol](../../../docs/00.workspace/02.process/documentation-protocol.md#document-retention-and-retirement)
  owns that rule.

### Failure Handling

Stop unsafe recovery, preserve metadata instead of prohibited payloads, and escalate immediately when authority or impact is uncertain. A readiness verdict never proves recovery success.

## Outputs

### Artifacts

- A sanitized response record with timeline, actions, decisions, outcome, and handoff.

### Handoff

Owning role, policies and related documents:

- [Incident responder](../../roles/incident-responder.md)
- [Operations scope](../../../docs/00.workspace/03.quality/quality-standards.md)
- [Approval boundaries](../../../docs/00.workspace/02.process/approval-boundaries.md)
- [Stateful recovery contract review](../stateful-recovery-contract-review/SKILL.md)

## Verification

### Checks

- The response record has a timeline, actions, decisions, outcome, and handoff, and holds no secret or raw auth data.
- Every executed step is inside the declared escalation boundary and records its expected and observed result.
- A stateful recovery carries the independent readiness verdict and a separate human approval before it runs.

### Limits

A readiness verdict never proves recovery success.
