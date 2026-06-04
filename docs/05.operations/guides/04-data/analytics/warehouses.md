---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/analytics/warehouses.md -->

# StarRocks Usage Guide

## Usage

### Overview (KR)

이 문서는 `infra/04-data/analytics/warehouses`의 StarRocks 사용 가이드다. 현재 compose는 `starrocks-fe`와 `starrocks-be` 단일 pair를 제공하고, BE는 FE에 `ALTER SYSTEM ADD BACKEND "starrocks-be:9050"` 명령으로 등록된다.

### Usage Type

`system-guide`

### Target Audience

- Data Engineer
- Analytics Developer
- Operator
- AI Agent

### Purpose

- FE/BE service boundary와 bind-backed named volume을 이해한다.
- MySQL-compatible port `9030`, FE HTTP port `8030`, BE HTTP port `8040`을 구분한다.
- verified recovery는 paired runbook으로 넘긴다.

### Prerequisites

- `infra/04-data/analytics/warehouses/docker-compose.yml`
- MySQL client
- `infra_net` access

### Step-by-step Instructions

1. Compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/analytics/warehouses/docker-compose.yml
   ```

2. FE 상태를 확인한다.

   ```bash
   mysql -u root -h starrocks-fe -P 9030 -e "SHOW FRONTENDS;"
   ```

3. BE 등록 상태를 확인한다.

   ```bash
   mysql -u root -h starrocks-fe -P 9030 -e "SHOW BACKENDS;"
   ```

### Common Pitfalls

- service host를 `starrocks`로 가정하는 경우
- compose에 없는 Prometheus exporter를 current implementation으로 문서화하는 경우
- BE registration command를 실행 절차 없이 수동 반복하여 duplicate backend state를 만드는 경우

## Common Checks

- `test -f infra/04-data/analytics/warehouses/docker-compose.yml`
- `bash scripts/validation/check-doc-implementation-alignment.sh`
- `bash scripts/validation/check-repo-contracts.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/analytics/warehouses.md)을 따른다.

## Related Documents

- [Operations guides index](../../../README.md)
- [Operations policy](../../../policies/04-data/analytics/warehouses.md)
- [Recovery runbook](../../../runbooks/04-data/analytics/warehouses.md)
- [Infra README](../../../../../infra/04-data/analytics/warehouses/README.md)
