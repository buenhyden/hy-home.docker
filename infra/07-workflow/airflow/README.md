# Airflow (07-workflow)

> Apache Airflow를 이용한 복잡한 데이터 파이프라인 및 작업의 프로그래밍 방식 워크플로 오케스트레이션.

## Overview

Apache Airflow는 `hy-home.docker` 플랫폼의 핵심 워크플로 엔진입니다. Python 기반의 DAG(Directed Acyclic Graph)를 사용하여 복잡한 작업 간의 의존성을 정의하고 예약 실행합니다. `CeleryExecutor`를 통한 분산 확장이 가능하며, Redis 호환 Valkey를 브로커로 사용하여 고가용성을 확보합니다.

## Audience

이 README의 주요 독자:

- **Data Engineers**: 파이프라인(DAG) 개발 및 관리
- **SREs**: 클러스터 가용성 및 성능 최적화
- **AI Agents**: 자동화된 작업 스케줄링 및 모니터링

## Scope

### In Scope

- Airflow 코어 서비스 (`apiserver`, `scheduler`, `dag-processor`, `worker`, `triggerer`)
- Celery 분산 실행 환경 및 Valkey 브로커 구성
- 메타데이터 DB(PostgreSQL) 연결 및 초기화 (`airflow-init`)
- 모니터링 구성 (`flower`, `statsd-exporter`)

### Out of Scope

- 개별 비즈니스 로직 DAG (다른 저장소 또는 `dags/` 하위 폴더에서 관리)
- 외부 데이터 소스 인프라 (04-data 등 시스템 레이어에서 관리)

## Structure

```text
airflow/
├── config/             # Airflow 설정 및 StatsD 매핑 파일
├── dags/               # 사용자 정의 DAG 파일 (Python)
├── docker-compose.yml  # 분산 Airflow 서비스 구성
└── README.md           # 이 파일
```

## How to Work in This Area

1. [진입 가이드](../../docs/07.guides/07-workflow/airflow.md)를 읽고 시스템 전반을 이해합니다.
2. [DAG 개발 가이드](../../docs/07.guides/07-workflow/01.airflow-dag-dev.md)를 참조하여 파이프라인을 작성합니다.
3. [운영 정책](../../docs/08.operations/07-workflow/airflow.md)에 따라 리소스 할당 및 보안 설정을 확인합니다.
4. 장애 발생 시 [장애 조치 런북](../../docs/09.runbooks/07-workflow/airflow.md)을 따릅니다.

## Tech Stack

| Category | Technology | Version | Notes |
| :--- | :--- | :--- | :--- |
| Engine | Apache Airflow | v2.10.3 (3.1.8) | Python 3.12 기반 |
| Executor | CeleryExecutor | Distributed | 분산 워커 노드 확장 |
| Broker | Valkey (Redis-compatible) | v9.0.2 | 태스크 큐 및 메시지 브로커 |
| DB | PostgreSQL | v16+ | 메타데이터 및 상태 저장 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :--- | :--- |
| `AIRFLOW_UID` | Yes | Airflow 컨테이너 실행 사용자 ID (기본: 50000) |
| `AIRFLOW_IMAGE_NAME` | No | 사용할 Airflow 베이스 이미지 |
| `AIRFLOW_DB_USER` | Yes | 메타데이터 DB 접속 사용자 |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose run --rm airflow-cli dags list` | 현재 로드된 DAG 목록 확인 |
| `docker compose run --rm airflow-cli tasks test <dag_id> <task_id> <date>` | 특정 태스크 실행 테스트 |

## AI Agent Guidance

1. **Idempotency**: 모든 DAG 및 태스크는 멱등성을 보장해야 하며, Scheduler에서 무거운 계산을 수행하지 않아야 합니다.
2. **Secrets**: 민감한 정보는 `Variables`나 `Connections`를 통해 관리하며, 환경 변수에 직접 노출하지 않습니다.
3. **Traceability**: 모든 변경 사항은 관련 [ARD](../../docs/02.ard/07-workflow.md) 또는 [Spec](../../docs/04.specs/07-workflow/spec.md)과 연결되어야 합니다.

## Related References

- **ARD**: [07-workflow Architecture](../../docs/02.ard/07-workflow.md)
- **Guide**: [Airflow System Guide](../../docs/07.guides/07-workflow/airflow.md)
- **Operation**: [Airflow Operations Policy](../../docs/08.operations/07-workflow/airflow.md)
- **Runbook**: [Airflow Recovery Runbook](../../docs/09.runbooks/07-workflow/airflow.md)
