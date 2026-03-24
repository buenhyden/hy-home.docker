---
layer: infra
---

# Workflow Tier: Usage & Operations

Operational guidelines for managing internal automation flows via n8n and Apache Airflow.

## 1. n8n Operations

### Workflow Deployment
1. Import via UI (JSON).
2. Set `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false` if mounting from non-root host.

### Performance Monitoring
- Keep `n8n-worker` queue backlog below 1,000 items.
- Monitor `n8n-task-runner` for OOM errors in Code nodes.

## 2. Airflow Operations

### DAG Deployment
1. Place Python DAG files in `${DEFAULT_WORKFLOW_DIR}/airflow/dags`.
2. Wait 30-60s for `airflow-dag-processor` to pick them up.
3. Enable the DAG in the UI (`https://airflow.${DEFAULT_URL}`).

### Troubleshooting
- **Import Errors**: Check "DAG Import Errors" in the UI banner.
- **Stuck Tasks**: Check `airflow-scheduler` logs for heartbeat failures.
- **Worker Crashes**: Verify `CeleryExecutor` connectivity to `airflow-valkey`.
