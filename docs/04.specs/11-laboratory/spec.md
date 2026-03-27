<!-- Target: docs/04.specs/11-laboratory/spec.md -->

# 11-laboratory Technical Specification (Spec)

## Overview (KR)

이 문서는 `11-laboratory` 계층의 기술 설계와 구현 계약을 정의하는 명세서다. 통합 대시보드, 컨테이너 관리 도구, 데이터베이스 조회 도구의 네트워크 구성 및 보안 설정을 구체화한다.

## Strategic Boundaries & Non-goals

- **Owns**: Service definition labels for Traefik, Docker socket integration, SSO middleware assignment.
- **Does Not Own**: Keycloak realm configuration, Traefik entrypoint definitions.

## Related Inputs

- **PRD**: `[../../01.prd/2026-03-26-11-laboratory.md]`
- **ARD**: `[../../02.ard/0011-laboratory-architecture.md]`
- **Related ADRs**: `[../../03.adr/0011-laboratory-services.md]`

## Contracts

- **Config Contract**: Services must be defined in `infra/11-laboratory/<service>/docker-compose.yml`.
- **Governance Contract**: Must include label `hy-home.tier: admin`.

## Core Design

### 1. Homer (Dashboard)
- **Image**: `b4bz/homer`
- **Internal Port**: 8080
- **Volume**: `./config:/www/assets`

### 2. Portainer (Orchestration UI)
- **Image**: `portainer/portainer-ce:sts`
- **Internal Port**: 9443
- **Volume**: `/var/run/docker.sock:/var/run/docker.sock`

### 3. RedisInsight (Data Ops)
- **Image**: `redis/redisinsight:3.0.3`
- **Internal Port**: 5540
- **Network**: `infra_net`

### 4. Dozzle (Log Viewer)
- **Image**: `amir20/dozzle:v10.2.0`
- **Internal Port**: 8080
- **Volume**: `/var/run/docker.sock:/var/run/docker.sock`

## Interfaces & Data Structures

### Traefik Label Contract (Example)
```yaml
labels:
  hy-home.tier: admin
  traefik.enable: 'true'
  traefik.http.routers.dozzle.rule: Host(`dozzle.${DEFAULT_URL}`)
  traefik.http.routers.dozzle.entrypoints: websecure
  traefik.http.routers.dozzle.tls: 'true'
  traefik.http.routers.dozzle.middlewares: sso-errors@file,sso-auth@file
```

## Verification

```bash
# Check if services are running
docker compose -f infra/11-laboratory/dozzle/docker-compose.yml ps
# Verify Traefik accessibility
curl -Ik https://dozzle.${DEFAULT_URL}
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: All services must return 302/401 when accessed without a valid SSO session.
- **VAL-SPC-002**: Portainer and Dozzle must correctly display the local Docker engine's resources.

## Related Documents

- **Plan**: `[../../05.plans/2026-03-26-11-laboratory-standardization.md]`
- **Tasks**: `[../../06.tasks/2026-03-26-11-laboratory-tasks.md]`
