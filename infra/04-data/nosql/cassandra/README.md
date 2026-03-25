<!-- [ID:04-data:cassandra] -->
# Apache Cassandra

> Distributed wide-column NoSQL database.

## Overview (KR)

이 서비스는 높은 가용성과 선형적 확장이 가능한 **분산 NoSQL 데이터베이스**로, 대규모 데이터 세트와 빠른 쓰기 성능을 제공합니다.

## Overview

The `cassandra` service provides a linearly scalable, high-throughput storage layer for application data requiring low latency and high availability. It is optimized for time-series and real-time data processing in `hy-home.docker`.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **cassandra-node1** | Cassandra 5.0 | Primary Data Node |
| **cassandra-exporter** | JMX Exporter | Metrics Integration |

## Networking

| Port | Protocol | Purpose |
| :--- | :--- | :--- |
| `9042` | CQL | Main Client Protocol (Binary). |
| `7000` | Intra-node | Inter-node Communication. |
| `8080` | HTTP | Metrics scraping. |

## Persistence

- **Volumes**: `cassandra-node1-volume` for database storage.
- **Secrets**: `cassandra_password` for secure authentication.
- **Path**: `${DEFAULT_DATA_DIR}/cassandra` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Single-node deployment script. |
| `config/` | JMX and Cassandra configurations. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
