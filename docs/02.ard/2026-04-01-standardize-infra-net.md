# infra_net Standardization Architecture Reference Document (ARD)

## Overview (KR)

이 문서는 `hy-home.docker` 프로젝트의 공통 네트워크 인프라인 `infra_net`의 표준 아키텍처를 정의한다. 모든 서비스가 명시적인 고정 IP를 할당받고, 사전 정의된 서브넷 내에서 통신하도록 보장하는 기준을 제공한다.

## Summary

`infra_net`은 서비스 간 내부 통신을 위한 격리된 시스템 네트워크 레이어다. 기존의 동적 IP 할당 방식에서 탈피하여, 모든 서비스에 `172.19.0.0/16` 대역의 고정 IP를 부여함으로써 서비스 디스커버리의 안정성을 확보하고 네트워크 트러블슈팅을 용이하게 한다.

## Boundaries & Non-goals

- **Owns**:
  - `infra_net` 서브넷 설계 (`172.19.0.0/16`)
  - 서비스 그룹별 IP 주소 영역 정의
  - Docker Compose 파일 내 네트워크 정의 표준화
- **Consumes**:
  - Docker Engine Bridge Driver
  - Host OS IP Stack
- **Does Not Own**:
  - 외부 네트워크 (`k3d-hyhome`, `project_net`) 라우팅
  - 서비스별 포트 맵핑 정책
- **Non-goals**:
  - 모든 서비스의 외부 노출 (Traefik을 통한 L7 라우팅 권장)
  - 서브넷 외부의 IP 대역 강제

## Quality Attributes

- **Performance**: 고정 IP 사용으로 DNS 조기 해석 오버헤드 감소 및 직접 통신 최적화.
- **Security**: 내부망 격리를 통해 불필요한 포트 노출 차단.
- **Reliability**: 컨테이너 재시작 시에도 동일 IP 유지로 의존성 있는 서비스 간 연결성 보장.
- **Scalability**: `/16` 서브넷(65,534개 IP) 확보로 서비스 확장성 극대화.
- **Observability**: IP 기반 로그 분석 및 모니터링 일관성 확보.
- **Operability**: 명확한 IP 맵핑 테이블을 통해 네트워크 충돌 방지 및 관리 편의성 증대.

## System Overview & Context

모든 인프라 구성 요소(DB, Cache, Messaging, AI, Tooling)는 `infra_net`을 통해 상호 연결된다. 각 서비스는 논리적 그룹에 따라 특정 IP 대역을 할당받는다.

## Data Architecture

- **Key Entities / Flows**:
  - Gateway (Traefik) -> Services via `infra_net`
  - Auth (Keycloak) -> DB via `infra_net`
  - AI (Ollama) -> Vector DB (Qdrant) via `infra_net`
- **Storage Strategy**: N/A (Network Layer)
- **Data Boundaries**: `172.19.0.0/16` 서브넷 경계 내 통신.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Compose
- **Deployment Model**: Dictionary-based network definition with `ipv4_address`.
- **Operational Evidence**: `docker network inspect infra_net`.

## Related Documents

- **PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`
- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
- **ADR**: `[../03.adr/2026-04-01-standardize-infra-net.md]`
