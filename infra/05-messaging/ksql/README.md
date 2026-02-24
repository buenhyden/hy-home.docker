# ksqlDB

ksqlDB is the streaming SQL engine for Apache Kafka. It allows you to build stream processing applications using a SQL-like syntax.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `ksqldb-server` | `cp-ksqldb-server:8.0.3` | Stream Processing | 1.0 CPU / 1G RAM |
| `ksqldb-cli` | `cp-ksqldb-cli:8.0.3` | Management CLI | Default |

## Networking

- **URL**: `${KSQLDB_HOST_PORT}` (Host) / `8088` (Internal).
- **Dependencies**: Connects to `kafka-1..3` and `schema-registry`.

## Persistence

- **Data**: `ksqldb-data-volume` mapped to `/var/lib/ksql`.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and SQL examples.  |
