# CouchDB Cluster

## Overview

High-Availability 3-node CouchDB cluster. This setup automatically configures a distributed database cluster using a dedicated initialization container.

## Architecture & Services

| Service | Description | Role |
| :--- | :--- | :--- |
| `couchdb-1` | Database Node 1 | Seed Node / Coordinator |
| `couchdb-2` | Database Node 2 | Cluster Member |
| `couchdb-3` | Database Node 3 | Cluster Member |
| `couchdb-cluster-init`| Initialization Script | Configuring the cluster (Ephemeral) |

### Initialization Process

The `couchdb-cluster-init` container waits for all nodes to be healthy, then:

1. **Joins** `couchdb-2` and `couchdb-3` to `couchdb-1`.
2. **Finishes** the cluster setup.
3. **Creates** system databases (`_users`, `_replicator`, `_global_changes`).
4. Exits successfully (restart policy: `no`).

## Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `COUCHDB_USER` | Admin username | `${COUCHDB_USERNAME}` |
| `COUCHDB_PASSWORD` | Admin password | `${COUCHDB_PASSWORD}` |
| `COUCHDB_COOKIE` | Erlang magic cookie | `${COUCHDB_COOKIE}` |
| `NODENAME` | Unique Erlang node name | `couchdb-X.infra_net` |

## Volumes

Each node has its own persistent storage:

- `couchdb1-data` → `/opt/couchdb/data`
- `couchdb2-data` → `/opt/couchdb/data`
- `couchdb3-data` → `/opt/couchdb/data`

## Networking & Ports

Nodes communicate via the internal `infra_net` network using DNS aliases (`couchdb-1.infra_net`, etc.).

### Exposed Ports (Internal)

- **5984**: HTTP API (Database commands)
- **4369**: Erlang Port Mapper Daemon (EPMD)
- **9100-9200**: Erlang Distribution (Cluster communication)

> **Note**: Ports are exposed to the internal network but not published to the host by default for security. Access is managed via Traefik.

## Traefik Configuration (Sticky Sessions)

To ensure Read-Your-Own-Writes consistency behind a load balancer, **Sticky Sessions** are enabled.

- **Host**: `couchdb.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service**: `couchdb-cluster`
- **Sticky Cookie**: `couchdb_sticky`

All three nodes register to the same `couchdb-cluster` service in Traefik, distributing traffic while maintaining session affinity.

## Usage

### Start Cluster

```bash
docker-compose up -d
```

### Verify Status

Check the status of the setup container or query the cluster endpoint:

```bash
# Check setup logs
docker logs couchdb-cluster-init

# Use the API (via Traefik or locally)
curl https://couchdb.<your-domain>/_up
```
