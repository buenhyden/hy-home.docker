---
title: "Grafana Provisioning and Access Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-30"
layer: "operations"
artifact_id: "RUN-0041"
parent_ids:
- "GDE-0041"
created: "2026-05-17"
---

# Grafana Provisioning and Access Recovery Runbook

## Overview

> Scope: Grafana readiness checks, OAuth role mapping triage, datasource/provisioning evidence, dashboard reload, restart, and config rollback.

이 런북은 Grafana readiness failure, OAuth login loop, role mapping drift, datasource query errors, dashboard provisioning failure, trace-to-log link regression, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-grafana` 상태를 확인하고 Keycloak OAuth environment, Docker Secret references, datasource provisioning, dashboard provider locks, dashboard JSON tree, protected route를 검증하며, Secret 노출이나 SSO/route/provisioning 정책 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

## When to Use

- Grafana UI `https://grafana.${DEFAULT_URL}` 또는 `/api/health`가 실패할 때.
- OAuth login loop, `OAuth Login Failed`, or unexpected Viewer/Editor/Admin role이 발생할 때.
- Dashboard 패널에 `Datasource not found`, `Query error`가 표시되거나 trace/log/profile link가 비어 있을 때.
- Provisioned dashboard JSON or datasource YAML 변경 후 reload/restart와 검증이 필요할 때.
- `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`, secret reference, datasource UID, dashboard provider, or route 변경 후 rollback 가능성을 확인해야 할 때.

## Procedure

### Checklist

- [ ] `grafana` service, `infra-grafana` container, `grafana-data` volume, provisioning mounts, dashboard mounts, and Docker Secret IDs 상태를 확인한다.
- [ ] 문제 유형을 readiness, OAuth/role mapping, datasource, dashboard provisioning, trace-to-log link, secret reference, config regression 중 하나로 분류한다.
- [ ] `grafana_admin_password`, `grafana_client_secret`, OAuth client secret, rendered secret values는 기록하지 않는다.
- [ ] Route, role mapping, secret reference, provider lock, datasource UID, or image version 변경이 필요해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태, 최근 로그, healthcheck를 캡처한다.

   ```bash
   docker compose --profile obs ps grafana
   docker logs --tail=200 infra-grafana
   docker exec infra-grafana wget -q --spider http://localhost:3000/api/health
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-med|image: grafana/grafana:|container_name: infra-grafana|GF_SERVER_ROOT_URL|GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE|GF_SECURITY_ADMIN_PASSWORD__FILE|grafana_admin_password|grafana_client_secret|grafana-data|/api/health|traefik.http.routers.grafana.middlewares: gateway-standard-chain@file' infra/06-observability/docker-compose.yml
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
   docker compose --profile obs restart grafana
   docker logs --tail=100 infra-grafana
   docker exec infra-grafana wget -q --spider http://localhost:3000/api/health
   ```

8. Provisioning or dashboard 변경 후 장애가 발생했다면 Git-managed diff를 되돌리고 healthcheck를 재확인한다.

   ```bash
   git diff -- infra/06-observability/grafana/provisioning infra/06-observability/grafana/dashboards infra/06-observability/docker-compose.yml
   docker compose --profile obs restart grafana
   docker exec infra-grafana wget -q --spider http://localhost:3000/api/health
   ```

   이 런북은 role mapping change, secret rotation, datasource UID migration, dashboard provider lock change, protected middleware change, or Grafana image change를 검증된 복구 절차로 제공하지 않는다. 해당 변경에는 별도 approval과 rollback evidence가 필요하다.

9. Grafana가 시작 직후 재시작을 반복하고 로그에 `Failed to provision data
   sources ... data source not found`가 있으면, 이미 있는 datasource의 UID를
   provisioning이 바꾸려는 경우다. `datasource.yml` 맨 위에 해당 이름의
   `deleteDatasources` 항목을 두고 재시작한다(SPEC-0193, Pyroscope).

   ```bash
   docker logs --since 5m infra-grafana 2>&1 | grep 'Failed to provision data sources'
   docker restart infra-grafana
   ```

10. 로그에 `failed to save dashboard ... deprecatedInternalID=... is already in
    use`가 있으면, 기존 dashboard의 `uid`를 바꿨거나 지운 파일과 같은 경로에
    다른 `uid`를 둔 경우다. 유지하는 dashboard는 이전 `uid`로 되돌리고,
    교체하는 dashboard는 새 파일 경로로 옮긴다. provider가 옛 dashboard를 지우고
    새 것을 만든다.

11. SQL dashboard(`n8n-db`, `airflow-db`)가 인증 오류를 내면 reader role을 다시
    provision한다. 이 job은 멱등이며 값을 출력하지 않는다.

    ```bash
    docker compose up --no-deps --no-build grafana-db-provision
    docker inspect grafana-db-provision -f '{{.State.ExitCode}}'
    ```

12. Datasource health API는 Tempo에 400, Alertmanager에 500을 돌려준다. 두
    plugin이 backend health를 제공하지 않기 때문이며 장애가 아니다. 대신
    `/api/datasources/proxy/uid/Tempo/api/echo`와
    `/api/datasources/proxy/uid/alertmanager/api/v2/status`로 확인한다.

### Verification Steps

- [ ] `docker compose --profile obs ps grafana`에서 `grafana` service가 running이다.
- [ ] `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`가 성공한다.
- [ ] Provisioned datasource identity가 변경되지 않았다: UID `Prometheus`, `Loki`, `Tempo`, `alertmanager`, Pyroscope datasource type `grafana-pyroscope-datasource`.
- [ ] Dashboard provider가 여전히 `editable: false`이고, tracked dashboard JSON 개수가 예상값과 일치한다.
- [ ] OAuth role mapping이 여전히 `/admins`를 `Admin`으로, `/editors`를 `Editor`로, 나머지를 `Viewer`로 매핑한다.
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

### Planned isolated restore rehearsal

Status: **planned and not executed**. Grafana SQLite restore 성공 사례를 주장하지 않는다.

1. image/plugin/schema identity와 object count를 기록하고, user/alert를 quiesce한 뒤 Grafana를 중지하고, provisioning과 secret reference에 맞춰 `grafana-data` 전체를 snapshot한다.
2. test route와 test Keycloak client를 사용하는 별도 project/network로 복원한다. production datasource는 read-only로 유지하거나 test endpoint로 대체한다.
3. Grafana를 시작하고 SQLite migration, users/teams, dashboards, alerts, plugins, datasource health, native OAuth를 검증하며 anonymous request가 거부되는지 확인한다.
4. 불일치가 발견되면 isolated project를 중지하고 log/checksum을 보존한다. untouched backup으로 돌아가며, production state/client/route 교체는 별도로 승인받는다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, token, OAuth payload, rendered secret values는 기록하지 않는다.
- Datasource/dashboard 장애는 affected dashboard/panel, datasource UID, backend endpoint, redacted log excerpt, and provisioning diff를 함께 기록한다.
- Role mapping/secret/datasource UID/provider/route 변경 필요성이 보이면 approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed provisioning/dashboard/compose rollback만 사용한다. Role mapping, secret rotation, datasource identity migration, dashboard provider lock, protected middleware, or image version 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, role mapping/secret/datasource/provider/route 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Traceability

- Declared parent: [Grafana Usage Guide](../guides/0041-grafana.md) (`GDE-0041`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0041-grafana.md) (`GDE-0041`), [Policy](../policies/0041-grafana.md) (`POL-0041`)

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative이며, [derived Compose image projection](../../../infra/tech-stack.versions.json)은 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0041-grafana.md)
- [Operations policy](../policies/0041-grafana.md)
