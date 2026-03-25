<!-- [ID:04-data:mng-db] -->
# Management Databases (mng-db)

> Shared database and cache services for infrastructure components.

## 1. Context (SSoT)

The `mng-db` stack provides essential persistence and caching for core infrastructure services (Keycloak, n8n, Airflow). Consolidating these requirements reduces resource overhead and simplifies backup/restore for the platform's control plane.

- **Status**: Production / Core
- **Upstream**: `infra/01-management`
- **SSoT Documentation**: [docs/07.guides/04-data/01.core-dbs.md](../../../docs/07.guides/04-data/01.core-dbs.md)

## 2. Structure

```text
mng-db/
├── docker-compose.yml   # Stack definition
├── pg/                  # PostgreSQL config & init scripts
└── valkey/              # Valkey configuration
```

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **mng-pg** | PostgreSQL 17 | Management SQL |
| **mng-valkey** | Valkey 9.0 | Shared Session/Cache |
| **redisinsight** | RedisInsight | Redis/Valkey GUI |

## 4. Configuration (Secrets & Env)

- **Secrets**: Uses `POSTGRES_PASSWORD_FILE` and `VALKEY_PASSWORD_FILE`.
- **Initialization**: `mng-pg-init` executes `init_users_dbs.sql` to prepare app-specific databases.
- **SSO**: RedisInsight is protected by `sso-auth@file` middleware.

## 5. Persistence

- **Postgres**: `${DEFAULT_MANAGEMENT_DIR}/pg`
- **Valkey**: `${DEFAULT_MANAGEMENT_DIR}/valkey`

## 6. Operational Status

- **Postgres**: `mng-pg:5432`
- **Valkey**: `mng-valkey:6379`
- **RedisInsight**: `https://redisinsight.${DEFAULT_URL}`

---
Copyright (c) 2026. Licensed under the MIT License.
