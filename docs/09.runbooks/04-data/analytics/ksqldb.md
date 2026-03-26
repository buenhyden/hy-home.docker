<!-- Target: docs/09.runbooks/04-data/analytics/ksqldb.md -->

# ksqlDB Recovery Runbook

: ksqlDB Stream Processing Layer

---

## Overview (KR)

이 런북은 ksqlDB 서비스 장애 시의 복구 절차를 정의한다. 스트림 지연(Lag), 스키마 레지스트리 연결 실패, 서버 리셋 등 주요 절차를 제공한다.

## Purpose

Ensure continuity of real-time data transformations and analytics.

## Canonical References

- `[../../02.ard/04-data/01-analytics-tier.md]`
- `../../../infra/04-data/analytics/ksql/docker-compose.yml`

## When to Use

- ksqlDB server health check fails.
- Streams/Tables stop emitting changes.
- Errors in logs regarding `Schema Registry` or `Bootstrap Servers`.

## Procedure or Checklist

### Procedure 1: Identifying Stream Lag

1. Open ksqlDB CLI.
2. Run `DESCRIBE <stream_name> EXTENDED;`
3. Check the `Consumer Group` lag metrics.
4. If lag is high, verify Kafka broker partitions and connectivity.

### Procedure 2: Schema Registry Connection Failure

1. Check if `schema-registry` is healthy: `curl http://schema-registry:8081/subjects`.
2. If unreachable, restart schema registry first.
3. Restart ksqlDB server to re-establish connection.

### Procedure 3: Full Server Reset (State Loss)

1. Stop services: `docker compose down ksqldb-server`
2. Wipe internal state volume: `sudo rm -rf ${DEFAULT_DATA_DIR}/ksql/*`
3. Restart: `docker compose up -d ksqldb-server`
4. Note: Permanent streams/tables must be re-created via CLI or scripts.

## Verification Steps

- [ ] Check server info: `curl -s http://ksqldb-server:8088/info`
- [ ] List streams: `SHOW STREAMS;` in CLI.

## Safe Rollback

- Re-creation of streams/tables should follow the versioned SQL scripts in the repository.

## Related Operational Documents

- **Operations**: `[../../../08.operations/04-data/analytics/ksqldb.md]`
