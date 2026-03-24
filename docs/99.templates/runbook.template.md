<!-- Target: docs/09.runbooks/####-<topic>.md -->

# [topic Name] Runbook

: [Service or Workflow Name]

> Use this template for `docs/09.runbooks/####-<topic>.md`.
>
> Rules:
>
> - This document exists for immediate execution.
> - This document is not a policy definition.
> - This document is not a tutorial-first guide.
> - If the main purpose is analysis after the event, write a Postmortem instead.

---

## Overview (KR)

이 런북은 [서비스 또는 워크플로명]에 대한 실행 절차를 정의한다. 운영자가 즉시 따라 할 수 있는 단계와 검증 기준을 제공한다.

## Purpose

[What operational problem this runbook addresses.]

## Canonical References

- `[../02.ard/####-<system-or-domain>.md]`
- `[../03.adr/####-<short-title>.md]`
- `[../04.specs/<feature-id>/spec.md]`
- `[../05.plans/YYYY-MM-DD-<feature>.md]`

## When to Use

- [Use case 1]
- [Use case 2]

## Procedure or Checklist

### Checklist

- [ ] [Check 1]
- [ ] [Check 2]

### Procedure

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Verification Steps

- [ ] [Verification command or manual check]

## Observability and Evidence Sources

- **Signals**:
- **Evidence to Capture**:

## Safe Rollback or Recovery Procedure

- [ ] [Recovery step 1]
- [ ] [Recovery step 2]

## Agent Operations (If Applicable)

- **Prompt Rollback**:
- **Model Fallback**:
- **Tool Disable / Revoke**:
- **Eval Re-run**:
- **Trace Capture**:

## Related Operational Documents

- **Incident examples**: `[../10.incidents/YYYY/YYYY-MM-DD-<incident-title>.md]`
- **Postmortem examples**: `[../11.postmortems/YYYY/YYYY-MM-DD-<incident-title>.md]`
