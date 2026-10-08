---
title: "Grafana Provisioning and Access Recovery Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0041"
parent_ids:
- "GDE-0041"
created: "2026-05-17"
---

# Grafana Provisioning and Access Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### Overview

> Scope: Grafana 준비 상태, OAuth 역할 매핑 진단, datasource·provisioning 증거, dashboard 다시 읽기, 재시작과 설정 rollback.

이 런북은 Grafana readiness failure, OAuth login loop, role mapping drift, datasource query errors, dashboard provisioning failure, trace-to-log link regression, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `grafana` 상태를 확인하고 Keycloak OAuth environment, Docker Secret references, datasource provisioning, dashboard provider locks, dashboard JSON tree, protected route를 검증하며, Secret 노출이나 SSO/route/provisioning 정책 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### When to Use

- Grafana UI `https://grafana.${DEFAULT_URL}` 또는 `/api/health`가 실패할 때.
- OAuth login loop, `OAuth Login Failed`, or unexpected Viewer/Editor/Admin role이 발생할 때.
- Dashboard 패널에 `Datasource not found`, `Query error`가 표시되거나 trace/log/profile link가 비어 있을 때.
- Provisioned dashboard JSON or datasource YAML 변경 후 reload/restart와 검증이 필요할 때.
- `GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH`, secret reference, datasource UID, dashboard provider, or route 변경 후 rollback 가능성을 확인해야 할 때.

## Procedure

### Procedure

### Execution Boundary

저장소 root에서 아래의 정확한 service/profile과 기존 container를 선택한다. 변경 전에 승인 대상, source/image, 선행 readiness, 필요한 운영 권한과 부작용 범위를 확인한다. `up`은 dependency/provisioning job을 만들 수 있고 profile은 격리가 아니다. 진단은 기존 container의 `exec`를 사용하고 단순 조회를 위해 client/provisioner를 띄우지 않는다. 재시작은 요청 중단·memory/queue 손실·부작용 반복을 일으킬 수 있으므로 대상 drain/backup 조건을 먼저 충족한다. `restart`는 바뀐 Compose 설정이나 교체된 secret bind를 불러오지 않는다.

Log를 보존하기 전에 payload·credential·header/cookie·private path를 제거하고 명령·시각·상태·제한된 시험 증거만 남긴다. 예상 밖 출력, backup 누락, dependency 실패나 승인되지 않은 부작용이면 중단하고 @buenhyden에게 넘긴다. Config rollback은 data/schema 복구가 아니다. 전체 기동·중지는 [cold-start Runbook](0098-cold-start-and-reboot.md)의 대상 선택·의존성 확인 절차를 사용한다. 공통 절차는 [백업](0021-backup-and-restore.md), [image 변경](0086-dependency-version-management.md), [시크릿](0085-openbao.md), [계정](0014-keycloak.md), [gateway·인증서](0013-traefik.md)가 소유한다. 대상이 실제 사용하는 자격 증명·상태에만 적용하며 secret 값은 증거로 요구하지 않는다.

### Service lifecycle prerequisites

`grafana`의 선택 backend가 없으면 해당 datasource만 실패할 수 있다. `grafana-db-provision`은 DB grant를 변경하는 별도 일회성 작업이며 Grafana 기동 의존성이 아니다. 기존 dashboard 조회를 위해 이 작업을 실행하지 않는다. 승인된 최초 provision·schema 변경 때만 DB 소유자가 표·역할 준비와 secret 참조를 확인하며, 종료 코드와 실제 필요한 표의 읽기 권한을 함께 검증한다. Helper는 자체 영속 데이터·HTTP health·독립 복원 대상이 없고 권한 회수는 DB 소유자 절차로 넘긴다.

### Checklist

- [ ] `grafana` service, `grafana` container, `grafana-data` volume, provisioning mounts, dashboard mounts, and Docker Secret IDs 상태를 확인한다.
- [ ] 문제 유형을 readiness, OAuth/role mapping, datasource, dashboard provisioning, trace-to-log link, secret reference, config regression 중 하나로 분류한다.
- [ ] `grafana_admin_password`, `grafana_client_secret`, OAuth client secret, rendered secret values는 기록하지 않는다.
- [ ] Route, role mapping, secret reference, provider lock, datasource UID, or image version 변경이 필요해 보이면 중단하고 repository owner @buenhyden approval을 받는다.

