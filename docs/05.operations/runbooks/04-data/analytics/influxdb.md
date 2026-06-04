---
status: active
---
<!-- Target: docs/05.operations/runbooks/04-data/analytics/influxdb.md -->

# InfluxDB Recovery Runbook

## InfluxDB Recovery Procedure

> Scope: InfluxDB service readiness, token mount verification, and primary/legacy compose selection.

### Overview (KR)

이 런북은 InfluxDB primary v3 service가 unhealthy이거나 token mount/readiness 문제가 의심될 때 사용한다. Legacy v2 절차는 `docker-compose.v2.yml`을 명시한 경우에만 적용한다.

### Purpose

- InfluxDB variant mismatch를 방지한다.
- secret value를 노출하지 않고 token mount와 health 상태를 확인한다.
- cleanup or retention changes를 escalation 없이 임의 수행하지 않도록 한다.

### Canonical References

- **Spec**: [Analytics spec](../../../../03.specs/04-data-analytics/spec.md)
- **Policy**: [InfluxDB policy](../../../policies/04-data/analytics/influxdb.md)
- **Guide**: [InfluxDB guide](../../../guides/04-data/analytics/influxdb.md)

## When to Use

- `influxdb` container healthcheck가 실패할 때
- token mount가 누락되었거나 write/read request가 `401` 또는 service unavailable 상태를 보일 때
- primary v3와 legacy v2 compose 선택이 불명확할 때

## Procedure

### Checklist

- [ ] 선택한 compose file이 `docker-compose.yml`인지 `docker-compose.v2.yml`인지 기록한다.
- [ ] Docker Secret mount paths만 확인하고 secret value는 출력하지 않는다.
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

3. Secret mount 존재만 확인한다.

   ```bash
   docker exec influxdb test -r /run/secrets/influxdb_api_token
   ```

4. Primary v3 readiness endpoint를 확인한다.

   ```bash
   curl -i http://influxdb:8181/
   ```

### Verification Steps

- [ ] compose file exists and docs implementation alignment passes.
- [ ] primary v3 endpoint returns `200`, `204`, or `401` as accepted by compose healthcheck.
- [ ] final evidence records compose file, container state, and whether escalation was needed.

### Observability and Evidence Sources

- **Logs**: `docker compose ... logs influxdb --tail 100`
- **Metrics**: N/A - no metrics endpoint is declared in the InfluxDB compose.
- **Evidence**: compose file selected, health response code, secret mount existence, volume pressure summary

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

- Record compose file, health response code, secret mount existence check, log summary, and final action.
- Do not record secret values.

## Rollback or Recovery

N/A - no verified rollback procedure can restore deleted InfluxDB data from this runbook. Use backup evidence and owner-approved recovery if data mutation is required.

## Escalation

Escalate when secret mounts are missing, health does not match accepted response codes, disk pressure requires cleanup, or the observed service variant differs from the selected compose file.

## Related Documents

- [Operations runbooks index](../../../README.md)
- [Usage guide](../../../guides/04-data/analytics/influxdb.md)
- [Operations policy](../../../policies/04-data/analytics/influxdb.md)
