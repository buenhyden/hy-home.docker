---
title: "Application Authentication Integration Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "operations"
artifact_id: "POL-0079"
parent_ids:
- "ADR-0038"
created: "2026-09-18"
---

# Application Authentication Integration Policy

## Overview

이 정책은 `hy-home.docker`에서 Keycloak을 중앙 IdP로 사용하면서
OAuth2 Proxy ForwardAuth와 application-native OIDC를 선택·운영하는 기준을 정의한다.

## Policy Scope

대상:
- Keycloak
- OAuth2 Proxy
- Traefik authentication middleware
- Kafbat UI
- Apache Airflow
- 이후 추가되는 OIDC-capable internal applications

## Controls

### Required

- 모든 사용자 인증 identity source는 Keycloak을 기준으로 한다.
- 서비스 onboarding 시 `ForwardAuth` 또는 `Native OIDC` 중 하나를 주 인증 경로로 명시한다.
- Native OIDC 서비스의 Traefik route에는 OAuth2 Proxy ForwardAuth를 중복 적용하지 않는다.
- 현재 Native OIDC 서비스:
  - Airflow
  - Kafbat UI
- 현재 Airflow router는 `gateway-standard-chain@file`만 사용한다.
- 현재 Kafbat UI router는 `gateway-standard-chain@file`만 사용한다.
- Flower/n8n 등 ForwardAuth 대상 서비스는 기존 `sso-errors@file,sso-auth@file` 경계를 유지한다.
- OIDC client secret은 Docker Secret으로 주입한다.
- token/refresh token/id token 원문을 문서, incident, task evidence, PR에 기록하지 않는다.
- local mkcert CA를 사용하는 애플리케이션은 기존 public CA trust를 보존한 상태로 local root CA를 추가한다.
- Airflow Keycloak provider 변경 시 기존 Keycloak permission migration 요구사항을 확인한다.
- Kafbat RBAC `clusters` 값은 configured cluster name과 일치해야 한다.

### Disallowed

- Airflow/Kafbat에 Native OIDC와 OAuth2 Proxy ForwardAuth를 동시에 기본 인증으로 적용
- `rootCA-key.pem` 배포/공유
- secret 값을 compose/documentation에 평문 기록
- 오래된 OAuth callback URL 또는 authorization code 재사용
- Keycloak access token을 Airflow internal JWT로 취급

## Exceptions

긴급한 우회가 필요하면:
- 적용 범위
- 시작/종료 조건
- rollback
- evidence
를 incident/task에 기록해야 한다.

Native OIDC 서비스에 임시 ForwardAuth를 적용하는 예외는 upstream `Authorization`
header를 차단하고 application login flow와 충돌하지 않음을 검증한 경우에만 허용한다.

## Verification

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=messaging bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

bash scripts/hardening/check-all-hardening.sh 02-auth
bash scripts/hardening/check-all-hardening.sh 05-messaging
bash scripts/hardening/check-all-hardening.sh 07-workflow
```

검증 시:
- Airflow/Kafbat route가 gateway-only인지 확인
- OAuth2 Proxy 보호 서비스는 ForwardAuth chain 유지
- Keycloak client redirect URI와 public application URL 일치
- secret file mapping 존재
- Airflow provider/permission bootstrap 상태 확인

## Review Cadence

- Keycloak major/minor update
- OAuth2 Proxy update
- Airflow Keycloak provider update
- Kafbat UI update
- 신규 Native OIDC 서비스 승인 시
- 분기별 auth integration review

## Traceability

- Parent: [ADR-0038](../../../../02.architecture/decisions/0038-selective-native-oidc-for-native-auth-apps.md)
- Child guide: [GDE-0079](guide.md)
- Related current architecture: [AD-0002](../../../../02.architecture/descriptions/0002-auth-architecture.md)

## Related Documents

- [Keycloak Guide](../0014-keycloak/guide.md)
- [OAuth2 Proxy Guide](../0015-oauth2-proxy/guide.md)
- [Kafka/Kafbat Guide](../../../05-messaging/0036-kafka/guide.md)
- [Airflow Guide](../../../07-workflow/0050-airflow/guide.md)
