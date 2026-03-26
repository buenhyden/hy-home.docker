<!-- Target: docs/07.guides/04-data/analytics/ksqldb.md -->

# ksqlDB System Guide

> Guide for real-time stream processing with ksqlDB in the hy-home.docker ecosystem.

---

## Overview (KR)

이 문서는 ksqlDB 스트리밍 SQL 엔진에 대한 가이드다. Kafka 스트림과 테이블의 개념, CLI 사용법, 그리고 데이터 생성 패턴을 설명한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Architect

## Purpose

Help users built real-time analytical applications on top of Kafka streams using SQL.

## Prerequisites

- Healthy Kafka cluster (brokers reachable at `kafka-1:19092`).
- Healthy Schema Registry (reachable at `schema-registry:8081`).
- `data` profile active in Docker Compose.

## Step-by-step Instructions

### 1. Connecting to ksqlDB CLI
Use the interactive CLI to run SQL queries against the stream processor.
```bash
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

### 2. Creating a Stream
Define a schema over an existing Kafka topic.
```sql
CREATE STREAM events (
  id VARCHAR,
  val INT,
  timestamp BIGINT
) WITH (
  KAFKA_TOPIC='events',
  VALUE_FORMAT='JSON',
  TIMESTAMP='timestamp'
);
```

### 3. Creating a Materialized Table
Aggregating stream data into a stateful queryable table.
```sql
CREATE TABLE event_counts AS
  SELECT id, COUNT(*) AS total
  FROM events
  GROUP BY id
  EMIT CHANGES;
```

## Common Pitfalls

- **Serialization Mismatch**: Ensure `VALUE_FORMAT` matches the actual data in Kafka.
- **Consumer Group Lag**: Monitor `KSQL_KSQL_LOGGING_PROCESSING_TOPIC` for errors.
- **Resource Exhaustion**: ksqlDB consumes significant memory; monitor JVM Heap closely.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [ksqldb.md](../../../08.operations/04-data/analytics/ksqldb.md)
- **Runbook**: [ksqldb.md](../../../09.runbooks/04-data/analytics/ksqldb.md)
