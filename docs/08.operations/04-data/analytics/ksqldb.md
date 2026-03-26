<!-- Target: docs/08.operations/04-data/analytics/ksqldb.md -->

# ksqlDB Operations Policy

> Governance standards for real-time stream processing.

---

## Overview (KR)

이 문서는 ksqlDB 운영 정책을 정의한다. 프로세싱 로그 보존, JVM 힙 관리, 그리고 자동 토픽 생성 정책을 규정한다.

## Policy Scope

Governs all stream processing workloads running on the ksqlDB server.

## Applies To

- **Systems**: ksqldb-server
- **Agents**: Developers, AI agents creating streams
- **Environments**: Production, Lab

## Controls

- **Required**:
  - `KSQL_KSQL_LOGGING_PROCESSING_TOPIC_REPLICATION_FACTOR` must be at least 3 for production.
  - All permanent streams/tables MUST be documented in the technical spec.
- **Allowed**:
  - Auto-creation of internal processing topics.
  - Use of `ksql-datagen` for lab and staging environments.
- **Disallowed**:
  - Running ksqlDB with less than 512MB heap in production.
  - Deleting underlying Kafka topics without dropping the associated ksqlDB stream/table first.

## Resource Management

| Metric | Target Value | Action on Threshold |
|--------|--------------|---------------------|
| JVM Heap Usage | < 80% | Scale memory or optimize queries |
| Stream Lag | < 1000 records | Check consumer group health |
| Error Rate | < 1/min | Investigate Processing Log |

## Review Cadence

- Per major release or schema change.

## Related Documents

- **ARD**: `[../../02.ard/04-data/analytics-tier.md]`
- **Runbook**: `[../../../09.runbooks/04-data/analytics/ksqldb.md]`
