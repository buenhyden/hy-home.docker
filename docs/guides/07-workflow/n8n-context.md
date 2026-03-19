---
layer: infra
---
# n8n System Context

**Overview (KR):** n8n 서비스의 전체 시스템 컨텍스트 — 커스텀 이미지, 외부 태스크 러너, 시크릿, 볼륨, 메트릭 구성을 포함합니다.

> **Component**: `n8n`
> **Activation**: Opt-in (disabled by default — uncomment include in root `docker-compose.yml`)
> **Execution Mode**: Queue mode via `n8n-valkey`

## 1. Service Overview

| Service | Container | Image | Role |
| --- | --- | --- | --- |
| `n8n` | `n8n` | `n8nio/n8n:2.12.3` | Main engine, UI, webhook receiver |
| `n8n-worker` | `n8n-worker` | `n8nio/n8n:2.12.3` | Executes queued workflow jobs |
| `n8n-task-runner` | `n8n-task-runner` | `n8nio/runners:2.12.3` | External process for Code nodes |
| `n8n-valkey` | `n8n-valkey` | `valkey/valkey:9.0.2-alpine` | Bull queue broker |
| `n8n-valkey-exporter` | `n8n-valkey-exporter` | `oliver006/redis_exporter` | Valkey metrics for Prometheus |

## 2. Custom Dockerfile

The `Dockerfile` in `infra/07-workflow/n8n/` extends the official `n8nio/n8n` image with:

- **CJK font support** (Noto CJK, Noto Emoji, DejaVu, Liberation) — required for PDF/image generation nodes that handle Korean, Chinese, or Japanese content.
- **Python 3 + pip + build-base** — enables the "Execute Command" node to run Python scripts directly.
- **`n8n-cli`** — global npm package for administrative tasks.
- **Custom node directory** (`/home/node/.n8n/custom`) — pre-created and owned by the `node` user.

> [!NOTE]
> The `Dockerfile` uses `ARG N8N_VERSION=2.12.3` as a default. The `docker-compose.yml` overrides this with the pinned image `n8nio/n8n:2.12.3` directly (not building from the Dockerfile). The Dockerfile is available for custom builds when additional packages or nodes are needed.

## 3. External Task Runner

n8n uses an external task runner (`N8N_RUNNERS_MODE: external`) instead of spawning subprocesses inside the main container.

```
n8n / n8n-worker → TCP broker → n8n-task-runner
```

Key environment variables:
- `N8N_RUNNERS_ENABLED: true`
- `N8N_RUNNERS_BROKER_LISTEN_ADDRESS: 0.0.0.0`
- `N8N_RUNNERS_AUTH_TOKEN_FILE: /run/secrets/n8n_runner_auth_token`
- `N8N_RUNNER_TASK_TIMEOUT: 300`
- `N8N_NATIVE_PYTHON_RUNNER: true`

The task runner runs isolated Python/JavaScript tasks without polluting the main n8n process memory.

## 4. Queue Mode Architecture

n8n runs in `EXECUTIONS_MODE: queue`. The main `n8n` process receives webhooks and enqueues jobs. Workers pull from the queue and execute them.

```
External webhook → n8n (main) → n8n-valkey queue → n8n-worker → n8n-task-runner
```

Key queue configuration:
- `QUEUE_BULL_REDIS_HOST: n8n-valkey`
- `QUEUE_BULL_REDIS_PORT: 6379`
- `QUEUE_BULL_PREFIX: n8n`
- Health check: `QUEUE_HEALTH_CHECK_ACTIVE: true`

## 5. Secrets

| Secret | Purpose |
| --- | --- |
| `n8n_db_password` | PostgreSQL connection (`DB_POSTGRESDB_PASSWORD_FILE`) |
| `n8n_encryption_key` | Credential encryption (`N8N_ENCRYPTION_KEY_FILE`) |
| `n8n_valkey_password` | Valkey queue auth (`QUEUE_BULL_REDIS_PASSWORD_FILE`) |
| `n8n_runner_auth_token` | Task runner auth (`N8N_RUNNERS_AUTH_TOKEN_FILE`) |

## 6. Volumes and Bind Mounts

| Volume | Host Path | Container Path | Contents |
| --- | --- | --- | --- |
| `n8n-data` | `${DEFAULT_WORKFLOW_DIR}/n8n` | `/home/node/.n8n` | n8n data, workflows, credentials |
| `n8n-task-runner-data` | `${DEFAULT_WORKFLOW_DIR}/n8n-task-runner` | `/home/node/.n8n` | Task runner working directory |
| `n8n-valkey-data` | `${DEFAULT_WORKFLOW_DIR}/valkey` | `/data` | Valkey AOF persistence |

The `custom/` directory is bind-mounted into both `n8n` and `n8n-worker` at `/home/node/.n8n/custom` for custom node development.

## 7. Networking and URLs

| Endpoint | URL | Notes |
| --- | --- | --- |
| n8n UI / Webhooks | `https://n8n.${DEFAULT_URL}` | Port `5678` internally |
| Prometheus metrics | `http://n8n:5678/metrics` | Enabled via `N8N_METRICS: true` |

Webhook URLs must use the external domain: `WEBHOOK_URL: https://n8n.${DEFAULT_URL}`.

## 8. Metrics

n8n exports Prometheus metrics at `/metrics`:
- `N8N_METRICS: true`
- `N8N_METRICS_PREFIX: n8n_`
- `N8N_METRICS_INCLUDE_WORKFLOW_ID_LABEL: true`
- `N8N_METRICS_INCLUDE_NODE_TYPE_LABEL: true`
- `N8N_METRICS_INCLUDE_QUEUE_METRICS: true`

`n8n-valkey-exporter` exposes Valkey queue depth as a separate Prometheus scrape target at `:9121`.

## 9. Database

n8n uses management PostgreSQL (`DB_TYPE: postgresdb`) with a dedicated `n8n` database:

```
DB_POSTGRESDB_HOST: ${POSTGRES_MNG_HOSTNAME}
DB_POSTGRESDB_DATABASE: n8n
DB_POSTGRESDB_USER: ${N8N_DB_USER}
```

All workflow definitions, execution history, and credentials are stored in PostgreSQL.
