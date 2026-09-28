---
title: "Grafana Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0041"
parent_ids:
- "POL-0041"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - grafana
created: "2026-05-10"
---

# Grafana Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Grafana 사용 맥락과 설정 확인 방법을 설명한다. Grafana는 [grafana/grafana image declaration](../../../infra/06-observability/docker-compose.yml)으로 실행되는 visualization hub이며 provisioned datasources, provisioned dashboards, Keycloak OAuth role mapping, protected route를 통해 metrics, logs, traces, alerts, profiles를 한 화면에서 탐색한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Grafana compose service, provisioning mounts, datasource UID, dashboard provider, Keycloak role mapping, protected route boundary를 빠르게 파악한다.
- Grafana Explore와 dashboards에서 Prometheus, Loki, Tempo, Alertmanager, Pyroscope 연결을 확인한다.
- 장애 대응, restart, provisioning rollback, SSO/datasource triage는 runbook으로 넘긴다.

### Prerequisites

- `infra/06-observability/grafana/provisioning`과 `infra/06-observability/grafana/dashboards`를 읽을 수 있는 권한.
- Docker Secret IDs `grafana_admin_password`, `grafana_client_secret`가 준비되어 있어야 한다. Secret 값은 문서, 로그, task evidence에 기록하지 않는다.
- Keycloak groups `/admins`, `/editors` role mapping 정책을 변경하지 않는다.
- Grafana UI `https://grafana.${DEFAULT_URL}` 접근 권한.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-med|image: grafana/grafana:|container_name: infra-grafana|GF_SERVER_ROOT_URL|GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|grafana_admin_password|grafana_client_secret|grafana-data|/api/health|traefik.http.routers.grafana.middlewares: gateway-standard-chain@file' infra/06-observability/docker-compose.yml
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
   - Traces: datasource `Tempo`, `Loki`로의 `tracesToLogsV2` link
   - Alerts: datasource `Alertmanager`
   - Profiles: datasource `Pyroscope`

5. Role mapping 기준을 확인한다.

   - `/admins` group: `Admin`
   - `/editors` group: `Editor`
   - `/viewers` group: `Viewer`
   - 그 외 realm 사용자: 거부 (`ROLE_ATTRIBUTE_STRICT=true`, catch-all 없음)
   - 익명 접근은 비활성화되어 있으며, 신규 사용자는 기본값으로 `Viewer`가 된다.
   - hy-home.k8s Kiali는 Viewer 서비스 계정 `k8s-kiali`의 토큰으로 Grafana를
     읽으며, [RUN-0096](../runbooks/0096-k8s-integration.md)이 이를 발급/재발급한다.
   - OAuth 호출은 마운트된 local root CA로 Keycloak을 검증한다
     (`TLS_SKIP_VERIFY_INSECURE=false`).
   - 이를 활성화하는 승인된 recreate 전에 Keycloak에서 owner 계정이
     `/admins`에 있고 읽기 전용 사용자를 위한 `/viewers` group이 존재하는지
     확인한다. 그렇지 않으면 해당 사용자들이 접근 권한을 잃는다. rollback은
     이전 Compose 값과 recreate이며, Grafana 데이터는 초기화되지 않는다.

### Common Pitfalls

- **Provisioning drift**: UI에서만 바꾼 dashboard나 datasource는 JSON/YAML로 export해 커밋하기 전까지 current truth가 되지 않는다.
- **Datasource identity drift**: dashboard는 UID `Prometheus`, `Loki`, `Tempo`, `alertmanager`, Pyroscope datasource type `grafana-pyroscope-datasource` 같은 provisioned datasource identity를 참조해야 한다.
- **Secret evidence**: `grafana_admin_password`, `grafana_client_secret`, OAuth client secret, 렌더링된 secret 값을 증거에 복사해서는 안 된다.
- **Role mapping drift**: `/admins`와 `/editors` mapping은 `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`가 제어한다.
- **Dashboard edit lock**: provider `editable: false`가 provisioned dashboard를 code-owned 상태로 유지한다.

### Source-backed operating contract

- **Purpose/classification/source**: `grafana`는 여러 observability profile이 선택하는 `HOME` observability UI이며, [Compose](../../../infra/06-observability/docker-compose.yml)와 provisioning 파일이 권위 있는 정의다.
- **State flow**: 현재 source는 `GF_DATABASE_*` 외부 데이터베이스 변수를 설정하지 않으므로, Grafana는 `grafana-data:/var/lib/grafana`의 기본 SQLite 데이터베이스를 plugin, runtime 상태와 함께 사용한다. datasource/dashboard는 추적되는 파일에서 읽기 전용으로 provision된다.
- **Secrets/auth/dependencies**: `grafana_admin_password`와 `grafana_client_secret`가 admin bootstrap과 native Keycloak OAuth에 공급된다. 익명 접근은 현재 source(2026-09-21)에서 비활성화되어 있다. 이전에는 로그인 없이 모든 dashboard가 노출되었다. Traefik, Keycloak, root CA, datasource, `obs_net`이 의존성이며, 익명 접근은 OAuth 관리와 별개로 평가한다.
- **Resources/normal use**: Compose 제한은 source 값일 뿐 측정된 여유 용량이 아니다. root에서 렌더링하고 `/api/health`, OAuth 로그인, 익명 거부, datasource health, provisioned dashboard 로드를 확인한다.
- **Lifecycle**: SQLite/`grafana-data`를 복사하기 전에 Grafana를 중지한다. provisioning과 대응하는 secret을 보존한다. plugin/schema 호환성을 검토하고, 핀된 버전을 하나씩 업그레이드하고, 재개 전에 users/teams/dashboards/alerts/datasources/OAuth를 확인한다.
- **Upstream/license**: 공식 [installation/database default](https://grafana.com/docs/grafana/latest/setup-grafana/installation/), [backup](https://grafana.com/docs/grafana/latest/administration/back-up-grafana/), [upgrade](https://grafana.com/docs/grafana/latest/upgrade-guide/when-to-upgrade/) 안내를 따른다. Grafana OSS는 AGPL-3.0 라이선스다.

## Common Checks

- `docker compose --profile obs ps grafana`
- `docker logs --tail=100 infra-grafana`
- `docker exec infra-grafana wget -q --spider http://localhost:3000/api/health`
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`
- `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0041-grafana.md)을 따른다.

## Traceability

- Declared parent: [Grafana Operations Policy](../policies/0041-grafana.md) (`POL-0041`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0041-grafana.md) (`POL-0041`), [Runbook](../runbooks/0041-grafana.md) (`RUN-0041`)

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0041-grafana.md)
- [Recovery runbook](../runbooks/0041-grafana.md)
