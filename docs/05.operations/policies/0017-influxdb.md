---
title: "InfluxDB Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0017"
parent_ids:
- "AD-0012"
created: "2026-05-17"
---

# InfluxDB Operations Policy

## Overview

이 문서는 `infra/04-data/analytics/influxdb`의 InfluxDB 운영 정책을 정의한다. Current implementation은 InfluxDB 3 Core 단일 compose와 database/endpoint source contract만 정의하며 token provisioning은 runtime-unverified 상태다.

## Policy Scope

- **Systems**: `influxdb` service, `docker-compose.yml`
- **Persistence**: `influxdb-data`, `influxdb-plugins`
- **Secrets**: root Compose declaration과 metadata는 leaf server wiring이 아니다; InfluxDB leaf는 선언된 secret을 마운트하지 않고 server token도 provision하지 않는다
- **Environments**: repo-local, development, homelab, production-like rehearsal

## Controls

- **Activation**: root-project selection `docker compose --profile influxdb config --quiet`를 사용한다; `influxdb` 시작 또는 재시작은 별도로 승인받아야 하는 runtime action이다.
- **Network and authorization**: 서비스를 선언된 TLS router와 gateway middleware 뒤 `edge_net`에 유지한다. `401`은 인증 challenge를 증명할 뿐 성공적인 authorization을 증명하지 않는다. token provisioning이나 rotation은 이 문서 범위 밖이다.
- **Retention and backup**: consumer를 활성화하기 전에 database retention을 정의한다. recovery point는 문서화된 local-object-store 순서 — snapshot, database Parquet 파일, WAL, catalog log, catalog checkpoint 순 — 를 보존해야 한다. live data path 밖에 저장하고 encryption at rest 구성 여부를 기록한다; 여기서 증명한 것은 없다.
- **Resources**: 측정된 ingest, compaction, query latency, disk growth, restore duration이 검토된 변경을 정당화할 때까지 상속된 1 CPU/512 MiB 상한을 유지한다.
- **Upgrade and migration**: release note를 검토하고 후보 image를 복사한 recovery point에 대해 rehearse한다. 이 Core 배포에 InfluxDB 2 backup/restore command나 Enterprise 전용 command를 대체하지 않는다.
- **Removal**: removal은 consumer가 없음을 확인, 양쪽 bind-backed volume에 대한 owner 결정, export 또는 보존된 recovery point, 삭제에 대한 별도 승인을 요구한다.
- **Required**: 운영은 `docker-compose.yml`, operator가 선택한 database 이름, port `8181`, line-protocol write용 `/api/v3/write_lp`를 사용한다.
- **Required**: token 생성/provisioning과 인증된 write 수락은 별도 runtime 승인이 필요하다; 이 source-only change는 offline admin token file을 선택하거나 활성화하지 않는다.
- **Required**: retention 또는 cleanup 변경은 database-scoped evidence와 별도 runtime 승인이 필요하다.
- **Allowed**: 서비스 시작 없는 source-only Compose 및 문서 validation.
- **Disallowed**: static source check를 runtime acceptance, authorization, data-migration evidence로 제시하는 것; source-only validation은 authorization을 증명할 수 없다.

## Exceptions

장기 retention 또는 수동 data cleanup은 owner 승인과 사용된 database, volume, token boundary를 보여주는 evidence가 필요하다.

## Verification

- `test -f infra/04-data/analytics/influxdb/docker-compose.yml`
- operator가 선택한 database 이름, port `8181`, `/api/v3/write_lp`가 source와 active docs 전반에서 일치하는지 확인한다. token provisioning을 주장하지 않는다.
- `python3 scripts/validation/check-document-links.py --mode all`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- compose image/tag 변경 시
- secret mount 또는 volume path 변경 시
- retention 또는 migration 요구사항 변경 시

## Traceability

- Declared parent: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](../guides/0017-influxdb.md) (`GDE-0017`), [Runbook](../runbooks/0017-influxdb.md) (`RUN-0017`)

## Related Documents

- [InfluxDB 3 Core backup and restore](https://docs.influxdata.com/influxdb3/core/admin/backup-restore/)
- [Compose implementation](../../../infra/04-data/analytics/influxdb/docker-compose.yml)

- [Operations policies index](../README.md)
- [Usage guide](../guides/0017-influxdb.md)
- [Recovery runbook](../runbooks/0017-influxdb.md)
- [Infra README](../../../infra/04-data/analytics/influxdb/README.md)
