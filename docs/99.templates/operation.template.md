---
status: draft
---
<!-- Target: docs/05.operations/{guides,policies,runbooks}/<topic>.md -->
<!-- Target variant: docs/05.operations/{guides,policies,runbooks}/<domain>/<topic>.md -->

# [Topic Name] Operations

> Use this template for `docs/05.operations/guides/<topic>.md`, `docs/05.operations/policies/<topic>.md`, or `docs/05.operations/runbooks/<topic>.md`.
>
> Rules:
>
> - Pick one operational purpose per document: guide, policy, or runbook.
> - Use `guides/` for usage, `policies/` for controls, and `runbooks/` for repeatable procedures.
> - This document is not an incident timeline or a postmortem.
> - Relative links must be calculated from the copied target path, not from `docs/99.templates/`.
> - For `docs/05.operations/<bucket>/<topic>.md`, use `../../` to reach `docs/`.
> - For `docs/05.operations/<bucket>/<domain>/<topic>.md`, use `../../../` to reach `docs/`.

---

## Overview (KR)

이 문서는 [주제명] 운영 지식을 정의한다. 대상 하위 폴더에 맞춰 사용 맥락, 통제 기준, 실행 절차 중 필요한 내용을 규정한다.

## Policy Scope

[What this policy governs.]

## Applies To

- **Systems**:
- **Agents**:
- **Environments**:

## Usage

- [When to use this system or procedure]
- [Required context before operation]

## Controls

- **Required**:
- **Allowed**:
- **Disallowed**:

## Procedure

1. [Step]
2. [Expected result]
3. [Failure handling]

## Exceptions

- [Exception rule and approval path]

## Verification

- [How compliance is checked]

## Review Cadence

- [Monthly / Quarterly / Per release]

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**:
- **Eval / Guardrail Threshold**:
- **Log / Trace Retention**:
- **Safety Incident Thresholds**:

## Related Documents

Choose the link depth that matches the copied target path, then remove the unused examples.

### Direct target: `docs/05.operations/<bucket>/<topic>.md`

- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Guide**: `[../guides/<topic>.md]`
- **Policy**: `[../policies/<topic>.md]`
- **Runbook**: `[../runbooks/<topic>.md]`
- **Postmortem**: `[../incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md]`

### Domain target: `docs/05.operations/<bucket>/<domain>/<topic>.md`

- **ARD**: `[../../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Guide**: `[../../guides/<domain>/<topic>.md]`
- **Policy**: `[../../policies/<domain>/<topic>.md]`
- **Runbook**: `[../../runbooks/<domain>/<topic>.md]`
- **Postmortem**: `[../../incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md]`
