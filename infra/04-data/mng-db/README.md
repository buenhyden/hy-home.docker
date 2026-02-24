# Management Databases (mng-db)

This stack provides shared database services for internal infrastructure components (e.g., Keycloak, n8n, Airflow).

## Services

| Service        | Image                           | Role               | Resources         |
| :------------- | :------------------------------ | :----------------- | :---------------- |
| `mng-db`       | `postgres:17.2-alpine`          | Shared SQL DB      | 0.5 CPU / 1GB RAM |
| `mng-valkey`   | `valkey/valkey:8.0.2`           | Shared Cache       | 0.2 CPU / 256MB   |
| `redisinsight` | `redis/redisinsight:latest`     | Cache GUI          | 0.2 CPU / 256MB   |

## Networking

| Service        | Internal Port | Endpoint                  |
| :------------- | :------------ | :------------------------ |
| `mng-db`       | `5432`        | `mng-db:5432`             |
| `redisinsight` | `5540`        | `redis.${DEFAULT_URL}`    |

## Persistence

- **PostgreSQL**: Mounted to `mng-db-data`.
- **Valkey**: Mounted to `mng-valkey-data`.

## Configuration

Shared databases are initialized with multiple users/databases via the `init-db/` scripts or environment variables.

| Variable           | Description           | Value                  |
| :----------------- | :-------------------- | :--------------------- |
| `POSTGRES_PASSWORD`| Root DB Password      | `${POSTGRES_PASSWORD}` |

## File Map

| Path                 | Description                                |
| -------------------- | ------------------------------------------ |
| `docker-compose.yml` | Shared DB + Cache stack definition.        |
| `README.md`          | Documentation for shared access policies.   |
