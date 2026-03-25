<!-- [ID:04-data:cassandra] -->
# Apache Cassandra

> Distributed wide-column NoSQL database.

## Overview (KR)

이 서비스는 쓰기 중심의 워크로드와 높은 처리량의 키-값 액세스에 최적화된 **분산 와이드 컬럼 NoSQL 데이터베이스**입니다.

## Overview

The `cassandra` service provides a linearly scalable, high-throughput storage layer for application data requiring low latency and high availability. It is particularly well-suited for time-series and real-time data processing.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **cassandra-node1** | Cassandra 4.x | Data Node |
| **cassandra-exporter**| JMX Exporter | Metrics |

## Networking

| Port | Protocol | Purpose |
| :--- | :--- | :--- |
| `9042` | CQL | Binary client protocol. |
| `7000` | Intra-node | Inter-node communication. |
| `9103` | JMX | Monitoring metrics. |

## Persistence

- **Data Volume**: `cassandra-node1-volume` mounted to `/bitnami/cassandra`.
- **Storage Path**: `${DEFAULT_DATA_DIR}/cassandra` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Single-node deployment script. |
| `config/` | JMX and Cassandra configurations. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
