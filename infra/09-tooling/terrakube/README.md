# Terrakube

Terrakube is an open-source alternative to Terraform Cloud and Terraform Enterprise.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `terrakube-api`| `api-server:2.29.0` | Backend API |
| `terrakube-ui` | `terrakube-ui:2.29.0`| Frontend GUI|
| `executor` | `executor:2.29.0` | Task Runner |

## Networking

- **UI**: `terrakube-ui.${DEFAULT_URL}`
- **API**: `terrakube-api.${DEFAULT_URL}`
- **Runner**: `terrakube-executor.${DEFAULT_URL}`

## Dependencies

- **IdP**: Keycloak (`infra/02-auth/keycloak`).
- **Store**: MinIO (`infra/04-data/minio`) for state/outputs.
- **Cache**: Management Valkey (`infra/04-data/mng-db`).

## Persistence

- **Database**: PostgreSQL (via `infra/04-data/mng-db`).
- **Object Storage**: MinIO (`infra/04-data/minio`) for state and plan logs.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and workflow docs. |
