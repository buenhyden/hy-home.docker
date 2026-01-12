# ksqlDB

## Overview

ksqlDB is a database purpose-built for stream processing applications.

## Service Details

- **Service**: `ksqldb-node1`
- **Image**: `bitnami/ksql:latest`
- **Port**: `${KSQLDB_HOST_PORT}:${KSQLDB_PORT}`
- **Volume**: `ksqldb-node-1-data-volume`

## Environment Variables

- `KSQL_BOOTSTRAP_SERVERS`: Kafka Connection string (e.g., `kafka-0:${KAFKA_PORT}`).

> **Note**: The current configuration refers to `kafka-0`, whereas the Kafka stack uses `kafka-1`, `2`, `3`. Verify connection settings if connectivity issues arise.
