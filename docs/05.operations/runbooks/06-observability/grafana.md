---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/grafana.md -->

# Grafana Runbook

## Overview (KR)

이 런북은 `docs/05.operations/runbooks/06-observability/grafana.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

## Grafana Recovery Procedure (06-observability)

Standardized procedures for resolving common Grafana service disruptions.

### SSO Authentication Failures

#### Symptom: "OAuth Login Failed" or redirection loops

1. **Verify Keycloak Status**: Ensure the Keycloak service is healthy and reachable.
2. **Check Secrets**: Ensure `oauth2_proxy_client_secret` is correctly loaded as a secret in the `06-observability` tier.
3. **Inspect Logs**: Check Grafana logs for OAuth2 token validation errors:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml logs grafana | grep -i "oauth"
   ```

4. **Group Synchronization**: If a user has incorrect roles, verify their group membership in Keycloak. Groups must start with `/admins` or `/editors`.
5. **Time Sync**: Ensure clocks are synchronized between Grafana and Keycloak (NTP check).

### Datasource Connection Issues

#### Symptom: Dashboard panels show "Datasource not found" or "Query error"

1. **Verify Backend Status**: Check if Prometheus, Loki, or Tempo containers are running and healthy.
2. **Check UID Matching**: Ensure the dashboard expects the same `uid` defined in `datasource.yml` (e.g., `Prometheus` vs `prometheus`).
3. **Trace-to-Log Link Break**: If "Logs" button disappears in Tempo, verify `tracesToLogsV2` configuration in `datasource.yml`.

### Dashboard Provisioning Issues

1. **Verify Volume Mount**: Ensure `./grafana/dashboards` is correctly mounted to `/etc/grafana/dashboards`.
2. **Check YAML Config**: Inspect `infra/06-observability/grafana/provisioning/dashboards/dashboards.yml` for correct path references.
3. **Grafana Refresh**: Restart the Grafana service to force a re-scan of the provisioning directory:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml restart grafana
   ```

### Service Unavailability

#### Symptom: HTTP/503 or healthcheck failed

1. **Resource Check**: Verify Grafana memory usage. By default, it is limited to 1GB.
2. **Database Integrity**: Check `/var/lib/grafana/grafana.db` (SQLite) for corruption if the service fails to start.
3. **Healthcheck Probe**: Run the healthcheck command manually:

   ```bash
   docker exec grafana wget -q --spider http://localhost:3000/api/health
   ```

### References

- [Grafana System Usage](../../guides/06-observability/grafana.md)
- [Keycloak Recovery Procedure](../02-auth/keycloak.md)

---

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Steps

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/grafana.md)
- [Operations policy](../../policies/06-observability/grafana.md)
- [Operations template](../../../99.templates/operation.template.md)
