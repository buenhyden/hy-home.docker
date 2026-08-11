---
status: active
artifact_id: policy-0020
artifact_type: policy
parent_ids: []
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/04-data/ops-0020-analytics-warehouses/policy.md -->

# StarRocks Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/warehouses`의 StarRocks 운영 정책을 정의한다. current implementation은 `starrocks-fe`와 `starrocks-be` 단일 pair를 `data` profile로 제공하고, FE/BE bind-backed named volumes와 compose healthchecks를 사용한다.

## Policy Scope

- **Systems**: `starrocks-fe`, `starrocks-be`
- **Persistence**: `starrocks-fe-data`, `starrocks-be-data`
- **Interfaces**: FE MySQL-compatible port `9030`, FE HTTP port `8030`, BE HTTP port `8040`
- **Environments**: repo-local, development, homelab, and production-like rehearsals

## Controls

- **Required**: BE registration must preserve the compose command that adds `starrocks-be:9050` to FE before starting BE.
- **Required**: FE and BE health evidence must use `SHOW FRONTENDS` and `SHOW BACKENDS` through `starrocks-fe:9030`.
- **Required**: data load retry procedures must record label, database, table, and final load state.
- **Allowed**: schema and load examples for development when they do not imply benchmark completion.
- **Disallowed**: documenting undeclared Prometheus exporters, undeclared Docker Secrets, or multi-node HA topology as current implementation.

## Exceptions

Manual FE metadata changes, backend add/drop operations, or destructive data cleanup require owner approval and captured pre-change state.

## Verification

- `test -f infra/04-data/analytics/warehouses/docker-compose.yml`
- `mysql -u root -h starrocks-fe -P 9030 -e "SHOW FRONTENDS;"`
- `mysql -u root -h starrocks-fe -P 9030 -e "SHOW BACKENDS;"`
- `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- On StarRocks image, FE/BE volume, port, or BE registration command change
- Monthly when load or schema examples are used as operating procedures

## Related Documents

- [Operations policies index](../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../infra/04-data/analytics/warehouses/README.md)
