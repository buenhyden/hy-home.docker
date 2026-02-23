# Workflow Stack Operations (n8n & Airflow)

> Standard operational guidelines for managing internal automation flows via n8n and Apache Airflow.

## 1. Description

The workflow infrastructure resides under `infra/07-workflow/`. These systems execute critical automation sequences ranging from standard data syncing (n8n) to complex DAG data-engineering pipelines (Apache Airflow).

## 2. n8n Operations

### State Management

n8n utilizes an embedded SQLite database persisted into a host volumetric mount (`n8n-data:/home/node/.n8n`).

- **Backup**: Always backup the raw SQLite database before major n8n version upgrades to prevent schema migration corruption.
- **Scaling**: If workflow concurrency bottlenecks, consider migrating from SQLite to the core management PostgreSQL database (`mng-db`) using the `DB_TYPE=postgres` env variables before scaling n8n into a multi-main queue mode.

### Webhook Handling

If external services (like GitHub or Stripe) fail to trigger n8n workflows:

1. Verify `WEBHOOK_URL` in the environment explicitly references the Traefik exterior domain (e.g., `https://n8n.${DEFAULT_URL}/`).
2. Ensure the firewall or security proxy allows inbound traffic across specific webhook pathways.

## 3. Apache Airflow Operations

### DAG Deployment

Airflow DAGs must be mounted to the scheduler and webserver simultaneously.

- Host Path: `${DEFAULT_WORKFLOW_DIR}/airflow/dags`
- To push a new pipeline, place the Python scripts within the DAG directory directly. Both the `airflow-webserver` and `airflow-scheduler` will ingest them typically within 30-60 seconds.

### Worker Resource Exhaustion

When running heavy Python dependencies via `CeleryExecutor` or `LocalExecutor`:

1. Modify the `airflow.cfg` or env flags to restrict `parallelism` and `max_active_tasks_per_dag`.
2. Evaluate container limits inside `docker-compose.yml`. Over-allocating memory limits prevents the Docker daemon from unexpectedly sending `OOMKilled` signals mid-pipeline execution.
