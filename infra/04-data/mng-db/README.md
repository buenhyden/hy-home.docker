<!-- [ID:04-data:mng-db] -->
# Management Databases (mng-db)

> Shared database and cache services for infrastructure components.

## Overview (KR)

이 스택은 Keycloak, n8n, Airflow와 같은 내부 인프라 컴포넌트를 위한 공유 데이터베이스 서비스를 제공합니다. PostgreSQL과 Valkey를 포함하며, RedisInsight를 통해 시각적으로 관리할 수 있습니다.

## Overview

The `mng-db` stack provides essential persistence and caching for core infrastructure services. By consolidating these requirements into a single management stack, we reduce resource overhead and simplify backup/restore procedures for the platform's control plane.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **mng-pg** | PostgreSQL 17 | Management SQL |
| **mng-valkey** | Valkey 9.0 | Shared Session/Cache |
| **redisinsight** | RedisInsight 3.0 | Redis/Valkey GUI |

## Networking

- **Internal DNS (infra_net)**:
  - Postgres: `mng-pg:5432`
  - Valkey: `mng-valkey:6379`
- **External URL**:
  - RedisInsight: `https://redisinsight.${DEFAULT_URL}` (Protected by SSO)

## Persistence

- **Postgres**: `${DEFAULT_MANAGEMENT_DIR}/pg`
- **Valkey**: `${DEFAULT_MANAGEMENT_DIR}/valkey`

## Configuration

- **Initialization**: `mng-pg-init` automatically executes `init_users_dbs.sql` on startup to prepare application-specific databases.
- **SSO Protection**: RedisInsight is integrated with the `sso-auth@file` middleware (Keycloak).

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Stack definition for core DBs. |
| `pg/` | PostgreSQL configuration and init scripts. |
| `valkey/` | Valkey configuration. |

---

## Documentation References

- [Core DB Guide](../../../docs/07.guides/04-data/01.core-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
