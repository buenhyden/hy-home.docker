---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/analytics/ksqldb.md -->

# ksqlDB Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/analytics/ksql`의 ksqlDB 사용 가이드다. 현재 compose는 `ksqldb-server`를 `data` profile로 실행하고, `ksqldb-cli`와 `ksql-datagen`은 `ksql` profile의 보조 job/tooling service로 유지한다.

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
   docker compose --profile ksql run --rm ksqldb-cli ksql http://ksqldb-server:8088
   ```

### Common Pitfalls

- `ksqldb-cli`와 `ksql-datagen`을 항상 실행되는 data service로 오해하는 경우
- Schema Registry 또는 Kafka Connect 없이 stream query failure를 ksqlDB 단독 장애로 판단하는 경우
- ksqlDB compose가 Docker Secrets를 선언한다고 가정하는 경우

## Common Checks

- `test -f infra/04-data/analytics/ksql/docker-compose.yml`
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/analytics/ksqldb.md)을 따른다.

## Related Documents

- [Operations guides index](../../../README.md)
- [Operations policy](../../../policies/04-data/analytics/ksqldb.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/ksqldb.md)
- [Infra README](../../../../../infra/04-data/analytics/ksql/README.md)
