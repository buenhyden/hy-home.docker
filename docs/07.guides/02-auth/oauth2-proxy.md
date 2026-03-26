# OAuth2 Proxy Guide

> Comprehensive guide for setting up and configuring OAuth2 Proxy as a ForwardAuth provider within the `hy-home.docker` ecosystem.

---

## Overview (KR)

이 문서는 OAuth2 Proxy의 설정 및 운영에 대한 가이드다. Traefik의 ForwardAuth 미들웨어 연동 방법, `oauth2-proxy.cfg` 설정, 그리고 Keycloak OIDC Client와의 연동 구성을 단계별로 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Developer
- Operator
- Agent-tuner

## Purpose

이 가이드는 사용자가 OIDC를 기본적으로 지원하지 않는 백엔드 서비스에 대해 OAuth2 Proxy를 사용하여 중앙 집중식 SSO(Single Sign-On)를 구현할 수 있도록 돕는다.

## Prerequisites

- `infra/02-auth/keycloak` 서비스가 정상 실행 중이어야 함.
- `infra/02-auth/oauth2-proxy` 서비스 빌드 및 실행 완료.
- Keycloak에서 OAuth2 Proxy를 위한 OIDC Client 생성 완료.

## Step-by-step Instructions

### 1. Keycloak Client Configuration

1. Keycloak Admin 콘솔에서 `hy-home` Realm을 선택한다.
2. **Clients** -> **Create client**를 클릭한다.
3. **Client ID**: `oauth2-proxy` 입력.
4. **Root URL**: `https://auth.${DEFAULT_URL}` 입력.
5. **Valid Redirect URIs**: `https://auth.${DEFAULT_URL}/oauth2/callback` 추가.
6. **Credentials** 탭에서 **Client Secret**을 복사하여 저장한다.

### 2. OAuth2 Proxy Configuration (`oauth2-proxy.cfg`)

1. `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg` 파일을 수정한다.
2. `oidc_issuer_url`을 Keycloak의 Realm URL로 설정한다.
3. `cookie_domains`를 서비스가 사용하는 도메인(예: `.127.0.0.1.nip.io`)으로 설정한다.
4. `cookie_secret`은 32바이트 이상의 임의의 문자열로 생성하여 등록한다.

### 3. Traefik ForwardAuth Middleware Integration

백엔드 서비스의 `docker-compose.yml` 레이블에 다음을 추가한다:

```yaml
labels:
  - "traefik.http.routers.my-app.middlewares=sso-auth@file"
```

*(참고: `sso-auth` 미들웨어는 Traefik 동적 설정 파일에서 `auth.${DEFAULT_URL}/oauth2/auth`를 가리키도록 정의되어야 함)*

## Common Pitfalls

- **Cookie Domain Mismatch**: 쿠키 도메인이 백엔드 서비스 도메인과 일치하지 않으면 무한 로그인 루프가 발생할 수 있음.
- **Client Secret 노출**: `client_secret_file`을 사용하여 런타임에 주입하는 방식을 권장함.

## Related Documents

- **Spec**: `[../../../docs/04.specs/02-auth/oauth2-proxy.md]`
- **Operation**: `[../../08.operations/02-auth/oauth2-proxy.md]`
- **Runbook**: `[../../09.runbooks/02-auth/oauth2-proxy.md]`
