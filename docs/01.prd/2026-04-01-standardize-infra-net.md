# Product Requirements Document

## Standardize `infra_net` Network Requirements

## Overview (KR)

이 문서는 프로젝트 내 모든 인프라 서비스들을 `infra_net` 네트워크에 통합하고 구체적인 서브넷(`172.19.0.0/16`)을 보장하기 위한 제품 요구사항을 정의한다. 이를 통해 서비스 간 통신의 표준화와 예측 가능한 IP 관리를 실현한다.

## Vision

모든 인프라 서비스가 단일 표준 네트워크(`infra_net`)를 통해 안전하고 효율적으로 통신하며, 명확한 IP 대역 관리를 통해 네트워크 충돌을 방지하고 운영 투명성을 높인다.

## Problem Statement

현재 여러 `docker-compose` 파일들이 파편화되어 있으며, 일부 서비스는 `infra_net`에 명시적으로 연결되어 있지 않거나 서브넷 설정이 모호할 수 있다. 이는 마이크로서비스 간의 통신 복잡도를 높이고 문제 해결 시 혼선이 발생할 수 있는 원인이 된다.

## Personas

- **Infrastructure Engineer**: 전체 네트워크 구조를 관리하고 서비스 간 통신 문제를 해결해야 함.
- **DevOps Engineer**: 새로운 서비스를 추가할 때 표준 네트워크 환경을 보장받아야 함.

## Key Use Cases

- **STORY-01**: 관리자는 모든 인프라 서비스가 `infra_net` 내에서 서로 통신할 수 있음을 보장받고 싶어 한다.
- **STORY-02**: 운영자는 `172.19.0.0/16` 대역을 통해 각 서비스의 IP를 예측 가능하게 관리하고 싶어 한다.
- **STORY-03**: 기존에 설정된 `k3d-hyhome` 네트워크 연결은 그대로 유지되어 로컬 k3s 클러스터와의 연동이 중단되지 않아야 한다.

## Functional Requirements

- **REQ-PRD-FUN-01**: `docker-compose.yml`에 포함된 모든 활성 서비스는 `infra_net` 네트워크를 사용해야 함.
- **REQ-PRD-FUN-02**: `infra_net`의 서브넷은 반드시 `172.19.0.0/16`으로 정의되어야 함.
- **REQ-PRD-FUN-03**: 기존에 정의된 `k3d-hyhome` 네트워크 설정은 수정하거나 삭제하지 않고 유지함.

## Success Criteria

- **REQ-PRD-MET-01**: 모든 서비스가 `docker-compose config` 실행 시 `infra_net`을 포함하고 있음.
- **REQ-PRD-MET-02**: `infra_net` 네트워크의 IPAM 설정이 `172.19.0.0/16` 대역을 가리킴.

## Scope and Non-goals

- **In Scope**:
  - 루트 `docker-compose.yml` 및 `include`된 모든 `docker-compose` 파일 수정.
  - `infra_net` 서브넷 표준화.
- **Out of Scope**:
  - `infra_net` 이외의 다른 네트워크(예: `project_net`)의 서브넷 변경.
  - 컨테이너 내부 서비스 로직 수정.

## Risks, Dependencies, and Assumptions

- **Risks**: IP 충돌 가능성 (기존에 수동으로 할당된 IP가 있을 경우).
- **Dependencies**: Root `docker-compose.yml`의 `networks` 기본 정의에 의존.
- **Assumptions**: `docker compose` V2의 `include` 기능을 사용하여 설정이 병합됨.

## Related Documents

- **ARD**: `[../02.ard/0026-standardize-infra-net.md]`
- **ADR**: `[../03.adr/0026-standardize-infra-net.md]`
- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
- **Task**: `[../06.tasks/2026-04-01-standardize-infra-net.md]`
