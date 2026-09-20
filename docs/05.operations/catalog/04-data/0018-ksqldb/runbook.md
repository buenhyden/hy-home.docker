---
title: "ksqlDB Recovery Runbook"
version: "1.0.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0018"
parent_ids:
- "GDE-0018"
created: "2026-05-17"
---

# ksqlDB Recovery Runbook

## Overview

> Scope: ksqlDB server readiness, Kafka dependency checks, and query lifecycle evidence.

이 런북은 `ksqldb-server`가 unhealthy이거나 Kafka/Schema Registry dependency 문제로 stream processing이 실패할 때 사용한다. CLI/datagen 절차는 `ksql` profile을 명시한 경우에만 적용한다.

### Purpose

- ksqlDB 장애와 upstream Kafka dependency 장애를 구분한다.
- query termination/replay 전 topic, query, offset evidence를 확보한다.
- profile boundary를 지키며 복구 절차를 수행한다.

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
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. Server logs and readiness를 확인한다.

   ```bash
   docker compose --profile ksql logs --tail 100 ksqldb-server
   curl -fsS http://ksqldb-server:8088/info
   ```

3. CLI가 필요한 경우 `ksql` profile로 접속한다.

   ```bash
   docker compose --profile ksql run --rm --entrypoint ksql ksqldb-cli http://ksqldb-server:8088
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

### Planned isolated recovery

This procedure is source-backed and **was not executed in this task**.

1. Record the service ID, persistent queries, streams/tables/types, UDFs, connectors, source/sink/internal topics, Schema Registry subjects, and Kafka recovery point. Pause query and topic mutations under a named approval.
2. Preserve SQL definitions and the ksqlDB command topic together with the Kafka and Schema Registry recovery artifacts. Do not treat `ksqldb-data-volume` as the authoritative backup.
3. Build a fresh isolated Kafka/Schema Registry/ksqlDB target on compatible versions and a non-conflicting network/service ID. Restore Kafka and schemas through their owning runbooks, then replay the reviewed SQL definitions or supported command-topic path.
4. Use the current `ksqldb-cli` Compose service to compare `SHOW QUERIES`, streams, tables, schemas, offsets, and representative query results. Validate that no experimental datagen input was introduced.
5. If replay, schema, or result validation fails, discard the isolated stack and retry from untouched artifacts. Never reset offsets or delete internal topics to force success.
6. Production cutover, offset changes, or destructive topic cleanup need separate approval. Recovery remains unverified until a full isolated rehearsal succeeds.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: rerun docs validation after docs-only changes.

## Evidence

- Capture service logs summary, `/info` status, dependency status, and query evidence.
- Do not mutate topics or offsets without approval.

## Rollback or Recovery

Rollback means leaving the existing Kafka/ksqlDB stack unchanged and discarding the isolated candidate. An in-place binary rollback is allowed only when the upstream version path and command-topic format remain compatible.

## Escalation

Escalate when Kafka/Schema Registry is unavailable, query replay is required, consumer lag cannot be explained, or service state diverges from compose evidence.

## Traceability

- Declared parent: [ksqlDB Usage Guide](guide.md) (`GDE-0018`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0018`), [Policy](policy.md) (`POL-0018`)

## Related Documents

- [ksqlDB architecture and command topic](https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html)
- [ksqlDB upgrade guidance](https://docs.confluent.io/platform/current/ksqldb/upgrading.html)
- [Compose implementation](../../../../../infra/04-data/analytics/ksql/docker-compose.yml)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations runbooks index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
