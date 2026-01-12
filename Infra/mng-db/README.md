# Management Databases Infrastructure

## Overview

This directory contains the configuration for shared management databases used by various platform services. Despite the folder name `mng-db` (historically "Management DB"), it currently hosts **Valkey** (Redis alternative) and **PostgreSQL**.

## Services

### 1. Valkey (`mng-valkey`)

A high-performance key-value store (fork of Redis).

- **Image**: `valkey/valkey:9.0.1-alpine`
- **Port**: `${VALKEY_PORT}` (Exposed to Infra settings)
- **Security**: Password protected via Docker Secret `valkey_password`.
- **Exporter**: `mng-valkey-exporter` exposed on `${VALKEY_EXPORTER_PORT}`.

### 2. PostgreSQL (`mng-pg`)

A powerful, open-source object-relational database system.

- **Image**: `postgres:17-bookworm`
- **Port**: `${POSTGRES_PORT}`
- **Security**: Superuser password set via `${PGPASSWORD_SUPERUSER}`.
- **Initialization**: A dedicated sidecar container `mng-pg-init` waits for the DB to be ready and runs `init_users_dbs.sql` to provision users and databases.
- **Exporter**: `mng-pg-exporter` exposed on `${POSTGRES_EXPORTER_PORT}`.

### 3. RedisInsight (`redisinsight`)

A GUI for managing and visualizing data in Valkey/Redis.

- **Image**: `redis/redisinsight:3.0.1`
- **Network**: `infra_net`
- **Traefik**: Exposed at `redisinsight.${DEFAULT_URL}` with **SSO Authentication**.

## Environment Variables

| Service | Variable | Description | Default |
| :--- | :--- | :--- | :--- |
| **Valkey** | Secret `valkey_password` | Master/Replica Password | via Docker Secret |
| **PostgreSQL**| `POSTGRES_USER` | Valid User | `${POSTGRES_USER}` |
| **PostgreSQL**| `POSTGRES_PASSWORD` | Superuser Password | `${PGPASSWORD_SUPERUSER}` |
| **PostgreSQL**| `POSTGRES_DB` | Init Database | `${POSTGRES_DB}` |
| **Init** | `PGPASSWORD_SUPERUSER` | Auth for Script | `${PGPASSWORD_SUPERUSER}` |

## Networking

All services are assigned **Static IPs** in the `infra_net` network for reliable discovery:

| Service | Static IPv4 |
| :--- | :--- |
| **Valkey** | `172.19.0.70` |
| **Valkey Exporter** | `172.19.0.71` |
| **PostgreSQL** | `172.19.0.72` |
| **PostgreSQL Exporter** | `172.19.0.73` |
| **RedisInsight** | `172.19.0.68` |

## Data Persistence

- **Valkey**: `mng-valkey-data` (Mapped to `/data`)
- **PostgreSQL**: `mng-pg-data` (Mapped to `/var/lib/postgresql/data`)
- **RedisInsight**: `redisinsight-data` (Mapped to `/db`)

## Usage

### Connecting to Valkey (Internal)

```bash
valkey-cli -h mng-valkey -p 6379 -a <server_password>
```

### Connecting to PostgreSQL (Internal)

```bash
psql -h mng-pg -U postgres
```