### Steps

1. 현재 service 상태, 최근 로그, healthcheck를 캡처한다.

   ```bash
   docker compose --profile obs ps grafana
   docker logs --tail=200 grafana
   docker exec grafana wget -q --spider http://localhost:3000/api/health
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-med|image: grafana/grafana:|container_name: grafana|GF_SERVER_ROOT_URL|GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE|GF_SECURITY_ADMIN_PASSWORD__FILE|grafana_admin_password|grafana_client_secret|grafana-data|/api/health|traefik.http.routers.grafana.middlewares: gateway-standard-chain@file' infra/06-observability/docker-compose.yml
   ```

3. OAuth or role mapping failure이면 role mapping과 OAuth endpoint references만 확인한다.

   ```bash
   rg -n 'GF_AUTH_GENERIC_OAUTH_ENABLED|GF_AUTH_GENERIC_OAUTH_AUTH_URL|GF_AUTH_GENERIC_OAUTH_TOKEN_URL|GF_AUTH_GENERIC_OAUTH_API_URL|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_PATH|GF_AUTH_GENERIC_OAUTH_ROLE_ATTRIBUTE_STRICT|GF_AUTH_GENERIC_OAUTH_USE_PKCE|GF_AUTH_GENERIC_OAUTH_CODE_CHALLENGE_METHOD' infra/06-observability/docker-compose.yml
   docker logs --tail=300 grafana | grep -Ei 'oauth|role|login|token|keycloak|auth'
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
   docker exec prometheus wget -qO- http://localhost:9090/-/healthy
   docker exec loki wget -qO- http://127.0.0.1:3100/ready
   docker exec tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready
   docker compose --profile profiling exec -T pyroscope /usr/bin/profilecli ready --url=http://127.0.0.1:${PYROSCOPE_PORT:-4040}
   ```

7. Config와 Secret ID 경계가 정책과 일치하지만 runtime state가 회복되지 않으면 Grafana를 재시작한다.

   ```bash
   docker compose --profile obs restart grafana
   docker logs --tail=100 grafana
   docker exec grafana wget -q --spider http://localhost:3000/api/health
   ```

8. Provisioning·dashboard의 bind-mounted 파일만 바뀌었으면 아래 `git diff`로 후보를 확인하고 승인된 정상 revision의 해당 파일만 복원한다. `git diff`는 복원 명령이 아니다. 같은 파일 bind가 기존 컨테이너에서도 복원 내용을 읽는지 확인한 뒤에만 아래 restart를 사용한다. 파일 교체로 inode가 달라졌거나 Compose 환경변수·secret 참조·mount·image가 바뀌었으면 이 restart 분기를 사용하지 말고 중단한다. [RUN-0086](0086-dependency-version-management.md)에서 이전 image/build와 선언을 복원하고 대상·backup·의존성 영향을 검토한 승인된 recreate 계획으로 넘긴다. Secret 내용·참조 복구는 [RUN-0085](0085-openbao.md)가 소유한다.

   ```bash
   git diff -- infra/06-observability/grafana/provisioning infra/06-observability/grafana/dashboards
   docker compose --profile obs restart grafana
   docker exec grafana wget -q --spider http://localhost:3000/api/health
   ```

   이 런북은 role mapping change, secret rotation, datasource UID migration, dashboard provider lock change, protected middleware change, or Grafana image change를 검증된 복구 절차로 제공하지 않는다. 해당 변경에는 별도 approval과 rollback evidence가 필요하다.

