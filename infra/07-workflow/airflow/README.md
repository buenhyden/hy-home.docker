# Airflow

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `airflow-apiserver` | `apache/airflow:slim-3.1.6` | REST API and UI | 1.0 CPU / 1G |
| `airflow-scheduler` | `apache/airflow:slim-3.1.6` | Orchestrator | 1.0 CPU / 1G |
| `airflow-dag-processor` | `apache/airflow:slim-3.1.6` | DAG File Parser | 1.0 CPU / 1G |
| `airflow-worker` | `apache/airflow:slim-3.1.6` | Celery Worker | 1.0 CPU / 1G |
| `airflow-triggerer` | `apache/airflow:slim-3.1.6` | Deferred Operators | 0.5 CPU / 0.5G |
| `airflow-valkey` | `valkey/valkey:9.0.2-alpine` | Celery Broker | 0.5 CPU / 0.5G |
| `airflow-valkey-exporter` | `oliver006/redis_exporter` | Valkey Metrics | - |
| `airflow-statsd-exporter` | `prom/statsd-exporter:v0.28.0` | StatsD→Prometheus | - |
| `airflow-init` | `apache/airflow:slim-3.1.6` | Bootstrap Job | - |

> Profile: all services require the `workflow` profile (`--profile workflow`).
> `airflow-cli` (profile: `debug`) and `flower` (profile: `flower`) are optional.

## Networking

- **API Server**: `airflow.${DEFAULT_URL}` (Traefik, HTTPS).
- **Flower**: `flower.${DEFAULT_URL}` (profile: `flower`, requires SSO middleware).
- **Broker**: `airflow-valkey:6379` (internal, DB 0).

## Persistence

- **PostgreSQL**: Metadata DB and Celery result backend (via `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_CMD`).
- **DAGs**: `${DEFAULT_WORKFLOW_DIR}/airflow/dags` → mounted as `airflow-dags` volume.
- **Logs**: `${DEFAULT_WORKFLOW_DIR}/airflow/logs` → mounted as `airflow-logs` volume.
- **Config**: `${DEFAULT_WORKFLOW_DIR}/airflow/config` → mounted as `airflow-config` volume.
- **Plugins**: `${DEFAULT_WORKFLOW_DIR}/airflow/plugins` → mounted as `airflow-plugins` volume.

## Secrets

| Secret | Purpose |
| :--- | :--- |
| `airflow_db_password` | PostgreSQL connection |
| `airflow_fernet_key` | Variable/connection encryption |
| `airflow_www_password` | Admin user password |
| `airflow_valkey_password` | Valkey broker auth |

## File Map

| Path                    | Description                                  |
| ----------------------- | -------------------------------------------- |
| `docker-compose.yml`    | Multi-node Airflow stack definition.         |
| `config/statsd_mapping.yml` | StatsD metric mapping rules for Prometheus. |
| `README.md`             | Service overview and DAG authoring docs.     |

