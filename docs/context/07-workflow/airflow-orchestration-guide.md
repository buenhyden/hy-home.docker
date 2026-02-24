# Apache Airflow Orchestration Blueprint

> **Component**: `airflow`
> **Executor**: CeleryExecutor
> **Internal Web Interface**: `8080`

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

- **Broker**: `redis://mng-redis:6379/1`
- **Result Backend**: Management PostgreSQL.

## 4. Resource Management

Large DAGs consuming significant memory should utilize a custom `Pool` to prevent exhausting the `airflow-worker` memory limits and triggering OOM events.
