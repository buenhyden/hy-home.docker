# OAuth2-Proxy (인증 프록시)

## 시스템 아키텍처에서의 역할

OAuth2-Proxy는 **Forward Auth 미들웨어**로 Traefik과 통합되어 서비스에 Keycloak SSO 인증을 적용합니다.

**핵심 역할:**

- 🔐 **인증 게이트웨이**: 서비스 앞단 인증
- 🎫 **토큰 검증**: OIDC 토큰 유효성 확인
- 🔄 **세션 관리**: 쿠키 기반 세션
- 🚪 **리다이렉트**: 로그인/로그아웃 흐름

## 주요 구성 요소

### OAuth2-Proxy

- **컨테이너**: `oauth2-proxy`
- **이미지**: `quay.io/oauth2-proxy/oauth2-proxy:v7.13.0`
- **포트**: `${OAUTH2_PROXY_PORT}` (기본 4180)
- **Traefik**: `https://auth.${DEFAULT_URL}`

**설정 파일:**

- `./oauth2-proxy.cfg`: 메인 설정

## 환경 변수

```bash
OAUTH2_PROXY_PORT=4180
OAUTH2_PROXY_CLIENT_ID=nginx-client
OAUTH2_PROXY_CLIENT_SECRET=<keycloak_secret>
OAUTH2_PROXY_PROVIDER=keycloak-oidc
OAUTH2_PROXY_OIDC_ISSUER_URL=https://keycloak.hy-home.local/realms/hy-home.realm
DEFAULT_URL=hy-home.local
```

## 설정 파일

### oauth2-proxy.cfg

```ini
http_address = "0.0.0.0:4180"
upstreams = [ "static://200" ]
email_domains = [ "*" ]
cookie_secret = "<random_32_bytes>"
cookie_secure = true
cookie_domains = [ ".hy-home.local" ]

provider = "keycloak-oidc"
client_id = "nginx-client"
client_secret = "<secret>"
oidc_issuer_url = "https://keycloak.hy-home.local/realms/hy-home.realm"
redirect_url = "https://auth.hy-home.local/oauth2/callback"
```

## Traefik 통합

### 미들웨어 정의 (dynamic/middlewares.yml)

```yaml
http:
  middlewares:
    sso-auth:
      forwardAuth:
        address: "http://oauth2-proxy:4180"
        trustForwardHeader: true
        authResponseHeaders:
          - "X-Auth-Request-User"
          - "X-Auth-Request-Email"
```

### 서비스에 적용

```yaml
labels:
  - "traefik.http.routers.myapp.middlewares=sso-auth@file"
```

## 참고 자료

- [OAuth2-Proxy 문서](https://oauth2-proxy.github.io/oauth2-proxy/)
- [Keycloak 통합](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc)
