# Traefik (리버스 프록시)

## 시스템 아키텍처에서의 역할

Traefik은 **동적 리버스 프록시 및 로드 밸런서**로 모든 인프라 서비스의 HTTPS 라우팅을 담당합니다. Docker 레이블 기반 자동 설정으로 서비스 디스커버리를 제공합니다.

**핵심 역할:**

- 🌐 **리버스 프록시**: HTTPS 라우팅 및 SSL/TLS 종료
- 🏷️ **동적 설정**: Docker 레이블 기반 자동 라우팅
- 🔒 **인증서 관리**: Let's Encrypt 또는 mkcert
- 🔐 **미들웨어**: OAuth2, BasicAuth, RateLimit

## 주요 구성 요소

### Traefik v3.6

- **컨테이너**: `traefik`
- **이미지**: `traefik:v3.6.2`
- **포트**:
  - HTTP: `${HTTP_HOST_PORT}:${HTTP_PORT}` (80)
  - HTTPS: `${HTTPS_HOST_PORT}:${HTTPS_PORT}` (443)
  - Dashboard: `${TRAEFIK_DASHBOARD_HOST_PORT}:${TRAEFIK_DASHBOARD_PORT}` (8080)
  - Metrics: `${TRAEFIK_METRICS_HOST_PORT}:${TRAEFIK_METRICS_PORT}` (8082)
- **Dashboard**: `https://dashboard.${DEFAULT_URL}`
- **IP**: 172.19.0.13

**설정 파일:**

- `./traefik.yml`: 메인 설정
- `./dynamic/*.yml`: 동적 라우팅, 미들웨어
- `./certs/`: TLS 인증서

## 환경 변수

```bash
HTTP_PORT=80
HTTP_HOST_PORT=80
HTTPS_PORT=443
HTTPS_HOST_PORT=443
TRAEFIK_DASHBOARD_PORT=8080
TRAEFIK_DASHBOARD_HOST_PORT=8080
TRAEFIK_METRICS_PORT=8082
TRAEFIK_METRICS_HOST_PORT=8082
DEFAULT_URL=127.0.0.1.nip.io
```

## 접속 정보

### Dashboard

- **URL**: `https://dashboard.127.0.0.1.nip.io`
- **인증**: BasicAuth (dynamic 설정)

## 주요 기능

### 1. 자동 라우팅 (Docker 레이블)

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myapp.rule=Host(`myapp.127.0.0.1.nip.io`)"
  - "traefik.http.routers.myapp.entrypoints=websecure"
  - "traefik.http.routers.myapp.tls=true"
  - "traefik.http.services.myapp.loadbalancer.server.port=8080"
```

### 2. 미들웨어

**OAuth2 인증 (sso-auth):**

```yaml
- "traefik.http.routers.myapp.middlewares=sso-auth@file"
```

**BasicAuth:**

```yaml
- "traefik.http.routers.myapp.middlewares=dashboard-auth@file"
```

### 3. SSL/TLS

- **mkcert**: 로컬 개발용 self-signed 인증서
- **Let's Encrypt**: 프로덕션용 자동 인증서

## 설정 파일

### traefik.yml

```yaml
entryPoints:
  web:
    address: ":80"
  websecure:
    address: ":443"

providers:
  docker:
    exposedByDefault: false
  file:
    directory: "/dynamic"
    watch: true

api:
  dashboard: true
```

### dynamic/middlewares.yml

```yaml
http:
  middlewares:
    sso-auth:
      forwardAuth:
        address: "http://oauth2-proxy:4180"
        trustForwardHeader: true
```

## 유용한 명령어

### 설정 검증

```bash
docker exec traefik traefik healthcheck
```

### 로그 확인

```bash
docker logs traefik -f
```

### 라우터 목록

- Dashboard에서 확인: `https://dashboard.127.0.0.1.nip.io`

## 참고 자료

- [Traefik 문서](https://doc.traefik.io/traefik/)
- [Docker Provider](https://doc.traefik.io/traefik/providers/docker/)
- [미들웨어](https://doc.traefik.io/traefik/middlewares/overview/)
