<!-- Target: docs/04.specs/07-workflow/spec.md -->

# Workflow Tier (07-workflow) Technical Specification

## Overview (KR)

이 문서는 `07-workflow` 계층(Airflow, n8n)의 상세 기술 설계와 시스템 간 인터페이스 계약을 정의한다. 분산 태스크 처리 인프라와 로우코드 자동화 플랫폼의 구동 방식 및 의존성을 명시한다.

## Strategic Boundaries & Non-goals

- **In Scope**:
  - Airflow `CeleryExecutor`와 `Valkey` 간의 연동 규격.
  - n8n `Queue` 모드와 `Task Runner` 간의 연동 규격.
  - 관련 환경 변수 및 시크릿 관리 체계.
- **Non-goals**:
  - 개별 DAG 코드 작성 가이드 (Guide 영역).
  - 외부 API의 엔드포인트 설계 (각 서비스 Spec 영역).

## Related Inputs

- **PRD**: [2026-03-26-07-workflow.md](../../01.prd/2026-03-26-07-workflow.md)
- **ARD**: [0007-workflow-architecture.md](../../02.ard/0007-workflow-architecture.md)
- **Related ADRs**: [0007-airflow-n8n-hybrid-workflow.md](../../03.adr/0007-airflow-n8n-hybrid-workflow.md)

## Interfaces

```yaml
# Airflow Broker URL (Valkey)
AIRFLOW__CELERY__BROKER_URL: redis://:v_passwd@v_host:6379/1
```

## Contracts

- **Config Contract**:
  - `AIRFLOW__CORE__EXECUTOR`: `CeleryExecutor` 고정.
  - `N8N_ENCRYPTION_KEY`: 필수 시크릿 (Vault 관리).
- **Data / Interface Contract**:
  - Message Format: Celery/Redis 프로토콜.
  - DB Schema: Airflow 2.x / n8n 1.x 표준 스키마.

## Core Design

### Apache Airflow (Celery Mode)

- **Scheduler**: DAG를 파싱하고 태스크 인스턴스를 생성.
- **Broker (Valkey)**: 태스크 큐를 관리. `airflow-valkey` 서비스로 분리.
- **Worker**: 브로커에서 태스크를 가져와 실행. `airflow-worker` 컨테이너.
- **Result Backend**: 태스크 상태를 저장 (PostgreSQL).

### Airflow Configuration

- **Executor**: CeleryExecutor

### n8n (Queue Mode)

- **Main Server**: UI 제어 및 워크플로 관리.
- **Worker**: 실행 대기열의 워크플로 실제 처리.
- **Task Runner**: 격리된 환경에서 Python 스크립트 등 무거운 연산 처리.

### n8n Configuration

- **Mode**: Queue Mode (Distributed)
- **Database**: PostgreSQL (shared management cluster)

## Data Modeling & Storage Strategy

- **Metadata Storage**: PostgreSQL (`infra/04-data`) 내 `airflow` 및 `n8n` 데이터베이스.
- **Persistence**: `${DEFAULT_WORKFLOW_DIR}` 하위 볼륨 매핑을 통한 데이터 보존.

## Verification

### Airflow Status Check

```bash
# 워커 상태 확인
docker exec airflow-webserver airflow celery inspect ping

# DB 연결성 확인
docker exec airflow-webserver airflow db check
```

### n8n Status Check

```bash
# 헬스체크 엔드포인트 확인
curl -f http://localhost:5678/healthz
```

## Related Documents

- **Plan**: [2026-03-26-07-workflow-standardization.md](../../05.plans/2026-03-26-07-workflow-standardization.md)
- **Tasks**: [2026-03-26-07-workflow-tasks.md](../../06.tasks/2026-03-26-07-workflow-tasks.md)
