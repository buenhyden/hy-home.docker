---
title: "Airflow Keycloak Native Authentication Migration Postmortem"
version: "0.1.0"
type: "operation/postmortem"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-26"
layer: "operations"
artifact_id: "inc-2026-0002-PM"
parent_ids:
- "inc-2026-0002"
created: "2026-09-26"
---

# Airflow Keycloak Native Authentication Migration Postmortem

## Summary

Airflow 3.3.1을 OAuth2 Proxy ForwardAuth에서 native Keycloak Auth Manager로
옮기는 과정에서 API server 기동 실패, UI/API `500`/`403`, 반복 재로그인이
이어졌다. 2026-09-26 owner의 Admin 세션에서 Pool, DAG, Asset, HITL이 모두
`200`으로 확인되어 [incident](incident.md)를 resolved로 닫았다.

## Impact

- Airflow API server 초기 기동 실패
- UI/API `500`/`403`, DAG/Pool/Asset 화면 일부 접근 불가
- Keycloak과 Airflow 양쪽의 반복 재로그인과 진단 작업

사용자 수, 중단 시간, 누락된 DAG run은 기록되어 있지 않다.

## Timeline

- 2026-09-18T15:43:32+09:00: incident 발생 시각 (`occurred_at`).
- 시각 미기록: incident Timeline 1–15단계 (파일 권한, DB migration,
  ForwardAuth와 Airflow JWT 충돌, native Auth Manager 전환, Keycloak role과
  Authorization Services bootstrap, provider 0.8.2의 global Admin permission
  `UNANIMOUS` 확인, provider 0.9.0 upgrade, `create-permissions` 재적용).
- 2026-09-26: 읽기 전용 점검에서 컨테이너 healthy, provider 0.9.0,
  `KeycloakAuthManager` 확인.
- 2026-09-26T22:02:37+09:00–22:03:08+09:00: owner Admin 세션의 요청 111건
  중 `403` 0건. Pool, DAG, Asset, HITL 경로 모두 `200`.

## Root Cause

기록된 원인은 여러 겹이다.

- OAuth2 Proxy ForwardAuth가 붙인 `Authorization: Bearer`가 Airflow 자체
  JWT 검증과 충돌했다.
- Keycloak에 Airflow용 realm role과 Authorization Services가 bootstrap되지
  않아 `create-all` `404`, `invalid_scope` `500`이 났다.
- provider 0.8.2의 global Admin permission이 `UNANIMOUS` 전략이어서 Admin
  사용자에게도 resource 접근이 거부됐다.

Pool/DAG/Asset `403`을 마지막으로 해소한 조치가 provider 0.9.0 upgrade인지
`create-permissions` 재적용인지는 기록되어 있지 않다.

## Contributing Factors

- ForwardAuth 경로를 native OIDC 앱에도 기본으로 적용하던 구성
- provider 업그레이드 절차에 permission 재적용 단계가 없었음
- 인증된 resource 접근을 확인하는 검증 경로가 없어 403 해소 여부를 늦게 확인

## Detection and Response

API server 기동 실패와 UI 오류로 발견했다. 단계별 대응은 incident의
Timeline과 Mitigation에 있다. 최종 확인은 owner 로그인 세션의 Traefik
access log에서 경로와 상태 코드만 읽어 수행했고, token·cookie는 읽지 않았다.

## Corrective Actions

| Action | Owner | Due date | Tracking ID | Verification |
| --- | --- | --- | --- | --- |
| RUN-0050에 auth troubleshooting 시나리오 추가 | @buenhyden | 완료 | RUN-0050 | 시나리오 0 "Keycloak 인증 또는 TLS 실패" 존재 |
| auth integration SSoT 신설 | @buenhyden | 완료 | POL-0079, GDE-0079 | 두 문서 존재 |
| selective native OIDC 결정 기록 | @buenhyden | 완료 | ADR-0038 | ADR 존재 |
| hardening의 stale Airflow ForwardAuth assertion 수정 | @buenhyden | 완료 | `check-all-hardening.sh` | Airflow double-auth middleware를 금지하는 `check_not_contains` 존재 |
| Kafbat/workflow 문서의 stale SSO 문구 수정 | @buenhyden | 완료 | GDE-0036, Airflow README | 두 문서가 native OIDC와 ForwardAuth 미적용을 기술 |
| provider 변경 시 permission 재적용을 checklist에 포함 | @buenhyden | 완료 (2026-09-26) | RUN-0050 Checklist | provider 변경 시 `create-permissions`와 Pool/DAG/Asset/HITL 확인 항목 존재 |
| 노출된 live token/session 폐기 | @buenhyden | 미정 | inc-2026-0002 | 이 세션에서 확인하지 못함; owner 확인 필요 |

## Learning

- Native OIDC 앱에 gateway ForwardAuth를 겹치면 `Authorization` header가
  충돌한다. ADR-0038이 앱별 선택 기준을 소유한다.
- provider의 permission 모델이 바뀌면 로그인 성공이 resource 권한을
  보장하지 않는다. 로그인 후 resource 화면까지 확인해야 한다.

## Traceability

- Incident: [inc-2026-0002](incident.md)
- Runbooks: [RUN-0050](../../../runbooks/0050-airflow.md), [RUN-0014](../../../runbooks/0014-keycloak.md)
- Policy and Guide: [POL-0079](../../../policies/0079-application-auth-integration.md), [GDE-0079](../../../guides/0079-application-auth-integration.md)
- Decision: [ADR-0038](../../../../02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md)
