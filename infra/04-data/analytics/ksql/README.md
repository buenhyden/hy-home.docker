# ksqlDB (ksql)

> Streaming SQL engine for Apache Kafka.

## Overview

ksqlDB allows building stream processing applications using familiar SQL syntax. It integrates directly with the Kafka cluster and Schema Registry to enable real-time analytics.

## Service Matrix

| Service | Image | Profile | Purpose |
| :--- | :--- | :--- | :--- |
| **ksqldb-server** | `cp-ksqldb-server:8.0.3` | `messaging-option` | Streaming SQL engine |
| **ksqldb-cli** | `cp-ksqldb-cli:8.0.3` | `ksql` | Interactive management CLI |
| **ksql-datagen** | `ksqldb-examples:8.0.3` | `ksql` | Sample data generator |

## Setup & Persistence

### 1. Persistence

- **Data Volume**: `ksqldb-data-volume`
- **Mount Path**: `/var/lib/ksql`
- **Host Path**: `${DEFAULT_DATA_DIR}/ksql`

### 2. Startup

The server is part of the `messaging-option` profile and requires the core `messaging` (Kafka) stack to be healthy.

```bash
# Start ksqlDB Server
docker compose --profile messaging-option up -d ksqldb-server
```

---

## Usage

### Interactive CLI

```bash
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

### Example SQL

```sql
CREATE STREAM page_views (viewtime BIGINT, userid VARCHAR, pageid VARCHAR)
  WITH (KAFKA_TOPIC='page-views', VALUE_FORMAT='JSON');

SELECT userid, COUNT(*) AS view_count
  FROM page_views
  WINDOW TUMBLING (SIZE 1 MINUTE)
  GROUP BY userid
  EMIT CHANGES;
```

## Navigation
- [Messaging Tier Overview](../README.md)
- [ksqlDB Guide](../../../docs/07.guides/05-messaging/02.ksql-streaming.md)
- [Operational Policy](../../../docs/08.operations/05-messaging/README.md)
