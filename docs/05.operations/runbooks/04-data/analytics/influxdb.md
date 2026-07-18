---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/analytics/influxdb.md -->

# InfluxDB Recovery Runbook

## InfluxDB Recovery Procedure

> Scope: InfluxDB 3 Core service readiness, database/endpoint verification, and unprovisioned-token escalation.

### Overview

이 런북은 InfluxDB 3 Core service가 unhealthy이거나 database/endpoint readiness 또는 token-provisioning 문제가 의심될 때 사용한다.

### Purpose

- InfluxDB 3 Core database/endpoint source contract mismatch를 방지한다.
- Root secret metadata를 leaf token provisioning으로 오인하지 않고 health 상태를 확인한다.
- cleanup or retention changes를 escalation 없이 임의 수행하지 않도록 한다.

### Canonical References

- **Spec**: [Analytics spec](../../../../03.specs/005-data-analytics/spec.md)
- **Policy**: [InfluxDB policy](../../../policies/04-data/analytics/influxdb.md)
- **Guide**: [InfluxDB guide](../../../guides/04-data/analytics/influxdb.md)

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
   bash scripts/validation/check-doc-implementation-alignment.sh
   ```

2. Runtime container 상태를 확인한다.

   ```bash
   docker ps --filter name=influxdb
   docker logs influxdb --tail 100
   ```

3. Token provisioning은 이 source-only runbook 범위 밖임을 확인한다. Operator/named token creation과 authenticated write acceptance에는 separate runtime approval이 필요하다.

4. InfluxDB 3 Core readiness endpoint를 확인한다.

   ```bash
   curl -i http://influxdb:8181/
   ```

### Verification Steps

- [ ] compose file exists and docs implementation alignment passes.
- [ ] primary v3 endpoint returns `200`, `204`, or `401` as accepted by compose healthcheck.
- [ ] write endpoint/schema contract is `POST /api/v3/write_lp?db=${INFLUXDB_DB_NAME}`; source-only validation cannot prove authorization and no write is sent during a readiness check.
- [ ] final evidence records compose file, container state, and whether escalation was needed.

### Observability and Evidence Sources

- **Logs**: `docker compose ... logs influxdb --tail 100`
- **Metrics**: N/A - no metrics endpoint is declared in the InfluxDB compose.
- **Evidence**: compose file selected, health response code, token-provisioning escalation state, volume pressure summary

### Safe Rollback or Recovery Procedure

- N/A - no verified data rollback procedure is documented for InfluxDB cleanup in this repository.
- Restarting `influxdb` is allowed only after preserving logs and selected compose evidence.
- Data deletion or retention changes must escalate unless backup/owner approval exists.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if command output exposes secret values.
- **Eval Re-run**: rerun documentation validation after docs-only changes.

## Evidence

- Record compose file, health response code, token-provisioning escalation state, log summary, and final action.
- Do not record secret values.

## Rollback or Recovery

N/A - no verified rollback procedure can restore deleted InfluxDB data from this runbook. Use backup evidence and owner-approved recovery if data mutation is required.

## Escalation

Escalate when token provisioning or authenticated write acceptance is needed, health does not match accepted response codes, disk pressure requires cleanup, or the observed database/endpoint contract differs from source.

## Related Documents

- [Operations runbooks index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/influxdb.md)
- [Operations policy](../../../policies/04-data/analytics/influxdb.md)
