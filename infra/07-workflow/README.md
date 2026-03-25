# Workflow Tier (07-workflow)

> Automation workflows, ETL pipelines, and task orchestration.

## Overview

The `07-workflow` tier provides the infrastructure for automating repetitive tasks and orchestrating complex data pipelines. It balances power and ease-of-use by offering Apache Airflow for programmatic, highly-customizing DAGs and n8n for rapid, low-code automation and third-party integrations.

## Audience

이 README의 주요 독자:

- Data Engineers (ETL & Pipelines)
- Backend Developers (Task automation)
- AI Agents (Process orchestration)

## Scope

### In Scope

- Apache Airflow (CeleryExecutor)
- n8n Automation platform
- Valkey (Broker for Celery)
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

1. Read the [Airflow DAG Development Guide](../../docs/07.guides/07-workflow/01.airflow-dag-dev.md).
2. Follow the [n8n Automation Guide](../../docs/07.guides/07-workflow/02.n8n-automation.md).
3. Check the [Operations Policy](../../docs/08.operations/07-workflow/README.md) for scaling.
4. Consult the [Workflow Runbook](../../docs/09.runbooks/07-workflow/README.md) for failure recovery.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Orchestration | Apache Airflow              | v2.10.3 (CeleryExecutor)  |
| Automation  | n8n                          | v1.64.3                   |
| Broker      | Valkey                       | Dedicated for Celery      |
| Database    | PostgreSQL                   | Management Cluster        |

## Service Matrix

| Service | Protocol | Profile | Port |
| :--- | :--- | :--- | :--- |
| `airflow-webserver` | HTTP | `workflow` | 8080 |
| `n8n` | HTTP | `workflow` | 5678 |
| `airflow-flower` | HTTP | `workflow` | 5555 (Celery monitoring) |

## Configuration

- **Database**: Airflow and n8n use the `mng-db` instance in `04-data`.
- **Broker**: Celery uses `valkey-workflow` as the message broker.
- **Persistence**: DAGs and workflows are stored in persistent volumes linked to `${DEFAULT_WORKFLOW_DIR}`.

## Testing

```bash
# Verify Airflow CLI connectivity
docker exec airflow-webserver airflow info

# Test n8n health
curl -f http://localhost:5678/healthz
```

## Change Impact

- Updating Airflow versions may require database migrations.
- Changing the Valkey broker configuration affects all active Celery workers.
- Deleting an n8n workflow is irreversible if not version-controlled externally.

## Related References

- [04-data](../04-data/README.md) - Metadata storage.
- [06-observability](../06-observability/README.md) - Monitoring task performance.
- [01-gateway](../01-gateway/README.md) - Routing to Web UIs.

## AI Agent Guidance

1. Always use `CeleryExecutor` for production-grade Airflow deployments.
2. New n8n nodes should be vetted for security before enabling in the primary instance.
3. Monitor `worker lag` in Flower to identify bottlenecks in the task queue.
