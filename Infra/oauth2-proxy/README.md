# OAuth2 Proxy

## 1. 서비스 개요 (Service Overview)
**서비스 정의**: 인증 메커니즘이 없는 백엔드 애플리케이션 앞에 배치되어, OpenID Connect(OIDC) 기반의 인증을 강제하는 리버스 프록시 및 인증 미들웨어입니다.  
Traefik의 `Forward Auth` 기능과 연동하여, 사용자가 Keycloak을 통해 로그인한 후에만 보호된 서비스에 접근할 수 있도록 보장합니다.

## 2. 주요 기능 (Key Features)
- **Centralized Authentication**: 모든 애플리케이션의 인증을 중앙(Keycloak)에서 통합 관리합니다.
- **Session Management**: Redis를 사용하여 분산 환경에서도 안정적인 세션 관리를 제공합니다.
- **Header Injection**: 인증 성공 시 백엔드 서비스로 사용자 정보(`X-User`, `X-Email` 등)를 헤더에 담아 전달합니다.
- **SSL Support**: 사설 CA(`rootCA.pem`)를 신뢰하여 내부 HTTPS 통신을 지원합니다.

## 3. 기술 스택 (Tech Stack)
- **Image**: `quay.io/oauth2-proxy/oauth2-proxy:v7.13.0`
- **Session Store**: Redis 8.4.0 (Bookworm)
- **Monitoring**: Redis Exporter (Prometheus Metrics)

## 4. 아키텍처 및 워크플로우 (Architecture & Workflow)
### 인증 흐름 (Forward Auth 패턴)
1.  **사용자**가 보호된 서비스(`app.${DEFAULT_URL}`)에 접근.
2.  **Traefik**이 `sso-auth` 미들웨어 설정에 따라 **OAuth2 Proxy**에게 인증 검사 요청.
3.  **OAuth2 Proxy**는 쿠키를 확인하여 세션 유효성 검사.
    - **유효함**: 200 OK 응답 및 사용자 헤더 반환 -> Traefik이 요청을 백엔드로 전달.
    - **무효함**: 401 Unauthorized 응답 -> 사용자를 ID Provider(Keycloak) 로그인 페이지로 리다이렉트.
4.  **로그인 완료** 후 생성된 세션 정보는 **Redis**에 저장됨.

## 5. 시작 가이드 (Getting Started)
**실행 방법**:
```bash
docker compose up -d
```
> **필수 조건**: 실행 전 `env` 파일에 `OAUTH2_PROXY_CLIENT_SECRET`, `OAUTH2_PROXY_COOKIE_SECRET` 등이 올바르게 설정되어야 합니다.

## 6. 상세 사용 가이드 (Detailed Usage Guide)
### 6.1 설정 파일 관리
`config/oauth2-proxy.cfg` 파일에서 세부 동작을 제어합니다.
- `provider`: `keycloak-oidc`
- `oidc_issuer_url`: Keycloak의 Realm URL.
- `email_domains`: `*` (모든 이메일 도메인 허용).
- `cookie_domains`: `.host.docker.internal` (쿠키가 유효한 도메인 범위).

### 6.2 새로운 서비스 보호 적용
Traefik 레이블에 다음을 추가하여 보호를 적용합니다.
```yaml
labels:
  - "traefik.http.routers.your-service.middlewares=sso-auth@file"
```

## 7. 환경 설정 명세 (Configuration Reference)
### 환경 변수 (Environment Variables)
- `OAUTH2_PROXY_CLIENT_SECRET`: Keycloak에서 발급받은 Client Secret.
- `OAUTH2_PROXY_COOKIE_SECRET`: 쿠키 암호화를 위한 랜덤 시크릿 (16/24/32 bytes).
- `OAUTH2_PROXY_REDIS_CONNECTION_URL`: Redis 연결 문자열 (`redis://...`).
- `SSL_CERT_FILE`: `/etc/ssl/certs/rootCA.pem` (내부 TLS 통신 신뢰용).

### 네트워크 포트 (Ports)
- **HTTP**: 4180 (내부 통신용).
- **Metrics**: 9121 (Redis Exporter).

## 8. 통합 및 API 가이드 (Integration Guide)
**API Endpoints**:
- `/oauth2/start`: 로그인 플로우 시작.
- `/oauth2/callback`: OIDC 콜백 처리.
- `/oauth2/sign_out`: 로그아웃 및 세션 파기.
- `/oauth2/userinfo`: 현재 로그인한 사용자 정보 조회 (JSON).

## 9. 가용성 및 관측성 (Availability & Observability)
**Health Check**:
- **OAuth2 Proxy**: `/ping` 엔드포인트.
- **Redis**: `redis-cli ping` 및 내부 Healthcheck.

**Monitoring**:
- **Redis Exporter**: `oauth2-proxy-redis-exporter` 컨테이너가 9121 포트에서 Prometheus 메트릭을 제공합니다.

## 10. 백업 및 복구 (Backup & Disaster Recovery)
**Redis 데이터 백업**:
- 세션은 일시적인 데이터이므로 필수 백업 대상은 아닙니다.
- 그러나 `appendonly yes` 설정으로 재시작 시 세션이 유지되도록 구성되어 있습니다.

## 11. 보안 및 강화 (Security Hardening)
- **Secure Cookies**: `cookie_secure=true`, `cookie_httponly=true` 설정으로 쿠키 탈취를 방지합니다.
- **Short-lived Sessions**: 토큰 만료 시간을 적절히 설정하여 보안 위험을 최소화합니다.

## 12. 트러블슈팅 (Troubleshooting)
**자주 발생하는 문제**:
- **Cookie Domain Error**: "Cookie Not Found"와 유사한 에러 발생 시 `cookie_domains` 설정이 실제 접속 도메인과 일치하는지 확인하십시오.
- **500 Internal Error**: Redis 연결 실패가 주원인입니다. `oauth2-proxy-redis` 상태를 확인하세요.

---
**공식 문서**: [https://oauth2-proxy.github.io/oauth2-proxy/](https://oauth2-proxy.github.io/oauth2-proxy/)
