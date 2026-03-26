# Nginx Guide

> Detailed guide for managing and understanding the Nginx Proxy in the hy-home.docker ecosystem.

---

## Overview (KR)

이 문서는 Nginx 프록시에 대한 가이드다. `hy-home.docker` 클러스터 내부에서 경로 기반(Path-based) 라우팅 설정, SSO(OAuth2 Proxy) 연동 방식, 그리고 업스트림 서비스 구성을 이해하고 관리할 수 있도록 단계별 절차와 주요 개념을 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Infrastructure Operators
- Backend Developers
- AI Agents

## Purpose

이 가이드는 사용자가 Nginx의 특수 프록시 규칙을 이해하고, 새로운 경로를 등록하며, SSO 인증을 앱에 적용하는 것을 돕는다.

## Prerequisites

- Traefik 에지 라우터 정상 작동
- SSL 인증서 (`/etc/nginx/certs` 볼륨에 위치)
- `infra_net` 네트워크 내의 업스트림 서비스 실행 중

## Step-by-step Instructions

### 1. Adding a New Path-based Route

새로운 서비스를 특정 경로(예: `/my-service/`)로 노출하려면 `nginx.conf`의 `server` 블록 내에 `location`을 추가한다:

```nginx
location /my-service/ {
    proxy_pass http://my-service-upstream/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 2. Enabling SSO (OAuth2 Proxy) for a Location

특정 경로를 SSO 인증으로 보호하려면 OAuth2 Proxy 시스템과 연동한다. Nginx는 `auth_request` 모듈을 사용하여 인증 수행 여부를 결정한다.

1. **Auth Check 엔드포인트**:
   `nginx.conf`에 내부 API 엔드포인트가 정의되어 있어야 한다:

   ```nginx
   location = /_oauth2_auth_check {
       internal;
       proxy_pass http://oauth2-proxy:4180/oauth2/auth;
       proxy_pass_request_body off;
       proxy_set_header Content-Length "";
   }
   ```

2. **Location 보호 적용**:

   ```nginx
   location /protected-app/ {
       auth_request /_oauth2_auth_check;
       error_page 401 = /oauth2/sign_in;

       auth_request_set $user $upstream_http_x_auth_request_user;
       proxy_set_header X-Auth-Request-User $user;

       proxy_pass http://protected-app-upstream/;
   }
   ```

### 3. Keycloak Integration

Keycloak을 Nginx 뒷단에 배치할 때는 정적 자산 및 리다이렉트 처리를 위해 다음 설정을 준수한다:

- **Realm 설정**: 기본 렐름은 `hy-home`을 사용한다.
- **Client 설정**: `oauth2-proxy` 클라이언트가 `confidential` 타입으로 생성되어야 한다.
- **Header 설정**: `X-Forwarded-Proto https`와 `X-Forwarded-Port 443`을 명시하여 Keycloak이 올바른 리다이렉트 URI를 생성하도록 한다.

### 4. Docker Healthcheck Configuration

Nginx 컨테이너의 상태 확인을 위해 `docker-compose.yml`에 다음과 같이 설정한다:

```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -q --spider http://localhost:80/ping || exit 1"]
  interval: 15s
  timeout: 30s
  retries: 5
```

이 설정은 Nginx 내부의 `/ping` 로케이션(200 OK 응답)을 주기적으로 점검한다.

## Common Pitfalls

- **Trailing Slash**: `proxy_pass http://service/;`와 `proxy_pass http://service;`의 차이로 인해 경로 맵핑이 어긋날 수 있다.
- **Buffer Size**: 대용량 헤더(SSO 토큰 등) 사용 시 `proxy_buffer_size` 부족으로 502 에러가 발생할 수 있다.
- **SSL Loop**: `X-Forwarded-Proto` 헤더가 올바르지 않으면 백엔드에서 무한 리다이렉트가 발생할 수 있다.

## Related Documents

- **Spec**: `[../04.specs/01-gateway/nginx.md]`
- **Operation**: `[../08.operations/01-gateway/nginx.md]`
- **Runbook**: `[../09.runbooks/01-gateway/nginx.md]`
