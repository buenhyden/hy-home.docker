<!-- Target: docs/02.ard/0001-gateway-architecture.md -->

# Gateway Tier Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `hy-home.docker` 시스템의 통합 진입점인 Gateway 티어의 아키텍처를 정의한다. Traefik과 Nginx의 하이브리드 구성을 통해 동적 서비스 발견과 정교한 경로 라우팅을 동시에 달성하는 구조를 설명한다.

## Summary

Gateway 티어는 외부 네트워크와 내부 서비스 네트워크 사이의 유일한 통로 역할을 수행한다. Traefik은 엣지 라우터로서 TLS 종료 및 컨테이너 자동 발견을 담당하고, Nginx는 특정 레거시 호환 및 특수 경로 처리를 위한 보조 프록시로 동작한다.

## Boundaries & Non-goals

- **Owns**:
  - 외부 Ingress 트래픽 수신 (Port 80, 443, 7687).
  - TLS/SSL 인증서 적용 및 종료.
  - 내부 서비스로의 트래픽 라우팅 및 부하 분산.
  - 보안 미들웨어 (Rate Limit, IP Allow List, Auth Integration).
- **Consumes**:
  - Docker Socket (Service Discovery).
  - Local Certificates (SSL/TLS).
  - OAuth2 Proxy (Authentication request).
- **Does Not Own**:
  - 개별 마이크로서비스의 내부 비즈니스 로직.
  - 데이터베이스 직접 연결 및 관리.
  - Identity Provide (Keycloak 내부 관리).
- **Non-goals**:
  - 모든 트래픽의 상세 페이로드 로깅 (관찰성 티어에서 샘플링 처리).
  - 서비스 메시(Service Mesh) 수준의 복잡한 동적 제어 (현재는 단순 Ingress 위주).

## Quality Attributes

- **Performance**: Traefik의 Go 기반 비동기 처리를 통해 낮은 지연 시간 보장. Nginx의 캐싱 기능을 활용한 정적 자원 최적화.
- **Security**: TLS 1.3 우선 적용, HSTS 강제화, 리퀘스트 크기 제한, 인증(SSO) 통합.
- **Reliability**: Health Check를 통한 비정상 타겟 자동 제외. Docker Provider 기반의 Self-healing 라우팅.
- **Scalability**: Docker 레이블만으로 신규 서비스 수평 확장 및 라우팅 추가 가능.
- **Observability**: Prometheus 메트릭 노출, OpenTelemetry(Tempo)를 통한 분산 트레이싱 연동.
- **Operability**: Traefik Dashboard를 통한 실시간 라우팅 가시성 확보. 파일 기반 동적 설정 지원.

## System Overview & Context

Gateway는 `infra_net` 독커 네트워크의 핵심 노드로 작동한다. 외부 IP(또는 도메인)로 들어오는 모든 요청은 Traefik을 거치며, 설정된 규칙에 따라 직접 백엔드 컨테이너로 가거나 Nginx 프록시를 거쳐 특수 처리가 이루어진 후 전달된다.

## Data Architecture

- **Key Entities / Flows**:
  - `Internet -> Traefik (TLS Term) -> Service Container`
  - `Internet -> Traefik (TLS Term) -> Nginx (Path Rewrite) -> Keycloak/MinIO`
- **Storage Strategy**: 무상태(Stateless) 아키텍처를 지향하며, 설정 파일과 인증서는 볼륨 마운트를 통해 공급받는다.
- **Data Boundaries**: 게이트웨이는 요청의 메타데이터(Header, Path)를 수정하거나 전달할 뿐, 요청 바디를 영구 저장하지 않는다.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose / Linux Alpine 기반 컨테이너.
- **Deployment Model**: `infra/01-gateway` 폴더 내부의 정의에 따라 독립적인 스택으로 배포.
- **Operational Evidence**: Traefik Dashboard (`dashboard.DEFAULT_URL`), `docker logs traefik`, Prometheus Metrics.

## Related Documents

- **PRD**: `[../01.prd/2026-03-26-01-gateway.md]`
- **Spec**: `[../04.specs/01-gateway/spec.md]`
- **Plan**: `[../05.plans/2026-03-26-01-gateway-standardization.md]`
- **ADR**: `[../03.adr/0001-traefik-nginx-hybrid.md]`
