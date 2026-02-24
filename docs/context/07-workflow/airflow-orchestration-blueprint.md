# Apache Airflow Orchestration Blueprint

> **Component**: `airflow`
> **Executor**: `CeleryExecutor`
> **Backend**: PostgreSQL + Redis

## 1. Service Architecture

Airflow is deployed as a multi-component cluster to support high-throughput DAG processing.

### Technical Specifications

| Component | Function | Internal Port |
| --- | --- | --- |
| `airflow-webserver` | UI and API Service | `8080` |
| `airflow-scheduler` | DAG Scheduling | `8974` |
| `airflow-worker` | Task Execution | - |
| `airflow-triggerer`| Deferred Operators | - |
| `statsd-exporter`  | Telemetry Bridge | `9125` (StatsD) |

### Persistence Layer

- **Metadata DB**: `postgres` (via `pg-router`)
- **Result Backend**: `postgres`
- **Broker**: `redis` (or unified `mng-redis`)

## 2. Initialization & Bootstrapping

The environment is strictly initialized by the `airflow-init` container.

### Provisioning Workflow

1. **DB Migration**: `airflow-init` runs `airflow db migrate`.
2. **User Creation**: Creates the administrative user from `airflow_www_password` secret.
3. **Permission Fix**: Repairs directory ownership for `${DEFAULT_AIRFLOW_DIR}`.

### Verification

```bash
docker logs airflow-init
```

## 3. Maintenance

### Log Inspection

Worker task logs are persisted to `${DEFAULT_AIRFLOW_DIR}/logs`.

### DAG Deployment

Mount or sync Python files to `${DEFAULT_AIRFLOW_DIR}/dags`.
