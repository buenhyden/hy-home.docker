---
status: active
---

<!-- README Target: docs/05.operations/releases/README.md -->

# Releases

> 실제로 수행된 release event의 artifact, 검증, 승인, rollout/rollback, 결과를 기록하는 Stage 05 index

## Overview

`docs/05.operations/releases/`는 실행된 release event의 증거를 한 건당 하나의
`YYYY-MM-DD-release-name.md` 문서로 보존합니다. changelog/release-readiness evidence는
release 입력이나 준비 상태를 설명할 수 있지만, 그 자체로 executed release record가
아닙니다.

Deployment target, promotion, CD behavior, runtime rollback의 소유권은
[Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
또는 이후 승인된 runtime chain에 남습니다. 이 index나 release record는 deployment
runtime 실행 권한을 부여하지 않습니다.

## Audience

- Release Owners
- Operators and SREs
- Approvers and Auditors
- AI Agents

## Scope

### In Scope

- 실제 release identity, version, 범위, 시각
- 포함된 변경과 immutable artifact 식별자
- validation과 approval evidence
- 실제 rollout, rollback, 결과, 알려진 문제
- 후속 Task, Incident, Runbook 링크

### Out of Scope

- changelog 또는 release-readiness evidence만으로 만든 실행 기록
- deployment target, promotion, CD workflow, runtime rollback 정책의 정의
- secret 값, credential, token, private key, raw log, shell history
- 실행되지 않은 가상 release leaf

## Structure

```text
releases/
├── README.md                         # This index
└── YYYY-MM-DD-release-name.md        # Real release event record only
```

현재 이 task는 Release contract와 routing만 추가하며 release event leaf를 만들지
않습니다.

## How to Work in This Area

1. 실제 event의 artifact, validation, approval, rollout 또는 rollback, outcome 증거가 있는지 확인합니다.
2. [Release template](../../99.templates/templates/operations/release.template.md)을 복사해 `YYYY-MM-DD-release-name.md`로 작성합니다.
3. `artifact_type: release`를 유지하고 Spec, Plan, Task 중 직접 parent를 `parent_ids`에 기록합니다.
4. 확인되지 않은 실행, 결과, 승인, artifact를 추정하지 않습니다.
5. deployment runtime 변경은 Spec 127 또는 이후 승인된 runtime chain과 별도 task evidence를 따릅니다.

## Related Documents

- [Operations index](../README.md)
- [Release template](../../99.templates/templates/operations/release.template.md)
- [Template selection](../../99.templates/support/template-selection.md)
- [Stage authoring matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- [Spec 127](../../03.specs/127-deployment-release-engineering-remediation/spec.md)
