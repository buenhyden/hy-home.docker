# Workflow (07-workflow)

This category manages automation workflows, ETL pipelines, and task orchestration.

## Services

| Service | Profile   | Path        | Purpose                                    |
| ------- | --------- | ----------- | ------------------------------------------ |
| n8n     | (core)    | `./n8n`     | Low-code automation tool                   |
| Airflow | `airflow` | `./airflow` | Programmatic workflow orchestration (DAGs) |

## Dependencies

- **Database**: Both n8n and Airflow use PostgreSQL (via `infra/04-data/postgresql-cluster`).
- **Redis**: Airflow uses Redis for task queuing (CeleryExecutor).

## File Map

| Path        | Description                              |
| ----------- | ---------------------------------------- |
| `n8n/`      | n8n service and persistence.             |
| `airflow/`  | Airflow nodes (Web, Scheduler, Worker).  |
| `README.md` | Category overview.                       |
