# PostgreSQL HA Cluster

## Overview

A High Availability (HA) PostgreSQL cluster using **Patroni**, **etcd**, and **HAProxy**.

## Architecture

### 1. Distributed Configuration Store (DCS)

- **Services**: `etcd-1`, `etcd-2`, `etcd-3`
- **Purpose**: Main settings and leader election consensus.

### 2. PostgreSQL Nodes (Patroni)

- **Services**: `pg-0`, `pg-1`, `pg-2`
- **Image**: `ghcr.io/zalando/spilo-17:4.0-p3`
- **Mechanism**: Patroni manages replication and failover automatically.

### 3. Routing (HAProxy)

- **Service**: `pg-router`
- **Endpoints**:
  - **Write**: `${POSTGRES_WRITE_PORT}` (Directs to Leader)
  - **Read**: `${POSTGRES_READ_PORT}` (Directs to Replicas)
- **Traefik**: `pg-haproxy.${DEFAULT_URL}` exposes the HAProxy Stats UI.

### 4. Initialization & Metrics

- **Init**: `pg-cluster-init` runs `init_users_dbs.sql` via the Write endpoint.
- **Exporters**: Sidecar exporters for each PG node.

## Environment Variables

Major configuration is loaded from `.env.postgres`. Key variables managed in `docker-compose.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SCOPE` | Patroni Cluster Scope Name | `pg-ha` |
| `ETCD3_HOSTS` | etcd Cluster Endpoints | `etcd-1:2379,etcd-2...` |
| `PATRONI_NAME` | Unique Node Name | `pg-0`, `pg-1`... |
| `PATRONI_NAMESPACE` | etcd Key Namespace | `/service/` |
| `PATRONI_*_LISTEN` | Network Binding Addresses | `0.0.0.0:...` |
| `POSTGRES_USER` | Init User Name | `${POSTGRES_USER}` |
| `POSTGRES_DB` | Init Database Name | `${POSTGRES_DB}` |

## Network

Services are assigned static IPs in the `172.19.0.5X` range on `infra_net`.

| Service | IP Address |
| :--- | :--- |
| `etcd-1` | `172.19.0.50` |
| `etcd-2` | `172.19.0.51` |
| `etcd-3` | `172.19.0.52` |
| `pg-0` | `172.19.0.53` |
| `pg-1` | `172.19.0.54` |
| `pg-2` | `172.19.0.55` |
| `pg-router` | `172.19.0.56` |
| `pg-0-exporter` | `172.19.0.57` |
| `pg-1-exporter` | `172.19.0.58` |
| `pg-2-exporter` | `172.19.0.59` |

## Usage

Connect applications to the **HAProxy** ports, not individual nodes, to ensure HA routing work correctly.
