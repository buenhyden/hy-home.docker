# ksqlDB

> Streaming SQL engine for Apache Kafka.

## 1. Context & Objective (SSoT)

ksqlDB enables building real-time stream processing applications using familiar SQL syntax. It integrates directly with the Kafka cluster and Schema Registry to enable real-time analytics and data transformation.

- **Status**: Production / Streaming
- **Role**: SQL Stream Processing
- **SSoT Documentation**: [Analytical Databases Guide](../../../docs/07.guides/04-data/05.analytical-specialized-dbs.md)

## 2. Requirements & Constraints

- **Dependency**: Kafka (messaging) and Schema Registry must be healthy.
- **Resources**: JVM Heap set to 512MB by default.
- **Port**: 8088 (Internal/External).

## 3. Setup & Installation

The server is part of the `messaging-option` profile.

```bash
# Start ksqlDB Server
docker compose --profile messaging-option up -d ksqldb-server
```

### Persistence

- **Volume**: `ksqldb-data-volume` (`/var/lib/ksql`)
- **Host Path**: `${DEFAULT_DATA_DIR}/ksql`

## 4. Usage & Integration

### Interactive CLI
```bash
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

### Integration Points

- **API**: `http://ksqldb-server:8088`
- **Schema Registry**: `http://schema-registry:8081`

## 5. Maintenance & Safety

- **Backups**: Managed via Kafka topic replication and Schema Registry backups.
- **Logging**: Logs available via `docker logs ksqldb-server`.
- **Processing**: Processing topics are auto-replicated for high availability.

---
Copyright (c) 2026. Licensed under the MIT License.
