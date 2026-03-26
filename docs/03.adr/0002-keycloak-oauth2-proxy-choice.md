<!-- Target: docs/03.adr/0002-keycloak-oauth2-proxy-choice.md -->

# ADR-0002: Choice of Keycloak and OAuth2 Proxy for IAM and SSO

> This ADR documents the decision to use Keycloak as the Identity Provider and OAuth2 Proxy as the authentication gateway.

---

## Overview (KR)

이 문서는 `hy-home.docker`의 인증 체계로 Keycloak과 OAuth2 Proxy를 선정한 기술적 결정 배경을 다룬다. 표준 OIDC 프로토콜 준수, 다양한 인증 수단 지원, 그리고 클라이언트 사이드 코드 수정 없이 기존 서비스를 보호할 수 있는 ForwardAuth 아키텍처 구현을 위한 선택이다.

## Context

We need an authentication system that is:

1. Centrally managed.
2. Protocol-standard (OIDC, SAML).
3. Easily integrable with Traefik.
4. Capable of protecting "dumb" upstream services that don't have built-in auth.

## Decision

We decided to use:

- **Keycloak**: As the primary Identity/OIDC Provider.
- **OAuth2 Proxy**: As the ForwardAuth middleware provider.

## Rationale

- **Keycloak** is the industry standard for open-source IAM, offering rich features like SSO, Identity Brokering, and MFA out of the box.
- **OAuth2 Proxy** allows us to enforce authentication at the ingress layer (Traefik) without modifying the source code of internal applications.
- This combination is well-supported, highly configurable, and integrates natively with our Traefik gateway via the ForwardAuth middleware pattern.

## Alternatives Considered

- **Authelia**: A lightweight alternative. While good, it lacks the advanced identity provider features and wide community support of Keycloak.
- **Casdoor**: Another IAM. Less "enterprise-proven" compared to Keycloak in our assessment.
- **App-level Auth**: Implementing auth in each app. Rejected due to high maintenance and lack of unified security policy.

## Consequence

- **Pros**: Robust, standard-based, zero-trust ready, unified UI for users.
- **Cons**: higher resource consumption (Keycloak is Java/Quarkus-based), increased complexity in managing realms and clients.

## AI Agent Guidance

Agents must use the OIDC discovery endpoint provided by Keycloak (`/realms/hy-home.realm/.well-known/openid-configuration`) to obtain token information.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-02-auth.md]`
- **ARD**: `[../02.ard/0002-auth-architecture.md]`
- **Spec**: `[../04.specs/02-auth/spec.md]`
- **Plan**: `[../05.plans/2026-03-26-02-auth-standardization.md]`
