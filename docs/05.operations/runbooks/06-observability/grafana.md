---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/grafana.md -->

# Grafana Provisioning and Access Recovery Runbook

## Grafana Provisioning and Access Recovery Procedure

> Scope: Grafana readiness checks, OAuth role mapping triage, datasource/provisioning evidence, dashboard reload, restart, and config rollback.

### Overview

이 런북은 Grafana readiness failure, OAuth login loop, role mapping drift, datasource query errors, dashboard provisioning failure, trace-to-log link regression, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-grafana` 상태를 확인하고 Keycloak OAuth environment, Docker Secret references, datasource provisioning, dashboard provider locks, dashboard JSON tree, protected route를 검증하며, Secret 노출이나 SSO/route/provisioning 정책 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Grafana operations policy](../../policies/06-observability/grafana.md)
- **Guide**: [Grafana usage guide](../../guides/06-observability/grafana.md)
- **Infrastructure**: [Grafana infra README](../../../../infra/06-observability/grafana/README.md)

## When to Use

- Grafana UI `https://grafana.${DEFAULT_URL}` 또는 `/api/health`가 실패할 때.
- OAuth login loop, `OAuth Login Failed`, or unexpected Viewer/Editor/Admin role이 발생할 때.
- Dashboard panels show `Datasource not found`, `Query error`, or empty trace/log/profile links.
- Provisioned dashboard JSON or datasource YAML 변경 후 reload/restart와 검증이 필요할 때.
- `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`, secret reference, datasource UID, dashboard provider, or route 변경 후 rollback 가능성을 확인해야 할 때.

## Procedure

### Checklist

- [ ] `grafana` service, `infra-grafana` container, `grafana-data` volume, provisioning mounts, dashboard mounts, and Docker Secret IDs 상태를 확인한다.
- [ ] 문제 유형을 readiness, OAuth/role mapping, datasource, dashboard provisioning, trace-to-log link, secret reference, config regression 중 하나로 분류한다.
- [ ] `grafana_admin_password`, `grafana_client_secret`, OAuth client secret, rendered secret values는 기록하지 않는다.
- [ ] Route, role mapping, secret reference, provider lock, datasource UID, or image version을 변경해야 해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태, 최근 로그, healthcheck를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps grafana
   docker logs --tail=200 infra-grafana
   docker exec infra-grafana wget -q --spider http://localhost:3000/api/health
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-med|image: grafana/grafana:13.1.0|container_name: infra-grafana|GF_SERVER_ROOT_URL|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE|GF_SECURITY_ADMIN_PASSWORD__FILE|grafana_admin_password|grafana_client_secret|grafana-data|/api/health|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

3. OAuth or role mapping failure이면 role mapping과 OAuth endpoint references만 확인한다.

   ```bash
   rg -n 'GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_AUTH_URL|GF_AUTH_GENERIC_OAUTH_TOKEN_URL|GF_AUTH_GENERIC_OAUTH_API_URL|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_STRICT|GF_AUTH_GENERIC_OAUTH_USE_PKCE|GF_AUTH_GENERIC_OAUTH_CODE_CHALLENGE_METHOD' infra/06-observability/docker-compose.yml
   docker logs --tail=300 infra-grafana | grep -Ei 'oauth|role|login|token|keycloak|auth'
   ```

   Secret value나 token payload가 포함된 줄은 그대로 복사하지 말고 redaction summary로 기록한다.

4. Datasource or dashboard query failure이면 datasource UID와 backend endpoints를 확인한다.

   ```bash
   rg -n 'uid: Prometheus|url: http://prometheus:9090|uid: Loki|url: http://loki:3100|uid: Tempo|url: http://tempo:3200|uid: alertmanager|url: http://alertmanager:9093|type: grafana-pyroscope-datasource|url: http://pyroscope:4040|tracesToLogsV2|datasourceUid: .Loki.' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

5. Dashboard provisioning failure이면 provider locks and dashboard inventory를 확인한다.

   ```bash
   rg -n 'folder:|editable: false|path: /etc/grafana/dashboards' infra/06-observability/grafana/provisioning/dashboards/dashboards.yml
   find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l
   ```

6. Backend dependency issue가 의심되면 dependent services의 readiness를 확인한다.

   ```bash
   docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy
   docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready
   docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready
   docker exec infra-pyroscope wget -q --spider http://localhost:4040/ready
   ```

7. Config와 Secret ID 경계가 정책과 일치하지만 runtime state가 회복되지 않으면 Grafana를 재시작한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart grafana
   docker logs --tail=100 infra-grafana
   docker exec infra-grafana wget -q --spider http://localhost:3000/api/health
   ```

8. Provisioning or dashboard 변경 후 장애가 발생했다면 Git-managed diff를 되돌리고 healthcheck를 재확인한다.

   ```bash
   git diff -- infra/06-observability/grafana/provisioning infra/06-observability/grafana/dashboards infra/06-observability/docker-compose.yml
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart grafana
   docker exec infra-grafana wget -q --spider http://localhost:3000/api/health
   ```

   이 런북은 role mapping change, secret rotation, datasource UID migration, dashboard provider lock change, protected middleware change, or Grafana image change를 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps grafana`에서 `grafana` service가 running이다.
- [ ] `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`가 성공한다.
- [ ] Provisioned datasource identities remain unchanged: UIDs `Prometheus`, `Loki`, `Tempo`, `alertmanager`, and Pyroscope datasource type `grafana-pyroscope-datasource`.
- [ ] Dashboard providers remain `editable: false`, and tracked dashboard JSON count is expected.
- [ ] OAuth role mapping still maps `/admins` to `Admin`, `/editors` to `Editor`, and others to `Viewer`.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-grafana`
- **Health**: Grafana `/api/health`, UI `https://grafana.${DEFAULT_URL}`
- **Config**: compose env/secret refs, datasource provisioning, dashboard provider YAML, dashboard JSON tree
- **Backends**: Prometheus healthy, Loki ready, Tempo ready, Pyroscope ready
- **Evidence to Capture**: failing panel or login symptom, datasource UID, dashboard provider path, redacted auth log excerpt, restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed provisioning YAML, dashboard JSON, Compose env/secret reference, or datasource endpoint change가 원인이면 직전 Git diff 단위로 되돌리고 Grafana를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Role mapping, secret rotation, datasource UID migration, dashboard provider lock, protected middleware, or image version change는 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, token, OAuth payload, rendered secret values는 기록하지 않는다.
- Datasource/dashboard 장애는 affected dashboard/panel, datasource UID, backend endpoint, redacted log excerpt, and provisioning diff를 함께 기록한다.
- Role mapping/secret/datasource UID/provider/route 변경 필요성이 보이면 approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed provisioning/dashboard/compose rollback만 사용한다. Role mapping, secret rotation, datasource identity migration, dashboard provider lock, protected middleware, or image version 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, role mapping/secret/datasource/provider/route 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/grafana.md)
- [Operations policy](../../policies/06-observability/grafana.md)
