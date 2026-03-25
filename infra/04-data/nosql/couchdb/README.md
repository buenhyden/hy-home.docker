<!-- [ID:04-data:couchdb] -->
# CouchDB Cluster

> Document-oriented NoSQL database with HTTP API and robust sync.

## Overview (KR)

이 서비스는 강력한 복제 및 동기화 기능을 제공하는 **문서 지향 NoSQL 데이터베이스**입니다. 분산 시스템에서의 데이터 일관성과 고가용성을 보장합니다.

## Overview

The `couchdb` stack provides a 3-node clustered document store for `hy-home.docker`. It features a RESTful HTTP API, ACID properties, and multi-master replication, enabling high availability and partition tolerance.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **couchdb-1, 2, 3** | CouchDB 3.5 | Cluster Nodes |
| **couchdb-init** | curl | Cluster Bootstrap Job |

## Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **API Port** | `5984` | Standard HTTP API (`couchdb.${DEFAULT_URL}`). |
| **Internal** | `4369, 9100` | Erlang distribution and mapper ports. |

## Persistence

- **Volumes**: `couchdb1-data`, `couchdb2-data`, `couchdb3-data`.
- **Secrets**: `couchdb_password`, `couchdb_cookie`.
- **Path**: `${DEFAULT_DATA_DIR}/couchdb/data-{1,2,3}` on the host.

## Operations

### Cluster Initialization

The `couchdb-cluster-init` job automatically joins nodes and finishes setup on the first deployment.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Cluster and initialization definitions. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
