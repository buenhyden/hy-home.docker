# Apache CouchDB Cluster

## Overview

A clustered Apache CouchDB installation with 3 nodes and an auto-initialization service.

## Services

- **couchdb-1**: Node 1 (Seed Node)
  - Port: `${COUCHDB_PORT}` (Exposed), `${COUCHDB_ERLANG_MAPPER_PORT}`, `${COUCHDB_ERLANG_DISTRIBUTION_PORT}`
  - URL: `https://couchdb.${DEFAULT_URL}` (Load Balanced)
- **couchdb-2**: Node 2
- **couchdb-3**: Node 3
- **couchdb-cluster-init**: One-shot service to join nodes into a cluster.

## Configuration

### Environment Variables

- `COUCHDB_USER`: Admin username.
- `COUCHDB_PASSWORD`: Admin password.
- `COUCHDB_COOKIE`: Erlang cookie for cluster communication.
- `NODENAME`: Unique node identifier (e.g., `couchdb-1.infra_net`).

### Volumes

- `couchdb1-data`: `/opt/couchdb/data` (Node 1)
- `couchdb2-data`: `/opt/couchdb/data` (Node 2)
- `couchdb3-data`: `/opt/couchdb/data` (Node 3)

## Networks

- `infra_net`
  - Aliases: `couchdb-N.infra_net`

## Traefik Routing

- **Domain**: `couchdb.${DEFAULT_URL}`
- **Service**: `couchdb-cluster` (Load balancing across all 3 nodes)
- **Sticky Session**: Enabled (cookie: `couchdb_sticky`)
