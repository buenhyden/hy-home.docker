---
title: "InfluxDB Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
artifact_id: "GDE-0017"
parent_ids:
- "POL-0017"
implementation_services:
  infra/04-data/influxdb/docker-compose.yml:
  - 'influxdb'
created: "2026-05-10"
---

# InfluxDB Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 `infra/04-data/influxdb`의 InfluxDB 사용 가이드다. 현재 구현은 InfluxDB 3 Core 단일 compose이며 database와 HTTP line-protocol endpoint/schema source contract를 정의한다.

### Current implementation

| Field | Current contract |
| --- | --- |
| Classification and consumer | OPTIONAL, on-demand time-series experiment이다. 명명된 production workload나 측정된 capacity는 확인되지 않았다. |
| Compose ownership | root project는 [InfluxDB Compose fragment](../../../infra/04-data/influxdb/docker-compose.yml)를 include한다. profile은 `influxdb`, service는 `influxdb`이다. Compose가 runtime image를 소유하고 Renovate가 update 제안을 소유한다. |
| Data flow and exposure | `edge_net`의 client가 container port `8181`에서 HTTP로 write/query한다. Traefik이 `gateway-standard-chain@file`을 통해 `influxdb.${DEFAULT_URL}`을 publish한다. 직접 host port는 없다. |
| Persistence | bind-backed named volume `influxdb-data`와 `influxdb-plugins`가 `${DEFAULT_DATA_DIR}/influxdb` 아래로 매핑된다. server는 node ID `node0`으로 local object storage를 사용한다. |
| Configuration and credentials | command가 data와 plugin directory를 선언한다. leaf service는 Docker Secret을 mount하지 않고 token을 provision하지 않는다. 따라서 authenticated write에는 별도로 관리되는 runtime credential이 필요하다. |
| Health and resources | `/`는 `200`, `204`, `401`을 수용한다. `template-stateful-med`가 1 CPU, 512 MiB, restart policy, log rotation, dropped capabilities, `no-new-privileges`를 제공한다. |
| Recovery and upgrade | InfluxDB 3 Core에는 내장 backup 명령이 없다. 승인된 quiet/downtime window에만 문서화된 순서의 local-object-store 복사를 사용하고, 새 호환 instance로 restore한 뒤 cutover 전에 검증한다. Compose pin을 변경하기 전에 Core release note를 검토한다. |

### Identity-specific behavior

InfluxDB3 Core3.11.5 의 `influxdb3 serve --object-store=file`와 node-id 설정이 실행 계약이다. InfluxDB2 org/bucket CLI 를 혼용하지 않는다. `/`의 200/204/401 허용은 authenticated query/write 성공을 뜻하지 않는다. 두 bind(node state/plugin)의 역할과 token custody 를 함께 보존하며 Core 백업은 object-store 일관성 순서와 node identity 가 필요하다. tag 는 설치 관측이 아니다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `influxdb` | 시계열 Core 서버; 파일 object store와 plugin state | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/04-data/influxdb/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../98.archive/completed/03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

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

- `infra/04-data/influxdb/docker-compose.yml`
- 요청 입력: operator가 선택한 database 이름. 보존된 registry의 `influxdb_api_token`, `influxdb_password` 항목은 local metadata일 뿐 leaf server wiring이나 provisioning이 아니다
- 서비스 간 점검을 위한 `edge_net` 접근 권한

### Step-by-step Instructions

1. Primary compose contract 위치를 확인한다.

   ```bash
   test -f infra/04-data/influxdb/docker-compose.yml
   ```

2. Current health endpoint contract를 확인한다.

   ```bash
   curl -i http://influxdb:8181/
   ```

   compose healthcheck는 token-protected service readiness도 auth challenge를 반환할 수 있으므로 `/`에서 HTTP `200`, `204`, `401`을 수용한다. 이 명령은 승인된 runtime context에서만 실행하며, 본 변경은 source-only verification만 수행한다.

3. Line Protocol write contract를 확인한다.

   `POST http://influxdb:8181/api/v3/write_lp?db=<operator-selected-database>`는 authorized operator/named token을 요구한다. Token creation/provisioning과 authenticated write acceptance에는 separate runtime approval이 필요하며 아직 검증되지 않았다.

### Common Pitfalls

- database 이름 대신 다른 resource 모델을 적용하는 경우
- Root secret declaration을 leaf server token provisioning으로 간주하는 경우
- host port가 직접 선언되어 있다고 가정하는 경우

### Common Checks

- `test -f infra/04-data/influxdb/docker-compose.yml`
- `/api/v3/write_lp`, operator-selected database name, port `8181` source references가 일치하는지 확인한다. Source-only validation cannot prove authorization.
- `python3 scripts/validation/check-document-links.py --mode all`
- 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0017-influxdb.md)을 따른다.

### Traceability

- Declared parent: [InfluxDB Operations Policy](../policies/0017-influxdb.md) (`POL-0017`)
- Governing authority: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Policy](../policies/0017-influxdb.md) (`POL-0017`), [Runbook](../runbooks/0017-influxdb.md) (`RUN-0017`)

## Related Documents

- [InfluxDB 3 Core backup and restore](https://docs.influxdata.com/influxdb3/core/admin/backup-restore/)
- [InfluxDB 3 Core installation and upgrade context](https://docs.influxdata.com/influxdb3/core/install/)
- [InfluxDB 3 Core source and licence](https://github.com/influxdata/influxdb)

- [Operations guides index](../README.md)
- [Operations policy](../policies/0017-influxdb.md)
- [Recovery runbook](../runbooks/0017-influxdb.md)
- [Infra README](../../../infra/04-data/influxdb/README.md)
- [Compose implementation: infra/04-data/influxdb/docker-compose.yml](../../../infra/04-data/influxdb/docker-compose.yml)
