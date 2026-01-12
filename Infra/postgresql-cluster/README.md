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

## Usage

Connect applications to the **HAProxy** ports, not individual nodes, to ensure HA routing work correctly.
