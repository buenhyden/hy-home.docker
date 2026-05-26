---
title: 'Runbook Template'
status: draft
type: runbook
stage: docs/05.operations/runbooks
template: docs/99.templates/runbook.template.md
project: ''
linked_zk: []
lessons_extracted: false
---

<!-- Target: docs/05.operations/runbooks/####-<topic>.md -->

# [topic Name] Runbook

> Use this template for `docs/05.operations/runbooks/####-<topic>.md`.
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

## Autonomous SDLC Contract

| Field                 | Value                                                                                   |
| :-------------------- | :-------------------------------------------------------------------------------------- |
| Stage                 | `05.operations/runbooks`                                                                |
| Methodology Alignment | SDD executable procedure, operations readiness                                          |
| Upstream              | Operation, Spec, ADR, ARD                                                               |
| Downstream            | Incident response, postmortem action items, operational evidence                        |
| Stage Exit Gate       | Trigger, procedure, verification, evidence capture, and rollback/recovery are explicit. |

## Purpose

[What operational problem this runbook addresses.]

## Canonical References

> Replace each placeholder with a real target-relative link from the generated runbook.
> If no real upstream exists, write `N/A - no upstream source`.
> If a required upstream is missing, write `Blocked - real upstream required`.

- **ARD**: Real target-relative ARD link, or `N/A - no upstream source`
- **ADR**: Real target-relative ADR link, or `N/A - no upstream source`
- **Spec**: Real target-relative spec link, or `N/A - no upstream source`
- **Plan**: Real target-relative plan link, or `N/A - no upstream source`

## When to Use

- [Use case 1]
- [Use case 2]

## Procedure

### Checklist

- [ ] [Check 1]
- [ ] [Check 2]

### Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Verification

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

## Related Documents

> Replace generated examples with real target-relative links, or use `N/A - no upstream source`.

- **Operation**: Real target-relative operation policy link, or `N/A - no upstream source`
- **Incident examples**: Real target-relative incident link, or `N/A - no upstream source`
- **Postmortem examples**: Real target-relative postmortem link, or `N/A - no upstream source`

## SDLC/PARA Boundary & ZK Extraction

> [!NOTE]
> AI Agent는 SDLC 문서를 작성/수정할 때 `30_PARA/31_Projects/`를 필수 소유자, 링크 대상, 증적 저장소로 사용하지 않는다.
> `30_PARA/31_Projects/`는 사용자의 개인/업무 프로젝트를 관리하는 별도 Vault 영역이다.
> 작성 중 발견한 독립적인 지식, 패턴, 의사결정 기준만 `20_ZK/22_Permanent/` 또는 `20_ZK/23_Maps/`로 추출한다.

- **Extracted ZK Notes**:
  - `[Link to 20_ZK/...]`
