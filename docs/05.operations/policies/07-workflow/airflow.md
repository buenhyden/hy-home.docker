---
status: active
---
<!-- Target: docs/05.operations/policies/07-workflow/airflow.md -->

# Airflow Operations Policy

## Overview

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 운영 정책을 정의한다. 현재 구현은 Airflow 3.2.2와 `airflow-apiserver` 기반 Airflow 3 서비스 구성을 기준으로 한다.

## Policy Scope

- Airflow 코어 컴포넌트(`airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `flower`) 관리
- 메타데이터 DB 및 브로커(Valkey) 연결 정책
- DAG 배포 및 운영 환경 보안 통제

- **Systems**: Apache Airflow 3.2.2, CeleryExecutor
- **Agents**: CI/CD 배포 에이전트, 모니터링 에이전트
- **Environments**: root-included local/dev compose, service-local production-like compose, homelab operations

## Controls

- **Required**:
  - 모든 DAG은 `Idempotent`(멱등성)를 유지해야 함.
  - 민감 정보는 반드시 Secret Backend(Docker Secrets/Vault) 및 Airflow Connections를 통해 관리함.
  - root-included dev compose와 service-local compose의 broker 차이(`mng-valkey` vs `airflow-valkey`)를 변경 문서에 명시함.
  - 운영 승격 전 `AIRFLOW__CORE__LOAD_EXAMPLES` 상태를 별도 변경/evidence로 검토함.
- **Allowed**:
  - 워커 노드의 동적 확장 (부하에 따른 Replica 조정).
  - 읽기 전용 UI 접근 (GUEST 권한).
- **Disallowed**:
  - Scheduler 노드에서의 직접적인 대용량 외부 API 호출 또는 파일 입출력.
  - 사용자 인증(FAB) 또는 gateway SSO가 비활성화된 상태에서의 UI 노출.

## Exceptions

- **Emergency Hotfix**: 중대한 파이프라인 중단 시, 사후 보고를 조건으로 수동 DB 수정 또는 워커 강제 재시작 가능 (관리자 승인 필요).

## Verification

- **Static Check**: `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- **Hardening Check**: `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- **Runtime Check**: 실행 중인 환경에서 `docker compose exec airflow-apiserver airflow db check`와 `docker compose exec airflow-apiserver airflow dags list` 결과를 확인한다.

## Review Cadence

- **Quarterly**: 매 분기별 리소스 사용량 분석 및 쿼터 조정.
- **Per Release**: 새로운 Airflow 버전 또는 Provider 업데이트 시 정책 재검토.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-workflow/airflow.md)
- [Recovery runbook](../../runbooks/07-workflow/airflow.md)
