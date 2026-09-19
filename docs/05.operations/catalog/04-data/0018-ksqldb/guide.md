---
title: "ksqlDB Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0018"
parent_ids:
- "POL-0018"
implementation_services:
  infra/04-data/analytics/ksql/docker-compose.yml:
  - 'ksql-datagen'
  - 'ksqldb-cli'
  - 'ksqldb-server'
created: "2026-05-10"
---

# ksqlDB Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/analytics/ksql`의 ksqlDB 사용 가이드다. 현재 Compose의 세 서비스는 모두 `ksql` profile에 속하며 on-demand OPTIONAL stream-processing 실험으로 유지한다.

### Current implementation

| Field | Current contract |
| --- | --- |
| Services and flow | `ksqldb-server` connects to `kafka-1..3`, `schema-registry`, and `kafka-connect`; `ksqldb-cli` is an interactive companion; `ksql-datagen` only waits for Kafka/Schema Registry and tails. It does not load sample data automatically. |
| Network and exposure | All services use `infra_net`; only server port `${KSQLDB_HOST_PORT:-8088}` is host-published. No Traefik route or Docker Secret is declared. |
| Persistence | `ksqldb-data-volume` persists local server state, while durable command and stream state also depends on Kafka internal/source/sink topics and Schema Registry. The local volume alone is not a complete recovery point. |
| Configuration | `KSQL_BOOTSTRAP_SERVERS`, `KSQL_KSQL_SCHEMA_REGISTRY_URL`, `KSQL_KSQL_CONNECT_URL`, listeners, replication factor, and 512 MiB JVM heap are declared in Compose. |
| Health and resources | `/info` is the readiness endpoint. The server inherits 1 CPU/512 MiB; CLI and datagen inherit low-tier limits and dependency health gates. |
| Upgrade and licence | Keep CLI/server compatibility, review the Confluent upgrade notes, command-topic compatibility, UDFs, and Kafka/Schema versions. ksqlDB uses the Confluent Community License, so distribution or service use needs licence review. |

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Data Engineer
- AI Agent

### Purpose

- ksqlDB server, CLI, datagen profile boundary를 이해한다.
- Kafka, Schema Registry, Kafka Connect dependency를 확인한다.
- stream/table SQL examples를 runtime 절차와 분리한다.

### Prerequisites

- Kafka brokers `kafka-1`, `kafka-2`, `kafka-3`
- Schema Registry service `schema-registry`
- Optional Kafka Connect service `kafka-connect`
- `infra/04-data/analytics/ksql/docker-compose.yml`

### Step-by-step Instructions

1. Compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/analytics/ksql/docker-compose.yml
   ```

2. Server readiness endpoint를 확인한다.

   ```bash
   curl -fsS http://ksqldb-server:8088/info
   ```

3. CLI profile은 server가 healthy일 때만 실행한다.

   ```bash
   docker compose --profile ksql run --rm --entrypoint ksql ksqldb-cli http://ksqldb-server:8088
   ```

### Common Pitfalls

- `ksqldb-cli`와 `ksql-datagen`을 항상 실행되는 data service로 오해하는 경우
- Schema Registry 또는 Kafka Connect 없이 stream query failure를 ksqlDB 단독 장애로 판단하는 경우
- ksqlDB compose가 Docker Secrets를 선언한다고 가정하는 경우

## Common Checks

- `test -f infra/04-data/analytics/ksql/docker-compose.yml`
- `python3 scripts/validation/check-document-links.py --mode all`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [ksqlDB Operations Policy](policy.md) (`POL-0018`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Policy](policy.md) (`POL-0018`), [Runbook](runbook.md) (`RUN-0018`)

## Related Documents

- [ksqlDB architecture and command topic](https://docs.confluent.io/platform/current/ksqldb/operate-and-deploy/how-it-works.html)
- [ksqlDB upgrade guidance](https://docs.confluent.io/platform/current/ksqldb/upgrading.html)
- [ksqlDB source and licence](https://github.com/confluentinc/ksql)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations guides index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/ksql/README.md)
- [Compose implementation: infra/04-data/analytics/ksql/docker-compose.yml](../../../../../infra/04-data/analytics/ksql/docker-compose.yml)
