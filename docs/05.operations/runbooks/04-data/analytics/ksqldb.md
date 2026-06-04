---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/analytics/ksqldb.md -->

# ksqlDB Recovery Runbook

## ksqlDB Recovery Procedure

> Scope: ksqlDB server readiness, Kafka dependency checks, and query lifecycle evidence.

### Overview (KR)

이 런북은 `ksqldb-server`가 unhealthy이거나 Kafka/Schema Registry dependency 문제로 stream processing이 실패할 때 사용한다. CLI/datagen 절차는 `ksql` profile을 명시한 경우에만 적용한다.

### Purpose

- ksqlDB 장애와 upstream Kafka dependency 장애를 구분한다.
- query termination/replay 전 topic, query, offset evidence를 확보한다.
- profile boundary를 지키며 복구 절차를 수행한다.

### Canonical References

- **Spec**: [Analytics spec](../../../../03.specs/04-data-analytics/spec.md)
- **Policy**: [ksqlDB policy](../../../policies/04-data/analytics/ksqldb.md)
- **Guide**: [ksqlDB guide](../../../guides/04-data/analytics/ksqldb.md)

## When to Use

- `ksqldb-server` `/info` endpoint가 실패할 때
- Kafka brokers or Schema Registry dependency가 unavailable일 때
- query state가 expected running state와 다를 때

## Procedure

### Checklist

- [ ] `ksqldb-server` compose config를 확인한다.
- [ ] Kafka brokers and Schema Registry dependency 상태를 분리해 기록한다.
- [ ] query termination 전 query ID, source topic, sink topic, and offset evidence를 확보한다.

### Steps

1. Compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/ksql/docker-compose.yml
   bash scripts/validation/check-doc-implementation-alignment.sh
   ```

2. Server logs and readiness를 확인한다.

   ```bash
   docker logs ksqldb-server --tail 100
   curl -fsS http://ksqldb-server:8088/info
   ```

3. CLI가 필요한 경우 `ksql` profile로 접속한다.

   ```bash
   docker run --rm --network infra_net confluentinc/cp-ksqldb-cli:8.0.5 ksql http://ksqldb-server:8088
   ```

4. Query mutation은 evidence 확보 후 수행한다.

   ```sql
   SHOW QUERIES;
   EXPLAIN <QUERY_ID>;
   ```

### Verification Steps

- [ ] `/info` endpoint succeeds.
- [ ] required Kafka/Schema Registry dependencies are reachable.
- [ ] query changes have before/after evidence and owner approval when replay or termination is needed.

### Observability and Evidence Sources

- **Logs**: `ksqldb-server` logs
- **Metrics**: Kafka consumer lag if the messaging stack exposes it
- **Evidence**: query ID, source/sink topics, command class, dependency status

### Safe Rollback or Recovery Procedure

- N/A - no verified generic query rollback is documented for all ksqlDB workloads.
- Reprocessing or offset replay must be approved per topic/query and recorded separately.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: rerun docs validation after docs-only changes.

## Evidence

- Capture service logs summary, `/info` status, dependency status, and query evidence.
- Do not mutate topics or offsets without approval.

## Rollback or Recovery

N/A - no verified workload-independent rollback procedure exists for ksqlDB query state. Escalate for replay, offset changes, or destructive topic changes.

## Escalation

Escalate when Kafka/Schema Registry is unavailable, query replay is required, consumer lag cannot be explained, or service state diverges from compose evidence.

## Related Documents

- [Operations runbooks index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/ksqldb.md)
- [Operations policy](../../../policies/04-data/analytics/ksqldb.md)
