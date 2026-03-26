# Keycloak IAM Setup & Configuration

> Comprehensive guide for deploying and configuring Keycloak as the central identity provider (02-auth).

---

## Overview (KR)

이 가이드는 `hy-home.docker` 플랫폼의 핵심 인증 시스템인 Keycloak의 초기 구축, 렐름(Realm) 및 OIDC 클라이언트 설정, 그리고 외부 Identity Provider(Google 등) 연동 절차를 다룬다.

## Guide Type

`system-guide | installation-guide`

## Target Audience

- Developers (Service integration)
- Operators (User & Realm management)
- Security Engineers (Identity provider auditing)

## Prerequisites

- `infra/01-gateway` (Traefik) 작동 중.
- `infra/04-data/mng-db` (PostgreSQL) 실행 중.
- `.env`에 `DEFAULT_URL`, `KEYCLOAK_ADMIN_USER` 등이 정의되어야 함.

## Step-by-Step Instructions

### 1. Initialization
Keycloak 컨테이너를 실행하고 관리자 콘솔에 접속한다.

```bash
cd infra/02-auth/keycloak
docker compose up -d
```
- **Access**: `https://keycloak.${DEFAULT_URL}`
- **Admin Login**: `KEYCLOAK_ADMIN_USER` 및 `keycloak_admin_password` (Secrets 참조).

### 2. Realm Configuration (`hy-home`)
플랫폼 루트 렐름인 `hy-home`을 생성하고 기본 보안 설정을 적용한다.

1. **Create Realm**: 드롭다운에서 'Create Realm' 선택 후 `hy-home` 입력.
2. **Login Settings**:
   - User Registration: Off (Admin provisioning only)
   - Forgot Password: On
   - Remember Me: On
3. **Tokens**:
   - Access Token Lifespan: 1 Hour
   - SSO Session Idle: 7 Days

### 3. OIDC Clients Setup
애플리케이션 연동을 위한 클라이언트를 생성한다.

- **`oauth2-proxy` (Global Auth)**:
  - Client ID: `oauth2-proxy`
  - Access Type: `confidential`
  - Valid Redirect URIs: `https://auth.${DEFAULT_URL}/oauth2/callback`
- **`grafana`**:
  - Client ID: `grafana`
  - Valid Redirect URIs: `https://grafana.${DEFAULT_URL}/login/generic_oauth`

### 4. Client Scopes & Groups
1. **Client Scopes**: `openid`, `profile`, `email` 외에 `groups` (Mapper: Group Membership) 커스텀 스코프를 추가하여 토큰에 그룹 정보를 포함함.
2. **User Groups**: `/admins`, `/operators`, `/users` 계층을 생성하고 롤 매핑을 수행함.

### 5. Identity Provider (Google)
1. **Google Cloud Console**: OAuth 2.0 클라이언트 ID 및 Secret 발급.
2. **Keycloak**: 'Identity Providers' 메뉴에서 'Google' 추가.
3. **Configuration**: 발급된 ID/Secret 입력 및 `Redirect URI`를 Google 콘솔에 등록.

## Common Pitfalls

- **Redirect URI Mismatch**: Traefik 라우팅 주소와 Keycloak 설정 주소가 정확히 일치해야 함.
- **HTTPS Trust**: `KC_PROXY_HEADERS: xforwarded` 설정이 누락되면 리디렉션 무한 루프가 발생함.

## Related Documents

- **Operation**: `[../../08.operations/02-auth/keycloak.md]`
- **Runbook**: `[../../09.runbooks/02-auth/keycloak.md]`
- **Spec**: `[../../04.specs/02-auth/keycloak.md]`
