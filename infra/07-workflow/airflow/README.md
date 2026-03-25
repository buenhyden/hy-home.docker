# Airflow (Workflow Orchestration)

> Programmatic, Python-based workflow orchestration using Apache Airflow.

## Overview (KR)

Apache Airflow를 사용하여 프로그래밍 방식으로 워크플로우를 작성, 예약 및 모니터링합니다. Python DAG(Directed Acyclic Graphs)를 통해 복잡한 종속성을 관리하고 CeleryExecutor를 통해 분산 작업을 수행합니다.

## Overview

Apache Airflow is the primary programmatic orchestrator in the `hy-home.docker` ecosystem. It allows developers to define complex pipelines as code (Python), enabling version control, testing, and high extensibility. This deployment uses the `CeleryExecutor` pattern with Valkey as the broker for scalable task execution.

## Structure

```text
airflow/
├── config/              # StatsD mapping and custom config
├── dags/                # [External] DAG source code
├── plugins/             # [External] Custom Airflow plugins
├── docker-compose.yml   # Multi-node Airflow stack
└── README.md            # This file
```

---

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Runtime | `apache/airflow:slim-3.1.6` | Lightweight Python 3.12+ image |
| Executor | CeleryExecutor | Distributed task processing |
| Broker | Valkey (9.0.2) | High-performance task queue |
| Monitoring | StatsD Exporter | Metrics bridge to Prometheus |

## Configuration

### Services & Resources

| Service | Role | Resources |
| :--- | :--- | :--- |
| `airflow-apiserver` | Web UI & API | 1.0 CPU / 1G |
| `airflow-scheduler` | DAG Scheduling | 1.0 CPU / 1G |
| `airflow-worker` | Task Execution | 1.0 CPU / 1G |
| `airflow-valkey` | Celery Broker | 0.5 CPU / 0.5G |

### Environment Variables

| Variable | Description |
| :--- | :--- |
| `AIRFLOW__CORE__EXECUTOR` | Set to `CeleryExecutor` |
| `AIRFLOW__WEBSERVER__BASE_URL` | `https://airflow.${DEFAULT_URL}` |

## Persistence

- **Metadata DB**: PostgreSQL (mng-pg) shared with other management services.
- **DAGs**: Mounted from `${DEFAULT_WORKFLOW_DIR}/airflow/dags`.
- **Logs**: Persistent task logs via `${DEFAULT_WORKFLOW_DIR}/airflow/logs`.

## Operational Status

| Metric | Target | Notes |
| :--- | :--- | :--- |
| App Availability | 99.9% | Traefik health checks enabled |
| Task Latency | < 5s | Monitored via StatsD |

---

## License

Copyright (c) 2026. Licensed under the MIT License.
