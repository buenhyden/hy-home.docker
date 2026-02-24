# CouchDB Cluster Blueprint

> **Component**: `couchdb`
> **Topology**: 3-node cluster with HAProxy router
> **Internal Port**: `5984` (API)

## 1. Cluster Architecture

The CouchDB setup operates in a "Full Partitioned Cluster" mode. Nodes `couchdb0`, `couchdb1`, and `couchdb2` form the quorum.

- **Initialization**: Handled by `couchdb-cluster-init` container.
- **Admin UI (Fauxton)**: Accessible via `https://couchdb.${DEFAULT_URL}/_utils`.

## 2. API Interaction

Clients should use the Traefik-exposed URL for load-balanced access:

```bash
# Verify cluster healthy membership
curl -u admin:${COUCHDB_PASSWORD} https://couchdb.${DEFAULT_URL}/_membership
```

## 3. Storage and State

Data is persisted on host paths defined by `${DEFAULT_DATA_DIR}/couchdb`.

- **Backup Strategy**: Snapshot the entire data volume. CouchDB handles file-system consistency well due to its append-only storage engine.
- **Re-sharding**: For large production growth, utilize the `_shards` API to rebalance across nodes.
