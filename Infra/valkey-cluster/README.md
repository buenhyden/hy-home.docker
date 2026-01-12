# Valkey Cluster

## Overview

A 6-node (3 Master, 3 Replica) Valkey (Redis fork) Cluster for high availability and sharding.

## Services

- **valkey-node-0 ~ 5**: Valkey Cluster nodes.
  - Internal Port: `6379`, `16379` (Bus)
  - External Ports (Node 0-5): `${VALKEY0_PORT}` ~ `${VALKEY5_PORT}`
- **valkey-cluster-init**: Cluster create script runner (one-shot).
- **valkey-exporter**: Prometheus metrics exporter.

## Configuration

### Environment Variables

- `VALKEY_PASSWORD`: Secret loaded from file.

### Volumes

- `valkey-data-N`: `/data`
- `valkey.conf`: `/usr/local/etc/valkey/valkey.conf`

## Networks

- `infra_net`
  - Fixed IPs (`172.19.0.60-67`) for reliable cluster announce.

## Note

- This is a 'Cluster Mode' setup.
- Valkey is fully compatible with Redis clients.