9. Grafana가 시작 직후 재시작을 반복하고 로그에 `Failed to provision data
   sources ... data source not found`가 있으면, 이미 있는 datasource의 UID를
   provisioning이 바꾸려는 경우다. `datasource.yml` 맨 위에 해당 이름의
   `deleteDatasources`를 사용한 SPEC-0193 Pyroscope 이력이 있다. 먼저 해당 UID 충돌을 확인하고 데이터/참조 영향, backup, migration 승인을 확보한다. 승인 없이 항목을 추가하거나 삭제하지 않는다; 승인된 변경 뒤 재시작한다.

   ```bash
   docker logs --since 5m grafana 2>&1 | grep 'Failed to provision data sources'
   docker restart grafana
   ```

10. 로그에 `failed to save dashboard ... deprecatedInternalID=... is already in
    use`가 있으면, 기존 dashboard의 `uid`를 바꿨거나 지운 파일과 같은 경로에
    다른 `uid`를 둔 경우다. 유지하는 dashboard는 이전 `uid`로 되돌리고,
    교체하는 dashboard는 새 파일 경로로 옮긴다. provider가 옛 dashboard를 지우고
    새 것을 만든다.

11. SQL dashboard(`n8n-db`, `airflow-db`)가 인증 오류를 내면 reader role을 다시
    provision하기 전에 DB 소유자와 대상 schema/table 존재 및 secret/role 이름을 확인하고 role/grant 변경 승인을 확보한다. 이 job은 DB role/password/grants를 변경하며 없는 table을 건너뛰므로 exit 0만으로 모든 dashboard 권한을 증명하지 않는다.

    ```bash
    docker compose up --no-deps --no-build grafana-db-provision
    docker inspect grafana-db-provision -f '{{.State.ExitCode}}'
    ```

12. SPEC-0193 당시 Datasource health API에서 Tempo 400, Alertmanager 500이
    관찰되었다. 그 시점 plugin 동작의 기록이며 현재 모든 4xx/5xx를 정상으로
    무시하는 규칙은 아니다. Backend 상태와 plugin error를 분리하고 대신
    `/api/datasources/proxy/uid/Tempo/api/echo`와
    `/api/datasources/proxy/uid/alertmanager/api/v2/status`로 확인한다.

### Authentication and provisioning limits

Native OAuth 요구를 유지한다. `GF_AUTH_DISABLE_LOGIN_FORM`은 로그인 폼만 숨기며 Basic API 인증을 끄지 않는다. 선언된 upstream은 Basic auth를 기본 활성화하고 Compose는 비활성화하지 않으므로 SSO-only 요구가 완전히 시행되지 않는다. 유효한 자격 증명은 여전히 필요하다. 임의 break-glass 예외를 만들지 않고 @buenhyden의 별도 수정 결정과 거부 검증을 요구한다. Strict group mapping은 지정 그룹에 organization Admin/Editor/Viewer만 부여한다. `GF_AUTH_GENERIC_OAUTH_GRAFANA_ADMIN_ATTRIBUTE_PATH`는 선언 버전이 지원하지 않는 필드여서 server-admin 부여 증거가 아니다.

`grafana-db-provision`은 DB 서버가 아닌 HOME 일회성 PostgreSQL 클라이언트다. 마운트된 script/SQL은 `mng-pg`를 기다린 뒤 제한된 읽기 전용 `grafana_reader`와 기존 Airflow/n8n 테이블 권한을 생성·갱신한다. HTTP health, 자체 상태 볼륨, 이 job에 대한 Grafana depends_on은 없다. 없는 테이블을 건너뛰어도 성공 종료하므로 애플리케이션 schema 준비 뒤 읽기 전용 query와 각 dashboard를 확인한다. 재실행은 role/grant를 변경하므로 단순 조회 진단이 아니다. DB·자격 증명 복구는 관리 DB·시크릿 소유자가 맡고 helper의 복구 자산은 추적 SQL/script다.

### Verification Steps

