# 03-Security Operations

> Vault 운영 정책 문서 모음

## Overview (KR)

이 디렉터리는 `03-security` 계층의 운영 정책을 관리한다. Vault 하드닝 기준, 단계적 auto-unseal/원격 audit 도입 조건, 검증 기준을 정의한다.

## Structure

```text
03-security/
├── vault.md   # Vault Operations Policy (hardening + phase adoption)
└── README.md  # This file
```

## Available Policies

- [Vault Operations Policy](./vault.md): Required/Allowed/Disallowed, 승인 조건, 검증 기준

## Related References

- [03-security Spec](../../../03.specs/03-security/spec.md)
- [03-security Plan](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [03-security Tasks](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- [03-security Usage](./vault.md)
- [03-security Procedure](./vault.md)

---

## Overview

`docs/05.operations/03-security`는 운영 정책, 통제 기준, 검증 방법을 정의하는 operation 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 운영 정책과 controls
- 허용/금지/예외 기준
- 검증 방법과 review cadence

### Out of Scope

- 단계별 복구 절차
- 튜토리얼 문서
- incident timeline

## How to Work in This Area

1. 같은 서비스의 guide와 runbook을 확인해 정책과 실행 절차가 분리되어 있는지 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Usage

> Migrated from `docs/05.operations/03-security/README.md` during the 2026-05-10 operations taxonomy consolidation.

### 03-Security Usages

> Vault 운영/개발 가이드 모음

#### Overview (KR)

이 디렉터리는 `03-security` 계층의 Vault 사용 가이드를 제공한다. 시크릿 경로 규약, AppRole 부트스트랩, 렌더 출력 확인 절차를 중심으로 optimization/hardening 기준을 설명한다.

#### Structure

```text
03-security/
├── 01.setup.md  # 초기 셋업 절차
├── vault.md     # Vault 운영/개발 가이드(최적화/하드닝 반영)
└── README.md    # This file
```

#### Available Usages

- [Vault Usage](./vault.md): 템플릿 경로 계약, AppRole bootstrap, 렌더 검증 절차
- [Setup Usage](./01.setup.md): 보안 티어 초기 구성 절차

#### Related References

- [03-security Spec](../../../03.specs/03-security/spec.md)
- [03-security Plan](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [03-security Tasks](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- [03-security Operation](./vault.md)
- [03-security Procedure](./vault.md)

---

#### Overview

`docs/05.operations/03-security`는 사용자와 운영자가 재현 가능한 작업 방법을 이해하도록 돕는 guide 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- how-to, onboarding, troubleshooting guide
- 관련 infra/operation/runbook 링크
- 작업 전제조건과 흔한 실수

##### Out of Scope

- 운영 통제 정책 원문
- 실시간 장애 대응 절차
- secret 값 또는 credential 원문

#### How to Work in This Area

1. 관련 `infra/` 서비스 README와 같은 tier의 operation/runbook 문서를 함께 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Procedure

> Migrated from `docs/05.operations/03-security/README.md` during the 2026-05-10 operations taxonomy consolidation.

### 03-Security Procedures

> Vault 장애 대응 및 복구 실행 절차

#### Overview (KR)

이 디렉터리는 `03-security` 계층의 실행형 복구 문서를 제공한다. Vault seal/unseal, raft 상태 점검, audit 점검, agent 렌더 실패 복구 절차를 포함한다.

#### Structure

```text
03-security/
├── vault.md   # Vault recovery and maintenance runbook
└── README.md  # This file
```

#### Available Procedures

- [Vault Procedure](./vault.md): seal/unseal, raft, audit, render 복구, 안전 롤백 절차

#### Related References

- [03-security Spec](../../../03.specs/03-security/spec.md)
- [03-security Plan](../../../04.execution/plans/2026-03-28-03-security-optimization-hardening-plan.md)
- [03-security Tasks](../../../04.execution/tasks/2026-03-28-03-security-optimization-hardening-tasks.md)
- [03-security Usage](./vault.md)
- [03-security Operation](./vault.md)

---

#### Overview

`docs/05.operations/03-security`는 운영자가 즉시 실행할 수 있는 runbook 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

#### Audience

이 README의 주요 독자:

- Developers
- Operators
- Documentation Writers
- AI Agents

#### Scope

##### In Scope

- 실행 절차와 checklist
- 검증 명령과 evidence source
- rollback 또는 recovery 기준

##### Out of Scope

- 정책 결정 자체
- 학습용 튜토리얼
- postmortem 분석

#### How to Work in This Area

1. 관련 operation policy를 확인한 뒤 절차, 검증, rollback 항목을 갱신한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
