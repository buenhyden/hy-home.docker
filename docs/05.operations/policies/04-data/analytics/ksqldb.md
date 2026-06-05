---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/analytics/ksqldb.md -->

# ksqlDB Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/ksql`의 ksqlDB 운영 정책을 정의한다. current implementation은 `ksqldb-server`를 `data` profile로 제공하고, `ksqldb-cli` 및 `ksql-datagen`을 `ksql` profile 보조 서비스로 분리한다.

## Policy Scope

- **Systems**: `ksqldb-server`, `ksqldb-cli`, `ksql-datagen`
- **Dependencies**: Kafka brokers, Schema Registry, Kafka Connect
- **Persistence**: `ksqldb-data-volume`
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Required**: server changes must preserve Kafka bootstrap server, Schema Registry URL, Kafka Connect URL, and `KSQL_HEAP_OPTS` evidence in compose.
- **Required**: CLI/datagen usage must explicitly enable the `ksql` profile and must not be documented as always-on data services.
- **Required**: stream query lifecycle changes must capture query ID, source topic, sink topic, and rollback/reprocessing evidence.
- **Allowed**: temporary debug streams or datagen workloads when the affected topics and cleanup path are documented.
- **Disallowed**: assuming Docker Secret coverage for ksqlDB because the current compose does not declare secrets.

## Exceptions

Offset replay, query termination, or datagen workloads that affect shared Kafka topics require owner approval and captured topic/query evidence.

## Verification

- `test -f infra/04-data/analytics/ksql/docker-compose.yml`
- `curl -fsS http://ksqldb-server:8088/info` when the service is running
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Per stream topology change
- On Kafka/Schema Registry/Connect dependency change
- On ksqlDB image or heap setting change

## Related Documents

- [Operations policies index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/ksqldb.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/ksqldb.md)
- [Infra README](../../../../../infra/04-data/analytics/ksql/README.md)
