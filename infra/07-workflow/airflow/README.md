# Airflow

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `api-server` | `airflow:slim-3.1.6`| Web / API | 1.0 CPU / 1G |
| `scheduler` | `airflow:slim-3.1.6`| Orchestrator | 1.0 CPU / 1G |
| `worker` | `airflow:slim-3.1.6`| Celery Worker| 1.0 CPU / 1G |
| `dag-proc` | `airflow:slim-3.1.6`| DAG Loader | 1.0 CPU / 1G |

## Networking

- **Webserver**: `airflow.${DEFAULT_URL}`.
- **Broker**: Redis (via `mng-valkey`).

## Persistence

- **PostgreSQL**: Used for the metadata database.
- **DAGs**: Mounted to `./dags` directory.

## File Map

| Path                 | Description                             |
| -------------------- | --------------------------------------- |
| `docker-compose.yml` | Multi-node Airflow stack definition.    |
| `dags/`              | User-defined Python DAGs.               |
| `README.md`          | Service overview and DAG authoring docs.|
