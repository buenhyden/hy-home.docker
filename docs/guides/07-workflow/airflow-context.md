---
layer: infra
---
# Apache Airflow System Context

**Overview (KR):** Airflow 서비스의 전체 시스템 컨텍스트 — 프로파일, 시크릿, 볼륨, 네트워킹, 모니터링 파이프라인을 포함합니다.

> **Component**: `airflow`
> **Profile**: `workflow` (all core services)
> **Image**: `apache/airflow:slim-3.1.6` (custom tag via `AIRFLOW_IMAGE_NAME`)

## 1. Architecture Overview (Airflow 3.x)

Airflow 3.x separates the web layer (API server) from the DAG file parsing layer (DAG processor). This is a departure from the 2.x model where the webserver handled both.

| Service | Container Name | Role |
| --- | --- | --- |
| `airflow-apiserver` | `airflow-apiserver` | REST API (`/api/v2`) and Airflow UI |
| `airflow-scheduler` | `airflow-scheduler` | Trigger DAG runs, monitor task status |
| `airflow-dag-processor` | `airflow-dag-processor` | Parse Python DAG files, detect new DAGs |
| `airflow-worker` | `airflow-worker` | Execute tasks via CeleryExecutor |
| `airflow-triggerer` | `airflow-triggerer` | Manage deferred (async) operators |
| `airflow-valkey` | `airflow-valkey` | Celery message broker (Valkey 9.x) |
| `airflow-valkey-exporter` | `airflow-valkey-exporter` | Export Valkey metrics to Prometheus |
| `airflow-statsd-exporter` | `airflow-statsd-exporter` | Translate Airflow StatsD → Prometheus |
| `airflow-init` | *(one-shot job)* | DB migration + admin user creation |

Optional services (separate profiles):
- **`airflow-cli`** — profile `debug`: interactive Airflow CLI shell.
- **`flower`** — profile `flower`: Celery worker monitoring UI at `flower.${DEFAULT_URL}`.

## 2. Profile Activation

```bash
# Start core Airflow stack
docker compose --profile workflow up -d

# Include Flower monitoring
docker compose --profile workflow --profile flower up -d
```

Airflow is **disabled by default**. The `workflow` profile must be present to start any Airflow container.

## 3. Secrets

All sensitive values are injected via Docker secrets (files in `/run/secrets/`). Commands (`_CMD` suffix env vars) dynamically read secret files at runtime.

| Secret | Env Var Pattern | Purpose |
| --- | --- | --- |
| `airflow_db_password` | `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_CMD` | PostgreSQL metadata DB connection |
| `airflow_fernet_key` | `AIRFLOW__CORE__FERNET_KEY_CMD` | Fernet encryption for Variables/Connections |
| `airflow_www_password` | `_AIRFLOW_WWW_USER_PASSWORD_CMD` | Admin UI user password (set during init) |
| `airflow_valkey_password` | `AIRFLOW__CELERY__BROKER_URL_CMD` | Valkey broker authentication |

## 4. Volumes and Bind Mounts

All data volumes bind-mount to host paths under `${DEFAULT_WORKFLOW_DIR}/airflow/`:

| Volume | Host Path | Container Path | Contents |
| --- | --- | --- | --- |
| `airflow-dags` | `…/airflow/dags` | `/opt/airflow/dags` | Python DAG files |
| `airflow-logs` | `…/airflow/logs` | `/opt/airflow/logs` | Task execution logs |
| `airflow-config` | `…/airflow/config` | `/opt/airflow/config` | `airflow.cfg` overrides |
| `airflow-plugins` | `…/airflow/plugins` | `/opt/airflow/plugins` | Custom operator plugins |
| `airflow-valkey-data` | *(named volume)* | `/data` | Valkey AOF persistence |

## 5. Networking

All services attach to the shared `infra_net` bridge network. No ports are exposed to the host directly — Traefik handles inbound routing.

| Endpoint | URL | Notes |
| --- | --- | --- |
| Airflow UI / API | `https://airflow.${DEFAULT_URL}` | Port `8080` internally |
| Flower UI | `https://flower.${DEFAULT_URL}` | Port `5555`, SSO-protected |
| Scheduler health | `http://airflow-scheduler:8974/health` | Internal only |

## 6. Metrics Pipeline (StatsD → Prometheus)

Airflow emits metrics via StatsD protocol. The `airflow-statsd-exporter` translates them into Prometheus format.

```
airflow services → StatsD UDP :9125 → airflow-statsd-exporter → Prometheus scrape :9102
```

Key metric mappings (defined in `config/statsd_mapping.yml`):
- `airflow_scheduler_tasks_running`
- `airflow_executor_queued_tasks`
- `airflow_dag_task_duration{dag_id, task_id}`

The `airflow-valkey-exporter` separately exposes Valkey queue depth and memory usage at `:9121`.

## 7. Initialization Bootstrap

The `airflow-init` container runs once before the main services start:

1. Creates required directories (`/opt/airflow/{logs,dags,plugins,config}`).
2. Runs `airflow db migrate` via `_AIRFLOW_DB_MIGRATE: 'true'`.
3. Creates the admin user via `_AIRFLOW_WWW_USER_CREATE: 'true'`.
4. Fixes directory ownership to `AIRFLOW_UID:0`.

All core services `depends_on: airflow-init: condition: service_completed_successfully`.

## 8. Configuration

The main Airflow config lives at `${DEFAULT_WORKFLOW_DIR}/airflow/config/airflow.cfg`. Key env-driven settings:

| Variable | Value |
| --- | --- |
| `AIRFLOW__CORE__EXECUTOR` | `CeleryExecutor` |
| `AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION` | `true` |
| `AIRFLOW__CORE__LOAD_EXAMPLES` | `false` |
| `AIRFLOW__WEBSERVER__BASE_URL` | `https://airflow.${DEFAULT_URL}` |
| `AIRFLOW__METRICS__STATSD_ON` | `true` |
