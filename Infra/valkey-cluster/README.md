# Valkey Cluster

## Overview

A 6-node **Valkey** (Redis fork) Cluster configured for sharding and high availability (3 Masters, 3 Replicas).

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `valkey-node-0..5`| `valkey/valkey:9.0.1-alpine` | Valkey Data Nodes |
| `valkey-cluster-init` | `valkey/valkey:9.0.1` | Cluster Formation Script |
| `valkey-exporter` | `oliver006/redis_exporter:v1.80.1-alpine` | Prometheus Metrics |

## Networking

Services run on `infra_net` with static IPs (172.19.0.6X).

| Service | Static IP | Internal Port | Host Port |
| :--- | :--- | :--- | :--- |
| `valkey-node-0` | `172.19.0.60` | `${VALKEY0_PORT}` | `${VALKEY0_PORT}` |
| `valkey-node-1` | `172.19.0.61` | `${VALKEY1_PORT}` | `${VALKEY1_PORT}` |
| `valkey-node-2` | `172.19.0.62` | `${VALKEY2_PORT}` | `${VALKEY2_PORT}` |
| `valkey-node-3` | `172.19.0.63` | `${VALKEY3_PORT}` | `${VALKEY3_PORT}` |
| `valkey-node-4` | `172.19.0.64` | `${VALKEY4_PORT}` | `${VALKEY4_PORT}` |
| `valkey-node-5` | `172.19.0.65` | `${VALKEY5_PORT}` | `${VALKEY5_PORT}` |
| `valkey-cluster-init` | `172.19.0.66` | - | - |
| `valkey-exporter` | `172.19.0.67` | `${VALKEY_EXPORTER_PORT}` | `${VALKEY_EXPORTER_HOST_PORT}` |

## Persistence

Data is persisted in named volumes and configuration via bind mounts:

- **Data**: `valkey-data-0` ... `valkey-data-5` → `/data`
- **Config**: `./config/valkey.conf` → `/usr/local/etc/valkey/valkey.conf`
- **Scripts**: `./scripts/` → `/usr/local/bin/`

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NODE_NAME` | Node Identity | `valkey-node-X` |
| `PORT` | Node Port | `${VALKEYX_PORT}` |
| `valkey_password` | Docker Secret | via file |

## Traefik Integration

The cluster is purely internal. No Traefik routes are exposed.

## Usage

1. **Internal**: Applications connect via the cluster protocol. Seed nodes: `valkey-node-0:6379`, etc.
2. **Primary Use**: Caching layer for `n8n` and other high-throughput services.
