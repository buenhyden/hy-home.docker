---
title: "Airflow Operations Policy"
version: "1.1.4"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0050"
parent_ids:
- "AD-0007"
created: "2026-05-17"
---

# Airflow Operations Policy

## Overview

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 운영 정책을 정의한다. 현재 구현은 Airflow와 `airflow-apiserver` 기반 Airflow 3 서비스 구성을 기준으로 한다.

## Scope

- Airflow 코어 컴포넌트(`airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `flower`) 관리
- 메타데이터 DB 및 브로커(Valkey) 연결 정책
- DAG 배포 및 운영 환경 보안 통제

- **Systems**: Apache Airflow, CeleryExecutor
- **Environments**: 루트가 무조건 include하는 단일 compose 파일, 그 안을 가르는 `workflow`/`dev`/`dedicated-valkey` profile, homelab operations

## Rules

- **Required**:
  - 모든 DAG은 `Idempotent`(멱등성)를 유지해야 함.
  - 민감 정보는 반드시 Secret Backend(Docker Secrets/OpenBao) 및 Airflow Connections를 통해 관리함.
  - `dedicated-valkey` profile 선택 여부가 만드는 broker 차이(`mng-valkey` vs `airflow-valkey`)를 변경 문서에 명시함.
  - 인증 manager는 Keycloak auth manager를 사용하고, client secret은
    `airflow_keycloak_client_secret` Docker Secret으로만 주입함.
  - Airflow 이미지는 `infra/07-workflow/airflow/Dockerfile`에서 고정된 Airflow/
    Python constraints와 Keycloak provider 버전으로 재현 가능하게 빌드함.
  - API server의 temporary CA bundle과 `--proxy-headers` 실행을 유지하고,
    `FORWARDED_ALLOW_IPS`는 신뢰된 Traefik 주소로 제한함.
  - 운영 승격 전 `AIRFLOW__CORE__LOAD_EXAMPLES` 상태를 별도 변경/evidence로 검토함.
- **Allowed**:
  - 워커 노드의 동적 확장 (부하에 따른 Replica 조정).
  - 읽기 전용 UI 접근 (native Keycloak `Viewer` 역할을 명시적으로 부여한 사용자).
- **Disallowed**:
  - Scheduler 노드에서의 직접적인 대용량 외부 API 호출 또는 파일 입출력.
  - Airflow native Keycloak 인증 또는 Flower proxy SSO가 비활성화된 상태에서의 UI 노출. Airflow에는 표준 gateway chain과 native SSO를 유지하며 추가 proxy SSO를 강제하지 않는다.

### Lifecycle and data controls

- Airflow 코어는 HOME, 전용 broker pair는 OPTIONAL을 유지한다. `dedicated-valkey`만으로 broker 전환이 승인·수행되지 않으며 matching host/secret과 drain 계획이 필요하다.
- PostgreSQL metadata, 현재 `airflow_fernet_key`, DAG/plugin/config와 필요한 log는 한 복구 단위다. 같은 Fernet key 없는 DB copy로 암호화 Connections를 복구하지 못한다.
- Backup/restore/broker migration/schema upgrade 전에 schedule·producer를 멈추고 실행/대기 task를 조정한다. Valkey queue를 task 이력 원본으로 간주하지 않는다.
- 격리 project/network와 복원 copy로 rehearsal하며 production volume을 덮어쓰지 않는다. Migration level, DAG parse, 값 비노출 복호화, worker/broker health, login과 canary를 검증한다.
- 자원 변경에는 전후 측정이 필요하다. 한도는 여유 증거가 아니다. 제거에는 export, 복구 집합 보존, client/secret 폐기와 삭제 승인이 필요하다.

## Exceptions

- **Emergency Hotfix**: 중대한 파이프라인 중단 시, 사후 보고를 조건으로 수동 DB 수정 또는 워커 강제 재시작 가능 (관리자 승인 필요).

### Verification

점검 명령은 [가이드의 Common Checks](../guides/0050-airflow.md#common-checks)를 따른다. 정적 검사와 hardening 검사 결과를 변경 증거로 남긴다.

- **Runtime Check**: 실행 중인 환경에서 `docker compose exec airflow-apiserver airflow db check`와 `docker compose exec airflow-apiserver airflow dags list` 결과를 확인한다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- **Quarterly**: 매 분기별 리소스 사용량 분석 및 쿼터 조정.
- **Per Release**: 새로운 Airflow 버전 또는 Provider 업데이트 시 정책 재검토.

### Traceability

- Declared parent: [Workflow Tier (07-workflow) Architecture Description](../../02.architecture/descriptions/0007-workflow-architecture.md) (`AD-0007`)
- Subject peers: [Guide](../guides/0050-airflow.md) (`GDE-0050`), [Runbook](../runbooks/0050-airflow.md) (`RUN-0050`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0050-airflow.md)
- [Recovery runbook](../runbooks/0050-airflow.md)
