# Apache Airflow

## Overview

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. This deployment includes the full Airflow stack (Webserver, Scheduler, DAG Processor, Triggerer, Worker) along with Flower for monitoring Celery workers and StatsD export for metrics.

## Services

The stack consists of the following services:

| Service | Description | Port (Internal) |
| :--- | :--- | :--- |
| `airflow-apiserver` | Airflow Webserver & API | `${AIRFLOW_PORT}` (8080) |
| `airflow-scheduler` | Scheduler service | - |
| `airflow-dag-processor`| Dedicated DAG processor | - |
| `airflow-triggerer` | Triggerer for deferrable operators | - |
| `airflow-worker` | Celery worker for executing tasks | - |
| `airflow-init` | Initialization service (DB migrations, user creation) | - |
| `airflow-cli` | Helper container for running CLI commands | - |
| `flower` | Celery monitoring tool | `${FLOWER_PORT}` (5555) |
| `airflow-statsd-exporter` | Prometheus StatsD Exporter | `${STATSD_PROMETHEUS_PORT}` (9102), `${STATSD_AIRFLOW_PORT}` (8125 UDP) |

### External Dependencies

This setup relies on the following external services within the `infra_net` network:

- **PostgreSQL**: Used as the Airflow Metadata Database.
- **Redis**: Used as the Celery Broker.

## Networking

All services are attached to the **`infra_net`** network to communicate with shared infrastructure (Traefik, Postgres, Redis, Prometheus).

## Configuration

### Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `AIRFLOW__CORE__EXECUTOR` | Executor Type | `CeleryExecutor` |
| `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN` | Metadata DB Connection | `postgresql+psycopg2://...` |
| `AIRFLOW__CELERY__RESULT_BACKEND` | Celery Backend | `db+postgresql://...` |
| `AIRFLOW__CELERY__BROKER_URL` | Celery Broker (Redis) | `redis://...` |
| `AIRFLOW__WEBSERVER__BASE_URL` | External URL | `https://airflow.${DEFAULT_URL}` |
| `AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX`| Trust Proxy Headers | `true` |
| `_AIRFLOW_WWW_USER_USERNAME` | Admin Username | `${_AIRFLOW_WWW_USER_USERNAME}` |
| `_AIRFLOW_WWW_USER_PASSWORD` | Admin Password | `${_AIRFLOW_WWW_USER_PASSWORD}` |
| `AIRFLOW__METRICS__STATSD_ON` | Enable StatsD | `true` |

### Configuration Files

The `config/` directory contains configuration files mapped into the containers:

- **`config/statsd_mapping.yml`**: Mapped to `/tmp/mappings.yml` in the `airflow-statsd-exporter` container.
  - **Purpose**: Defines mapping rules to convert Airflow's hierarchical StatsD metrics into labeled Prometheus metrics.
  - **Key Mappings**:
    - `airflow.dag_processing.*` → `airflow_dag_processing_*`
    - `airflow.scheduler.*` → `airflow_scheduler_*`
    - `airflow.executor.*` → `airflow_executor_*`
    - `airflow.dag.*.*.duration` → `airflow_dag_task_duration` (with `dag_id` and `task_id` labels)

## Persistence

| Host Path | Container Path | Description |
| :--- | :--- | :--- |
| `airflow-dags` | `/opt/airflow/dags` | Stores DAG files |
| `airflow-plugins` | `/opt/airflow/plugins` | Stores Airflow plugins |
| `./config/statsd_mapping.yml` | `/tmp/mappings.yml` | StatsD Exporter mapping config |

## Traefik Integration

Services are exposed via Traefik with the following configuration:

| Service | Host Rule | Entrypoint | TLS | Middleware |
| :--- | :--- | :--- | :--- | :--- |
| **Airflow** | `airflow.${DEFAULT_URL}` | `websecure` | True | - |
| **Flower** | `flower.${DEFAULT_URL}` | `websecure` | True | `sso-auth@file` |

> **Note**: Flower is protected by `sso-auth` middleware because it lacks robust built-in authentication.

## Usage

### Starting Airflow

```bash
docker-compose up -d
```

The `airflow-init` service will automatically run first to migrate the database and create the default user.

### Accessing Interfaces

- **Airflow UI**: `https://airflow.<your-domain>`
  - Default Credentials: `${_AIRFLOW_WWW_USER_USERNAME}` / `${_AIRFLOW_WWW_USER_PASSWORD}` (default: `airflow` / `airflow`)
- **Flower UI**: `https://flower.<your-domain>`
