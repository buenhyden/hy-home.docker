# Terrakube

Terrakube is an open-source alternative to Terraform Cloud and Terraform Enterprise.

## Services

| Service              | Image                         | Role           | Resources       |
| :------------------- | :---------------------------- | :------------- | :-------------- |
| `terrakube-api`      | `terrakube/api:latest`        | Backend API    | 0.5 CPU / 1GB RAM |
| `terrakube-ui`       | `terrakube/ui:latest`         | Management UI  | 0.2 CPU / 256MB |
| `terrakube-executor` | `terrakube/executor:latest`   | Job Runner     | 1 CPU / 1GB RAM |

## Networking

Exposed via Traefik at `terrakube.${DEFAULT_URL}`.

## Persistence

- **Database**: PostgreSQL (via `infra/04-data/mng-db`).
- **Object Storage**: MinIO (`infra/04-data/minio`) for state and plan logs.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and workflow docs. |
