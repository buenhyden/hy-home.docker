---
title: "Airflow Keycloak Native Authentication Migration Incident"
version: "0.1.0"
type: "operation/incident"
status: "mitigated"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "operations"
artifact_id: "inc-2026-0002"
parent_ids:
- "RUN-0050"
created: "2026-09-18"
occurred_at: "2026-09-18T15:43:32+09:00"
---

# Airflow Keycloak Native Authentication Migration Incident

## Summary

Airflow 3.3.1 환경에서 파일 권한/DB migration 문제를 해결한 뒤 OAuth2 Proxy ForwardAuth와
Airflow 자체 JWT가 충돌했고, Native Keycloak Auth Manager로 전환하는 과정에서
Keycloak Authorization bootstrap과 provider permission 문제를 순차적으로 확인했다.

현재 login과 일부 API는 정상화되었으며 Pool/DAG/Asset resource 403의 최종 검증이 남아 있다.

## Impact

- API server 초기 기동 실패
- UI/API 500 및 403
- DAG/Pool/Asset dashboard 데이터 접근 제한
- 인증 구조 변경과 재로그인 필요

## Coordination

- Airflow 3.3.1
- Keycloak
- OAuth2 Proxy
- Traefik
- `apache-airflow-providers-keycloak` 0.8.2 -> 0.9.0

실행 절차:
- `RUN-0050`
- `RUN-0014`

## Timeline

1. `/opt/airflow/config/airflow.cfg` PermissionError.
2. DB migration/version mismatch.
3. OAuth2 Proxy `Authorization: Bearer`와 Airflow JWT validation 충돌.
4. Airflow Native Keycloak Auth Manager로 전환.
5. Airflow internal JWT secret 고정.
6. Keycloak default roles 부재로 `create-all` 404.
7. roles 생성 후 dry-run 성공.
8. 실제 bootstrap 전 `invalid_scope GET/LIST`로 500.
9. 실제 bootstrap 후 500 -> 403.
10. `/admins` group과 effective realm `Admin` role 확인.
11. provider 0.8.2 global Admin permission `UNANIMOUS` 문제 확인.
12. provider 0.9.0으로 업그레이드.
13. 새 login token/cookie 발급 확인.
14. `/ui/auth/me`, `/ui/auth/menus`, plugins/importErrors 200.
15. Pool/DAG/Asset 403은 resource authorization 검증으로 분리.

## Mitigation

- shared files owner/runtime UID 정렬
- `airflow db migrate`, `airflow db check`
- Airflow route에서 OAuth2 Proxy ForwardAuth 제거
- fixed `airflow_api_jwt_secret`
- Keycloak roles/scopes/resources/policies bootstrap
- provider 0.9.0 upgrade
- non-team `create-permissions` 재적용
- stale callback/session 제거

## Current Status

정상:
- `/`
- `/ui/config`
- `/ui/auth/me`
- `/ui/auth/menus`
- `/api/v2/plugins`
- `/api/v2/importErrors`

추가 검증:
- `/api/v2/pools`
- `/ui/dags`
- `/api/v2/assets/events`
- DAG run/HITL

## Corrective Actions

1. `RUN-0050`에 장애 패턴 추가.
2. `POL/GDE-0079`로 auth integration SSoT 신설.
3. `ADR-0038`로 selective Native OIDC 결정 기록.
4. hardening script의 stale Airflow ForwardAuth assertion 수정.
5. Kafbat/Workflow 문서의 stale SSO 문구 수정.
6. provider update 시 permission repair를 release checklist에 포함.
7. 노출된 live token/session 폐기.

## Traceability

- `RUN-0050`
- `RUN-0014`
- `POL-0079`
- `GDE-0079`
- `ADR-0038`

## Communications

token/refresh token/id token/client secret 원문은 incident/issue/PR에 기록하지 않는다.
