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

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Airflow (07-workflow) service leaf in `07-workflow`; services: `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, `airflow-init`, plus 12 more; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/airflow/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Config files | `docker-compose.dev.yml`, `docker-compose.yml`, `config`, `config/statsd_mapping.yml` |
| Config values | env keys: `AIRFLOW__CORE__EXECUTOR`, `AIRFLOW__CORE__AUTH_MANAGER`, `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_CMD`, `AIRFLOW__CELERY__RESULT_BACKEND_CMD`, `AIRFLOW__CELERY__BROKER_URL_CMD`, `AIRFLOW__CORE__FERNET_KEY_CMD`, `AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION`, `AIRFLOW__CORE__LOAD_EXAMPLES`, plus 15 more; profiles: `workflow`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/07-workflow/airflow/docker-compose.dev.yml`; local compose only: `docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `airflow-dags:/opt/airflow/dags`, `airflow-plugins:/opt/airflow/plugins`, `airflow-logs:/opt/airflow/logs`, `airflow-config:/opt/airflow/config`, `./config/statsd_mapping.yml:/tmp/mappings.yml:ro`, `airflow-dags`, `airflow-logs`, `airflow-config`, plus 3 more |
| Ports | `${STATSD_PROMETHEUS_PORT:-9102}`, `${STATSD_AIRFLOW_PORT:-9125}`, `${VALKEY_PORT:-6379}`, `${VALKEY_BUS_PORT:-16379}`, `${VALKEY_EXPORTER_PORT:-9121}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.airflow.rule`, `traefik.http.routers.airflow.entrypoints`, `traefik.http.routers.airflow.tls`, `traefik.http.routers.airflow.middlewares`, `traefik.http.services.airflow.loadbalancer.server.port`, `traefik.http.routers.flower.rule`, plus 4 more |
| Secret refs | names: `airflow_db_password`, `airflow_fernet_key`, `airflow_www_password`, `mng_valkey_password`, `airflow_valkey_password`; mounts: `/run/secrets/airflow_db_password`, `/run/secrets/airflow_fernet_key`, `/run/secrets/airflow_www_password`, `/run/secrets/mng_valkey_password`, `/run/secrets/airflow_valkey_password` |
| Healthcheck | Compose healthcheck declared for `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`, `airflow-worker`, `airflow-triggerer`, plus 8 more; not declared for `airflow-init`, `airflow-statsd-exporter`, `airflow-init`, `airflow-valkey-exporter`, `airflow-statsd-exporter` |
| Operations | [Guide](../../../docs/05.operations/guides/07-workflow/airflow.md), [Policy](../../../docs/05.operations/policies/07-workflow/airflow.md), [Runbook](../../../docs/05.operations/runbooks/07-workflow/airflow.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. [진입 가이드](../../../docs/05.operations/guides/07-workflow/airflow.md)를 읽고 시스템 전반을 이해합니다.
2. [DAG 개발 가이드](../../../docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md)를 참조하여 파이프라인을 작성합니다.
3. [운영 정책](../../../docs/05.operations/guides/07-workflow/airflow.md)에 따라 리소스 할당 및 보안 설정을 확인합니다.
4. 장애 발생 시 [장애 조치 런북](../../../docs/05.operations/guides/07-workflow/airflow.md)을 따릅니다.

## Tech Stack

| Category | Technology | Version | Notes |
| :--- | :--- | :--- | :--- |
| Engine | Apache Airflow | v3.1.8 | Python 3.12 기반 |
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
3. **Traceability**: 모든 변경 사항은 관련 [ARD](../../../docs/02.architecture/requirements/0007-workflow-architecture.md) 또는 [Spec](../../../docs/03.specs/07-workflow/spec.md)과 연결되어야 합니다.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect Airflow.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking Airflow documentation ready.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For DAG errors: check the Airflow UI task logs and verify DAG file syntax with `airflow dags list`.
- For scheduler errors: confirm the scheduler container is running and check `docker logs airflow-scheduler | grep -i 'error'`.
- For worker errors: verify the executor configuration and confirm the message broker is reachable.

## Related Documents

- **ARD**: [07-workflow Architecture](../../../docs/02.architecture/requirements/0007-workflow-architecture.md)
- **Guide**: [Airflow System Guide](../../../docs/05.operations/guides/07-workflow/airflow.md)
- **Operation**: [Airflow Operations Policy](../../../docs/05.operations/guides/07-workflow/airflow.md)
- **Runbook**: [Airflow Recovery Runbook](../../../docs/05.operations/guides/07-workflow/airflow.md)
