---
title: "Application Authentication Integration Policy"
version: "0.4.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
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
- OpenBao
- 신규 OIDC-capable internal applications
- Open WebUI/Gatus native integrations and the deferred Terrakube candidate under Task 0004

## Controls

### Required

- 모든 사용자 authentication identity source는 Keycloak을 기준으로 한다.
- 서비스 onboarding 시 `Gateway ForwardAuth` 또는 `Application-native OIDC` 중
  하나를 주 인증 경로로 명시한다.
- 현재 Native OIDC 서비스는 Airflow, Kafbat UI, OpenBao, Open WebUI, Gatus, Superset이다.
- Airflow/Kafbat/OpenBao/Open WebUI/Gatus/Superset Traefik router는 `gateway-standard-chain@file`만 사용한다.
- Flower/n8n 등 ForwardAuth 대상은 승인된 `sso-errors@file,sso-auth@file`
  chain을 유지한다.
- 모든 Traefik HTTP router는 SSO chain을 쓰거나, guide의 Route Authentication
  Matrix에 대체 인증을 명시한다. 인증 없는 route와 TCP route는 두지 않는다
  (`RouteAuthContractTests`).
- Open WebUI, Gatus, Terrakube의 ForwardAuth 제거는 Task 0004의 서비스별 acceptance evidence가 기록된 뒤에만 허용한다. 단계별 전환은 사용자가 이미 승인했으며, 같은 범위의 재승인을 요구하지 않는다.
- Compose 기반 OIDC client secret은 Docker Secret으로 주입한다. OpenBao native
  OIDC secret은 승인된 절차로 auth backend에 저장한다. 비밀값은 공개 설정에 넣지 않는다.
- token/refresh token/id token 원문을 문서, incident, PR, task evidence에 기록하지 않는다.
- local mkcert CA는 기존 public CA trust를 보존한 상태로 추가한다.
- Airflow provider update 시 Keycloak permission migration 요구사항을 확인한다.
- Kafbat RBAC `clusters`는 configured cluster name과 일치해야 한다.

- Open WebUI 초기 전환은 가입을 비활성화하고 기존 gateway를 유지한다. 이메일 병합은
  검증된 단일 기존 관리자 연결에 한정하며, 수용 검증 후 비활성화한다.
- Gatus는 cookie/PKCE 보완과 전용 client·로그인 검증 전까지 gateway를 유지한다.
- 미기동 Terrakube는 명시적 API audience 검증과 실행 검증 전까지 완료로 보지 않는다.

### Disallowed

- Native OIDC 서비스에 OAuth2 Proxy ForwardAuth를 동시에 기본 인증으로 적용
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
HYHOME_COMPOSE_PROFILES=security bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=availability bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES=ai bash scripts/validation/validate-docker-compose.sh
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh

bash scripts/hardening/check-all-hardening.sh 02-auth
bash scripts/hardening/check-all-hardening.sh 03-security
bash scripts/hardening/check-all-hardening.sh 05-messaging
bash scripts/hardening/check-all-hardening.sh 07-workflow
bash scripts/hardening/check-all-hardening.sh 06-observability
bash scripts/hardening/check-all-hardening.sh 08-ai
```

추가 검증:

- Airflow/Kafbat/OpenBao/Open WebUI/Gatus/Superset router = gateway-only; Gatus는 외부 metrics 제외
- ForwardAuth 대상 서비스 = SSO chain 유지
- Keycloak client redirect URI/public URL 정합
- Compose client secret Docker Secret mapping
- OpenBao auth-backend OIDC client/role/policy 설정은 [OpenBao runbook](../../03-security/0085-openbao/runbook.md)의 비밀값 없는 점검 절차로 확인
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

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Keycloak Guide](../0014-keycloak/guide.md)
- [OAuth2 Proxy Guide](../0015-oauth2-proxy/guide.md)
- [Kafka/Kafbat Guide](../../05-messaging/0036-kafka/guide.md)
- [Airflow Guide](../../07-workflow/0050-airflow/guide.md)
