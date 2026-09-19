---
title: "Application Authentication Integration Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0079"
parent_ids:
- "ADR-0038"
created: "2026-09-18"
---

# Application Authentication Integration Policy

## Overview

이 정책은 Keycloak을 중앙 IdP로 사용하면서 OAuth2 Proxy ForwardAuth와
application-native OIDC를 선택·운영하는 기준을 정의한다.

## Policy Scope

- Keycloak
- OAuth2 Proxy
- Traefik authentication middleware
- Kafbat UI
- Apache Airflow
- 신규 OIDC-capable internal applications

## Controls

### Required

- 모든 사용자 authentication identity source는 Keycloak을 기준으로 한다.
- 서비스 onboarding 시 `Gateway ForwardAuth` 또는 `Application-native OIDC` 중
  하나를 주 인증 경로로 명시한다.
- 현재 Native OIDC 서비스는 Airflow와 Kafbat UI다.
- Airflow/Kafbat Traefik router는 `gateway-standard-chain@file`만 사용한다.
- Flower/n8n 등 ForwardAuth 대상은 승인된 `sso-errors@file,sso-auth@file`
  chain을 유지한다.
- OIDC client secret은 Docker Secret으로 주입한다.
- token/refresh token/id token 원문을 문서, incident, PR, task evidence에 기록하지 않는다.
- local mkcert CA는 기존 public CA trust를 보존한 상태로 추가한다.
- Airflow provider update 시 Keycloak permission migration 요구사항을 확인한다.
- Kafbat RBAC `clusters`는 configured cluster name과 일치해야 한다.

### Disallowed

- Airflow/Kafbat에 Native OIDC와 OAuth2 Proxy ForwardAuth를 동시에 기본 인증으로 적용
- `rootCA-key.pem` 배포/공유
- secret/token 원문 기록
- 과거 OAuth callback URL 또는 authorization code 재사용
- Keycloak access token을 Airflow internal JWT로 취급

## Exceptions

긴급한 auth 우회는 적용 범위, 시작/종료 조건, rollback, evidence를 incident/task에
기록한 경우에만 허용한다. Native OIDC 앱에 임시 ForwardAuth를 적용하려면
`Authorization` header 충돌이 없음을 먼저 검증해야 한다.

## Verification

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

bash scripts/hardening/check-all-hardening.sh 02-auth
bash scripts/hardening/check-all-hardening.sh 05-messaging
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

추가 검증:

- Airflow/Kafbat router = gateway-only
- ForwardAuth 대상 서비스 = SSO chain 유지
- Keycloak client redirect URI/public URL 정합
- client secret Docker Secret mapping
- Airflow provider/Authorization Services bootstrap 상태

## Review Cadence

- Keycloak update
- OAuth2 Proxy update
- Airflow Keycloak provider update
- Kafbat UI update
- 신규 Native OIDC 서비스 승인
- Quarterly auth integration review

## Traceability

- Parent: [ADR-0038](../../../../02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- Child: [GDE-0079](guide.md)
- Architecture: [AD-0002](../../../../02.architecture/descriptions/0002-auth-architecture.md)

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [curated version projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Keycloak Guide](../0014-keycloak/guide.md)
- [OAuth2 Proxy Guide](../0015-oauth2-proxy/guide.md)
- [Kafka/Kafbat Guide](../../05-messaging/0036-kafka/guide.md)
- [Airflow Guide](../../07-workflow/0050-airflow/guide.md)
