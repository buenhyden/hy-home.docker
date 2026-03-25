# Management Database (mng-db)

> Shared core database and cache for platform management services.

## Overview

A lightweight, shared persistence instance for management tier services (e.g., identity, monitoring meta-data). It provides a standalone PostgreSQL instance and a single-node Valkey cache for non-HA critical management data during the initial bootstrap phase.

## Audience

- Platform Ops (Bootstrap & Management)
- SREs (Metadata maintenance)

## Scope

- Shared PostgreSQL instance
- Shared Valkey instance
- Initial SQL bootstrap for platform accounts

## Structure

```text
mng-db/
├── pg/                 # PostgreSQL init scripts
├── valkey/             # Valkey data (ephemeral cache)
└── docker-compose.yml  # Service orchestration
```

## How to Work in This Area

1. Check `pg/init-scripts/init_users_dbs.sql` for initial credentials.
2. Use the [Data Runbook](../../../docs/09.runbooks/04-data/README.md) for backup tasks.

## Configuration

| Variable | Target | Description |
| :--- | :--- | :--- |
| `POSTGRES_DB` | pg | Management root DB |
| `VALKEY_PORT` | valkey | Shared cache port |

## Testing

```bash
# Test pg connectivity
docker exec mng-db-pg pg_isready
```

## Change Impact

- Restarting `mng-db` will impact all management services relying on shared state.
- This is NOT an HA service; use `postgresql-cluster` for production workloads.

## AI Agent Guidance

1. This database is primarily for platform metadata; avoid storing large datasets here.
2. Ensure `mng-db` is healthy before starting `02-auth` services.
