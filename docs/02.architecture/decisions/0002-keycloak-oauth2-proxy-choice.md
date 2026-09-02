---
title: Choice of Keycloak and OAuth2 Proxy for IAM and SSO
type: architecture/decision
layer: architecture
status: active
owner: "@buenhyden"
artifact_id: ADR-0002
parent_ids:
  - AD-0002
created: 2026-03-26
updated: 2026-09-01
---
# ADR-0002: Choice of Keycloak and OAuth2 Proxy for IAM and SSO

> This ADR documents the decision to use Keycloak as the Identity Provider and OAuth2 Proxy as the authentication gateway.

---

## Overview

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

## Options Considered

- **Authelia**: A lightweight alternative. While good, it lacks the advanced identity provider features and wide community support of Keycloak.
- **Casdoor**: Another IAM. Less "enterprise-proven" compared to Keycloak in our assessment.
- **App-level Auth**: Implementing auth in each app. Rejected due to high maintenance and lack of unified security policy.

## Consequences

- **Pros**: Robust, standard-based, zero-trust ready, unified UI for users.
- **Cons**: higher resource consumption (Keycloak is Java/Quarkus-based), increased complexity in managing realms and clients.

## AI Agent Guidance

Agents must use the OIDC discovery endpoint provided by Keycloak (`/realms/hy-home.realm/.well-known/openid-configuration`) to obtain token information.

## Explicit Non-goals

- This ADR does not change runtime behavior.
- This ADR does not rewrite historical decision evidence.
- Implementation details remain in linked specs, plans, and tasks.

### Additional Consequences

Existing rationale, positive/negative notes, and trade-off text in this ADR remain the consequence record. This alignment section introduces no new decision outcome.

## Traceability

이 결정의 확인 근거는 `Related Documents`에 연결된 Architecture Description, Spec, Operations 문서와 현재 저장소 구성으로 한정한다. 별도 실행 증거가 없는 런타임 상태는 주장하지 않는다.

## Decision Drivers

The decision context above records the applicable drivers and evidence.

## Related Documents

- **PRD**: [../../01.requirements/0002-auth.md](../../01.requirements/0002-auth.md)
- **Architecture Description**: [../descriptions/0002-auth-architecture.md](../descriptions/0002-auth-architecture.md)
- **Spec**: [../../03.specs/002-auth/spec.md](../../03.specs/0002-auth/spec.md)
