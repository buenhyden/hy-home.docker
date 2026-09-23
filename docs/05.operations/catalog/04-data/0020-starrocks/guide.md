---
title: "StarRocks Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0020"
parent_ids:
- "POL-0020"
implementation_services:
  infra/04-data/analytics/starrocks/docker-compose.yml:
  - 'starrocks-be'
  - 'starrocks-fe'
created: "2026-05-10"
---

# StarRocks Usage Guide

## Usage

### Overview

이 문서는 `infra/04-data/analytics/starrocks`의 StarRocks 사용 가이드다. `starrocks` profile은 on-demand OPTIONAL analytical-database experiment로 단일 FE/BE pair를 제공하고, BE 시작 전에 FE에 `starrocks-be:9050`을 등록한다. 같은 호스트의 pair는 HA가 아니다.

### Current implementation

| Field | Current contract |
| --- | --- |
| Source and updater | [Compose](../../../../../infra/04-data/analytics/starrocks/docker-compose.yml) owns `starrocks-fe` and `starrocks-be`; Renovate proposes image updates. |
| Exposure and flow | FE publishes MySQL `9030` and HTTP `8030`; BE publishes HTTP `8040` on the host. Both join `lab_net`; no gateway or TLS boundary is declared. |
| Persistence | `starrocks-fe-data` stores FE metadata and `starrocks-be-data` stores BE data below `${DEFAULT_DATA_DIR}/starrocks`. Both are required for coherent recovery. |
| Auth and security | Compose supplies no Docker Secret and health checks connect as native `root` without a password. Treat the stack as isolated LAB/OPTIONAL use until credentials and exposure are reviewed. Both services run as root with `no-new-privileges`; the DB-high template supplies 2 CPUs/2 GiB each. |
| Backup and restore | Use StarRocks `BACKUP`/`RESTORE` with a configured remote repository and least-privilege `REPOSITORY` plus `EXPORT` grants. Restore asynchronously into an isolated compatible cluster and database before cutover. |
| Upgrade and licence | Review the StarRocks upgrade path and compatibility notes for FE metadata and BE data. StarRocks is Apache-2.0; no enterprise-only backup command is assumed. |

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

- `infra/04-data/analytics/starrocks/docker-compose.yml`
- MySQL client
- `lab_net` access

### Step-by-step Instructions

1. Compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/analytics/starrocks/docker-compose.yml
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

- `test -f infra/04-data/analytics/starrocks/docker-compose.yml`
- `python3 scripts/validation/check-document-links.py --mode all`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [StarRocks Operations Policy](policy.md) (`POL-0020`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Policy](policy.md) (`POL-0020`), [Runbook](runbook.md) (`RUN-0020`)

## Related Documents

- [StarRocks backup and restore statements](https://docs.starrocks.io/docs/sql-reference/sql-statements/backup_restore/)
- [StarRocks authentication and authorization](https://docs.starrocks.io/docs/best_practices/authentication_authorization/)
- [StarRocks source and licence](https://github.com/StarRocks/starrocks)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations guides index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
- [Infra README](../../../../../infra/04-data/analytics/starrocks/README.md)
- [Compose implementation: infra/04-data/analytics/starrocks/docker-compose.yml](../../../../../infra/04-data/analytics/starrocks/docker-compose.yml)
