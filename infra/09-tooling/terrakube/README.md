# Terrakube

Terrakube is an open-source alternative to Terraform Cloud and Terraform Enterprise.

## Services

| Service             | Image                       | Role              |
| :---                | :---                        | :---              |
| `terrakube-api`     | `api-server:2.29.0`         | Backend API       |
| `terrakube-ui`      | `terrakube-ui:2.29.0`       | Frontend GUI      |
| `terrakube-executor`| `executor:2.29.0`           | Task Runner       |

## Networking

- **UI**: `terrakube-ui.${DEFAULT_URL}`
- **API**: `terrakube-api.${DEFAULT_URL}`
- **Runner**: `terrakube-executor.${DEFAULT_URL}`

## Dependencies

- **IdP**: Keycloak (`infra/02-auth/keycloak`) — OIDC/DEX validation.
- **Store**: MinIO (`infra/04-data/minio`) — Terraform state files and plan output logs.
- **Cache**: Management Valkey (`infra/04-data/mng-db`) — Distributed job locking.
- **Database**: Management PostgreSQL (`infra/04-data/mng-db`).

## Persistence

- **Database**: PostgreSQL (via `infra/04-data/mng-db`). Database: `terrakube`, user: `${TERRAKUBE_DB_USERNAME}`.
- **Object Storage**: MinIO (`infra/04-data/minio`) for state and plan logs. Bucket: `tfstate`.

## Secrets

| Secret                   | Description                                              |
| :---                     | :---                                                     |
| `terrakube_db_password`  | PostgreSQL password for the `terrakube` database.        |
| `terrakube_pat_secret`   | Personal Access Token signing secret.                    |
| `terrakube_internal_secret` | Shared secret between API and Executor nodes.         |
| `terrakube_valkey_password` | Password for management Valkey (Redis-compat) cache.  |
| `minio_app_user_password`| MinIO app-user password for state storage.               |

## File Map

| Path                | Description                                    |
| ------------------- | ---------------------------------------------- |
| `docker-compose.yml`| Service definitions for API, UI, and Executor. |
| `README.md`         | Service overview and workflow docs.            |
