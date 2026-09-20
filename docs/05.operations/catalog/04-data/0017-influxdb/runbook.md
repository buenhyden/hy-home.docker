---
title: "InfluxDB Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0017"
parent_ids:
- "GDE-0017"
created: "2026-05-17"
---

# InfluxDB Recovery Runbook

## Overview

> Scope: InfluxDB 3 Core service readiness, database/endpoint verification, and unprovisioned-token escalation.

이 런북은 InfluxDB 3 Core service가 unhealthy이거나 database/endpoint readiness 또는 token-provisioning 문제가 의심될 때 사용한다.

### Purpose

- InfluxDB 3 Core database/endpoint source contract mismatch를 방지한다.
- Root secret metadata를 leaf token provisioning으로 오인하지 않고 health 상태를 확인한다.
- cleanup or retention changes를 escalation 없이 임의 수행하지 않도록 한다.

## When to Use

- `influxdb` container healthcheck가 실패할 때
- token provisioning이 승인/검증되지 않았거나 write/read request가 `401` 또는 service unavailable 상태를 보일 때
- database 이름, port `8181`, 또는 `/api/v3/write_lp` 경로가 current contract와 다를 때

## Procedure

### Checklist

- [ ] compose file이 `docker-compose.yml`인지 기록한다.
- [ ] Root secret declarations are not leaf mounts; token provisioning evidence가 없음을 기록한다.
- [ ] volume cleanup이나 retention 변경이 필요한 경우 owner approval을 확보한다.

### Steps

1. Compose file과 repo-local 문서 계약을 확인한다.

   ```bash
   test -f infra/04-data/analytics/influxdb/docker-compose.yml
   python3 scripts/validation/check-document-links.py --mode all
   ```

2. After separate runtime-read approval, inspect the root-project service state and logs without rendering secrets.

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

- [ ] compose file exists and docs implementation alignment passes.
- [ ] primary v3 endpoint returns `200`, `204`, or `401` as accepted by compose healthcheck.
- [ ] write endpoint/schema contract is `POST /api/v3/write_lp?db=<operator-selected-database>`; source-only validation cannot prove authorization and no write is sent during a readiness check.
- [ ] final evidence records compose file, container state, and whether escalation was needed.

### Observability and Evidence Sources

- **Logs**: `docker compose ... logs influxdb --tail 100`
- **Metrics**: N/A - no metrics endpoint is declared in the InfluxDB compose.
- **Evidence**: compose file selected, health response code, token-provisioning escalation state, volume pressure summary

### Planned isolated backup and restore

This procedure is documented from upstream guidance and **has not been executed in this task**.

1. Record `node0`, the source image compatibility boundary, database list, data/plugin bind paths, available space, owners, and an approved destination outside the live volume. Quiesce writers or schedule downtime; a live recursive copy is not an accepted backup.
2. After runtime/data approval, stop or drain writes and copy the `node0` object-store content in the upstream order: `snapshots/`, `dbs/`, `wal/`, `catalog/`, then `_catalog_checkpoint`. Exclude regenerated `table-snapshots/`. Preserve ownership, modes, a manifest, and checksums.
3. Create a fresh isolated target with the same node ID and a compatible InfluxDB 3 Core image. Restore into an empty data directory; never overlay the active bind path.
4. Start only the isolated target. Confirm readiness, enumerate expected databases/tables, compare representative time ranges and row counts, test an authenticated query with a separately supplied credential, and retain logs plus checksum evidence.
5. On any catalog/WAL error or validation mismatch, stop the target, discard the failed isolated target, and retry from an untouched recovery copy. Do not repair or replace the live volume in place.
6. Cutover, restart, retention changes, or deletion require a separate approval naming the target and rollback window. Until a rehearsal records success, restoration remains unverified.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if command output exposes secret values.
- **Eval Re-run**: rerun documentation validation after docs-only changes.

## Evidence

- Record compose file, health response code, token-provisioning escalation state, log summary, and final action.
- Do not record secret values.

## Rollback or Recovery

Keep the original service and bind paths unchanged during rehearsal. A failed restore rolls back by destroying only the isolated target and returning to the unchanged source; it does not authorize copying files into the live path.

## Escalation

Escalate when token provisioning or authenticated write acceptance is needed, health does not match accepted response codes, disk pressure requires cleanup, or the observed database/endpoint contract differs from source.

## Traceability

- Declared parent: [InfluxDB Usage Guide](guide.md) (`GDE-0017`)
- Governing authority: [Analytics Tier Architecture Description](../../../../02.architecture/descriptions/0012-data-analytics-architecture.md) (`AD-0012`)
- Subject peers: [Guide](guide.md) (`GDE-0017`), [Policy](policy.md) (`POL-0017`)

## Related Documents

- [InfluxDB 3 Core backup and restore](https://docs.influxdata.com/influxdb3/core/admin/backup-restore/)
- [Compose implementation](../../../../../infra/04-data/analytics/influxdb/docker-compose.yml)

- [Operations runbooks index](../../../README.md)
- [Usage guide](guide.md)
- [Operations policy](policy.md)
