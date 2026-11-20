---
title: "Airflow Operations Policy"
version: "2.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0050"
parent_ids:
- "AD-0007"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Airflow Operations Policy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 운영 정책을 정의한다. 현재 구현은 Airflow와 `airflow-apiserver` 기반 Airflow 3 서비스 구성을 기준으로 한다.

###### Authority
<!-- core-payload-level:4 -->

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../../02.architecture/01.descriptions/0007-workflow-architecture.md) (`AD-0007`)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

##### Applies To

- Airflow 코어 컴포넌트(`airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, `flower`, `airflow-statsd-exporter`) 관리
- 메타데이터 DB 및 브로커(Valkey) 연결 정책
- DAG 배포 및 운영 환경 보안 통제

- **Systems**: Apache Airflow, CeleryExecutor
- **Environments**: 루트가 무조건 include하는 단일 compose 파일, 그 안을 가르는 `workflow`/`workflow-airflow` profile, homelab operations

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0050-R1 | 항상 | 필수: 모든 DAG는 `Idempotent`(멱등성)를 유지한다 | 수동 | none |
| POL-0050-R2 | 민감 정보 | 필수: 민감 정보는 Secret Backend(Docker Secrets/OpenBao)와 Airflow Connections로 관리한다 | none | none |
| POL-0050-R3 | 항상 | 필수: broker는 공유 `mng-valkey`뿐이며 앱별 전용 Valkey는 쓰지 않는다 | none | none |
| POL-0050-R4 | 인증 | 필수: Keycloak auth manager를 쓰고 client secret은 `airflow_keycloak_client_secret` Docker Secret 또는 `/run/openbao/airflow` 아래 OpenBao Agent 출력 파일로만 주입한다 | none | none |
| POL-0050-R5 | 인증 | 금지: client secret을 환경 변수 값으로 주입 | none | none |
| POL-0050-R6 | 이미지 빌드 | 필수: `infra/07-workflow/airflow/Dockerfile`에서 고정된 Airflow/Python constraints와 Keycloak provider 버전으로 재현 가능하게 빌드한다 | none | none |
| POL-0050-R7 | API server | 필수: temporary CA bundle과 `--proxy-headers` 실행을 유지한다 | none | none |
| POL-0050-R8 | API server | 필수: `FORWARDED_ALLOW_IPS`를 신뢰된 Traefik 주소로 제한한다 | none | none |
| POL-0050-R9 | 운영 승격 전 | 필수: `AIRFLOW__CORE__LOAD_EXAMPLES` 상태를 별도 변경/evidence로 검토한다 | 수동 | none |
| POL-0050-R10 | 워커 확장 | 허용: 검토된 Compose 변경으로만 한다 | 수동 | none |
| POL-0050-R11 | 읽기 전용 UI 접근 | 허용: native Keycloak `Viewer` 역할을 명시적으로 부여한 사용자의 접근 | none | none |
| POL-0050-R12 | 항상 | 금지: Scheduler 노드에서의 직접적인 대용량 외부 API 호출 또는 파일 입출력 | 수동 | none |
| POL-0050-R13 | 항상 | 금지: native Keycloak 인증 또는 Flower proxy SSO가 비활성화된 상태에서의 UI 노출 | none | none |
| POL-0050-R14 | 항상 | 금지: 추가 proxy SSO 강제(표준 gateway chain과 native SSO를 유지한다) | none | none |
| POL-0050-R15 | broker 이전 | 필수: broker 이전에는 drain 계획을 갖춘다 | none | none |
| POL-0050-R16 | 항상 | 필수: PostgreSQL metadata, 현재 `airflow_fernet_key`, DAG/plugin/config와 필요한 log를 한 복구 단위로 취급한다 | 수동 | none |
| POL-0050-R17 | Backup/restore/broker migration/schema upgrade 전 | 필수: schedule·producer를 멈추고 실행/대기 task를 조정한다 | none | none |
| POL-0050-R18 | 항상 | 금지: Valkey queue를 task 이력 원본으로 간주 | none | none |
| POL-0050-R19 | rehearsal | 필수: 격리 project/network와 복원 copy로 rehearsal한다 | 수동 | none |
| POL-0050-R20 | rehearsal | 금지: production volume 덮어쓰기 | 수동 | none |
| POL-0050-R21 | rehearsal | 필수: Migration level, DAG parse, 값 비노출 복호화, worker/broker health, login과 canary를 검증한다 | 수동 | none |
| POL-0050-R22 | 자원 변경 | 필수: 전후 측정을 갖춘다 | none | none |
| POL-0050-R23 | 항상 | 금지: 한도를 여유 증거로 해석 | none | none |
| POL-0050-R24 | 제거 시 | 필수: export, 복구 집합 보존, client/secret 폐기와 삭제 승인을 갖춘다 | 수동 | none |

- **Required**:
  - 모든 DAG은 `Idempotent`(멱등성)를 유지해야 함.
  - 민감 정보는 반드시 Secret Backend(Docker Secrets/OpenBao) 및 Airflow Connections를 통해 관리함.
  - broker는 공유 `mng-valkey`뿐이며 앱별 전용 Valkey는 ADR-0062 결정 10으로 제거되었다.
  - 인증 manager는 Keycloak auth manager를 사용하고, client secret은
    `airflow_keycloak_client_secret` Docker Secret 또는 `/run/openbao/airflow` 아래의
    OpenBao Agent 출력 파일(`AIRFLOW_CLIENT_SECRET_FILE`)로만 주입함. 환경 변수 값으로 넣지 않음.
  - Airflow 이미지는 `infra/07-workflow/airflow/Dockerfile`에서 고정된 Airflow/
    Python constraints와 Keycloak provider 버전으로 재현 가능하게 빌드함.
  - API server의 temporary CA bundle과 `--proxy-headers` 실행을 유지하고,
    `FORWARDED_ALLOW_IPS`는 신뢰된 Traefik 주소로 제한함.
  - 운영 승격 전 `AIRFLOW__CORE__LOAD_EXAMPLES` 상태를 별도 변경/evidence로 검토함.
- **Allowed**:
  - 워커 확장은 검토된 Compose 변경으로만 한다. 현재 `airflow-worker`는 고정 `container_name`이라 `--scale`로 replica를 늘릴 수 없다.
  - 읽기 전용 UI 접근 (native Keycloak `Viewer` 역할을 명시적으로 부여한 사용자).
- **Disallowed**:
  - Scheduler 노드에서의 직접적인 대용량 외부 API 호출 또는 파일 입출력.
  - Airflow native Keycloak 인증 또는 Flower proxy SSO가 비활성화된 상태에서의 UI 노출. Airflow에는 표준 gateway chain과 native SSO를 유지하며 추가 proxy SSO를 강제하지 않는다.

###### Lifecycle and data controls
<!-- core-payload-level:4 -->

- Airflow 코어는 HOME이고 broker는 공유 `mng-valkey`다. broker 이전에는 drain 계획이 필요하다.
- PostgreSQL metadata, 현재 `airflow_fernet_key`, DAG/plugin/config와 필요한 log는 한 복구 단위다. 같은 Fernet key 없는 DB copy로 암호화 Connections를 복구하지 못한다.
- Backup/restore/broker migration/schema upgrade 전에 schedule·producer를 멈추고 실행/대기 task를 조정한다. Valkey queue를 task 이력 원본으로 간주하지 않는다.
- 격리 project/network와 복원 copy로 rehearsal하며 production volume을 덮어쓰지 않는다. Migration level, DAG parse, 값 비노출 복호화, worker/broker health, login과 canary를 검증한다.
- 자원 변경에는 전후 측정이 필요하다. 한도는 여유 증거가 아니다. 제거에는 export, 복구 집합 보존, client/secret 폐기와 삭제 승인이 필요하다.

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

- **Emergency Hotfix**: 중대한 파이프라인 중단 시, 사후 보고를 조건으로 수동 DB 수정 또는 워커 강제 재시작 가능 (관리자 승인 필요).

###### Approval and Review
<!-- core-payload-level:4 -->

- **Quarterly**: 매 분기별 리소스 사용량 분석 및 쿼터 조정.
- **Per Release**: 새로운 Airflow 버전 또는 Provider 업데이트 시 정책 재검토.

#### Enforcement

##### Mechanisms

점검 명령은 [가이드의 Common Checks](../../01.guides/08.workflows-and-automation/0050-airflow.md#common-checks)를 따른다. 정적 검사와 hardening 검사 결과를 변경 증거로 남긴다.

- **Runtime Check**: 실행 중인 환경에서 `docker compose --profile workflow-airflow exec airflow-apiserver airflow db check`와 `docker compose --profile workflow-airflow exec airflow-apiserver airflow dags list` 결과를 확인한다.

##### Limits

이 정책은 정적 검사와 hardening 검사 결과를 변경 증거로 남기도록 하지만 각 규칙과 검사의 대응은 가이드에 위임하므로 표의 모든 규칙에 규칙별 검사가 지정되어 있지 않다.

- DAG와 Scheduler 운영(POL-0050): R1, R12은 수동 검토나 승인에 의존한다.
- 보안과 인증(POL-0050): R2, R4-R5, R11, R13-R14에는 정책이 지정한 검사가 없다.
- 구성 고정(POL-0050): R3, R6-R8에는 정책이 지정한 검사가 없다.
- 운영 승격과 확장(POL-0050): R9-R10은 수동 검토나 승인에 의존한다.
- 복구 단위와 lifecycle(POL-0050): R16, R19-R21, R24은 수동 검토나 승인에 의존한다; R15, R17-R18, R22-R23에는 정책이 지정한 검사가 없다.
- 점검 명령은 가이드의 Common Checks에 있으며 이 문서는 규칙별 검사를 지정하지 않는다.
- Runtime Check(`airflow db check`, `airflow dags list`)는 실행 중인 환경이 있을 때에 한하며 어느 규칙을 검증하는지 지정되지 않고 이 문서에 결과 증거가 없다.
- 복구 단위 보존과 rehearsal 검증은 runbook 절차에 의존한다.

#### Ownership

##### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

##### Review Triggers

- Subject peers: [Guide](../../01.guides/08.workflows-and-automation/0050-airflow.md) (`GDE-0050`), [Runbook](../../03.runbooks/08.workflows-and-automation/0050-airflow.md) (`RUN-0050`)

- [Operations index](../../README.md)
- [Usage guide](../../01.guides/08.workflows-and-automation/0050-airflow.md)
- [Recovery runbook](../../03.runbooks/08.workflows-and-automation/0050-airflow.md)

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
