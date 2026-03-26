# 11-laboratory - Management & Laboratory Tier

## Overview

`11-laboratory` 계층은 시스템 관리, 리소스 시각화 및 실험적 도구들을 위한 통합 관리 환경을 제공한다. Homer 대시보드를 기반으로 모든 인프라 서비스에 대한 직관적인 접근 성능과 Portainer/RedisInsight를 통한 강력한 제어 기능을 제공한다.

## Architecture

### Component Diagram

```mermaid
graph TD
    subgraph "Access Layer"
        User[Admin/Developer]
        TF[Traefik Proxy]
    end

    subgraph "11-laboratory"
        Dash[Homer Dashboard]
        Port[Portainer]
        RI[RedisInsight]
    end

    subgraph "Downstream Infrastructure"
        DockerPool[Docker Engine]
        RedisPool[Valkey/Redis Cluster]
    end

    User --> TF
    TF -- "sso-auth" --> Dash
    TF -- "sso-auth" --> Port
    TF -- "sso-auth" --> RI

    Port -.-> DockerPool
    RI -.-> RedisPool
```

- **Homer**: 인프라 전용 서비스 진입점 대시보드.
- **Portainer**: 시각적 컨테이너 오케스트레이션 및 상태 관리.
- **RedisInsight**: 데이터 저장소(Valkey/Redis)의 데이터 탐색 및 성능 분석.

## Integration

### Upstream Dependencies

- **02-auth**: Keycloak SSO 연동을 통한 통합 인증 및 접근 제어.
- **01-gateway**: Traefik 리버스 프록시를 이용한 보안 라우팅.

### Downstream Consumers

- **Administrators**: 전체 인프라 상태 및 컨테이너 리소스 관리.
- **Developers**: 데이터베이스 조회 및 서비스 접근 경로 확인.

## Operations

### Deployment

```bash
# 개별 서비스 실행 (Homer 예시)
cd infra/11-laboratory/dashboard
docker compose up -d
```

### Key Ports

- **Dashboard**: `homer.${DEFAULT_URL}` (Port: 8080)
- **Container UI**: `portainer.${DEFAULT_URL}` (Port: 9443)
- **Data UI**: `redisinsight.${DEFAULT_URL}` (Port: 5540)

## Governance

### Standard Compliance

- **Architecture**: March 2026 "Thin Root" 규격을 준수한다.
- **Documentation**: [docs/README.md](../../docs/README.md) 기반의 Stage-Gate Taxonomy를 따른자.

### Related Documents

- [PRD](../../docs/01.prd/2026-03-26-11-laboratory.md)
- [ARD](../../docs/02.ard/0011-laboratory-architecture.md)
- [ADR](../../docs/03.adr/0011-laboratory-services.md)
- [Technical Spec](../../docs/04.specs/11-laboratory/spec.md)
