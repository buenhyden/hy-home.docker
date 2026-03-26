<!-- Target: docs/04.specs/01-gateway/spec.md -->

# Gateway Tier (01-gateway) Technical Specification

## Overview (KR)

이 문서는 `01-gateway` 티어의 기술 설계와 구현 세부 사항을 정의하는 명세서다. Traefik과 Nginx의 하이브리드 구성에 필요한 구체적인 설정, 미들웨어 체인, 보안 제어 및 검증 방법을 기술한다.

## Strategic Boundaries & Non-goals

- **Owns**:
  - Traefik 정적/동적 설정 파일 (`traefik.yml`, `dynamic/*.yml`).
  - Nginx 프록시 구성 (`nginx.conf`).
  - TLS 인증서 바인딩 및 프로토콜 최적화.
- **Does Not Own**:
  - 인증서 자동 갱신 로직 (외부 스크립트 또는 Certbot 담당).
  - 백엔드 서비스의 헬스체크 구현 (개별 앱 담당).

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-26-01-gateway.md]`
- **ARD**: `[../../02.ard/0001-gateway-architecture.md]`
- **Related ADRs**: `[../../03.adr/0001-traefik-nginx-hybrid.md]`

## Contracts

- **Config Contract**:
  - Traefik Entrypoints: `web` (80), `websecure` (443), `neo4j-bolt` (7687), `metrics` (8082).
  - Traefik Providers: `docker`, `file` (/dynamic).
- **Security Contract**:
  - TLS: v1.2 min, v1.3 preferred.
  - ForwardAuth: `oauth2-proxy:4180/oauth2/auth`.
  - BasicAuth: Based on Docker secrets (`traefik_basicauth_password`).

## Core Design

### Component Boundary

- **Traefik (v3.6.8)**: 엣지 라우팅, TLS 종료, SSO 미들웨어 적용.
- **Nginx (Alpine)**: `/keycloak/`, `/minio/` 등 특수 경로의 헤더 조작 및 프록시 패스.

### Key Dependencies

- **Docker Socket**: `ro` 마운트를 통한 서비스 감지.
- **Shared Secrets**: `scripts/gen-secrets.sh`에 의해 생성된 인증서 및 패스워드 파일.

### Tech Stack

- Traefik v3.6.8
- Nginx Alpine
- TLS 1.2/1.3

## Data Modeling & Storage Strategy

- 게이트웨이는 전적으로 무상태(Stateless)로 운영됨.
- 구성 요소(Config)는 Git에 관리되며 배포 시 볼륨 마운트됨.

## Interfaces & Data Structures

### Traefik Middleware Contract (dashboard-auth)

```yaml
dashboard-auth:
  basicAuth:
    usersFile: "/run/secrets/traefik_basicauth_password"
```

## API Contract

Gateway의 통계 및 모니터링은 Prometheus 포맷을 따르며 별도 API Spec은 현재 불필요함. Traefik Dashboard는 내부 관리용으로만 노출됨.

## Verification

Required verification steps for Gateway tier.

```bash
# Traefik Ping (Health Check)
docker exec traefik traefik healthcheck --ping

# Nginx Config Test
docker exec nginx nginx -t

# TLS Protocol Check
openssl s_client -connect localhost:443 -tls1_3
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: 모든 HTTP 요청은 HTTPS로 301 리다이렉트되어야 함.
- **VAL-SPC-002**: Traefik Dashboard는 Basic Auth를 통해서만 접근 가능해야 함.
- **VAL-SPC-003**: OAuth2 Proxy 미들웨어가 적용된 경로는 미인증 시 로그인 페이지로 리다이렉트되어야 함.

## Related Documents

- **Plan**: `[../../05.plans/2026-03-26-01-gateway-standardization.md]`
- **Tasks**: `[../../06.tasks/2026-03-26-01-gateway-tasks.md]`
