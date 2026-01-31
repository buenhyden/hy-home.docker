# ksqlDB

## Overview

ksqlDB is a database purpose-built for stream processing applications. It allows you to build event streaming applications using a familiar SQL syntax.

## Profile

This stack is **optional** and runs under the `ksql` profile.

```bash
docker compose --profile ksql up -d ksqldb-server
```

## Services

| Service | Image | Role | Notes |
| --- | --- | --- | --- |
| `ksqldb-server` | `confluentinc/cp-ksqldb-server:8.0.3` | ksqlDB Engine (REST + Stream Processing) | `${KSQLDB_HOST_PORT}:${KSQLDB_PORT}` |
| `ksqldb-cli` | `confluentinc/cp-ksqldb-cli:8.0.3` | Interactive CLI Client | Internal-only |
| `ksql-datagen` | `confluentinc/ksqldb-examples:8.0.3` | Example data generator | Enabled via `ksql` profile |

## Networking

- **Network**: `infra_net`
- **Static IP**: *None assigned* (Dynamic IP allocation)
- **Traefik**: **Not Configured**. This service is currently **internal only** within the docker network, or accessible via the exposed host port.

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `KSQL_BOOTSTRAP_SERVERS` | Kafka Brokers | `kafka-1:${KAFKA_INTERNAL_PORT},kafka-2:${KAFKA_INTERNAL_PORT},kafka-3:${KAFKA_INTERNAL_PORT}` |

## Persistence

- **Data Persistence**: `ksqldb-data-volume` matches `/var/lib/ksql` inside the container.
- **Host Path**: Mapped to `${DEFAULT_DATABASE_DIR}/ksqldb/node1`

## Usage

### Accessing via CLI (Internal)

`ksqldb-cli` 서비스를 통해 접속할 수 있습니다:

```bash
docker exec -it ksqldb-cli ksql http://ksqldb-server:${KSQLDB_PORT}
```

### Checking Logs

```bash
docker logs ksqldb-server
```

## File Map

| Path | Description |
| --- | --- |
| `docker-compose.yml` | ksqlDB server + CLI + example datagen profile. |
| `README.md` | Service overview and usage notes. |
