# Traefik Guide

> Detailed guide for managing and understanding the Traefik Edge Router in the hy-home.docker ecosystem.

---

## Overview (KR)

이 문서는 Traefik 에지 라우터에 대한 가이드다. `hy-home.docker` 클러스터 내부에서 동적 서비스 탐색, TLS 종료, 그리고 미들웨어 설정을 이해하고 관리할 수 있도록 단계별 절차와 주요 개념을 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Infrastructure Operators
- Backend Developers
- AI Agents

## Purpose

이 가이드는 사용자가 Traefik의 작동 방식을 이해하고, 새로운 서비스를 관문에 등록하며, 기존 설정을 유지보수하는 것을 돕는다.

## Prerequisites

- Docker 및 Docker Compose 설치
- `infra_net` 네트워크 생성 확인
- SSL 인증서 (`/certs` 볼륨에 위치)

## Step-by-step Instructions

### 1. New Service Registration
새로운 서비스를 Traefik에 등록하려면 해당 서비스의 `docker-compose.yml`에 다음과 같은 라벨을 추가한다:

```yaml
labels:
  traefik.enable: "true"
  traefik.http.routers.my-app.rule: "Host(`app.${DEFAULT_URL}`)"
  traefik.http.routers.my-app.entrypoints: "websecure"
  traefik.http.routers.my-app.tls: "true"
  traefik.http.services.my-app.loadbalancer.server.port: "8080"
```

### 2. Applying Shared Middlewares
`dynamic/middleware.yml`에 정의된 공통 미들웨어(예: SSO)를 적용하려면 라벨에 추가한다:

```yaml
labels:
  traefik.http.routers.my-app.middlewares: "sso-auth@file"
```

### 3. Monitoring via Dashboard
Traefik 대시보드는 `dashboard.${DEFAULT_URL}`에서 접근 가능하다. 상호 요약 정보와 라우팅 규칙의 상태를 실시간으로 확인할 수 있다.



## Common Pitfalls

- **Network Mismatch**: 서비스가 `infra_net` 외부에서 실행되면 Traefik이 백엔드에 접근할 수 없다 (504 Gateway Timeout 발생).
- **Certificate Path**: `dynamic/tls.yaml`의 경로가 실제 컨테이너 내부의 `/certs` 위치와 다를 경우 SSL 오류가 발생한다.
- **Label Typo**: 라벨 이름에 오타가 있으면 Traefik이 서비스를 무시한다.

## Related Documents

- **Spec**: `[../04.specs/01-gateway/traefik.md]`
- **Operation**: `[../08.operations/01-gateway/traefik.md]`
- **Runbook**: `[../09.runbooks/01-gateway/traefik.md]`
