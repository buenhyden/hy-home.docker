---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/grafana.md -->

# Grafana Operations Policy

## Overview

이 정책은 Grafana visualization hub의 dashboard provisioning, datasource
provisioning, Keycloak role mapping, secret boundary, protected route를
정의한다. 사용 흐름은 Grafana guide가, 장애 대응 절차는 Grafana runbook이
담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/grafana` compose, provisioning,
dashboard tree에 선언된 Grafana 운영 기준을 다룬다.

- **Systems**: compose service `grafana`, container `infra-grafana`, image `grafana/grafana:13.1.0`, volume `grafana-data`, provisioning path `infra/06-observability/grafana/provisioning`, dashboard path `infra/06-observability/grafana/dashboards`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Dashboards는 `infra/06-observability/grafana/dashboards/`의 JSON
    파일로 관리한다.
  - Dashboard providers는
    `infra/06-observability/grafana/provisioning/dashboards/dashboards.yml`
    에서 `editable: false`를 유지한다.
  - Datasources는
    `infra/06-observability/grafana/provisioning/datasources/datasource.yml`
    로 선언하고, dashboard references는 `Prometheus`, `Loki`, `Tempo`,
    `alertmanager`, `Pyroscope` 같은 provisioned UID와 맞춘다.
  - Grafana role mapping은 Keycloak groups `/admins`, `/editors`와
    `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`를 기준으로 한다.
  - `grafana_admin_password`와 `grafana_client_secret`은 Docker Secret
    file reference로만 주입한다.
  - Service는 `template-stateful-med`, image `grafana/grafana:13.1.0`,
    read-only provisioning/dashboard mounts, persistent `grafana-data`
    volume을 유지한다.
  - Grafana route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
- **Allowed**:
  - 새 dashboard는 unique `uid`를 가진 JSON 파일로 추가한다.
  - 새 datasource는 provisioning YAML과 연결 dashboard 변경을 같은
    evidence 단위로 검증한다.
  - Development 환경에서 UI로 탐색한 dashboard 변경은 JSON export와 review
    후 git에 반영한다.
- **Disallowed**:
  - Provisioned dashboard 또는 datasource를 UI-only 변경으로 운영 기준에
    반영하는 행위
  - `GRAFANA_ADMIN_USERNAME`, `grafana_admin_password`,
    `grafana_client_secret`, OAuth client secret 값을 문서, 로그, task
    evidence에 기록하는 행위
  - 승인 없이 route, role mapping, secret reference, provisioning mount,
    dashboard provider lock, image version을 runtime에서 변경하는 행위

## Exceptions

- Dashboard provider lock, datasource UID, role mapping, secret reference,
  route 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Grafana runbook에서 최소 조치와
  rollback evidence를 기록한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-med|image: grafana/grafana:13.1.0|grafana_admin_password|grafana_client_secret|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`
- Provisioning boundary:
  `rg -n 'editable: false|uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning`
- Dashboard count:
  `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`
- Repository contracts:
  `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Grafana image, provisioning YAML, dashboard tree, datasource UID, role
  mapping, route, secret reference가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/grafana.md)
- [Recovery runbook](../../runbooks/06-observability/grafana.md)