- [ ] `docker compose --profile obs ps grafana`에서 `grafana` service가 running이다.
- [ ] `docker exec grafana wget -q --spider http://localhost:3000/api/health`가 성공한다.
- [ ] Provisioned datasource identity가 변경되지 않았다: UID `Prometheus`, `Loki`, `Tempo`, `alertmanager`, Pyroscope datasource type `grafana-pyroscope-datasource`.
- [ ] Dashboard provider가 여전히 `editable: false`이고, tracked dashboard JSON 개수가 예상값과 일치한다.
- [ ] OAuth role mapping이 여전히 `/admins`를 `Admin`으로, `/editors`를 `Editor`로, `/viewers`를 `Viewer`로 매핑하고 이 그룹들에 속하지 않은 사용자는 strict mapping으로 거부한다. `Admin`은 organization role이며 server-admin 승격 증거가 아니다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 grafana`
- **Health**: Grafana `/api/health`, UI `https://grafana.${DEFAULT_URL}`
- **Config**: Compose 환경변수·secret 참조, datasource provisioning, dashboard provider YAML과 dashboard JSON 경로
- **Backends**: Prometheus·Loki·Tempo·Pyroscope의 준비 상태
- **Evidence to Capture**: 실패한 panel·로그인 증상, datasource UID, dashboard provider 경로, 정제된 인증 로그, 재시작 시각, 최종 복구 또는 보고 상태

### Safe Rollback or Recovery Procedure

- Git-managed provisioning YAML, dashboard JSON, Compose env/secret reference, or datasource endpoint change가 원인이면 직전 Git diff 단위로 되돌리고 Grafana를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Role mapping, secret rotation, datasource UID migration, dashboard provider lock, protected middleware, or image version change는 이 런북의 안전 롤백 범위를 벗어난다.

### Planned isolated restore rehearsal

**Project 이름만 바꿔서는 실행할 수 없다.** Rehearsal 전에 고정 container name, host port, bind path, external network와 route 충돌을 제거하고 production 통지·workflow egress를 차단한 별도 Compose/storage 정의를 승인한다. 격리와 대상 backup 계약을 검토하기 전에는 NOT_RUN으로 유지한다. 임의 project에 production volume이나 credential을 연결하지 않는다.

Status: **planned and not executed**. Grafana SQLite restore 성공 사례를 주장하지 않는다.

1. image/plugin/schema identity와 object count를 기록하고, user/alert를 quiesce한 뒤 Grafana를 중지하고, provisioning과 secret reference에 맞춰 `grafana-data` 전체를 snapshot한다.
2. test route와 test Keycloak client를 사용하는 별도 project/network로 복원한다. production datasource는 read-only로 유지하거나 test endpoint로 대체한다.
3. Grafana를 시작하고 SQLite migration, users/teams, dashboards, alerts, plugins, datasource health, native OAuth를 검증하며 anonymous request가 거부되는지 확인한다.
4. 불일치가 발견되면 isolated project를 중지하고 log/checksum을 보존한다. untouched backup으로 돌아가며, production state/client/route 교체는 별도로 승인받는다.

## Verification

### Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, token, OAuth payload, rendered secret values는 기록하지 않는다.
- Datasource/dashboard 장애는 affected dashboard/panel, datasource UID, backend endpoint, redacted log excerpt, and provisioning diff를 함께 기록한다.
- Role mapping/secret/datasource UID/provider/route 변경 필요성이 보이면 approval state를 기록한다.

## Rollback and Escalation

### Rollback or Recovery

이 Runbook의 검증과 동일 bind-mounted provisioning·dashboard 파일 복원 후 재시작만 해당 분기에서 사용한다. Compose·image·secret bind 복원은 restart로 반영되지 않으므로 위의 R0086/R0085 승인된 재생성 경계로 넘긴다. Role mapping, secret rotation, datasource identity migration, dashboard provider lock, protected middleware, or image version 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

### Escalation

verification이 실패하거나, secret exposure risk가 보이거나, role mapping/secret/datasource/provider/route 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 repository owner @buenhyden에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

### Traceability

- Declared parent: [Grafana Usage Guide](../guides/0041-grafana.md) (`GDE-0041`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0041-grafana.md) (`GDE-0041`), [Policy](../policies/0041-grafana.md) (`POL-0041`)

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative이며, [derived Compose image projection](../../../infra/tech-stack.versions.json)은 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0041-grafana.md)
- [Operations policy](../policies/0041-grafana.md)
