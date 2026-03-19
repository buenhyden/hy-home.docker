---
layer: infra
---
# Workflow Stack Operations (n8n & Airflow)

**Overview (KR):** n8n과 Airflow를 포함한 전체 워크플로우 스택의 통합 운영 가이드입니다.

> Standard operational guidelines for managing internal automation flows via n8n and Apache Airflow.

## 1. Description

The workflow infrastructure resides under `infra/07-workflow/`. These systems execute critical automation sequences ranging from standard data syncing (n8n) to complex DAG data-engineering pipelines (Apache Airflow).

## 2. n8n Operations

### State Management

n8n uses PostgreSQL (`mng-pg`) as its persistent store, configured via `DB_TYPE: postgresdb`.

- **Backup**: Before major n8n version upgrades, export all workflows via the n8n UI or API (`GET /api/v1/workflows`) and store the export. Also snapshot the PostgreSQL `n8n` database.
- **Scaling**: To scale beyond a single worker, add more `n8n-worker` replicas. The queue broker (`n8n-valkey`) handles task distribution without code changes.

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
