# Apache Airflow

## Overview

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows. This deployment includes the Webserver, Scheduler, Triggerer, Worker, and Flower for monitoring Celery.

## Service Details

- **Image**: `${AIRFLOW_IMAGE_NAME:-apache/airflow:3.1.5}`
- **Components**:
  - `airflow-apiserver`: Webserver and API.
  - `airflow-scheduler`: Scheduler.
  - `airflow-worker`: Celery worker.
  - `airflow-triggerer`: Triggerer for deferrable operators.
  - `airflow-cli`: Helper for CLI commands.
  - `flower`: Celery monitoring tool.
  - `airflow-statsd-exporter`: Metrics exporter.

### Volumes

- `airflow-dags`: `/opt/airflow/dags`
- `airflow-plugins`: `/opt/airflow/plugins`
- `./config/statsd_mapping.yml`: `/tmp/mappings.yml` (for StatsD)

## Environment Variables (Key Highlights)

- `AIRFLOW__CORE__EXECUTOR`: `CeleryExecutor`
- `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`: PostgreSQL connection string.
- `AIRFLOW__CELERY__RESULT_BACKEND`: Celery result backend (PostgreSQL).
- `AIRFLOW__CELERY__BROKER_URL`: Redis broker URL.
- `AIRFLOW__WEBSERVER__BASE_URL`: `https://airflow.${DEFAULT_URL}`

## Traefik Configuration

| Service | Host Rule | Entrypoint | TLS |
| :--- | :--- | :--- | :--- |
| **Airflow** | `airflow.${DEFAULT_URL}` | `websecure` | True |
| **Flower** | `flower.${DEFAULT_URL}` | `websecure` | True |

> **Note**: Flower is configured with `sso-auth` middleware for security.
