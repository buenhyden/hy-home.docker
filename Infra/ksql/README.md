# ksqlDB

## Overview

ksqlDB is a database purpose-built for stream processing applications. It allows you to build event streaming applications using a familiar SQL syntax.

## Services

- **Service Name**: `ksqldb-node1`
- **Image**: `bitnami/ksql:latest`
- **Exposed Port**: `${KSQLDB_HOST_PORT}:${KSQLDB_PORT}` (Default usually 8088)

## Networking

- **Network**: `infra_net`
- **Static IP**: *None assigned* (Dynamic IP allocation)
- **Traefik**: **Not Configured**. This service is currently **internal only** within the docker network, or accessible via the exposed host port.

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `KSQL_BOOTSTRAP_SERVERS` | Kafka Brokers | `kafka-0:${KAFKA_PORT}` |

> [!WARNING]
> **Configuration Mismatch**: The current configuration points to `kafka-0`. However, the main Kafka stack (in `infra/kafka`) uses `kafka-1`, `kafka-2`, and `kafka-3`.
> Verify if `kafka-0` exists in another context or if this needs to be updated to `kafka-1:${KAFKA_PORT}`.

## Persistence

- **Data Persistence**: `ksqldb-node-1-data-volume` matches `/bitnami/ksql` inside the container.
- **Host Path**: Mapped to `${DEFAULT_DATABASE_DIR}/ksqldb/node1`

## Usage

### Accessing via CLI (Internal)

Since the `ksqldb-cli` service is commented out in the compose file, you can access the CLI by executing into the node:

```bash
docker exec -it ksqldb-node1 ksql http://localhost:8088
```

### Checking Logs

```bash
docker logs ksqldb-node1
```
