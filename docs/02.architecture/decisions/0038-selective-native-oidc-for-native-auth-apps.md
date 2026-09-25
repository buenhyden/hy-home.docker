---
title: "Selective Native OIDC for Applications with Built-in Authentication"
version: "0.1.0"
type: "sdlc/architecture-decision"
status: "proposed"
owner: "@buenhyden"
updated: "2026-09-18"
layer: "architecture"
artifact_id: "ADR-0038"
parent_ids:
- "AD-0002"
created: "2026-09-18"
---

# ADR-0038: Selective Native OIDC for Applications with Built-in Authentication

## Context

`ADR-0002`는 Keycloak을 중앙 Identity Provider로, OAuth2 Proxy를 Traefik
ForwardAuth provider로 선택했다. 이 패턴은 자체 인증이 없는 서비스에는 적합하지만,
자체 OIDC와 application-level RBAC를 가진 서비스에서는 double-auth,
`Authorization` header 충돌, 책임 중복을 만들 수 있다.

Airflow 3.3.1의 Keycloak Auth Manager와 Kafbat UI v1.5.0은 애플리케이션 자체
OIDC와 authorization 기능을 제공한다.

## Decision

Keycloak은 중앙 IdP로 유지한다.

서비스 인증 경로는 두 패턴으로 분리한다.

### Gateway ForwardAuth

```text
Browser -> Traefik -> OAuth2 Proxy -> Keycloak -> Service
```

자체 OIDC가 없거나 gateway SSO가 적절한 서비스에 사용한다.

### Application-native OIDC

```text
Browser -> Traefik -> Application -> Keycloak
```

자체 OIDC/RBAC를 제공하는 승인된 서비스에 사용한다.

현재 승인:

- Apache Airflow
- Kafbat UI

Airflow와 Kafbat UI router에는 `gateway-standard-chain@file`만 적용하고
OAuth2 Proxy `sso-auth@file`/`sso-errors@file`을 중복 적용하지 않는다.

## Rationale

- Keycloak 중앙 IAM을 유지한다.
- Airflow의 Keycloak Authorization Services를 그대로 사용한다.
- Kafbat의 native OAuth2/RBAC를 그대로 사용한다.
- Proxy가 주입한 `Authorization`과 application 자체 token 충돌을 방지한다.
- 자체 인증이 없는 서비스에는 ForwardAuth의 단순성을 유지한다.

## Options Considered

### ForwardAuth-only

장점:

- gateway 정책이 단순하다.

단점:

- Native OIDC 앱에서 double-auth 발생
- application-level RBAC와 gateway auth 책임 중복
- Airflow에서 실제 Bearer/JWT 충돌이 관찰됨

### Native OIDC-only

장점:

- 각 application authorization model을 직접 사용할 수 있다.

단점:

- OIDC가 없는 서비스에는 적용할 수 없다.
- 서비스별 Keycloak client 관리 비용이 증가한다.

## Consequences

### Positive

- authentication/authorization ownership이 명확해진다.
- Airflow/Kafbat application RBAC를 유지한다.
- OAuth2 Proxy header injection과 application JWT 충돌을 피한다.

### Negative

- 서비스 onboarding 시 auth pattern을 명시적으로 선택해야 한다.
- Keycloak client 수가 증가한다.

## Guardrails

- Native OIDC 서비스에 ForwardAuth를 기본적으로 중복 적용하지 않는다.
- OIDC client secret은 Docker Secret으로 주입한다.
- local mkcert CA는 system/JDK public root trust를 보존한 상태로 추가한다.
- gateway `Authorization` forwarding은 upstream token scheme과 충돌하지 않음을 검증한다.
- 신규 Native OIDC 서비스는 architecture/operations 문서에 명시한다.

## Traceability

- [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
- [Auth Architecture](../descriptions/0002-auth-architecture.md)
- [Application Auth Integration Policy](../../05.operations/policies/0079-application-auth-integration.md)
- [Application Auth Integration Guide](../../05.operations/guides/0079-application-auth-integration.md)

## Related Documents

- [ADR-0002](0002-keycloak-oauth2-proxy-choice.md)
- [AD-0002](../descriptions/0002-auth-architecture.md)
