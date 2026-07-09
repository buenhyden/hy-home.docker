---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/grafana.md -->

# Grafana Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Grafana 사용 맥락과 설정 확인 방법을 설명한다. Grafana는 `grafana/grafana:13.1.0`으로 실행되는 visualization hub이며, provisioned datasources, provisioned dashboards, Keycloak OAuth role mapping, and protected route를 통해 metrics, logs, traces, alerts, and profiles를 한 화면에서 탐색한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Grafana compose service, provisioning mounts, datasource UID, dashboard provider, Keycloak role mapping, and protected route boundary를 빠르게 파악한다.
- Grafana Explore와 dashboards에서 Prometheus, Loki, Tempo, Alertmanager, Pyroscope 연결을 확인한다.
- 장애 대응, restart, provisioning rollback, SSO/datasource triage는 runbook으로 넘긴다.

### Prerequisites

- `infra/06-observability/grafana/provisioning` and `infra/06-observability/grafana/dashboards`를 읽을 수 있는 권한.
- Docker Secret IDs `grafana_admin_password`, `grafana_client_secret`가 준비되어 있어야 한다. Secret 값은 문서, 로그, task evidence에 기록하지 않는다.
- Keycloak groups `/admins`, `/editors` role mapping 정책을 변경하지 않는다.
- Grafana UI `https://grafana.${DEFAULT_URL}` 접근 권한.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-med|image: grafana/grafana:13.1.0|container_name: infra-grafana|GF_SERVER_ROOT_URL|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|grafana_admin_password|grafana_client_secret|grafana-data|/api/health|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

2. Datasource provisioning boundary를 확인한다.

   ```bash
   rg -n 'uid: Prometheus|url: http://prometheus:9090|uid: Loki|url: http://loki:3100|uid: Tempo|url: http://tempo:3200|uid: alertmanager|url: http://alertmanager:9093|type: grafana-pyroscope-datasource|url: http://pyroscope:4040|tracesToLogsV2|datasourceUid: .Loki.' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

3. Dashboard provisioning boundary를 확인한다.

   ```bash
   rg -n 'folder:|editable: false|path: /etc/grafana/dashboards' infra/06-observability/grafana/provisioning/dashboards/dashboards.yml
   find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l
   ```

4. UI에서 주요 탐색 경로를 확인한다.

   - UI: `https://grafana.${DEFAULT_URL}`
   - Metrics: datasource `Prometheus`
   - Logs: datasource `Loki`
   - Traces: datasource `Tempo`, `tracesToLogsV2` link to `Loki`
   - Alerts: datasource `Alertmanager`
   - Profiles: datasource `Pyroscope`

5. Role mapping 기준을 확인한다.

   - `/admins` group: `Admin`
   - `/editors` group: `Editor`
   - Other authenticated users: `Viewer`
   - Anonymous role remains `Viewer`; browser login still uses OAuth auto-login.

### Common Pitfalls

- **Provisioning drift**: UI-only dashboard or datasource changes do not become current truth until exported to JSON/YAML and committed.
- **Datasource identity drift**: dashboards must reference provisioned datasource identities such as UIDs `Prometheus`, `Loki`, `Tempo`, `alertmanager`, and the Pyroscope datasource type `grafana-pyroscope-datasource`.
- **Secret evidence**: `grafana_admin_password`, `grafana_client_secret`, OAuth client secret, and rendered secret values must not be copied into evidence.
- **Role mapping drift**: `/admins` and `/editors` mapping is controlled by `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`.
- **Dashboard edit lock**: provider `editable: false` keeps provisioned dashboards code-owned.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps grafana`
- `docker logs --tail=100 infra-grafana`
- `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`
- `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/grafana.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/grafana.md)
- [Recovery runbook](../../runbooks/06-observability/grafana.md)
