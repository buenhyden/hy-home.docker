# Workflow (07-workflow)

This category manages automation workflows, ETL pipelines, and task orchestration.

## Services

| Service | Profile     | Path        | Purpose                                    |
| ------- | ----------- | ----------- | ------------------------------------------ |
| n8n     | *(disabled)*| `./n8n`     | Low-code automation tool                   |
| Airflow | `workflow`  | `./airflow` | Programmatic workflow orchestration (DAGs) |

> [!NOTE]
> n8n is not included in the root `docker-compose.yml` by default. Uncomment the include entry to enable it.

## Dependencies

- **Database**: Both n8n and Airflow use management PostgreSQL (via `infra/04-data/postgresql-cluster`).
- **Valkey (Airflow)**: `airflow-valkey` — dedicated Valkey instance for Celery task brokering.
- **Valkey (n8n)**: `n8n-valkey` — dedicated Valkey instance for n8n queue mode.

## File Map

| Path        | Description                              |
| ----------- | ---------------------------------------- |
| `n8n/`      | n8n service and persistence.             |
| `airflow/`  | Airflow nodes (API server, Scheduler, Worker, DAG Processor). |
| `README.md` | Category overview.                       |

