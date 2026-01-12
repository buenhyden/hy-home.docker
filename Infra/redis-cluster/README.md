# Redis Cluster

## Overview

A 6-node Redis Cluster configured for sharding and high availability.

## Architecture

### Nodes

- **Masters**: 3 Nodes
- **Replicas**: 3 Nodes
- **Services**: `redis-node-0` through `redis-node-5`
- **Image**: `redis:8.4.0-bookworm`

### Initialization

- **Service**: `redis-cluster-init`
- **Logic**: Runs `redis-cluster-init.sh` to form the cluster once nodes are healthy.

### Networking

- **Discovery**: Relies on static IPs or Docker network DNS (`infra_net`).
- **Ports**: Each node listens on its respective port (`${REDIS0_PORT}`, etc.) and Bus port.

### Exporter

- **Service**: `redis-exporter`
- **Mode**: Scrapes `redis-node-0` (or cluster-aware) for Prometheus metrics.

## Network

Services are assigned static IPs in the `172.19.0.6X` range on `infra_net`.

| Service | IP Address | Role |
| :--- | :--- | :--- |
| `redis-node-0` | `172.19.0.60` | Master/Replica |
| `redis-node-1` | `172.19.0.61` | Master/Replica |
| `redis-node-2` | `172.19.0.62` | Master/Replica |
| `redis-node-3` | `172.19.0.63` | Master/Replica |
| `redis-node-4` | `172.19.0.64` | Master/Replica |
| `redis-node-5` | `172.19.0.65` | Master/Replica |
| `redis-cluster-init` | `172.19.0.66` | Init Script |
| `redis-exporter` | `172.19.0.67` | Metrics |

## Note

This cluster is primarily for internal infrastructure usage (`infra_net`). No external Traefik routes are configured by default.
