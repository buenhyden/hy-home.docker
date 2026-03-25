# Apache Airflow Orchestration

> Programmatic workflow orchestration using Python-based DAGs.

## Overview

Apache Airflow is the platform's primary engine for complex data pipelines and scheduled tasks. It uses `CeleryExecutor` for distributed horizontal scaling, managing tasks via a dedicated Valkey broker.

## Audience

- Data Engineers (Pipeline development)
- SREs (Cluster scaling)

## Structure

```text
airflow/
├── config/             # Airflow configuration and entrypoints
├── dags/               # User-defined DAGs (Python)
├── docker-compose.yml  # Distributed Airflow services
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Airflow DAG Development Guide](../../../docs/07.guides/07-workflow/01.airflow-dag-dev.md).
2. Access the UI at `http://airflow.${DEFAULT_URL}`.
3. Monitor workers via Flower: `http://flower.${DEFAULT_URL}`.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Engine | Apache Airflow | v2.10.3 |
| Executor | CeleryExecutor | Distributed workers |
| Broker | Valkey | Task queueing |

## Testing

```bash
# List all DAGs
docker exec airflow-webserver airflow dags list
```

## AI Agent Guidance

1. DAGs MUST NOT perform heavy computation on the scheduler; offload to workers.
2. Use `Variables` and `Connections` (managed via UI/CLI) for sensitive credentials.
3. Ensure all DAG files follow the `hy-home` naming convention.
