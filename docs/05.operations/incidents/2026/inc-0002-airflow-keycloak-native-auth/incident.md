---
title: "Airflow Keycloak Native Authentication Migration Incident"
version: "0.4.0"
type: "operation/incident"
status: "resolved"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "inc-2026-0002"
parent_ids:
- "RUN-0050"
created: "2026-09-18"
occurred_at: "2026-09-18T15:43:32+09:00"
resolved_at: "2026-09-26T22:03:08+09:00"
---

# Airflow Keycloak Native Authentication Migration Incident

## Impact

### Affected Users

Airflow UI/API 사용자와 이를 운영하는 owner가 영향을 받았다.

- API server 초기 기동 실패
- UI/API 500/403
- DAG/Pool/Asset dashboard 일부 접근 제한
- 반복 재로그인과 Keycloak/Airflow 양측 진단 필요

### Observed Scope

Airflow 3.3.1 환경에서 file ownership/DB migration 문제를 해결한 뒤
OAuth2 Proxy ForwardAuth와 Airflow 자체 JWT가 충돌했다. Native Keycloak Auth
Manager로 전환하는 과정에서 Keycloak Authorization bootstrap, provider 0.8.2
permission strategy, OAuth state/cookie, resource-level authorization 문제를
순차적으로 확인했다.

관련 시스템은 Airflow 3.3.1, Keycloak, OAuth2 Proxy, Traefik,
`apache-airflow-providers-keycloak` 0.8.2 -> 0.9.0이다. 관련 Runbook은
`RUN-0050`, `RUN-0014`다.

발생 2026-09-18T15:43:32+09:00 (`occurred_at`), 해소
2026-09-26T22:03:08+09:00 (`resolved_at`). 심각도 등급, 사용자 수, 누락된
DAG run은 기록되어 있지 않다.

## Response

### Timeline

1. `/opt/airflow/config/airflow.cfg` PermissionError.
2. DB migration/version mismatch.
3. OAuth2 Proxy `Authorization: Bearer`와 Airflow JWT validation 충돌.
4. Airflow Native Keycloak Auth Manager로 전환.
5. Airflow internal JWT secret 고정.
6. Keycloak default roles 부재로 `create-all` 404.
7. `Viewer`, `User`, `Op`, `Admin`, `SuperAdmin` 생성.
8. 실제 bootstrap 전 `invalid_scope GET/LIST`로 500.
9. 실제 `create-all` 실행 후 500 -> 403.
10. `/admins` group과 effective realm `Admin` role 확인.
11. provider 0.8.2 global Admin permission `UNANIMOUS` 문제 확인.
12. provider 0.9.0으로 upgrade.
13. 새 login token/cookie 발급 확인.
14. `/ui/auth/me`, `/ui/auth/menus`, plugins/importErrors 200.
15. Pool/DAG/Asset 403은 resource authorization 문제로 분리.
16. 2026-09-26: 읽기 전용 점검에서 Airflow/Keycloak 컨테이너 healthy, provider
    0.9.0, auth manager `KeycloakAuthManager`를 확인했다. 인증된 접근 기록은
    없었다.
17. 2026-09-26T22:02:37+09:00–22:03:08+09:00: owner가 Admin으로 로그인해
    DAGs, Pools, Assets, DAG run/HITL 화면을 열었다. Traefik access log에서
    요청 111건 중 `200` 107건, `303` 1건, `307` 2건, `401` 1건(로그인 전
    `/ui/config`), `403` 0건. `/api/v2/pools`, `/ui/dags`,
    `/api/v2/assets`, `/api/v2/dags/{dag}/dagRuns/{run}/hitlDetails`가 `200`.

### Actions

조치를 수행한 사람은 기록되어 있지 않다. 결정 세 건은 기록된 Timeline 단계를
따르고, 나머지 완화 조치는 수행 단계가 기록되어 있지 않다.

| Action | Owner | Condition | Evidence |
| --- | --- | --- | --- |
| Airflow router에서 OAuth2 Proxy ForwardAuth를 제거하고 Native Keycloak Auth Manager로 전환 | 기록 없음 | 4단계 결정 | `ADR-0038`이 앱별 선택 기준을 소유한다 |
| provider 0.8.2의 global Admin permission 문제를 해소하려고 0.9.0으로 upgrade | 기록 없음 | 12단계 결정 | none |
| 남은 Pool/DAG/Asset 403을 로그인 문제가 아닌 resource authorization 문제로 분리 | 기록 없음 | 15단계 결정 | none |
| shared Airflow file ownership/runtime UID 정렬 | 기록 없음 | 완화 조치, 단계 기록 없음 | none |
| `airflow db migrate`, `airflow db check` | 기록 없음 | 완화 조치, 단계 기록 없음 | none |
| `airflow_api_jwt_secret` 고정 | 기록 없음 | 완화 조치, 단계 기록 없음 | none |
| Keycloak realm roles와 Authorization Services bootstrap | 기록 없음 | 완화 조치, 단계 기록 없음 | none |
| non-team `create-permissions` 재적용 | 기록 없음 | 완화 조치, 단계 기록 없음 | none |
| stale callback/session 제거 | 기록 없음 | 완화 조치, 단계 기록 없음 | none |

## Resolution

### Verified State

Resolved. 2026-09-26 owner의 로그인 세션에서 Pool/DAG/Asset/HITL이 모두
`200`으로 확인되어 resolved로 닫았다. 어느 조치가 마지막 `403`을 해소했는지와
그 시각은 기록되어 있지 않다.

로그인한 Admin 세션에서 다음 경로가 모두 `200`이다 (2026-09-26, Traefik
access log, 경로와 상태 코드만 기록):

- `/`, `/ui/config`, `/ui/auth/me`, `/ui/auth/menus`
- `/api/v2/plugins`, `/api/v2/importErrors`
- `/api/v2/pools`
- `/ui/dags`, `/api/v2/dags/{dag}`
- `/api/v2/assets`, `/api/v2/dags/{dag}/assets/{asset}`
- `/api/v2/dags/{dag}/dagRuns`, `/api/v2/dags/{dag}/dagRuns/{run}/hitlDetails`

근거 기록은 다음과 같다.

- Traefik access log의 경로와 상태 코드 (2026-09-26). token/refresh token/id
  token/client secret 원문은 incident/issue/PR에 기록하지 않는다.
- Runbook: `RUN-0050`, `RUN-0014`
- Policy와 Guide: `POL-0079`, `GDE-0079`
- Decision: `ADR-0038`
- [Postmortem](postmortem.md)

### Remaining Work

후속 조치의 owner·tracking ID·검증과 상태는 [postmortem](postmortem.md)이
추적한다. 이 incident에서 기록한 조치는 다음과 같다.

1. `RUN-0050`에 auth troubleshooting 시나리오 추가.
2. `POL/GDE-0079`로 auth integration SSoT 신설.
3. `ADR-0038`로 selective Native OIDC 결정 기록.
4. hardening script의 stale Airflow ForwardAuth assertion 수정.
5. Kafbat/workflow 문서의 stale SSO 문구 수정.
6. provider update 시 permission repair를 release checklist에 포함.
7. 노출된 live token/session 폐기: 2026-09-27 완료. Keycloak `home-airflow`
   session은 0건이었고, `airflow_api_jwt_secret`을 교체해 기존 Airflow JWT를
   무효화했다.

2026-11-17 owner 결정에 따라 본문을 공통 역할 설계 core의 incident 절로
옮겼다. 기록된 사실은 바뀌지 않았고, Decisions와 Mitigation은 Actions 표의
행이 되었다.
