# infra_net Architecture Reference Document

## Overview (KR)

이 문서는 프로젝트의 인프라 네트워크(`infra_net`)에 대한 참조 아키텍처와 품질 속성을 정의한다. 시스템 내 각 서비스가 어떻게 네트워크적으로 격리되거나 연결되는지, 그리고 IP 관리 전략은 무엇인지 정리한다.

## Summary

`infra_net`은 모든 인프라 관련 서비스(데이터베이스, 인증, 메시지 브로커, 모니터링 등)가 통신하는 핵심 가상 네트워크다. 중앙 집중식 네트워크 관리를 통해 서비스 간의 연결성을 보장하고, 고정 서브넷을 통해 예측 가능한 호스트 통신을 가능하게 한다.

## Boundaries & Non-goals

- **Owns**:
  - `infra_net` 네트워크 정의 및 서브넷 할당 (`172.19.0.0/16`).
  - 브리지 드라이버 수준의 네트워크 격리와 라우팅.
- **Consumes**:
  - Docker Compose의 네트워크 추상화 레이어.
  - 시스템 리소스 (IPAM 엔진).
- **Does Not Own**:
  - `project_net`, `k3d-hyhome` 등 다른 외부 네트워크의 상세 설정 (단, 연결성은 유지).
  - 클라우드 VPC나 물리적 방화벽 설정.
- **Non-goals**:
  - 동적 IP 주소 관리 (Static IP 위주의 관리 지향).
  - 네트워크 단에서의 트래픽 패킷 필터링 (이는 서비스 레벨에서 관리).

## Quality Attributes

- **Performance**: 브리지 모드에서 오버헤드를 최소화하고 지연 시간을 1ms 이내로 유지.
- **Security**: 외부 네트워크로부터의 무분별한 접근을 차단하고, 게이트웨이(Traefik)를 통해서만 노출되도록 구성.
- **Reliability**: 단일 장애 지점이 아닌 전체 환경에서의 일관된 연결성 제공.
- **Scalability**: `/16` 서브넷(65,534개 IP)을 사용하여 장기적인 서비스 확장 수용.
- **Observability**: Docker 네트워크 로그와 연동하여 트래픽 존재 여부 확인 가능.
- **Operability**: 명확한 IP 스키마(Static IP)를 제공하여 운영 시 주소 예측 가능성 제공.

## System Overview & Context

모든 서비스는 `docker-compose.yml`의 `include` 기능을 통해 개별적으로 정의되지만, 런타임 시점에는 모두 `infra_net`에 합쳐져 하나의 클러스터처럼 동작한다. IPAM(IP Address Management)은 루트 파일에서 전역적으로 정의한다.

## Data Architecture

- **Key Entities / Flows**:
  - **Service Discovery**: Docker 내부 DNS를 통해 서비스명을 IP로 해결.
  - **Static IP Mapping**: 일부 핵심 서비스(Traefik, DB)는 하드코딩된 IP를 사용하여 참조 편의성을 높임.
- **Storage Strategy**: 네트워크 자체는 상태가 없으나, IP 할당 정보는 Compose 상태 파일에서 관리.

## Infrastructure & Deployment

- **Runtime / Platform**: Docker Engine (Linux).
- **Deployment Model**: Infrastructure as Code (Docker Compose).
- **Operational Evidence**: `docker network inspect infra_net` 결과를 통해 검증 가능.

## Related Documents

- **PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`
- **ADR**: `[../03.adr/0026-standardize-infra-net.md]`
- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
- **TASK**: `[../06.tasks/2026-04-01-standardize-infra-net.md]`
