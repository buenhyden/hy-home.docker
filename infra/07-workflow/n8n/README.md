# n8n

n8n is a low-code workflow automation tool that allows you to connect any app.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `n8n` | `n8nio/n8n:2.12.3` | Main engine | 1.0 CPU / 2G |
| `n8n-worker` | `n8nio/n8n:2.12.3` | Job worker | 1.0 CPU / 2G |
| `n8n-task-runner` | `n8nio/runners:2.12.3` | External task runner | 0.5 CPU / 1G |
| `n8n-valkey` | `valkey/valkey:9.0.2-alpine` | Queue broker | 0.5 CPU / 0.5G |
| `n8n-valkey-exporter` | `oliver006/redis_exporter` | Valkey metrics | - |

## Networking

Exposed via Traefik at `n8n.${DEFAULT_URL}`.

> [!NOTE]
> `n8n` is not enabled in the root `docker-compose.yml` by default. Enable it by uncommenting the `infra/07-workflow/n8n/docker-compose.yml` include entry.

## Persistence

- **Database**: PostgreSQL (`mng-pg`) via `DB_TYPE: postgresdb`.
- **Data**: `${DEFAULT_WORKFLOW_DIR}/n8n` → `/home/node/.n8n` (volume: `n8n-data`).
- **Task Runner**: `${DEFAULT_WORKFLOW_DIR}/n8n-task-runner` → `/home/node/.n8n` (volume: `n8n-task-runner-data`).
- **Valkey**: `${DEFAULT_WORKFLOW_DIR}/valkey` → `/data` (volume: `n8n-valkey-data`).

## Secrets

| Secret | Purpose |
| :--- | :--- |
| `n8n_db_password` | PostgreSQL connection |
| `n8n_encryption_key` | Credential encryption |
| `n8n_valkey_password` | Valkey queue auth |
| `n8n_runner_auth_token` | Task runner auth |

## File Map

| Path                   | Description                              |
| ---------------------- | ---------------------------------------- |
| `docker-compose.yml`   | n8n service and env configuration.       |
| `Dockerfile`           | Custom image with CJK fonts and Python3. |
| `docker-entrypoint.sh` | Entrypoint with custom cert support.     |
| `custom/`              | Custom n8n nodes (mounted into container). |
| `README.md`            | Service overview and usage notes.        |
