---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/analytics/influxdb.md -->

# InfluxDB Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 사용 가이드다. 현재 구현은 InfluxDB 3 Core 단일 compose이며 database와 HTTP line-protocol endpoint/schema source contract를 정의한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

- InfluxDB 3 Core database/endpoint source contract와 runtime token-provisioning 경계를 이해한다.
- Runtime-unverified token provisioning, healthcheck, service port, persistent volume 경계를 확인한다.
- 장애 대응은 paired runbook으로 넘긴다.

### Prerequisites

- `infra/04-data/analytics/influxdb/docker-compose.yml`
- Environment key `INFLUXDB_DB_NAME`; root declarations for `influxdb_api_token` and `influxdb_password` are metadata, not leaf server wiring or provisioning
- `infra_net` access for service-to-service checks

### Step-by-step Instructions

1. Primary compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/analytics/influxdb/docker-compose.yml
   ```

2. Current health endpoint contract를 확인한다.

   ```bash
   curl -i http://influxdb:8181/
   ```

   The compose healthcheck accepts HTTP `200`, `204`, or `401` from `/` because token-protected service readiness can still return an auth challenge. 이 명령은 승인된 runtime context에서만 실행하며, 본 변경은 source-only verification만 수행한다.

3. Line Protocol write contract를 확인한다.

   `POST http://influxdb:8181/api/v3/write_lp?db=${INFLUXDB_DB_NAME}`는 authorized operator/named token을 요구한다. Token creation/provisioning과 authenticated write acceptance는 separate runtime approval이 필요하며 아직 검증되지 않았다.

### Common Pitfalls

- database 이름 대신 다른 resource 모델을 적용하는 경우
- Root secret declaration을 leaf server token provisioning으로 간주하는 경우
- host port가 직접 선언되어 있다고 가정하는 경우

## Common Checks

- `test -f infra/04-data/analytics/influxdb/docker-compose.yml`
- `/api/v3/write_lp`, `INFLUXDB_DB_NAME`, port `8181` source references가 일치하는지 확인한다. Source-only validation cannot prove authorization.
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/analytics/influxdb.md)을 따른다.

## Related Documents

- [Operations guides index](../../../README.md)
- [Operations policy](../../../policies/04-data/analytics/influxdb.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/influxdb.md)
- [Infra README](../../../../../infra/04-data/analytics/influxdb/README.md)
