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
}
```

### 2. Enabling SSO for a Location
특정 경로를 SSO 인증으로 보호하려면 `auth_request` 설정을 포함한다:

```nginx
location /protected-app/ {
    auth_request /_oauth2_auth_check;
    error_page 401 = /oauth2/sign_in;

    # 유저 정보 추출 (선택)
    auth_request_set $user $upstream_http_x_auth_request_user;
    proxy_set_header X-User $user;

    proxy_pass http://protected-app-upstream/;
}
```


### 3. Reloading Configuration
설정 변경 후 다운타임 없이 반영하려면 다음 명령을 실행한다:

```bash
docker exec nginx nginx -s reload
```

## Common Pitfalls

- **Trailing Slash**: `proxy_pass http://service/;`와 `proxy_pass http://service;`의 차이로 인해 경로 맵핑이 어긋날 수 있다.
- **Buffer Size**: 대용량 헤더(SSO 토큰 등) 사용 시 `proxy_buffer_size` 부족으로 502 에러가 발생할 수 있다.
- **SSL Loop**: `X-Forwarded-Proto` 헤더가 올바르지 않으면 백엔드에서 무한 리다이렉트가 발생할 수 있다.

## Related Documents

- **Spec**: `[../04.specs/01-gateway/nginx.md]`
- **Operation**: `[../08.operations/01-gateway/nginx.md]`
- **Runbook**: `[../09.runbooks/01-gateway/nginx.md]`
