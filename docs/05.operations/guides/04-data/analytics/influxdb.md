---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/analytics/influxdb.md -->

# InfluxDB Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 사용 가이드다. 현재 primary compose는 InfluxDB 3.x Core이며, `docker-compose.v2.yml`은 InfluxDB 2.x legacy Flux 호환 경로로만 유지된다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

- InfluxDB primary/legacy compose 경계를 이해한다.
- API token secret, healthcheck, service port, persistent volume 계약을 확인한다.
- 장애 대응은 paired runbook으로 넘긴다.

### Prerequisites

- `infra/04-data/analytics/influxdb/docker-compose.yml`
- Docker Secret `influxdb_api_token` and `influxdb_password`
- `infra_net` access for service-to-service checks

### Step-by-step Instructions

1. Primary compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/analytics/influxdb/docker-compose.yml
   ```

2. Primary v3 runtime endpoint를 확인한다.

   ```bash
   curl -i http://influxdb:8181/
   ```

   The compose healthcheck accepts HTTP `200`, `204`, or `401` from `/` because token-protected service readiness can still return an auth challenge.

3. Legacy v2 path가 필요한 경우에만 `docker-compose.v2.yml`을 선택한다.

   ```bash
   test -f infra/04-data/analytics/influxdb/docker-compose.v2.yml
   ```

### Common Pitfalls

- InfluxDB 3.x primary에 InfluxDB 2.x bucket/Flux commands를 그대로 적용하는 경우
- `/run/secrets/influxdb_api_token` 값을 출력하거나 shell history에 남기는 경우
- host port가 직접 선언되어 있다고 가정하는 경우

## Common Checks

- `test -f infra/04-data/analytics/influxdb/docker-compose.yml`
- `test -f infra/04-data/analytics/influxdb/docker-compose.v2.yml`
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/analytics/influxdb.md)을 따른다.

## Related Documents

- [Operations guides index](../../../README.md)
- [Operations policy](../../../policies/04-data/analytics/influxdb.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/influxdb.md)
- [Infra README](../../../../../infra/04-data/analytics/influxdb/README.md)
