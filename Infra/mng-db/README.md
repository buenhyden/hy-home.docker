# Management Database Stack

## Overview

Centralized management databases (PostgreSQL & Valkey) used by various services like n8n and others.

## Services

- **mng-valkey**: Valkey (Redis compatible) server.
  - Port: `6379`
- **mng-valkey-exporter**: Prometheus exporter for Valkey metrics.
- **redisinsight**: GUI for Redis/Valkey.
  - URL: `https://redisinsight.${DEFAULT_URL}`
- **mng-pg**: PostgreSQL server.
  - Port: `${POSTGRES_PORT}`
- **mng-pg-init**: Initialization container for Postgres users/DBs.
- **mng-pg-exporter**: Prometheus exporter for Postgres metrics.

## Configuration

### Environment Variables

- `POSTGRES_PASSWORD`: Superuser password.
- `POSTGRES_USER`: Default user.
- `POSTGRES_DB`: Default DB.

### Volumes

- `mng-valkey-data`: `/data`
- `redisinsight-data`: `/db`
- `mng-pg-data`: `/var/lib/postgresql/data`
- `./init-scripts/init_users_dbs.sql`: Initialization script.

## Networks

- `infra_net`
  - mng-valkey: `172.19.0.70`
  - mng-pg: `172.19.0.72`
  - redisinsight: `172.19.0.68`

## Traefik Routing

- **RedisInsight**: `redisinsight.${DEFAULT_URL}` (SSO Enabled)
