<!-- Target: docs/09.runbooks/04-data/analytics/ksqldb.md -->

# ksqlDB Recovery Runbook

: ksqlDB Stream Processing Recovery

---

## Overview (KR)

이 런북은 ksqlDB 스트림 처리 지연, 쿼리 실패 및 서버 연결 이슈 상황에 대한 실행 절차를 정의한다. Kafka와의 연결성을 복원하고 처리 무결성을 유지하기 위한 단계를 제공한다.

## Purpose

실시간 스트림 처리 파이프라인의 중단을 최소화하고, 잘못된 상태를 가진 쿼리를 안전하게 재시작하는 것을 목적으로 한다.

## Canonical References

- `[../../02.ard/0012-data-analytics-architecture.md]`
- `[../../07.guides/04-data/analytics/ksqldb.md]`
- `[../../08.operations/04-data/analytics/ksqldb.md]`

## When to Use

- ksqlDB 서버가 Kafka 브로커에 연결하지 못할 때.
- `ksql-cli`에서 특정 쿼리의 상태가 `RUNNING`이 아닐 때.
- 컨슈머 래그(Lag)가 급격히 증가하여 실시간성이 훼손될 때.

## Procedure or Checklist

### Checklist

- [ ] Kafka 브로커 가용성 확인 (`kafka-1:19092`)
- [ ] Schema Registry 가용성 확인 (`schema-registry:8081`)
- [ ] ksqlDB 서버 로그의 `KafkaException` 발생 여부 확인

### Procedure

1. **쿼리 상태 점검**:
   CLI에 접속하여 비정상 쿼리를 식별한다.
   ```sql
   SHOW QUERIES;
   DESCRIBE <QUERY_ID>;
   ```

2. **서버 상태 확인**:
   ```bash
   docker compose logs ksqldb-server --tail 50
   ```

3. **실패한 쿼리 재시작**:
   문제 있는 쿼리를 종료하고 다시 등록한다. (상태 보존 주의)
   ```sql
   TERMINATE <QUERY_ID>;
   -- 기존 CREATE 문 실행
   ```

4. **연결성 강제 갱신**:
   Kafka 브로커와의 메타데이터 갱신을 위해 서버를 재시작한다.
   ```bash
   docker compose restart ksqldb-server
   ```

## Verification Steps

- [ ] `SHOW QUERIES;` 결과 모든 핵심 쿼리가 `RUNNING` 상태인지 확인.
- [ ] 샘플 데이터를 Kafka에 전송하여 결과 테이블이 즉시 업데이트되는지 확인.

## Observability and Evidence Sources

- **Signals**: Kafka Consumer Lag metrics, ksqlDB `error_rate`.
- **Evidence to Capture**: `EXPLAIN <QUERY>;` 결과물, ksqlDB 서버 에러 스택트레이스.

## Safe Rollback or Recovery Procedure

- [ ] 쿼리 종료 전 `DESCRIBE EXTENDED <SINK_TOPIC>;`를 통해 현재 오프셋 기록.
- [ ] 데이터 정합성 이슈 시, 오프셋을 특정 시점으로 되돌려 재처리 수행.

## Related Operational Documents

- **Operations**: [docs/08.operations/04-data/analytics/ksqldb.md](../../08.operations/04-data/analytics/ksqldb.md)
