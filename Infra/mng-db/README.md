# Management Databases Infrastructure

## Overview

This directory contains the configuration for shared management databases used by various platform services. Despite the folder name `mng-db` (historically "Management DB"), it currently hosts **Valkey** (Redis alternative) and **PostgreSQL**.

## Services

### Valkey (`mng-valkey`)

- **Image**: `valkey/valkey:9.0.1-alpine`
- **Role**: High-performance key-value store (Redis fork)
- **Port**: `${VALKEY_PORT}`
- **Exports**: `${VALKEY_EXPORTER_PORT}` (Metrics)

### PostgreSQL (`mng-pg`)

- **Image**: `postgres:17-bookworm`
- **Role**: Relational Database
- **Port**: `${POSTGRES_PORT}`
- **Exports**: `${POSTGRES_EXPORTER_PORT}` (Metrics)

### RedisInsight (`redisinsight`)

- **Image**: `redis/redisinsight:3.0.1`
- **Role**: GUI for Valkey/Redis management

## Networking

All services are assigned **Static IPs** in the `infra_net` network for reliable discovery:

| Service | Static IPv4 |
| :--- | :--- |
| **Valkey** | `172.19.0.70` |
| **Valkey Exporter** | `172.19.0.71` |
| **PostgreSQL** | `172.19.0.72` |
| **PostgreSQL Exporter** | `172.19.0.73` |
| **RedisInsight** | `172.19.0.68` |

## Persistence

- **Valkey**: `mng-valkey-data` (Mapped to `/data`)
- **PostgreSQL**: `mng-pg-data` (Mapped to `/var/lib/postgresql/data`)
- **RedisInsight**: `redisinsight-data` (Mapped to `/db`)

## Configuration

### Secrets & Environment

| Service | Variable | Description | Default |
| :--- | :--- | :--- | :--- |
| **Valkey** | Secret `valkey_password` | Master/Replica Password | via Docker Secret |
| **PostgreSQL**| `POSTGRES_USER` | Valid User | `${POSTGRES_USER}` |
| **PostgreSQL**| `POSTGRES_PASSWORD` | Superuser Password | `${PGPASSWORD_SUPERUSER}` |
| **PostgreSQL**| `POSTGRES_DB` | Init Database | `${POSTGRES_DB}` |
| **Init** | `PGPASSWORD_SUPERUSER` | Auth for Script | `${PGPASSWORD_SUPERUSER}` |

## Traefik Integration

### RedisInsight

- **Domain**: `redisinsight.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Authentication**: **SSO Enabled** (via `sso-auth` middleware)

## Usage

### Connecting to Valkey (Internal)

```bash
valkey-cli -h mng-valkey -p 6379 -a <server_password>
```

### Connecting to PostgreSQL (Internal)

```bash
psql -h mng-pg -U postgres
```
