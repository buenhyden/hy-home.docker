---
title: "07-Workflow Optimization Hardening Operations Policy"
version: "1.2.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0054"
parent_ids:
- "AD-0007"
created: "2026-05-10"
next_review_at: "2027-05-13"
---

# 07-Workflow Optimization Hardening Operations Policy

## Purpose and Scope

### Objective

이 문서는 `07-workflow` 계층의 최적화/하드닝 운영 정책을 정의한다. gateway 경계 보안, health 기반 의존성, n8n 컨테이너 하드닝, 카탈로그 기반 확장 승인 기준을 통제한다.

#### Authority

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../../02.architecture/01.descriptions/0007-workflow-architecture.md) (`AD-0007`)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

### Applies To

- `infra/07-workflow/airflow/docker-compose.yml`
- `infra/07-workflow/n8n/{docker-compose.yml,Dockerfile,dev.Dockerfile,docker-entrypoint.sh,docker-entrypoint.dev.sh}`
- `scripts/hardening/check-all-hardening.sh 07-workflow`

- **Systems**: Airflow, Flower, n8n, n8n-worker, n8n-task-runner-worker, workflow Valkey
- **Environments**: 로컬·개발·검증 및 운영 환경에 준하는 환경

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0054-R1 | Airflow 공개 라우터 | 필수: `gateway-standard-chain@file`과 native Keycloak SSO를 유지한다 | none | none |
| POL-0054-R2 | Flower 공개 라우터 | 필수: `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 유지한다 | none | none |
| POL-0054-R3 | n8n 공개 라우터 | 필수: n8n은 자체 로그인만 쓰므로 `gateway-standard-chain@file`만 유지한다 | none | none |
| POL-0054-R4 | Airflow | 금지: Airflow double-auth 추가(표준 복구가 아니다) | `check_07_workflow`가 Airflow double proxy-auth를 거부 | none |
| POL-0054-R5 | 항상 | 필수: broker는 shared `mng-valkey`뿐이다 | none | none |
| POL-0054-R6 | 항상 | 필수: 그 broker 경계를 문서와 검증 evidence에 명시한다 | 수동 | none |
| POL-0054-R7 | 항상 | 필수: n8n worker/task-runner healthcheck를 유지한다 | none | none |
| POL-0054-R8 | 항상 | 필수: n8n task-runner는 main health, task-runner-worker는 worker health 의존성을 유지한다 | none | none |
| POL-0054-R9 | 항상 | 필수: broker/DB readiness를 별도로 확인한다 | none | none |
| POL-0054-R10 | 항상 | 필수: n8n compose 기본 이미지는 custom image를 사용한다 | none | none |
| POL-0054-R11 | 항상 | 필수: n8n runtime은 non-root이다 | none | none |
| POL-0054-R12 | 항상 | 필수: n8n entrypoint secret guard를 유지한다 | none | none |
| POL-0054-R13 | workflow 변경 | 필수: `check-all-hardening.sh 07-workflow` 및 CI `infrastructure-hardening`을 통과한다 | `check-all-hardening.sh 07-workflow` / CI `infrastructure-hardening` | 정적 검사와 hardening 검사 결과 |
| POL-0054-R14 | 문서(PRD~Procedure) | 필수: optimization-hardening 링크를 유지한다 | 수동 | none |
| POL-0054-R15 | 단계적 강화 | 허용: Airflow DAG quality gate/worker autoscale 기준의 단계적 강화 | none | none |
| POL-0054-R16 | 단계적 강화 | 허용: n8n workflow Git backup/OpenBao credential 연계의 단계적 강화 | none | none |
| POL-0054-R17 | 항상 | 허용: 미구현 workflow service 문서 제거 및 archive ledger 추적 | none | none |
| POL-0054-R18 | 항상 | 금지: 무승인 middleware 완화 | none | none |
| POL-0054-R19 | 항상 | 금지: root runtime 복귀 | none | none |
| POL-0054-R20 | 항상 | 금지: 검증 게이트 우회 배포 | none | none |
| POL-0054-R21 | Airflow 카탈로그 확장 | 필수: DAG parse/schedule/delay 기준 품질 게이트를 문서화하고 CI에 반영한다 | 수동 | none |
| POL-0054-R22 | Airflow 카탈로그 확장 | 필수: worker autoscale 트리거(큐 지연, 실행 대기 수, CPU/memory) 기준을 합의한다 | 수동 | none |
| POL-0054-R23 | autoscale 전 | 필수: `airflow-worker`·`n8n-worker`의 고정 `container_name` 선언을 바꾸는 Compose 변경을 한다 | 수동 | none |
| POL-0054-R24 | n8n 카탈로그 확장 | 필수: workflow Git backup 표준 운영 절차를 수립한다 | 수동 | none |
| POL-0054-R25 | n8n 카탈로그 확장 | 필수: credential store OpenBao 연계 모델 및 롤백 절차를 문서화한다 | 수동 | none |
| POL-0054-R26 | 문자열 검사 통과 | 금지: 문자열 검사 통과로 n8n 버전·timeout·guard 결함을 닫음 | none | none |
| POL-0054-R27 | 필수 통제 | 필수: 추가 소스 검토와 승인된 런타임 근거를 갖춘다 | 수동 | none |

- **Required**:
  - Airflow 공개 라우터는 `gateway-standard-chain@file`과 native Keycloak SSO를 유지한다. Flower는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 유지하고 n8n은 자체 로그인만 쓰므로 `gateway-standard-chain@file`만 유지한다(owner 결정 2026-11-09). Airflow double-auth 추가는 표준 복구가 아니다.
  - broker는 shared `mng-valkey`뿐이다(앱별 전용 Valkey는 ADR-0062 결정 10으로 제거됨). 그 경계를 문서와 검증 evidence에 명시한다.
  - n8n worker/task-runner healthcheck를 필수로 유지한다.
  - n8n task-runner는 main health, task-runner-worker는 worker health 의존성을 유지한다. broker/DB readiness를 별도로 확인한다.
  - n8n compose 기본 이미지는 custom image([hyhome/n8n image declaration](../../../../infra/07-workflow/n8n/docker-compose.yml))를 사용한다.
  - n8n runtime은 non-root이며 entrypoint secret guard를 유지한다.
  - workflow 변경은 `check-all-hardening.sh 07-workflow` 및 CI `infrastructure-hardening`을 통과해야 한다.
  - 문서(PRD~Procedure)는 optimization-hardening 링크를 유지한다.
- **Allowed**:
  - Airflow DAG quality gate/worker autoscale 기준의 단계적 강화
  - n8n workflow Git backup/OpenBao credential 연계의 단계적 강화
  - 미구현 workflow service 문서 제거 및 archive ledger 추적
- **Disallowed**:
  - 무승인 middleware 완화
  - root runtime 복귀
  - 검증 게이트 우회 배포

#### Catalog Expansion Approval Gates

- **Airflow 승인 조건**:
  - DAG parse/schedule/delay 기준 품질 게이트 문서화 및 CI 반영
  - worker autoscale 트리거(큐 지연, 실행 대기 수, CPU/memory) 기준 합의
  - 현재 `airflow-worker`·`n8n-worker`는 고정 `container_name`이므로 autoscale 전에 이 선언을 바꾸는 Compose 변경이 필요하다.
- **n8n 승인 조건**:
  - workflow Git backup 표준 운영 절차 수립
  - credential store OpenBao 연계 모델 및 롤백 절차 문서화

#### Static gate boundary

`check_07_workflow`는 파일과 일부 인증 문자열을 확인하고 Airflow double proxy-auth를 거부한다. Runner 호환성, 선택 Dockerfile/guard, 모든 probe, DB/broker readiness와 로그인 성공까지 증명하지 않는다. 필수 통제에는 추가 소스 검토와 승인된 런타임 근거가 필요하다. 문자열 검사 통과로 n8n 버전·timeout·guard 결함을 닫지 않는다.

### Exceptions

#### Exception Conditions

- 장애 대응 시 일시적 접근제어 완화는 허용될 수 있다.
- 단, 변경 승인 기록과 동일 릴리스 내 원상 복구/재검증이 필수다.

#### Approval and Review

- 월 1회 정기 검토
- Airflow/n8n 버전 변경 또는 인증/보안 이슈 발생 시 수시 검토

## Enforcement

### Mechanisms

점검 명령은 [가이드의 Common Checks](../../01.guides/08.workflows-and-automation/0054-workflow-optimization-hardening.md#common-checks)를 따른다. 정적 검사와 hardening 검사 결과를 변경 증거로 남긴다.

### Limits

이 정책은 hardening 스크립트와 CI 게이트를 지정하지만 그 범위는 정적 검사에 한정되며, 아래 규칙에는 지정된 검사가 없거나 수동 검토에 의존한다.

- 공개 라우터(POL-0054): R1-R3에는 정책이 지정한 검사가 없다.
- broker와 의존성(POL-0054): R6은 수동 검토나 승인에 의존한다; R5, R7-R9에는 정책이 지정한 검사가 없다.
- n8n 이미지와 runtime(POL-0054): R10-R12에는 정책이 지정한 검사가 없다.
- 문서 링크(POL-0054): R14은 수동 검토나 승인에 의존한다.
- 허용 사항(POL-0054): R15-R17에는 정책이 지정한 검사가 없다.
- 금지 사항(POL-0054): R18-R20에는 정책이 지정한 검사가 없다.
- 카탈로그 확장 승인(POL-0054): R21-R25은 수동 검토나 승인에 의존한다.
- 정적 게이트 경계(POL-0054): R27은 수동 검토나 승인에 의존한다; R26에는 정책이 지정한 검사가 없다.
- `check_07_workflow`는 파일과 일부 인증 문자열만 확인하며 Airflow double proxy-auth 거부 외에 어떤 규칙을 검증하는지 정책이 지정하지 않는다.
- `check_07_workflow`는 runner 호환성, 선택 Dockerfile/guard, 모든 probe, DB/broker readiness, 로그인 성공을 증명하지 않으며 문자열 검사 통과로 n8n 버전, timeout, guard 결함을 닫지 않는다.
- 필수 통제에는 추가 소스 검토와 승인된 런타임 근거가 필요하다.
- 점검 명령은 가이드 Common Checks에 위임되어 있다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- Subject peers: [Guide](../../01.guides/08.workflows-and-automation/0054-workflow-optimization-hardening.md) (`GDE-0054`), [Runbook](../../03.runbooks/08.workflows-and-automation/0054-workflow-optimization-hardening.md) (`RUN-0054`)

- [Operations index](../../README.md)
- [Usage guide](../../01.guides/08.workflows-and-automation/0054-workflow-optimization-hardening.md)
- [Recovery runbook](../../03.runbooks/08.workflows-and-automation/0054-workflow-optimization-hardening.md)
