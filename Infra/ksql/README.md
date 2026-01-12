# KSQLDB

## Overview

Streaming SQL Engine for Apache Kafka.

## Services

- **ksqldb-node1**: KSQLDB Server node.
  - Port: `${KSQLDB_PORT}`
  - Depends on: `kafka-0` (from Kafka cluster)

## Configuration

### Environment Variables

- `KSQL_BOOTSTRAP_SERVERS`: Kafka broker connection (`kafka-0:${KAFKA_PORT}`).

### Volumes

- `ksqldb-node-1-data-volume`: `/bitnami/ksql`

## Networks

- `infra_net`
