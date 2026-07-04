# Workflow Tier (07-workflow)

> Automation workflows, ETL pipelines, and task orchestration.

## Overview

The `07-workflow` tier provides the infrastructure for automating repetitive tasks and orchestrating complex data pipelines. It balances power and ease-of-use by offering Apache Airflow for code-first DAG orchestration and n8n for rapid, low-code automation and third-party integrations.

## Audience

이 README의 주요 독자:

- Data Engineers (ETL & Pipelines)
- Backend Developers (Task automation)
- AI Agents (Process orchestration)

## Scope

### In Scope

- Apache Airflow (CeleryExecutor)
- n8n Automation platform
- Valkey broker wiring for Airflow/n8n queue mode
- Workflow Database (Shared Management Postgres)

### Out of Scope

- Business logic within individual DAGs
- External CI/CD workflows (handled via GitHub Actions)
- Real-time stream processing (handled by `05-messaging`)

## Structure

```text
07-workflow/
├── airflow/            # Programmatic workflow orchestration
├── n8n/                # Low-code automation and integrations
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Airflow DAG basics guide](../../docs/05.operations/guides/07-workflow/airflow-dag-basics.md).
2. Follow the [n8n usage guide](../../docs/05.operations/guides/07-workflow/n8n.md).
3. Check the [Operations Policy](../../docs/05.operations/policies/07-workflow/README.md) for scaling.
4. Consult the [Workflow Runbook](../../docs/05.operations/runbooks/07-workflow/README.md) for failure recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Orchestration | Apache Airflow              | v3.2.2 (CeleryExecutor)   |
| Automation  | n8n                          | v2.29.5-local             |
| Broker      | Valkey                       | root dev uses `mng-valkey`; service-local compose declares `airflow-valkey` and `n8n-valkey` |
| Database    | PostgreSQL                   | Management PostgreSQL (`mng-pg`) |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `airflow-apiserver` | HTTP | `workflow` | 8080 |
| `airflow-scheduler` | internal | `workflow` | 8974 health endpoint |
| `airflow-worker` | internal | `workflow` | Celery worker |
| `n8n` | HTTP | `workflow` | 5678 |
| `n8n-worker` | internal | `workflow` | 5679 broker health |
| `n8n-task-runner` | internal | `workflow` | 5680 |
| `flower` | HTTP | `workflow` | 5555 (Celery monitoring) |

## Configuration

- **Database**: Airflow and n8n use the `mng-db` instance in `04-data`.
- **Broker**: root-included dev compose uses shared `mng-valkey`; service-local compose declares dedicated `airflow-valkey` and `n8n-valkey`.
- **Persistence**: DAGs and workflows are stored in persistent volumes linked to `${DEFAULT_WORKFLOW_DIR}`.

## Testing

```bash
# Verify workflow root compose
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

# Verify workflow hardening baseline
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

## Change Impact

- Updating Airflow versions may require database migrations.
- Changing the Valkey broker configuration affects Airflow Celery workers and n8n queue workers.
- Deleting an n8n workflow is irreversible if not version-controlled externally.

## Related Documents

- [04-data](../04-data/README.md) - Metadata storage.
- [06-observability](../06-observability/README.md) - Monitoring task performance.
- [01-gateway](../01-gateway/README.md) - Routing to Web UIs.

## AI Agent Guidance

1. Always use `CeleryExecutor` for production-grade Airflow deployments.
2. New n8n nodes should be vetted for security before enabling in the primary instance.
3. Monitor `worker lag` in Flower to identify bottlenecks in the task queue.
