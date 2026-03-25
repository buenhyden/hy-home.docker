<!-- [ID:04-data:couchdb] -->
# CouchDB Cluster

> Document-oriented NoSQL database with HTTP API and robust sync.

## Overview (KR)

Apache CouchDB는 Erlang으로 구현된 **문서 지향 NoSQL 데이터베이스**입니다. HTTP API를 통해 데이터를 관리하며, 강력한 복제 및 동기화 기능을 제공하여 분산 시스템에 최적화되어 있습니다.

## Overview

The `couchdb` stack provides a 3-node clustered document store for `hy-home.docker`. It features a RESTful HTTP API, ACID properties, and multi-master replication, enabling high availability and partition tolerance (AP in CAP theorem).

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **couchdb-1, 2, 3** | CouchDB 3.5.1 | Cluster Nodes |
| **couchdb-init** | curl | Cluster Bootstrap Job |

## Networking

| Service | Access | Description |
| :--- | :--- | :--- |
| **API Port** | `5984` | Standard HTTP API access. |
| **Cluster URL** | `couchdb.${DEFAULT_URL}` | External access via Traefik (Sticky). |
| **Internal** | `4369, 9100` | Erlang distribution and mapper ports. |

## Persistence

- **Volumes**: `couchdb1-data`, `couchdb2-data`, `couchdb3-data`.
- **Path**: `${DEFAULT_DATA_DIR}/couchdb/data-{1,2,3}` on the host.
- **Mount**: `/opt/couchdb/data` within containers.

## Configuration

- **Authentication**: Uses `couchdb_password` and `couchdb_cookie` Docker secrets.
- **Initialization**: `couchdb-cluster-init` automatically joins nodes and finishes setup on first run.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Cluster and initialization definitions. |
| `README.md` | Service overview and documentation. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
