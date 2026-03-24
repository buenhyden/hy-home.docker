---
layer: infra
---

# Workflow Tier: System Context

The `07-workflow` tier provides distributed automation and orchestration services using Apache Airflow (complex DAGs) and n8n (low-code webhooks).

## 1. Architecture Overview

### Apache Airflow (3.x)
Airflow 3.x separates the web layer (API server) from the DAG file parsing layer (DAG processor).

| Service | Role |
| --- | --- |
| `airflow-apiserver` | REST API and UI |
| `airflow-scheduler` | Trigger DAG runs |
| `airflow-dag-processor` | Parse Python DAG files |
| `airflow-worker` | Execute tasks via Celery |
| `airflow-valkey` | Celery message broker |

### n8n (Queue Mode)
n8n runs in distributed queue mode for scalability and resilience.

| Service | Role |
| --- | --- |
| `n8n` | Main engine, UI, webhook receiver |
| `n8n-worker` | Executes queued workflow jobs |
| `n8n-task-runner` | Isolated process for Code nodes |
| `n8n-valkey` | Bull queue broker |

## 2. Secrets & Security

All sensitive values are injected via Docker secrets.

| Tier Component | Secret Name | Purpose |
| --- | --- | --- |
| **Airflow** | `airflow_db_password` | PostgreSQL metadata DB connection |
| **Airflow** | `airflow_fernet_key` | Encryption for Variables/Connections |
| **n8n** | `n8n_db_password` | PostgreSQL connection |
| **n8n** | `n8n_encryption_key` | Credential encryption |

## 3. Storage & Volumes

| Component | Host Path | Purpose |
| --- | --- | --- |
| **Airflow** | `${DEFAULT_WORKFLOW_DIR}/airflow/dags` | Python DAG files |
| **Airflow** | `${DEFAULT_WORKFLOW_DIR}/airflow/logs` | Task execution logs |
| **n8n** | `${DEFAULT_WORKFLOW_DIR}/n8n` | Workflow data, credentials |
| **General** | `${DEFAULT_WORKFLOW_DIR}/valkey` | Persistence for task brokers |

## 4. Networking

Services use the `infra_net` bridge. Traefik routes inbound traffic:

- **Airflow**: `https://airflow.${DEFAULT_URL}`
- **n8n**: `https://n8n.${DEFAULT_URL}`
- **Flower**: `https://flower.${DEFAULT_URL}` (Celery monitoring)

## 5. Metrics & Observability

- **Airflow**: StatsD → Prometheus (port `9102`).
- **n8n**: Native Prometheus endpoint (`/metrics`) on port `5678`.
- **Brokers**: Valkey exporters on port `9121`.
