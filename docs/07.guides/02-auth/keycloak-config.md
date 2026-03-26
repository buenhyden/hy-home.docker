# Keycloak Configuration Guide

> Detailed configuration specifications for Realms, Clients, and Identity Providers (02-auth)

---

## Overview (KR)

이 문서는 `hy-home.docker` 플랫폼의 Keycloak 설정 세부 사항을 다룬다. 렐름(Realm), OIDC 클라이언트, 클라이언트 스코프, 그룹 구조, 그리고 외부 Identity Provider(Google 등) 연동에 대한 표준 설정을 제공한다.

## Guide Type

`system-guide`

## Target Audience

- **Developers**: OIDC 클라이언트 연동 및 스코프 매핑 이해
- **Operators**: 렐름 설정 및 사용자 그룹 관리
- **Security Engineers**: 인증 정책 및 외부 IdP 보안 검토

## Purpose

플랫폼 인증 체계의 정합성을 유지하기 위한 표준 설정 가이드라인을 제공하고, 신규 서비스 연동 시 참고할 수 있는 기반 정보를 기술한다.

## Prerequisites

- Keycloak 서비스가 가동 중이어야 함 (`infra/02-auth/keycloak`).
- 관리자 권한(`admin` 계정)이 필요함.

## Configuration Specifications

### 1. Realm: `hy-home`

플랫폼의 기본 렐름으로 모든 서비스의 루트 인증 체계로 사용된다.

- **Login Settings**:
  - User Registration: Off (Admin provisioning only)
  - Edit Username: Off
  - Forgot Password: On
  - Remember Me: On
- **Tokens**:
  - Access Token Lifespan: 1 Hour
  - Refresh Token Lifespan: 30 Days
  - SSO Session Idle: 7 Days
- **SSL**: `all` (Required for all requests)

### 2. OIDC Clients

#### `oauth2-proxy` (Global Ingress Auth)

- **Client ID**: `oauth2-proxy`
- **Access Type**: `confidential`
- **Valid Redirect URIs**: `https://auth.${DEFAULT_URL}/oauth2/callback`
- **Service Accounts Enabled**: On (For backend-to-backend calls if needed)

#### `grafana` (Observability Hub)

- **Client ID**: `grafana`
- **Access Type**: `confidential`
- **Valid Redirect URIs**: `https://grafana.${DEFAULT_URL}/login/generic_oauth`

### 3. Client Scopes

- **`openid`**: 기본 OpenID Connect 스코프.
- **`profile`**: 사용자 이름, 선호 언어 등 기본 프로필 정보.
- **`email`**: 이메일 주소 및 검증 여부 (`email_verified`).
- **`groups` (Custom)**:
  - Protocol: `openid-connect`
  - Mapper Type: `Group Membership`
  - Token Claim Name: `groups`
  - Full group path: On

### 4. User Groups

권한 관리를 위해 다음과 같은 계층 구조를 권장한다.

- `/admins`: 플랫폼 전체 관리자 (Keycloak `admin` 역할 매핑)
- `/operators`: 인프라 및 서비스 운영자
- `/users`: 일반 서비스 사용자
- `/external`: 외부 IdP(Google 등) 연동 사용자

### 5. Identity Providers (IdP)

#### Google OAuth2

- **Alias**: `google`
- **Client ID**: Google Cloud Console에서 발급된 ID
- **Client Secret**: Google Cloud Console에서 발급된 Secret
- **Default Scopes**: `openid profile email`
- **Redirect URI**: `https://keycloak.${DEFAULT_URL}/realms/hy-home/broker/google/endpoint`
- **First Login Flow**: `first broker login` (사용자 프로필 자동 완성)

## Common Pitfalls

- **Redirect URI Mismatch**: Traefik의 도메인 설정과 Keycloak의 Redirect URI가 정확히 일치해야 함.
- **Client Secret Leak**: `confidential` 클라이언트의 Secret은 반드시 Vault 또는 Secrets 시스템을 통해 관리해야 함.

## Related Documents

- **Spec**: `[../../04.specs/02-auth/spec.md]`
- **Operation**: `[../../08.operations/02-auth/keycloak.md]`
- **Runbook**: `[../../09.runbooks/02-auth/keycloak.md]`
