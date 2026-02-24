# Airflow

Apache Airflow is a platform to programmatically author, schedule, and monitor workflows.

## Services

| Service            | Image                         | Role           | Resources         |
| :----------------- | :---------------------------- | :------------- | :---------------- |
| `airflow-webserver`| `apache/airflow:2.10.0`      | Web UI         | 0.5 CPU / 1GB RAM |
| `airflow-scheduler`| `apache/airflow:2.10.0`      | Orchestrator   | 0.5 CPU / 512MB   |
| `airflow-worker`   | `apache/airflow:2.10.0`      | Task Execution | 1 CPU / 1GB RAM   |
| `airflow-init`     | `apache/airflow:2.10.0`      | Initialization | -                 |

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
