# PostgreSQL HA Cluster

## Overview

A High Availability (HA) PostgreSQL cluster using **Patroni**, **etcd**, and **HAProxy**. It provides automatic failover, leader election, and read/write splitting.

## Architecture

1. **Distributed Configuration Store (DCS)**: 3-node **etcd** cluster for consensus.
2. **PostgreSQL Nodes**: 3-node **Patroni** cluster (1 Leader, 2 Replicas).
3. **Routing**: **HAProxy** splits traffic (Write → Leader, Read → Replicas).
4. **Monitoring**: Sidecar exporters for Prometheus metrics.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `etcd-1/2/3` | `quay.io/coreos/etcd:v3.6.7` | DCS Cluster |
| `pg-0/1/2` | `ghcr.io/zalando/spilo-17:4.0-p3` | PostgreSQL 17 + Patroni |
| `pg-router` | `haproxy:3.3.1` | Load Balancer (Write/Read split) |
| `pg-cluster-init`| `postgres:17-alpine` | Initialization Script Runner |
| `pg-*-exporter` | `prometheuscommunity/postgres-exporter:v0.18.1`| Metrics Exporter |

## Networking

Services run on `infra_net` with static IPs (172.19.0.5X).

| Service | Static IP | Internal Port | Host Port | Traefik Domain |
| :--- | :--- | :--- | :--- | :--- |
| `etcd-1` | `172.19.0.50` | `2379` | `${ETCD_CLIENT_PORT}` | - |
| `etcd-2` | `172.19.0.51` | `2379` | `${ETCD_CLIENT_PORT}` | - |
| `etcd-3` | `172.19.0.52` | `2379` | `${ETCD_CLIENT_PORT}` | - |
| `pg-0` | `172.19.0.53` | `${POSTGRES_PORT}` | `${POSTGRES_PORT}` | - |
| `pg-1` | `172.19.0.54` | `${POSTGRES_PORT}` | `${POSTGRES_PORT}` | - |
| `pg-2` | `172.19.0.55` | `${POSTGRES_PORT}` | `${POSTGRES_PORT}` | - |
| `pg-router` | `172.19.0.56` | Write: `${POSTGRES_WRITE_PORT}`<br>Read: `${POSTGRES_READ_PORT}` | `${POSTGRES_WRITE_HOST_PORT}`<br>${POSTGRES_READ_HOST_PORT}` | `pg-haproxy.${DEFAULT_URL}` (Stats) |
| `pg-0-exporter` | `172.19.0.57` | `${POSTGRES_EXPORTER_PORT}` | - | - |
| `pg-1-exporter` | `172.19.0.58` | `${POSTGRES_EXPORTER_PORT}` | - | - |
| `pg-2-exporter` | `172.19.0.59` | `${POSTGRES_EXPORTER_PORT}` | - | - |

## Persistence

Data is persisted in named volumes:

- **etcd**: `etcd1-data`, `etcd2-data`, `etcd3-data`
- **Postgres**: `pg0-data`, `pg1-data`, `pg2-data` (Mapped to `/home/postgres/pgdata`)
- **HAProxy**: `./config/haproxy.cfg` (Bind mount configuration)

## Configuration

Configuration is managed via `.env.postgres` and `docker-compose.yml`.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SCOPE` | Patroni Cluster Scope Name | `pg-ha` |
| `ETCD3_HOSTS` | etcd Cluster Endpoints | `etcd-1:2379,etcd-2...` |
| `PATRONI_NAME` | Unique Node Name | `pg-0`, `pg-1`... |
| `POSTGRES_USER` | Init User Name | `${POSTGRES_USER}` |
| `POSTGRES_DB` | Init Database Name | `${POSTGRES_DB}` |
| `POSTGRES_WRITE_PORT`| Router Write Port | `5432` |
| `POSTGRES_READ_PORT` | Router Read Port | `5433` |

## Traefik Integration

The **PG Router** (HAProxy) exposes a statistics dashboard via Traefik.

- **Stats UI**: `pg-haproxy.${DEFAULT_URL}`
- **Auth**: None (Dashboard authentication handled by HAProxy config if set).

## Usage

Applications should connect to the **PG Router** ports to ensure proper failover and load balancing.

| Connection Type | Host | Port | Description |
| :--- | :--- | :--- | :--- |
| **Write (Leader)** | `localhost` | `${POSTGRES_WRITE_HOST_PORT}` | DML/DDL Operations |
| **Read (Replica)** | `localhost` | `${POSTGRES_READ_HOST_PORT}` | Read-Only Queries |

> **Note**: Do not connect directly to `pg-0/1/2` unless for debugging, as roles (Leader/Replica) can change dynamically.
