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

## Note

This cluster is primarily for internal infrastructure usage (`infra_net`). No external Traefik routes are configured by default.
