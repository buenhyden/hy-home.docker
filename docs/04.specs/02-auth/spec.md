<!-- Target: docs/04.specs/02-auth/spec.md -->

# 02-Auth Technical Specification

> Detailed implementation specification for the Identity and Access Management and ForwardAuth Gateway components.

---

## Overview (KR)

이 문서는 `hy-home.docker`의 인증 시스템(`02-auth`)의 상세 기술 명세를 정의한다. Keycloak의 OIDC 프로 엔드포인트 구성, OAuth2 Proxy의 ForwardAuth 연동 방식, 그리고 PostgreSQL 및 Valkey와의 데이터 인터렉션을 명시하여 구현과 운영의 기준을 제공한다.

## Design Boundaries

- **In Scope**:
  - Keycloak server configuration (Quarkus runtime).
  - OAuth2 Proxy command-line flags and config files.
  - PostgreSQL schema for Keycloak.
  - Valkey session store interface.
- **Support / Non-goals**:
  - Infrastructure provisioning (handled by Terraform/Ansible).

## Core Specification

### 1. Keycloak Implementation Details

- **Image**: `quay.io/keycloak/keycloak:26.5.4`
- **DB**: PostgreSQL 16+ via JDBC.
- **Port**: `8080` (main), `9000` (management/metrics).
- **Features**: Metrics enabled, Health enabled, Proxy headers set to `xforwarded`.

### 2. OAuth2 Proxy Implementation Details

- **Provider**: `keycloak-oidc`
- **Session Store**: `redis` (targeting Valkey).
- **ForwardAuth Flow**:
  - Traefik intercepts requests.
  - Calls `/oauth2/auth` for verification.
  - Redirects to `/oauth2/start` if unauthenticated.
  - Keycloak callback handled at `/oauth2/callback`.

## Data Model & Configuration

### Keycloak Environment Variables

- `KC_DB`: `postgres`
- `KC_HTTP_ENABLED`: `true`
- `KC_PROXY_HEADERS`: `xforwarded`

### OAuth2 Proxy Config Flags

- `--provider=keycloak-oidc`
- `--oidc-issuer-url=https://keycloak.127.0.0.1.nip.io/realms/hy-home.realm`
- `--cookie-domain=.127.0.0.1.nip.io`
- `--upstream=static://200` (ForwardAuth mode)

## Operation & Monitoring

### Healthcheck

- **Keycloak**: `/health/ready` (Management port 9000)
- **OAuth2 Proxy**: `/ping` (Port 4180)

### Metrics

- **Keycloak**: `/metrics` in Prometheus format.
- **OAuth2 Proxy**: Standard logging to stdout.

## Security Controls

- MFA enforced via Keycloak Realm settings.
- Cookie security: `HttpOnly`, `Secure`, `SameSite=Lax`.

## Related Documents

- **PRD**: `[../../01.prd/2026-03-26-02-auth.md]`
- **ARD**: `[../../02.ard/0002-auth-architecture.md]`
- **Plan**: `[../../05.plans/2026-03-26-02-auth-standardization.md]`
