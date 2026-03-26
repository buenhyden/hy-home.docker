<!-- Target: docs/04.specs/11-laboratory/spec.md -->

# Laboratory Tier Technical Specification

## Technical Specification

## Overview (KR)
이 문서는 `11-laboratory` 계층의 기술 사양을 정의한다. 통합 대시보드, 컨테이너 관리 도구, 데이터베이스 조회 도구의 네트워크 구성 및 보안 설정을 포함한다.

## Components

### 1. Homer (Dashboard)
- **Role**: 인프라 서비스 내비게이션 게이트웨이.
- **Configuration**: `/www/assets/config.yml`을 통한 정적 서비스 매핑.
- **Endpoint**: `homer.${DEFAULT_URL}`

### 2. Portainer (Orchestration UI)
- **Role**: Docker 엔진 리소스 관리.
- **Security**: `/var/run/docker.sock` 마운트를 통한 로컬 소켓 통신.
- **Endpoint**: `portainer.${DEFAULT_URL}`

### 3. RedisInsight (Data Ops)
- **Role**: Redis 클러스터 모니터링 및 데이터 조회.
- **Connection**: `infra_net` 가상 네트워크를 통해 `04-data` 티어의 Redis 노드에 접속.
- **Endpoint**: `redisinsight.${DEFAULT_URL}`

## Interface Definition

### Network Ports
| Service | Internal Port | External Port (Traefik) | Protocol | Auth |
| :--- | :--- | :--- | :--- | :--- |
| Homer | 8080 | 443 (websecure) | HTTP | SSO |
| Portainer | 9443 | 443 (websecure) | HTTPS/TCP | SSO |
| RedisInsight | 5540 | 443 (websecure) | HTTP | SSO |

## Security & Compliance

- **SSO Integration**: 모든 대시보드 서비스는 Traefik 미들웨어(`sso-auth`)를 경유하며, Keycloak에서 인증된 세션이 없을 경우 접근이 차단됨.
- **Labeling Policy**: `hy-home.tier: admin` 레이블을 부여하여 인프라 관리 서비스임을 명시함.
- **Data Persistence**: Portainer와 RedisInsight는 바인드 마운트 볼륨을 사용하여 설정 정보를 영구 보관함.

## Related Documents
- **PRD**: [2026-03-26-11-laboratory.md](../../01.prd/2026-03-26-11-laboratory.md)
- **ARD**: [0011-laboratory-architecture.md](../../02.ard/0011-laboratory-architecture.md)
- **ADR**: [0011-laboratory-services.md](../../03.adr/0011-laboratory-services.md)
