# Airflow Celery Recovery Runbook

> **Service**: `airflow`
> **Profile**: `airflow`, `flower`
> **Scenario**: Task queues are frozen, DAGs remain in "running" state indefinitely, or workers are unreachable.

## 1. Prerequisites

- Target Environment: Local Docker Compose/WSL
- Required Tools: `docker`, `docker compose`, `curl`

## 2. Assessment Steps

1. Verify Broker (Valkey) Connection:

   ```bash
   docker compose -f docker-compose.yml --profile airflow exec airflow-webserver celery inspect ping -A airflow.providers.celery.executors.celery_executor.app
   ```

2. Check `Flower` UI (if active) at `http://localhost:5555` to analyze worker nodes.

## 3. Remediation

### Scenario A: Unresponsive Celery Worker

Usually caused by OOM (Out of Memory) or zombie processes.

```bash
docker compose -f docker-compose.yml --profile airflow restart airflow-worker
```

### Scenario B: Stuck Tasks in Database

If tasks are marked as queued but never picked up after a broker failure.

```bash
docker compose -f docker-compose.yml --profile airflow exec airflow-webserver airflow tasks clear -s [START_DATE] -e [END_DATE] [DAG_ID]
```

## 4. Rollback

If the whole orchestrator state is corrupted, revert to a clean state (WARNING: This loses history unless volume data is backed up):

```bash
docker compose -f docker-compose.yml --profile airflow down
# CAUTION: Removing volumes
docker volume rm hy-home-docker_airflow-metadata
docker compose -f docker-compose.yml --profile airflow up -d
```
