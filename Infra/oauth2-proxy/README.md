# OAuth2 Proxy Infrastructure

## 1. 개요 (Overview)
이 디렉토리는 Traefik의 ForwardAuth 미들웨어로 사용되는 OAuth2 Proxy를 정의합니다. Keycloak(OIDC)과 연동하여 통합 인증을 수행하며, 인증된 세션 정보를 Redis에 저장하여 관리합니다.

## 2. 포함된 도구 (Tools Included)

| 서비스명 | 역할 | 설명 |
|---|---|---|
| **oauth2-proxy** | Auth Middleware | HTTP 요청을 가로채 인증 여부를 확인하고, 인증되지 않은 경우 Keycloak 로그인 페이지로 리다이렉트합니다. |
| **oauth2-proxy-redis** | Session Store | 사용자 세션 쿠키 및 토큰 정보를 저장하는 Redis입니다. |
| **oauth2-proxy-redis-exporter** | Metrics Exporter | Redis 메트릭을 수집합니다. |

## 3. 구성 및 설정 (Configuration)

### 인증 흐름
1. 사용자가 보호된 서비스(예: `redisinsight.${DEFAULT_URL}`)에 접근
2. Traefik이 `sso-auth` 미들웨어를 통해 OAuth2 Proxy로 요청 전달
3. OAuth2 Proxy는 세션이 없으면 Keycloak으로 리다이렉트
4. 로그인 성공 후 OAuth2 Proxy가 세션을 Redis에 생성하고 원래 요청을 통과시킴

### 주요 설정
- **설정 파일**: `/etc/oauth2-proxy.cfg` (마운트됨)
- **Secrets**: `OAUTH2_PROXY_CLIENT_SECRET`, `OAUTH2_PROXY_COOKIE_SECRET`
- **SSL**: 사설 인증서(`rootCA.pem`)를 신뢰하도록 설정됨.

### 로드밸런싱 (Traefik)
- **Callback URL**: `https://auth.${DEFAULT_URL}`
- 이 라우터는 OAuth2 콜백(`redirect_url`)을 처리하는 엔드포인트입니다.
