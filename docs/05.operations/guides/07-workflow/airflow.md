---
status: active
---
<!-- Target: docs/05.operations/guides/07-workflow/airflow.md -->

# Airflow Usage Guide

## Usage

### Overview

이 문서는 `hy-home.docker` 플랫폼의 Apache Airflow 시스템에 대한 가이드다. 현재 구현은 Airflow 3.2.2, `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `flower`, `airflow-statsd-exporter`를 기준으로 한다.

---

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

### Usage Type

`system-guide`

### Target Audience

- **Developers**: DAG 개발 및 시스템 통합
- **Operators**: 서버 상태 모니터링 및 리소스 관리
- **AI Agents**: 자동화된 스케줄링 환경 분석

### Purpose

- Airflow 분산 아키텍처 (CeleryExecutor) 이해
- 웹 UI 및 모니터링 도구 접근 방법 확인
- 기본 개발 환경 설정 및 검증 절차 습득

### Prerequisites

- **Docker/Compose**: 로컬 실행 환경
- **Secrets**: `airflow_www_password` 등 서비스 접근 권한
- **Network**: `infra_net` 외부 통신 가능 상태

### Step-by-step Instructions

#### 1. 시스템 아키텍처 이해

Airflow는 다음과 같은 분산 컴포넌트로 구성됩니다:

- **Scheduler & DAG Processor**: 작업 예약 및 DAG 파일 해석 (독립 실행으로 안정성 확보)
- **Celery Workers**: 실제 태스크가 실행되는 동적 확장 노드
- **Valkey Broker**: 스케줄러와 워커 간의 메시지 교환. root-included dev compose는 `mng-valkey`를 사용하고, service-local `docker-compose.yml`은 `airflow-valkey`를 선언한다.
- **API Server**: UI 및 외부 통합을 위한 `airflow-apiserver` 엔드포인트

#### 2. UI 접근 및 모니터링

- **Main UI**: `https://airflow.${DEFAULT_URL}` (작업 모니터링, 로그 확인)
- **Flower Dashboard**: `https://flower.${DEFAULT_URL}` (Celery 워커 부하 상태 확인)
- **Metrics**: Prometheus/Grafana를 통해 StatsD 지표 확인 가능

#### 3. 개발 환경 검증

새로운 DAG를 추가하기 전에 다음 명령으로 시스템 상태를 확인합니다:

```bash

## workflow root compose static validation
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

## DAG 목록 로드 확인
docker compose exec airflow-apiserver airflow dags list
```

### Common Pitfalls

- **Scheduler Heavy Load**: DAG 파일 내에서 DB 쿼리나 파일 시스템 접근을 직접 수행하면 스케줄러 성능이 저하됩니다.
- **Worker Timeout**: 리소스 부족으로 워커가 종료되면 태스크가 `Queued` 상태로 멈출 수 있습니다.
- **XCom Abuse**: XCom은 작은 데이터 교환용입니다. 대용량 데이터는 S3/MinIO 등 외부 저장소를 사용하십시오.

## Common Checks

- `HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 07-workflow`
- Runtime이 실행 중이면 `docker compose exec airflow-apiserver airflow dags list`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/07-workflow/airflow.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/07-workflow/airflow.md)
- [Recovery runbook](../../runbooks/07-workflow/airflow.md)
