# ksqlDB

ksqlDB is the streaming SQL engine for Apache Kafka. It allows you to build stream processing applications using a SQL-like syntax.

## Services

| Service | Image | Profile | Role | Resources |
| :--- | :--- | :--- | :--- | :--- |
| `ksqldb-server` | `confluentinc/cp-ksqldb-server:8.0.3` | `messaging-option` | Stream processing engine | 1.0 CPU / 512M RAM |
| `ksqldb-cli` | `confluentinc/cp-ksqldb-cli:8.0.3` | `ksql` | Interactive management CLI | Default |
| `ksql-datagen` | `confluentinc/ksqldb-examples:8.0.3` | `ksql` | Sample data generator | 0.5 CPU / 256M RAM |

> **Profile Note**: `ksqldb-server` uses the `messaging-option` profile (not `messaging`). It is NOT started by the standard `messaging` profile. `ksqldb-cli` and `ksql-datagen` use the `ksql` profile.

## Networking

- **ksqlDB Server URL**: Port `${KSQLDB_PORT:-8088}` (host-mapped to `${KSQLDB_HOST_PORT:-8088}`).
- **Dependencies**: Connects to `kafka-1..3` (via `infra_net`) and `schema-registry`.
- **Kafka Connect**: Integrates with `kafka-connect` at `http://kafka-connect:${KAFKA_CONNECT_PORT:-8083}`.

## Persistence

- **Data Volume**: `ksqldb-data-volume` mapped to `/var/lib/ksql`.
- **Host Path**: `${DEFAULT_DATA_DIR}/ksql`.

## Usage

### Start ksqlDB Server

```bash
docker compose --profile messaging-option up -d ksqldb-server
```

### Access Interactive CLI

```bash
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

### Example SQL

```sql
-- Create a stream from a Kafka topic
CREATE STREAM page_views (viewtime BIGINT, userid VARCHAR, pageid VARCHAR)
  WITH (KAFKA_TOPIC='page-views', VALUE_FORMAT='JSON');

-- Query the stream
SELECT userid, COUNT(*) AS view_count
  FROM page_views
  WINDOW TUMBLING (SIZE 1 MINUTE)
  GROUP BY userid
  EMIT CHANGES;
```

### Check Server Logs

```bash
docker compose logs ksqldb-server
```

## File Map

| Path | Description |
| --- | --- |
| `docker-compose.yml` | ksqlDB server, CLI, and datagen service definitions |
| `README.md` | Service overview and SQL examples (this file) |

## Documentation References

| Topic | Guide |
| --- | --- |
| Kafka Operations | [kafka-operations.md](../../../docs/guides/05-messaging/kafka-operations.md) |
| Messaging Context | [kafka-context.md](../../../docs/guides/05-messaging/kafka-context.md) |
