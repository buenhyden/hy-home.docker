# Valkey Cluster

## Overview

A 6-node **Valkey** (Redis fork) Cluster configured for sharding and high availability.

## Architecture

### Nodes

- **Services**: `valkey-node-0` through `valkey-node-5`
- **Image**: `valkey/valkey:9.0.1-alpine`
- **Configuration**: Mapped from `./config/valkey.conf`.

### Initialization

- **Service**: `valkey-cluster-init`
- **Logic**: Runs `valkey-cluster-init.sh` to form the cluster automatically.

### Networking

- **Discovery**: Static IPs (`172.19.0.60` - `.65`).
- **Ports**: Exposes Cluster Bus ports.

### Exporter

- **Service**: `valkey-exporter`
- **Details**: Runs in "Stateless Mode" using `r_pwd` and probing specific nodes when scraped.

## Network

Services are assigned static IPs in the `172.19.0.6X` range on `infra_net`.

| Service | IP Address | Role |
| :--- | :--- | :--- |
| `valkey-node-0` | `172.19.0.60` | Master/Replica |
| `valkey-node-1` | `172.19.0.61` | Master/Replica |
| `valkey-node-2` | `172.19.0.62` | Master/Replica |
| `valkey-node-3` | `172.19.0.63` | Master/Replica |
| `valkey-node-4` | `172.19.0.64` | Master/Replica |
| `valkey-node-5` | `172.19.0.65` | Master/Replica |
| `valkey-cluster-init` | `172.19.0.66` | Init Script |
| `valkey-exporter` | `172.19.0.67` | Metrics |

## Note

Primary caching layer for `n8n` and other high-throughput services.
