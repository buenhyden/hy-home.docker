---
layer: infra
---
# Workflow Stack Lifecycle Guide

**Overview (KR):** n8n과 Airflow의 시작, 업그레이드, DAG 배포, 스케일 아웃 등 전체 라이프사이클 절차 가이드입니다.

> Covers operational procedures for both n8n and Apache Airflow running under `infra/07-workflow/`.

---

## Airflow Lifecycle

### Startup Order

The `airflow-init` job must complete before any other Airflow service starts. Docker Compose enforces this via `depends_on: condition: service_completed_successfully`.

Recommended startup sequence:
```
airflow-valkey → airflow-init → airflow-apiserver → airflow-scheduler
                                                  → airflow-dag-processor
                                                  → airflow-worker
                                                  → airflow-triggerer
```

Start the full stack:
```bash
docker compose --profile workflow up -d
```

Verify init completed cleanly:
```bash
docker logs airflow-init
docker exec airflow-scheduler airflow jobs check --job-type SchedulerJob
```

### DAG Deployment

DAGs are Python files placed in `${DEFAULT_WORKFLOW_DIR}/airflow/dags`. Both the scheduler and the dag-processor watch this directory.

```bash
# Copy a new DAG
cp my_pipeline.py ${DEFAULT_WORKFLOW_DIR}/airflow/dags/

# Verify it parsed without errors (within ~30 seconds)
docker exec airflow-apiserver airflow dags list
docker exec airflow-apiserver airflow dags list-import-errors
```

File changes are picked up automatically — no restart required. The `airflow-dag-processor` polls the DAGs directory and the scheduler receives updates via the internal execution API.

### Database Migration (Version Upgrade)

Before upgrading the `AIRFLOW_IMAGE_NAME`:

1. Stop all Airflow services (keep `airflow-valkey` running to preserve queued tasks).
2. Update `AIRFLOW_IMAGE_NAME` in your environment.
3. Run migration via `airflow-init`:

```bash
docker compose --profile workflow up airflow-init
docker logs -f airflow-init
```

4. Once init exits with code 0, start the rest:
```bash
docker compose --profile workflow up -d
```

### Scaling Workers

Airflow workers are stateless. Add replicas without restarting other services:

```bash
docker compose --profile workflow up -d --scale airflow-worker=3
```

> Memory limits are set at `1G` per worker in `common-optimizations.yml`. Adjust with `docker update` or in the compose if OOM becomes an issue on heavy DAGs.

### Celery Queue Inspection

```bash
# Check active workers
docker exec airflow-worker celery -A airflow.providers.celery.executors.celery_executor.app inspect active

# Clear stuck tasks from Valkey (use with caution)
docker exec airflow-valkey valkey-cli -a "$(cat /run/secrets/airflow_valkey_password)" FLUSHDB
```

### Airflow Admin Operations

```bash
# Create a new admin user
docker exec airflow-apiserver airflow users create \
  --username user --password pass --role Admin \
  --email user@example.com --firstname First --lastname Last

# Reset a fernet-encrypted variable
docker exec airflow-apiserver airflow variables set MY_VAR "value"
```

---

## n8n Lifecycle

### Startup Order

n8n requires its Valkey broker to be healthy before either the main engine or the worker starts.

```
n8n-valkey → n8n → n8n-worker
                 → n8n-task-runner
```

Enable n8n (uncommenting the include in root `docker-compose.yml`) then start:
```bash
docker compose up -d n8n-valkey n8n n8n-worker n8n-task-runner n8n-valkey-exporter
```

Health check:
```bash
docker exec n8n wget -q --spider http://localhost:5678/healthz && echo "healthy"
```

### Workflow Export Before Upgrade

Before upgrading the n8n image version:

1. Export all workflows:
```bash
# Via API (requires API key or basic auth)
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  https://n8n.${DEFAULT_URL}/api/v1/workflows \
  -o workflows-backup-$(date +%Y%m%d).json
```

2. Also export credentials list (values are encrypted and non-exportable, but names are):
```bash
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  https://n8n.${DEFAULT_URL}/api/v1/credentials
```

3. Snapshot the PostgreSQL `n8n` database:
```bash
docker exec mng-pg pg_dump -U ${N8N_DB_USER} n8n > n8n-db-$(date +%Y%m%d).sql
```

### Upgrading n8n

After backup:
1. Update the image tag in `docker-compose.yml` (`n8nio/n8n:NEW_VERSION`).
2. Update `n8n-task-runner` image tag to match (`n8nio/runners:NEW_VERSION`).
3. Restart with the new image:
```bash
docker compose up -d --force-recreate n8n n8n-worker n8n-task-runner
```

n8n auto-migrates its PostgreSQL schema on first start.

### Scaling n8n Workers

Workers are stateless — add more without restarting the main `n8n` process:

```bash
docker compose up -d --scale n8n-worker=3
```

The `n8n-valkey` Bull queue distributes jobs across all registered workers automatically.

### Webhook Troubleshooting

If external webhooks (GitHub, Stripe, etc.) fail to reach n8n:
1. Verify `WEBHOOK_URL` matches `https://n8n.${DEFAULT_URL}`.
2. Confirm Traefik is routing correctly:
```bash
curl -I https://n8n.${DEFAULT_URL}/healthz
```
3. Check `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS` — if using Docker volume mounts, this may need to be `false` to allow n8n to write settings.

---

## Monitoring

### Airflow
- **StatsD metrics** → `airflow-statsd-exporter` → Prometheus (port `9102`).
- **Valkey queue depth** → `airflow-valkey-exporter` → Prometheus (port `9121`).
- **Scheduler health** → `http://airflow-scheduler:8974/health`.

### n8n
- **Prometheus metrics** → `http://n8n:5678/metrics`.
- **Valkey queue stats** → `n8n-valkey-exporter` → Prometheus (port `9121`).

See `docs/guides/07-workflow/workflow-operations.md` for incident tracking and operational history.
