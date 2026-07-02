---
status: draft
---
<!-- Target: docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md -->

# Postmortem: [Incident Title]

> Use this template for `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md`.
>
> Target Contract:
>
> - Each incident owns one packet folder: `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/`.
> - The paired incident facts file is `INC-###-<incident-title>.md` inside that packet folder.
> - This postmortem analysis file is always named `postmortem.md` inside the same packet folder.
> - `YYYY` comes from the incident detection date, not the analysis date.
> - Use the same `Incident ID`, severity, and primary service metadata as the paired incident record.
>
> Rules:
>
> - Analyze systemic causes without blaming individuals.
> - Link the paired Incident document in the same incident packet folder.
> - Create postmortems for every SEV1/SEV2 incident; create SEV3 postmortems when recurrence, security exposure, or learning value warrants it.
> - Convert prevention work into follow-up tasks with owners and verification.
> - Do not include secret values, credentials, private keys, raw logs, or shell history.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
>
> Target-relative examples from `docs/05.operations/incidents/YYYY/INC-###-<incident-title>/postmortem.md`:
>
> - Incident document: `./INC-###-incident-title.md`
> - Direct runbook: `../../../runbooks/topic.md`
> - Domain policy: `../../../policies/domain/policy-or-standard.md`
> - Follow-up task: `../../../../04.execution/tasks/YYYY-MM-DD-topic.md`

---

## Overview

이 문서는 사고의 구조적 원인과 재발 방지 조치를 분석하는 Postmortem 문서다. 비난 없는 분석과 시스템 개선에 집중한다.

## Incident Summary

| Field | Value |
| --- | --- |
| Incident ID | `INC-###-<incident-title>` |
| Incident Date | `YYYY-MM-DD` |
| Analysis Date | `YYYY-MM-DD` |
| Severity | `SEV-1 / SEV-2 / SEV-3` |
| Incident Document | [INC-###-<incident-title>.md](./INC-###-<incident-title>.md) |

## Agent Metadata (If Applicable)

- **Model Version**:
- **Prompt Version**:
- **Tool Set / Config**:
- **Guardrail State**:
- **Trace IDs**:
- **Eval Run IDs**:

## Impact

- **Affected Users or Systems**:
- **Operational Impact**:
- **Business / Maintenance Impact**:

## Timeline

| Time (UTC) | Event |
| --- | --- |
| HH:MM | [Detection / investigation / mitigation / resolved] |

## Root Cause Analysis

### Primary Root Cause

[Systemic cause.]

### Contributing Factors

- [Factor 1]
- [Factor 2]

### Detection Gaps

- [Gap 1]
- [Gap 2]

## What Went Well

- [Point 1]

## What Went Wrong

- [Point 1]

## Action Items

| Action | Owner | Priority | Ticket / Reference | Status |
| --- | --- | --- | --- | --- |
| [Action item] | [Name] | High | [Link] | Pending |

## Prevention and Verification

- [Prevention work]
- [Verification rule]

## Required Documentation Feedback Loop

- **ADR updates**:
- **Spec updates**:
- **Operation updates**:
- **Runbook updates**:
- **Guardrail / Eval updates**:

## Related Documents

- **Runbook, direct target**: [../../../runbooks/<topic>.md](../../../runbooks/<topic>.md)
- **Runbook, domain target**: [../../../runbooks/<domain>/<topic>.md](../../../runbooks/<domain>/<topic>.md)
- **Runbook, nested target**: [../../../runbooks/<domain>/<subdomain>/<topic>.md](../../../runbooks/<domain>/<subdomain>/<topic>.md)
- **Operation Policy, domain target**: [../../../policies/<domain>/<policy-or-standard>.md](../../../policies/<domain>/<policy-or-standard>.md)
- **Incident**: [INC-###-<incident-title>.md](./INC-###-<incident-title>.md)
- **Follow-up Task**: [../../../../04.execution/tasks/YYYY-MM-DD-<topic>.md](../../../../04.execution/tasks/YYYY-MM-DD-<topic>.md)
