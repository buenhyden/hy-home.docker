---
layer: infra
---
# ksqlDB System Context

**Overview (KR):** ksqlDB 스트리밍 SQL 엔진의 시스템 컨텍스트, 역할, 프로파일 구조, 및 사용 패턴을 설명합니다.

> **Component**: `ksqldb`
> **Profile**: `messaging-option` (server) / `ksql` (CLI + datagen)

## 1. Role in Ecosystem

ksqlDB provides a **SQL interface for real-time stream processing** on top of Kafka. It allows building streaming transformations, aggregations, and joins without writing Java-based Kafka Streams applications.

| Use Case | Description |
| --- | --- |
| Real-time aggregations | Count events per window (tumbling/hopping/session) |
| Stream-to-stream joins | Correlate events across multiple topics |
| Event filtering | Route events matching specific conditions to new topics |
| Materialized views | Build always-up-to-date read models from event streams |

## 2. Profile Structure

ksqlDB uses a split profile approach to allow the server to run optionally alongside Kafka without pulling in the interactive CLI tools:

| Service | Profile | Prerequisites |
| --- | --- | --- |
| `ksqldb-server` | `messaging-option` | Requires `kafka-1..3` healthy + `schema-registry` healthy |
| `ksqldb-cli` | `ksql` | Requires `ksqldb-server` healthy |
| `ksql-datagen` | `ksql` | Requires `ksqldb-server` healthy |

> **Important**: `ksqldb-server` is NOT activated by the `messaging` profile. You must explicitly use `messaging-option` or add it to `COMPOSE_PROFILES`.

## 3. Architecture

```text
                   Kafka Cluster (infra_net)
                 kafka-1:19092 | kafka-2:19092 | kafka-3:19092
                         │
              ┌───────────▼──────────────────────┐
              │  ksqldb-server (messaging-option) │
              │  Port: 8088                       │
              │  Schema Registry: :8081           │
              │  Kafka Connect: :8083             │
              └───────────┬──────────────────────┘
                          │
          ┌───────────────┼────────────────┐
          │               │                │
   ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
   │ ksqldb-cli  │ │ksql-datagen │ │  HTTP API   │
   │ (ksql prof) │ │ (ksql prof) │ │  clients    │
   └─────────────┘ └─────────────┘ └─────────────┘
```

## 4. Configuration

Key environment variables for `ksqldb-server`:

| Variable | Value | Purpose |
| --- | --- | --- |
| `KSQL_BOOTSTRAP_SERVERS` | `kafka-1:19092,kafka-2:19092,kafka-3:19092` | Kafka cluster connection |
| `KSQL_KSQL_SCHEMA_REGISTRY_URL` | `http://schema-registry:8081` | Schema integration |
| `KSQL_KSQL_CONNECT_URL` | `http://kafka-connect:8083` | Connect integration |
| `KSQL_KSQL_LOGGING_PROCESSING_TOPIC_REPLICATION_FACTOR` | `3` | Internal topic replication |
| `KSQL_HEAP_OPTS` | `-Xms512m -Xmx512m` | JVM heap |

## 5. Starting ksqlDB

```bash
# Start just the ksqlDB server alongside the already-running messaging stack
docker compose --profile messaging-option up -d ksqldb-server

# Open the interactive CLI
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088

# Or start everything together
COMPOSE_PROFILES=messaging,messaging-option,ksql docker compose up -d
```

## 6. Common SQL Patterns

### Create a Stream from a Kafka Topic

```sql
CREATE STREAM orders (
  order_id VARCHAR KEY,
  user_id VARCHAR,
  amount DOUBLE,
  status VARCHAR
) WITH (
  KAFKA_TOPIC = 'orders',
  VALUE_FORMAT = 'JSON'
);
```

### Create a Persistent Query (aggregation)

```sql
CREATE TABLE order_totals AS
  SELECT user_id,
         COUNT(*) AS order_count,
         SUM(amount) AS total_amount
  FROM orders
  WINDOW TUMBLING (SIZE 1 HOUR)
  GROUP BY user_id
  EMIT CHANGES;
```

### Inspect Processing Status

```sql
-- List running queries
SHOW QUERIES;

-- Describe a stream
DESCRIBE orders EXTENDED;

-- Check server status
SHOW PROPERTIES;
```

## 7. Persistence

ksqlDB stores internal state (materialized tables, processing state) in:

- **Volume**: `ksqldb-data-volume` → `/var/lib/ksql`
- **Host path**: `${DEFAULT_DATA_DIR}/ksql`

Internal Kafka topics are automatically created for query state stores and logging (with replication factor 3).

## 8. Lifecycle

### Startup

`ksqldb-server` waits for all 3 Kafka brokers and `schema-registry` to be healthy before starting.

### Shutdown

```bash
docker compose --profile messaging-option stop ksqldb-server
```

> Stopping the server pauses persistent queries. On restart, they automatically resume from their last committed Kafka offset.

### Reset State

```bash
docker compose --profile messaging-option down ksqldb-server
docker volume rm ksql_ksqldb-data-volume
```

> **Warning**: This drops all materialized tables and their state. Persistent queries can be re-created from SQL scripts.
