---
title: "Grafana Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0041"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Grafana Operations Policy

## Overview

이 정책은 Grafana visualization hub의 dashboard provisioning, datasource
provisioning, Keycloak role mapping, secret boundary, protected route를
정의한다. 사용 흐름은 Grafana guide가, 장애 대응 절차는 Grafana runbook이
담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/grafana` compose, provisioning,
dashboard tree에 선언된 Grafana 운영 기준을 다룬다.

- **Systems**: compose service `grafana`, container `infra-grafana`, image [grafana/grafana image declaration](../../../infra/06-observability/docker-compose.yml), volume `grafana-data`, provisioning path `infra/06-observability/grafana/provisioning`, dashboard path `infra/06-observability/grafana/dashboards`
- **Environments**: 로컬·개발·홈랩 운영

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
    `alertmanager`, `Pyroscope`, `n8n-db`, `airflow-db` 같은 provisioned
    UID 또는 datasource 변수와 맞춘다.
  - 서비스 대시보드는 방출 메트릭과 맞는 벤더·mixin·grafana.com 대시보드를
    먼저 쓰고, 파일의 `description`에 출처와 revision 또는 commit을 남긴다.
    맞는 것이 없을 때만 로컬 대시보드를 둔다(SPEC-0193).
  - 같은 소스를 같은 목적으로 그리는 대시보드는 하나만 둔다. Grafana README의
    Service Coverage 표가 모든 Compose 서비스의 메트릭 소스와 대시보드를
    기록하고, 대시보드 계약 테스트가 표와 파일을 대조한다.
  - 이미 provision된 dashboard의 `uid`는 바꾸지 않는다. 교체하는 dashboard는
    새 경로와 새 `uid`로 둔다.
  - PostgreSQL datasource는 `grafana_reader`(named table `SELECT`만, 읽기 전용
    세션)로만 접속하고, 비밀번호는 Docker Secret file로만 주입한다.
  - Grafana role mapping은 Keycloak groups `/admins`, `/editors`, `/viewers`와
    `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`를 기준으로 한다. catch-all
    `Viewer`를 두지 않으며 strict mode로 그 밖의 realm 사용자를 거부한다.
  - 익명 접근은 비활성화하고 OAuth TLS는 로컬 root CA로 검증한다.
  - `grafana_admin_password`와 `grafana_client_secret`은 Docker Secret
    file reference로만 주입한다.
  - Service는 `template-stateful-med`, image [grafana/grafana image declaration](../../../infra/06-observability/docker-compose.yml),
    read-only provisioning/dashboard mounts, persistent `grafana-data`
    volume을 유지한다.
  - Grafana route는 TLS와 `gateway-standard-chain@file`을 유지하고,
    authentication/authorization은 Grafana Generic OAuth와 Keycloak role
    mapping이 소유한다. Proxy `sso-auth@file`을 중복 적용하지 않는다.
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

### Lifecycle and data controls

- Grafana를 HOME으로 유지하고 native Keycloak OAuth, gateway, 익명 거부, 그룹별 역할, TLS 검증과 secret-file을 보존한다. 다른 서비스로 Grafana 외부 DB를 추정하지 않는다.
- `grafana-data` SQLite/runtime, provisioning, plugin과 대응 OAuth/admin secret을 한 복구 집합으로 취급한다. 쓰기 중단 또는 SQLite 일관 backup이 필요하다.
- Production route 없는 격리 환경에서 schema·identity/team·dashboard/alert·datasource·OAuth·익명 거부를 검증한다.
- Plugin/image 변경에는 호환성·rollback 근거가 필요하다. 제거에는 dashboard/alert export, client 폐기, route 폐쇄, audit 보존과 데이터 삭제 승인이 필요하다.

### Authentication and provisioning limits

Native OAuth 요구를 유지한다. `GF_AUTH_DISABLE_LOGIN_FORM`은 로그인 폼만 숨기며 Basic API 인증을 끄지 않는다. 선언된 upstream은 Basic auth를 기본 활성화하고 Compose는 비활성화하지 않으므로 SSO-only 요구가 완전히 시행되지 않는다. 유효한 자격 증명은 여전히 필요하다. 임의 break-glass 예외를 만들지 않고 @buenhyden의 별도 수정 결정과 거부 검증을 요구한다. Strict group mapping은 지정 그룹에 organization Admin/Editor/Viewer만 부여한다. `GF_AUTH_GENERIC_OAUTH_GRAFANA_ADMIN_ATTRIBUTE_PATH`는 선언 버전이 지원하지 않는 필드여서 server-admin 부여 증거가 아니다.

`grafana-db-provision`은 DB 서버가 아닌 HOME 일회성 PostgreSQL 클라이언트다. 마운트된 script/SQL은 `mng-pg`를 기다린 뒤 제한된 읽기 전용 `grafana_reader`와 기존 Airflow/n8n 테이블 권한을 생성·갱신한다. HTTP health, 자체 상태 볼륨, 이 job에 대한 Grafana depends_on은 없다. 없는 테이블을 건너뛰어도 성공 종료하므로 애플리케이션 schema 준비 뒤 읽기 전용 query와 각 dashboard를 확인한다. 재실행은 role/grant를 변경하므로 단순 조회 진단이 아니다. DB·자격 증명 복구는 관리 DB·시크릿 소유자가 맡고 helper의 복구 자산은 추적 SQL/script다.

## Exceptions

- Dashboard provider lock, datasource UID, role mapping, secret reference,
  route 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Grafana runbook에서 최소 조치와
  rollback evidence를 기록한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-med|image: grafana/grafana:|GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|grafana_admin_password|grafana_client_secret|traefik.http.routers.grafana.middlewares: gateway-standard-chain@file' infra/06-observability/docker-compose.yml`
- Provisioning boundary:
  `rg -n 'editable: false|uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning`
- Dashboard count:
  `find infra/06-observability/grafana/dashboards -type f -name '*.json' | wc -l`
- Repository contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Review Cadence

- Grafana image, provisioning YAML, dashboard tree, datasource UID, role
  mapping, route, secret reference가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0041-grafana.md) (`GDE-0041`), [Runbook](../runbooks/0041-grafana.md) (`RUN-0041`)

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0041-grafana.md)
- [Recovery runbook](../runbooks/0041-grafana.md)
