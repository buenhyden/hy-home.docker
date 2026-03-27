<!-- Target: docs/07.guides/04-data/analytics/ksqldb.md -->

# ksqlDB System Guide

> Guide for real-time stream processing with ksqlDB in the hy-home.docker ecosystem.

---

## Overview (KR)

이 문서는 ksqlDB 스트리밍 SQL 엔진에 대한 가이드다. Kafka 스트림과 테이블의 개념, CLI 사용법, 그리고 데이터 생성 패턴을 설명한다. 실시간 데이터 분석 및 변환을 위한 스트림 처리 애플리케이션 구축의 핵심 지침을 제공한다.

## Guide Type

`system-guide`

## Target Audience

- Developer
- Operator
- Architect

## Purpose

이 가이드는 사용자가 SQL을 사용하여 Kafka 스트림 위에 실시간 분석 애플리케이션을 구축하도록 돕는다.

## Prerequisites

- 정상 작동하는 Kafka 클러스터 (`kafka-1:19092` 접근 가능).
- 정상 작동하는 Schema Registry (`schema-registry:8081` 접근 가능).
- Docker Compose의 `data` 프로필 활성화.

## Step-by-step Instructions

### 1. ksqlDB CLI 연결 (Connecting to ksqlDB CLI)

대화형 CLI를 사용하여 스트림 프로세서에 대해 SQL 쿼리를 실행한다.

```bash
docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
```

### 2. 스트림 생성 (Creating a Stream)

기존 Kafka 토픽에 대해 스키마를 정의한다.

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

### 3. 실체화된 테이블 생성 (Creating a Materialized Table)

스트림 데이터를 상태가 있는 쿼리 가능한 테이블로 집계한다.

```sql
CREATE TABLE event_counts AS
  SELECT id, COUNT(*) AS total
  FROM events
  GROUP BY id
  EMIT CHANGES;
```

## Common Pitfalls

- **직렬화 불일치 (Serialization Mismatch)**: `VALUE_FORMAT`이 Kafka의 실제 데이터와 일치하는지 확인한다.
- **컨슈머 그룹 지연 (Consumer Group Lag)**: 에러 확인을 위해 `KSQL_KSQL_LOGGING_PROCESSING_TOPIC`을 모니터링한다.
- **자원 고갈 (Resource Exhaustion)**: ksqlDB는 상당한 메모리를 소비하므로 JVM Heap을 면밀히 모니터링한다.

## Related Documents

- **PRD**: [2026-03-26-04-data-analytics.md](../../../01.prd/2026-03-26-04-data-analytics.md)
- **ARD**: [0012-data-analytics-architecture.md](../../../02.ard/0012-data-analytics-architecture.md)
- **ADR**: [0015-analytics-engine-selection.md](../../../03.adr/0015-analytics-engine-selection.md)
- **Spec**: [spec.md](../../../04.specs/04-data-analytics/spec.md)
- **Operation**: [ksqldb.md](../../../08.operations/04-data/analytics/ksqldb.md)
- **Runbook**: [ksqldb.md](../../../09.runbooks/04-data/analytics/ksqldb.md)
