<!-- [ID:04-data:couchdb] -->
# CouchDB Cluster

> Document-oriented NoSQL database with HTTP API and robust sync.

## 1. Context & Objective

CouchDB is a document-oriented NoSQL database that excels in data synchronization and replication. In `hy-home.docker`, it provides a highly available 3-node cluster for application data requiring multi-master replication and a simple RESTful HTTP API.

## 2. Requirements & Constraints

* **Clustering**: Requires 3 nodes (`couchdb-1`, `couchdb-2`, `couchdb-3`) for a healthy quorum.
* **Security**: Uses `couchdb_password` for admin access and `couchdb_cookie` for inter-node communication.
* **Persistence**: Data is mapped to `${DEFAULT_DATA_DIR}/couchdb/data-{1,2,3}`.
* **Network**: Nodes must communicate over `infra_net` using Erlang distribution ports.

## 3. Setup & Installation

The cluster is automatically bootstrapped via the `couchdb-cluster-init` job.

```bash
# Deploy CouchDB cluster
docker compose up -d
```

| Service | Image | Role |
| :--- | :--- | :--- |
| `couchdb-1,2,3` | `couchdb:3.5.1` | Cluster Nodes |
| `couchdb-cluster-init` | `curlimages/curl:8.18.0` | Bootstrap Automation |

## 4. Usage & Integration

* **API Endpoint**: `https://couchdb.${DEFAULT_URL}` (via Traefik).
* **Internal Port**: `5984` (Standard HTTP API).
* **Sticky Sessions**: Traefik is configured with sticky cookies for specific node affinity.

Integration Example:

```json
{
  "db_url": "http://couchdb-1:5984",
  "username": "${COUCHDB_USERNAME}"
}
```

## 5. Maintenance & Safety

* **Health Checks**: Each node is verified via the `/_up` endpoint.
* **Initialization**: The init job runs only on first deployment or if reset.
* **Scaling**: Always maintain an odd number of nodes for quorum consistency.
* **Data Safety**: Cross-node replication provides redundancy, but host-level backups of `${DEFAULT_DATA_DIR}/couchdb` are mandatory.

---

## Documentation References

* [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
* [Backup Operations](../../../docs/08.operations/04-data/README.md)
* [Operational Runbooks](../../../docs/09.runbooks/04-data/README.md)
