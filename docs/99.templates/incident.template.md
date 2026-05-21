---
status: draft
---
<!-- Target: docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md -->

# Incident: [Incident Title]

INC-YYYYMMDD-XXX / [Short Incident Title]

> Use this template for `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`.
>
> Rules:
>
> - Record facts, status, and response state.
> - Separate confirmed facts from current hypotheses.
> - Keep final root cause analysis in a paired Postmortem under `docs/05.operations/incidents/`.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.
>
> Target-relative examples from `docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md`:
>
> - Same-incident postmortem: `./YYYY-MM-DD-incident-title-postmortem.md`
> - Direct runbook: `../../runbooks/topic.md`
> - Domain runbook: `../../runbooks/domain/topic.md`
> - Nested runbook: `../../runbooks/domain/subdomain/topic.md`
> - Follow-up task: `../../../04.execution/tasks/YYYY-MM-DD-topic.md`

---

## Overview (KR)

이 문서는 사고의 영향, 현재 상태, 주요 대응 흐름을 기록하는 Incident 문서다. 사실 기록과 대응 로그에 집중한다.

## Incident Metadata

| Field | Value |
| --- | --- |
| Incident ID | `INC-YYYYMMDD-XXX` |
| Severity | `SEV-1 / SEV-2 / SEV-3` |
| Status | `Investigating / Identified / Mitigating / Monitoring / Resolved / Closed` |
| Detection Time | `YYYY-MM-DD HH:MM UTC` |
| Primary Service | [Affected service] |
| Evidence Source | [Log / dashboard / report] |
| Runbook Link | [../../runbooks/<topic>.md](../../runbooks/<topic>.md) |

## Agent Metadata (If Applicable)

- **Model Version**:
- **Prompt Version**:
- **Tool Set / Config**:
- **Guardrail State**:
- **Trace IDs**:
- **Eval Run IDs**:

## Incident Summary

[Short summary.]

## Impact

- [Impact 1]
- [Impact 2]

## Timeline

| Time (UTC) | Actor | Detail |
| --- | --- | --- |
| HH:MM | [Name] | [What happened] |

## Current Hypothesis / Response State

- **Current Hypothesis**:
- **Mitigation Actions**:
- **Resolution State**:

## Evidence

- [Evidence 1]
- [Evidence 2]

## Follow-up Actions

- [ ] [Action] — Owner: [Name]

## Postmortem Link

- [YYYY-MM-DD-<incident-title>-postmortem.md](./YYYY-MM-DD-<incident-title>-postmortem.md)

## Related Documents

- **Runbook, direct target**: [../../runbooks/<topic>.md](../../runbooks/<topic>.md)
- **Runbook, domain target**: [../../runbooks/<domain>/<topic>.md](../../runbooks/<domain>/<topic>.md)
- **Runbook, nested target**: [../../runbooks/<domain>/<subdomain>/<topic>.md](../../runbooks/<domain>/<subdomain>/<topic>.md)
- **Operations Guide, domain target**: [../../guides/<domain>/<topic>.md](../../guides/<domain>/<topic>.md)
- **Operations Policy, domain target**: [../../policies/<domain>/<topic>.md](../../policies/<domain>/<topic>.md)
- **Follow-up Task**: [../../../04.execution/tasks/YYYY-MM-DD-<topic>.md](../../../04.execution/tasks/YYYY-MM-DD-<topic>.md)
