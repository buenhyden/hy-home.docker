# Apache Airflow

## Overview

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

## Services

- **airflow-apiserver**: Airflow API Server and Web Interface.
  - Port: `${AIRFLOW_PORT}` (Internal)
  - URL: `https://airflow.${DEFAULT_URL}`
- **airflow-scheduler**: Monitors all tasks and DAGs, then triggers task instances once their dependencies are complete.
- **airflow-dag-processor**: Parses DAG files and writes them to the database.
- **airflow-worker**: Executes the tasks given by the scheduler.
- **airflow-triggerer**: Runs an event loop for deferrable operators.
- **airflow-init**: Initialization service (sets up DB, users).
- **flower**: Celery Flower for monitoring distributed workers.
  - URL: `https://flower.${DEFAULT_URL}`
- **airflow-statsd-exporter**: Exports StatsD metrics to Prometheus.

## Configuration

### Environment Variables

- `AIRFLOW__CORE__EXECUTOR`: `CeleryExecutor`
- `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`: Postgres connection string.
- `AIRFLOW__CELERY__RESULT_BACKEND`: Postgres connection string (for Celery results).
- `AIRFLOW__CELERY__BROKER_URL`: Redis connection string.
- `AIRFLOW__WEBSERVER__BASE_URL`: External URL for the webserver.
- `AIRFLOW_UID`: User ID for Airflow processes.

### Volumes

- `airflow-dags`: `/opt/airflow/dags`
- `airflow-plugins`: `/opt/airflow/plugins`
- `./config/statsd_mapping.yml`: `/tmp/mappings.yml` (Read-only)

## Networks

- `infra_net`

## Traefik Routing

- **Airflow**: `airflow.${DEFAULT_URL}`
- **Flower**: `flower.${DEFAULT_URL}`
