<!-- Target: docs/03.adr/0001-traefik-nginx-hybrid.md -->

# ADR-0001: Traefik & Nginx Hybrid Gateway Architecture

## Overview (KR)

이 문서는 `hy-home.docker`의 진입점(Ingress)으로 Traefik과 Nginx를 혼합하여 사용하는 결정에 대한 아키텍처 결정 기록이다.

## Context

- 시스템에는 Docker 컨테이너 기반으로 동적으로 수량이 변하는 다수의 마이크로서비스가 존재함.
- 동시에 Keycloak, MinIO와 같이 특정 경로(Path) 재작성 및 복잡한 헤더 조작이 필요한 인프라 서비스들이 존재함.
- Traefik은 Docker Label 기반의 자동 서비스 발견(Dynamic Discovery)에 매우 강력하지만, 복잡한 Nginx 수준의 세밀한 경로 제어는 설정이 다소 번거로울 수 있음.
- 반면 Nginx는 정교한 설정이 가능하지만, 동적으로 변하는 Docker 가상 IP 환경에서 업스트림 관리가 수동적이거나 별도의 솔루션이 필요함.

## Decision

- **Primary Edge Router**: Traefik v3를 사용함.
  - 모든 외부 트래픽(80, 443)의 최초 수신 및 TLS 종료 담당.
  - Docker Provider를 통한 대다수 서비스의 자동 라우팅 처리.
- **Secondary Path Proxy**: Nginx Alpine을 사용함.
  - Traefik이 처리하기 복잡한 특정 경로(예: `/keycloak/`, `/minio/`)를 Traefik의 백엔드 서비스로 등록.
  - Nginx 내부에서 상세한 Proxy Pass, Header 조작, Buffering 설정을 수행.
- **Service Flow**: `Client -> Traefik (Edge) -> Nginx (Specialized) -> Backend Service`.

## Explicit Non-goals

- 모든 내부 서비스 앞에 Nginx를 두는 방식 (불필요한 홉 증가 방지).
- Nginx를 외부 Edge로 직접 노출하는 방식.

## Consequences

- **Positive**:
  - 신규 서비스 추가 시 별도 설정 없이 Docker Label만으로 라우팅 가능 (Traefik의 장점).
  - Keycloak 등 까다로운 프록시 설정이 필요한 서비스에 대해 안정적인 Nginx 설정 적용 가능.
  - 통합 대시보드를 통한 가시성 확보.
- **Trade-offs**:
  - 특정 서비스에 대해 네트워크 홉(Hop)이 하나 추가됨 (Traefik -> Nginx).
  - 두 종류의 프록시 설정 문법을 모두 관리해야 하는 운영 부담.

## Alternatives

### [Alternative 1: Traefik Only]

- Good: 아키텍처가 단순해지고 관리 포인트가 줄어듬.
- Bad: Keycloak의 redirect loop 문제나 MinIO의 특수한 헤더 처리를 Traefik 미들웨어만으로 구현하기가 상대적으로 복잡하고 검증 사례가 적음.

### [Alternative 2: Nginx Only (with Nginx Proxy Manager 등)]

- Good: 설정이 매우 강력하고 친숙함.
- Bad: 순수 Nginx 사용 시 Docker 컨테이너의 동적 변화를 감지하기 위해 `jwilder/nginx-proxy` 같은 추가 도구가 필요하거나 수동 관리가 필요함.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-01-gateway.md]`
- **ARD**: `[../02.ard/0001-gateway-architecture.md]`
- **Related Spec**: `[../04.specs/01-gateway/spec.md]`
