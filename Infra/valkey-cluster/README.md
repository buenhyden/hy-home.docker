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

## Note

Primary caching layer for `n8n` and other high-throughput services.
