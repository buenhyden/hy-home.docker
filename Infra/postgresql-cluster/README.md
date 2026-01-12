# PostgreSQL High Availability Cluster

## Overview

A 3-node PostgreSQL 17 cluster managed by Patroni, dealing with failover and high availability using Etcd as the DCS (Distributed Configuration Store) and HAProxy for request routing.

## Services

- **etcd-1, etcd-2, etcd-3**: Distributed Configuration Store (DCS).
  - Client Port: `${ETCD_CLIENT_PORT}` (2379)
- **pg-0, pg-1, pg-2**: PostgreSQL nodes running Patroni.
  - Port: `${POSTGRES_PORT}` (5432)
- **pg-router**: HAProxy load balancer.
  - Write: `${POSTGRES_WRITE_PORT}` (5000)
  - Read: `${POSTGRES_READ_PORT}` (5001)
  - Stats: `http://pg-haproxy.${DEFAULT_URL}`
- **pg-cluster-init**: Initialization job.
- **pg-N-exporter**: Metrics exporters.

## Configuration

### Environment Variables

- `POSTGRES_PASSWORD`: Superuser password.
- `POSTGRES_USER`: Application user.
- `SCOPE`: Cluster name (`pg-ha`).
- `ETCD3_HOSTS`: Connection string for Etcd.

### Volumes

- `etcdN-data`: `/etcd-data`
- `pgN-data`: `/home/postgres/pgdata`
- `haproxy.cfg`: `/usr/local/etc/haproxy/haproxy.cfg` (Config map)

## Networks

- `infra_net`
  - Fixed IPs assigned to all nodes (`172.19.0.50-58`).

## Traefik Routing

- **HAProxy Stats**: `pg-haproxy.${DEFAULT_URL}`
