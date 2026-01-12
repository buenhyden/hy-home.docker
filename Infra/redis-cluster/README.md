# Redis Cluster

## Overview

A 6-node (3 Master, 3 Replica) Redis Cluster for high availability and sharding.

## Services

- **redis-node-0 ~ 5**: Redis Cluster nodes.
  - Internal Port: `6379`, `16379` (Bus)
  - External Ports (Node 0-5): `${REDIS0_PORT}` ~ `${REDIS5_PORT}`
- **redis-cluster-init**: Cluster create script runner (one-shot).
- **redis-exporter**: Prometheus metrics exporter.

## Configuration

### Environment Variables

- `REDIS_PASSWORD`: Secret loaded from file.

### Volumes

- `redis-data-N`: `/data`
- `redis.conf`: `/usr/local/etc/redis/redis.conf`

## Networks

- `infra_net`
  - Fixed IPs (`172.19.0.60-67`) for reliable cluster announce.

## Note

- This is a 'Cluster Mode' setup, different from Standalone or Sentinel.
- Clients must support Redis Cluster protocol.
