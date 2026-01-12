# Management Databases

## Overview

Shared database infrastructure for management tools, including **Valkey** (Redis fork) and **PostgreSQL**.

## Service Details

### Valkey (`mng-valkey`)

- **Image**: `valkey/valkey:9.0.1-alpine`
- **Port**: `${VALKEY_PORT}` (Internal)
- **Secrets**: `valkey_password`
- **Exporter**: `mng-valkey-exporter` (Port `${VALKEY_EXPORTER_PORT}`)

### PostgreSQL (`mng-pg`)

- **Image**: `postgres:17-bookworm`
- **Port**: `${POSTGRES_PORT}` (Internal)
- **Init**: Uses `mng-pg-init` to run `init_users_dbs.sql`.
- **Exporter**: `mng-pg-exporter` (Port `${POSTGRES_EXPORTER_PORT}`)

### RedisInsight (`redisinsight`)

- **Image**: `redis/redisinsight:3.0.1`
- **Purpose**: GUI for managing Redis/Valkey.
- **Traefik**: `redisinsight.${DEFAULT_URL}` (with SSO).

## Networks

- Static IPs assigned in `infra_net` (e.g., `172.19.0.70`, `172.19.0.72`).
