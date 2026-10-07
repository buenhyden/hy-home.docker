---
title: "InfluxDB Recovery Runbook"
version: "1.0.4"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0017"
parent_ids:
- "GDE-0017"
created: "2026-05-17"
---

# InfluxDB Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

> Scope: InfluxDB 3 Core service readiness, database/endpoint 검증, unprovisioned-token escalation.

이 런북은 InfluxDB 3 Core service가 unhealthy이거나 database/endpoint readiness 또는 token-provisioning 문제가 의심될 때 사용한다.

### Purpose

- InfluxDB 3 Core database/endpoint source contract mismatch를 방지한다.
- Root secret metadata를 leaf token provisioning으로 오인하지 않고 health 상태를 확인한다.
- cleanup이나 retention 변경을 escalation 없이 임의 수행하지 않도록 한다.

### When to Use

- `influxdb` container healthcheck가 실패할 때
- token provisioning이 승인/검증되지 않았거나 write/read request가 `401` 또는 service unavailable 상태를 보일 때
- database 이름, port `8181`, 또는 `/api/v3/write_lp` 경로가 current contract와 다를 때

### Execution and stop boundary

대상: `influxdb`. 운영 checkout의 repository root와 승인된 Docker context를 확인한다. static source 점검만 승인된 경우 모든 runtime command는 NOT_RUN이다. raw log, rendered Compose, SQL/문서/벡터 payload, credential URI는 evidence에 붙이지 않고 결과·시간·target·source revision·종료 코드만 요약한다.

기동/정지는 [GDE-0099](../guides/0099-system-operations.md#selection-and-readiness)와 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의 consumer 영향·graceful shutdown 계약을 적용한다. 아래 재기동 예시는 정확한 daemon과 의존성 정상 상태를 owner가 승인했을 때만 사용한다. init/key-generator/provisioning job은 DDL·cluster identity·bucket policy를 변경하므로 routine restart 대상에서 제외한다. `--no-deps`는 이미 준비된 dependency를 유지할 때만 쓰며 최초 provisioning을 대신하지 않는다.

Upgrade/config 변경은 declared image/build/entrypoint와 mount를 비교하고 release 호환성·보존된 recovery point를 승인받은 뒤 대상만 적용한다. Git/image rollback은 schema/data/credential rollback이 아니다. 예상 health와 실제 사용자 기능이 다르거나 data/backup/ownership/credential이 불명확하면 중단하고 @buenhyden에게 scope·실패 신호·다음 검토를 전달한다. 실패한 복원 target과 증거는 보존하며 cleanup은 원래 기록한 identity를 확인한 소유 artifact만 별도 승인한다. 새로운 restore executor·client·network를 즉석에서 만들지 않는다.

## Procedure

### Procedure

### Checklist

- [ ] compose file이 `docker-compose.yml`인지 기록한다.
- [ ] root secret 선언은 leaf mount가 아니다. token provisioning evidence가 없음을 기록한다.
- [ ] volume cleanup이나 retention 변경이 필요한 경우 owner approval을 확보한다.

### Steps

1. Compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/influxdb/docker-compose.yml
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. 별도의 runtime-read approval을 받은 후, secret을 노출하지 않고 root-project service 상태와 로그를 확인한다.

   ```bash
   docker compose --profile influxdb ps influxdb
   docker compose --profile influxdb logs --tail 100 influxdb
   ```

3. Token provisioning은 이 source-only runbook 범위 밖임을 확인한다. Operator/named token creation과 authenticated write acceptance에는 separate runtime approval이 필요하다.

4. InfluxDB 3 Core readiness endpoint를 확인한다.

   ```bash
   curl -i http://influxdb:8181/
   ```

### Verification Steps

- [ ] compose file이 존재하고 docs implementation alignment가 통과한다.
- [ ] primary v3 endpoint가 compose healthcheck가 허용하는 `200`, `204`, `401` 중 하나를 반환한다.
- [ ] write endpoint/schema contract는 `POST /api/v3/write_lp?db=<operator-selected-database>`이다. source-only validation으로는 authorization을 증명할 수 없으며 readiness check 중에는 어떤 write도 전송하지 않는다.
- [ ] 최종 evidence에 compose file, container 상태, escalation 필요 여부를 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker compose ... logs influxdb --tail 100`
- **Metrics**: N/A - InfluxDB compose에 선언된 metrics endpoint가 없다.
- **Evidence**: 선택한 compose file, health 응답 코드, token-provisioning escalation 상태, volume pressure 요약

### Planned isolated backup and restore

이 절차는 upstream guidance를 바탕으로 문서화했으며 **이 task에서 실행되지 않았다**.

1. `node0`, source image 호환 경계, database 목록, data/plugin bind 경로, 가용 공간, owner, live volume 외부의 승인된 목적지를 기록한다. writer를 정지하거나 downtime을 예약한다. live recursive copy는 허용된 backup이 아니다.
2. runtime/data approval을 받은 후 write를 중지하거나 drain하고, `node0` object-store 내용을 upstream 순서(`snapshots/`, `dbs/`, `wal/`, `catalog/`, 그 다음 `_catalog_checkpoint`)대로 복사한다. 재생성되는 `table-snapshots/`는 제외한다. ownership, mode, manifest, checksum을 보존한다.
3. 동일한 node ID와 호환되는 InfluxDB 3 Core image로 새 isolated target을 만든다. 빈 data directory로 복원하며, active bind 경로에는 절대 덮어쓰지 않는다.
4. isolated target만 시작한다. readiness를 확인하고, 예상 database/table을 나열하고, 대표 시간 범위와 row count를 비교하고, 별도로 제공된 credential로 authenticated query를 테스트하고, 로그와 checksum evidence를 보존한다.
5. catalog/WAL 오류나 validation mismatch가 있으면 target을 중지하고 실패한 isolated target을 보존하고 별도 승인된 새 target에서 손대지 않은 recovery copy에서 다시 시도한다. live volume을 제자리에서 수리하거나 교체하지 않는다.
6. cutover, restart, retention 변경, 삭제는 target과 rollback window를 명시한 별도 approval이 필요하다. rehearsal이 성공을 기록하기 전까지 restoration은 검증되지 않은 상태다.

## Verification

### Evidence

- compose file, health 응답 코드, token-provisioning escalation 상태, 로그 요약, 최종 조치를 기록한다.
- secret 값은 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

rehearsal 동안 원본 service와 bind 경로를 변경하지 않는다. 실패한 restore는 isolated target만 보존하고 변경되지 않은 원본으로 되돌아가는 방식으로 rollback한다. live 경로로의 파일 복사는 허용하지 않는다.

### Escalation

token provisioning이나 authenticated write acceptance가 필요할 때, health가 허용된 응답 코드와 일치하지 않을 때, disk pressure로 cleanup이 필요할 때, 관찰된 database/endpoint contract가 source와 다를 때 escalation한다.

### Traceability

- Declared parent: [InfluxDB Usage Guide](../guides/0017-influxdb.md) (`GDE-0017`)
- Governing authority: [Analytics Tier Architecture Description](../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](../guides/0017-influxdb.md) (`GDE-0017`), [Policy](../policies/0017-influxdb.md) (`POL-0017`)

## Related Documents

- [InfluxDB 3 Core backup and restore](https://docs.influxdata.com/influxdb3/core/admin/backup-restore/)
- [Compose implementation](../../../infra/04-data/influxdb/docker-compose.yml)

- [Operations runbooks index](../README.md)
- [Usage guide](../guides/0017-influxdb.md)
- [Operations policy](../policies/0017-influxdb.md)
