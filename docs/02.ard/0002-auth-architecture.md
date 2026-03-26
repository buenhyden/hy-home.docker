<!-- Target: docs/02.ard/0002-auth-architecture.md -->

# 02-Auth Architecture Reference

> This document defines the technical architecture for Identity and Access Management (IAM) and Authentication ForwardAuth Gateway.

---

## Overview (KR)

`02-auth` 아키텍처는 사용자 식별 및 액세스 제어를 위한 두 가지 핵심 계층으로 구성된다. 중앙 IAM 역할을 수행하는 `Keycloak`과 트래픽 가로채기를 통해 SSO를 강제하는 `OAuth2 Proxy`가 긴밀하게 연동된다. 이 구조는 `Traefik`의 ForwardAuth 메커니즘을 활용하여 모든 백엔드 서비스에 대한 통일된 인증 게이트웨이를 제공한다.

## Status

- **Proposed**: 2026-03-26
- **Status**: Active (Standardized)
- **Stakeholders**: AI Platform Team, DevOps Team, Security Team

## Principles

- **Zero-Trust Enforcement**: All requests must be explicitly authenticated.
- **Protocol Standardization**: Use OIDC (OpenID Connect) for all internal integrations.
- **Stateless Verification**: Leverage JWT (JSON Web Tokens) where applicable, backed by server-side sessions.
- **High Availability**: Identity data and sessions must be resilient to container failures.

## Context

The auth system sits between the `01-gateway` and other internal services. It validates user presence before traffic enters any protected container.

### System Architecture Diagram (Mermaid)

```mermaid
graph TD
    Client["User Browser"]
    Gateway["01-Gateway (Traefik)"]
    OAuth2Proxy["OAuth2 Proxy (SSO Gateway)"]
    Keycloak["Keycloak (IAM Provider)"]
    PostgreSQL["PostgreSQL (Identity DB)"]
    Valkey["Valkey (Session Cache)"]

    Client -->|HTTPS| Gateway
    Gateway -->|ForwardAuth Check| OAuth2Proxy
    OAuth2Proxy -->|OIDC Flow| Keycloak
    Keycloak <--> PostgreSQL
    OAuth2Proxy <--> Valkey
    OAuth2Proxy -->|Inject Headers| Gateway
    Gateway -->|Authorized Request| InternalService["Internal Service"]
```

## Decisions

- **IAM Engine**: Keycloak (Quarkus distribution) for robust OIDC/SAML support.
- **SSO Gateway**: OAuth2 Proxy for standardized ForwardAuth implementation.
- **Session Manager**: Valkey as a high-performance Redis-compatible session store.
- **Storage**: PostgreSQL for identity persistence (Realms, Users, Clients).

## Data Models

Refer to `docs/04.specs/02-auth/spec.md` for detailed OIDC claims and realm structures.

## AI Agent Integration

Agents access services using Service Account tokens issued by Keycloak. All agent-initiated actions must include the `X-Auth-Request-User` header for auditing.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-02-auth.md]`
- **Spec**: `[../04.specs/02-auth/spec.md]`
- **ADR**: `[../03.adr/####-keycloak-oauth2-proxy-choice.md]`
