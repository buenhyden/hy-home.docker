---
layer: infra
---
# Apache Cassandra Context

**Overview (KR):** Apache Cassandra 단일 노드 구성과 Prometheus 메트릭 수집을 위한 아키텍처 컨텍스트 가이드입니다.

> **Component**: `cassandra`
> **Profile**: `standalone` (Optional)
> **Internal Port**: `9042` (CQL native client)

## 1. System Role

Cassandra is a wide-column NoSQL database optimized for write-heavy workloads, time-series data, and high-throughput key-value access patterns. In this stack it is provisioned as an optional single-node instance primarily for application data requiring flexible schema evolution or large-scale write throughput.

- **Internal DNS**: `cassandra-node1`
- **Client Port**: `9042` (CQL)

## 2. Architecture

The current configuration runs as a single `cassandra-node1` container backed by the `bitnami/cassandra` image. A sidecar `cassandra-exporter` container scrapes JMX metrics and exposes them to Prometheus.

```text
[Application] --> cassandra-node1:9042 (CQL)
                        |
               cassandra-exporter:${CASSANDRA_EXPORTER_PORT}  --> Prometheus
```

## 3. Secrets & Configuration

| Variable / Secret | Description |
| :--- | :--- |
| `CASSANDRA_USERNAME` | CQL client username (from `.env`) |
| `cassandra_password` | Docker secret at `secrets/db/cassandra/cassandra_password.txt` |
| `CASSANDRA_EXPORTER_PORT` | Prometheus exporter port (from `.env`) |

## 4. Persistence

Data is stored in the named Docker volume `cassandra-node1-volume`, mounted at `/bitnami/cassandra`. Exporter configuration is persisted in `cassandra-exporter-volume`.

## 5. Scaling Considerations

The current single-node setup is suitable for development and light workloads. For production HA, a 3-node ring is recommended with `num_tokens: 256` and a replication factor of at least 3.
