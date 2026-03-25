<!-- [ID:04-data:neo4j] -->
# Neo4j Graph Database

> Native property-graph database for connected data.

## Overview (KR)

이 서비스는 고도로 연결된 데이터와 관계 탐색에 최적화된 **네이티브 속성 그래프 데이터베이스**입니다. Cypher 쿼리 언어를 사용합니다.

## Overview

The `neo4j` service provides a specialized graph storage layer for relationship-intensive data models. It allows for efficient querying of deep hierarchies and complex netowrk structures.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **neo4j** | Neo4j Community | Graph Engine |

## Networking

| Port | Protocol | Purpose |
| :--- | :--- | :--- |
| `7687` | Bolt | High-performance binary protocol. |
| `7474` | HTTP | Browser UI (Default: Internal). |
| `7473` | HTTPS | Browser UI (Default: Internal). |

## Persistence

- **Data Volume**: `neo4j-volume` mounted to `/bitnami/neo4j`.
- **Storage Path**: `${DEFAULT_DATA_DIR}/neo4j` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Service definition. |
| `scripts/` | Data import/export utilities. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Recovery Runbook](../../../docs/09.runbooks/04-data/README.md)
