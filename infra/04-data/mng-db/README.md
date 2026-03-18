# Management Databases (mng-db)

This stack provides shared database services for internal infrastructure components (e.g., Keycloak, n8n, Airflow).

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `mng-valkey` | `valkey/valkey:9.0.2-alpine`| Shared Session/Cache | 0.5 CPU / 512MB |
| `mng-pg` | `postgres:17-bookworm` | Management SQL | 1.0 CPU / 1GB RAM |
| `redisinsight`| `redis/redisinsight:3.0.3` | Redis/Valkey GUI | 0.5 CPU / 512MB |
| `exporters` | `redis_exporter`, `postgres_exporter` | Metrics | 128MB ea |

## Networking

- **Internal DNS (infra_net)**:
  - Postgres: `mng-pg:${POSTGRES_PORT:-5432}`
  - Valkey: `mng-valkey:${VALKEY_PORT:-6379}`
- **External URL (Traefik)**:
  - RedisInsight: `https://redisinsight.${DEFAULT_URL}`

## Persistence

- **Valkey**: `${DEFAULT_MANAGEMENT_DIR}/valkey`
- **Postgres**: `${DEFAULT_MANAGEMENT_DIR}/pg`
- **Insights**: `${DEFAULT_MANAGEMENT_DIR}/redisinsight`

## Configuration

- **Auth**: `redisinsight` is protected by `sso-auth@file` (Keycloak).
- **Postgres Init**: `mng-pg-init` automatically runs `init_users_dbs.sql`.

| Variable           | Description           | Value                  |
| :----------------- | :-------------------- | :--------------------- |
| `POSTGRES_PASSWORD_FILE`| Root DB Password file | `/run/secrets/mng_postgres_password` |

## File Map

| Path                 | Description                                |
| -------------------- | ------------------------------------------ |
| `docker-compose.yml` | Shared DB + Cache stack definition.        |
| `README.md`          | Documentation for shared access policies.   |
