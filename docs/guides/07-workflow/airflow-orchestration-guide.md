---
layer: infra
---
# Apache Airflow Orchestration Guide

**Overview (KR):** 데이터 엔지니어링 허브로서의 Airflow 아키텍처와 통합 운영 가이드입니다.

> **Component**: `airflow`
> **Executor**: CeleryExecutor
> **Internal API Interface**: `8080` (Airflow 3.x uses `api-server`, not `webserver`)

## 1. Data Engineering Hub

Airflow manages complex dependency-aware data pipelines (DAGs).

- **Webserver URL**: `https://airflow.${DEFAULT_URL}`
- **Worker Management**: Flower UI (`https://flower.${DEFAULT_URL}`)

## 2. DAG Deployment Pattern

Pipelines are defined as Python code and mounted from the host:

- **Host Path**: `${DEFAULT_WORKFLOW_DIR}/airflow/dags`
- **Dynamic Loading**: Workers and Schedulers automatically refresh Dags folder every 30 seconds.

## 3. Scalability (Celery)

The cluster utilizes Valkey as the message broker for Celery task distribution.

- **Broker**: `redis://airflow-valkey:6379/0` (dedicated `airflow-valkey` container)
- **Result Backend**: Airflow's own database in management PostgreSQL (via `AIRFLOW__CELERY__RESULT_BACKEND_CMD`).

## 4. Resource Management

Large DAGs consuming significant memory should utilize a custom `Pool` to prevent exhausting the `airflow-worker` memory limits and triggering OOM events.
