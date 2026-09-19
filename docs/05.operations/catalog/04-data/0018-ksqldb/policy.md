---
title: "ksqlDB Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0018"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# ksqlDB Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/ksql`의 ksqlDB 운영 정책을 정의한다. current implementation은 server, CLI, datagen companion 모두를 `ksql` profile의 OPTIONAL on-demand stack으로 제공한다.

## Policy Scope

- **Systems**: `ksqldb-server`, `ksqldb-cli`, `ksql-datagen`
- **Dependencies**: Kafka brokers, Schema Registry, Kafka Connect
- **Persistence**: `ksqldb-data-volume`
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Activation**: validate from the root with `docker compose --profile ksql config --quiet`. `ksql-datagen` is readiness-only and must not be described as automatic sample ingestion.
- **Authorization**: current Compose declares no TLS, authentication, ACL, RBAC, or secret mount for ksqlDB. Keep host publication bounded to approved development use; any broader exposure requires Kafka/ksqlDB authentication design first.
- **Recovery**: preserve the ksqlDB command topic, source/sink/internal topics, Schema Registry subjects, service ID, SQL definition export, and required UDFs. The local `ksqldb-data-volume` is rebuildable cache/state and is not sufficient alone.
- **Resources and retention**: retain the server heap and inherited 1 CPU/512 MiB limit until query lag/state-store metrics justify change. Topic retention and compaction belong to the Kafka owner and must cover the recovery horizon.
- **Upgrade**: server and CLI must move through an upstream-supported compatibility path; inspect breaking changes and rehearse command-topic replay using a separate service ID where in-place upgrade is unsupported.
- **Removal**: confirm every persistent query and downstream consumer is retired, retain SQL/UDF/Schema Registry and Kafka topic recovery evidence with expiry/owner, and require separate approval before deleting the command topic, internal topics, or local volume.
- **Removal**: stop persistent queries, identify all owned topics/connectors/schema subjects, preserve SQL and recovery evidence, then obtain approval before deleting topics or the local volume.
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
- `python3 scripts/validation/check-document-links.py --mode all`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- Per stream topology change
- On Kafka/Schema Registry/Connect dependency change
- On ksqlDB image or heap setting change

## Traceability

- Declared parent: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0018`), [Runbook](runbook.md) (`RUN-0018`)

## Related Documents

- [ksqlDB upgrade guidance](https://docs.confluent.io/platform/current/ksqldb/upgrading.html)
- [Compose implementation](../../../../../infra/04-data/analytics/ksql/docker-compose.yml)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations policies index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/ksql/README.md)
