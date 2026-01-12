# Redis Cluster

## Overview

A 6-node Redis Cluster configured for sharding and high availability (3 Masters, 3 Replicas).

## Architecture

- **Topology**: 3 Primary Nodes + 3 Replica Nodes.
- **Failover**: Automatic failover via Redis Sentinel logic embedded in Cluster mode.
- **Initialization**: `redis-cluster-init` container creates the cluster after nodes are up.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `redis-node-0..5`| `redis:8.4.0-bookworm` | Redis Data Nodes |
| `redis-cluster-init` | `redis:8.4` | Cluster Formation Script |
| `redis-exporter` | `oliver006/redis_exporter:v1.80.1-alpine` | Prometheus Metrics |

## Networking

Services run on `infra_net` with static IPs (172.19.0.6X).

| Service | Static IP | Internal Port | Host Port |
| :--- | :--- | :--- | :--- |
| `redis-node-0` | `172.19.0.60` | `${REDIS0_PORT}` | `${REDIS0_PORT}` |
| `redis-node-1` | `172.19.0.61` | `${REDIS1_PORT}` | `${REDIS1_PORT}` |
| `redis-node-2` | `172.19.0.62` | `${REDIS2_PORT}` | `${REDIS2_PORT}` |
| `redis-node-3` | `172.19.0.63` | `${REDIS3_PORT}` | `${REDIS3_PORT}` |
| `redis-node-4` | `172.19.0.64` | `${REDIS4_PORT}` | `${REDIS4_PORT}` |
| `redis-node-5` | `172.19.0.65` | `${REDIS5_PORT}` | `${REDIS5_PORT}` |
| `redis-cluster-init` | `172.19.0.66` | - | - |
| `redis-exporter` | `172.19.0.67` | `${REDIS_EXPORTER_PORT}` | `${REDIS_EXPORTER_HOST_PORT}` |

## Persistence

Data is persisted in named volumes and configuration via bind mounts:

- **Data**: `redis-data-0` ... `redis-data-5` -> `/data`
- **Config**: `./config/redis.conf` -> `/usr/local/etc/redis/redis.conf`
- **Scripts**: `./scripts/` -> `/usr/local/bin/`

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NODE_NAME` | Node Identity | `redis-node-X` |
| `PORT` | Node Port | `${REDISX_PORT}` |
| `redis_password` | Docker Secret | via file |

## Traefik Integration

This cluster is purely internal for infrastructure. No Traefik routes are exposed.

## Usage

Applications on `infra_net` should connect using a Cluster-aware client with seed nodes:

- `redis-node-0:6379`
- `redis-node-1:6380`...

**Debug**:
Host ports are exposed (e.g., `localhost:6379`) for debugging, but cluster redirection might fail if client cannot reach container IPs from host.
