# CouchDB Cluster

## Overview

A 3-node CouchDB cluster configuration. It uses a setup helper container (`couchdb-cluster-init`) to automatically join nodes into a cluster.

## Service Details

- **Image**: `couchdb:3.5.1`
- **Nodes**: `couchdb-1`, `couchdb-2`, `couchdb-3`
- **Helper**: `couchdb-cluster-init` (Exits after setup)
- **Volumes**:
  - `couchdb1-data`, `couchdb2-data`, `couchdb3-data`: Persistent storage for each node.

## Environment Variables

- `COUCHDB_USER`: Admin username.
- `COUCHDB_PASSWORD`: Admin password.
- `COUCHDB_COOKIE`: Erlang magic cookie for cluster sync.
- `NODENAME`: Node identifier (e.g., `couchdb-1.infra_net`).

## Traefik Configuration

The cluster uses **Sticky Sessions** to ensure consistency directly from the load balancer.

- **Domain**: `couchdb.${DEFAULT_URL}`
- **Service Name**: `couchdb-cluster`
- **Load Balancing**:
  - Sticky Cookie Name: `couchdb_sticky`
  - Sticky Cookie Enabled: `true`

All nodes (`couchdb-1`, `couchdb-2`, `couchdb-3`) register themselves to the `couchdb-cluster` Traefik service.
