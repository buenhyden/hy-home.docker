---
title: "Compose Network Segmentation Product Requirements"
version: "1.0.1"
type: "sdlc/requirement"
status: "approved"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "requirements"
artifact_id: "REQ-0023"
parent_ids: []
created: "2026-04-01"
---
# Compose Network Segmentation Product Requirements

## Problem and Goals

이 문서는 프로젝트 내 인프라 서비스의 Docker 네트워크 소속을 흐름 단위로 분리하고 각 네트워크의 서브넷을 보장하기 위한 제품 요구사항을 정의한다. 이를 통해 서비스 간 통신의 표준화와 예측 가능한 IP 관리를 실현한다.

### Problem Statement

여러 `docker-compose` 파일이 파편화되어 있고, 한때 모든 서비스가 단일 `infra_net` mesh를 공유해 서로 도달할 수 있었으며, 일부 서비스는 네트워크가 명시되어 있지 않거나 서브넷 설정이 모호할 수 있다. 이는 마이크로서비스 간의 통신 복잡도를 높이고 문제 해결 시 혼선이 발생할 수 있는 원인이 된다.

## Stakeholders and User Needs

인프라 서비스가 흐름 단위로 분리된 네트워크를 통해 안전하고 효율적으로 통신하며, 명확한 IP 대역 관리를 통해 네트워크 충돌을 방지하고 운영 투명성을 높인다.

### Personas

- **Infrastructure Engineer**: 전체 네트워크 구조를 관리하고 서비스 간 통신 문제를 해결해야 함.
- **DevOps Engineer**: 새로운 서비스를 추가할 때 표준 네트워크 환경을 보장받아야 함.

### Key Use Cases

- **STORY-01**: 관리자는 각 서비스가 실제 사용하는 상대와만 통신할 수 있도록 네트워크 경계를 보장받고 싶어 한다.
- **STORY-02**: 운영자는 각 network의 `10.250.x.0/24` 대역과 고정 주소 사용 여부를 예측 가능하게 관리하고 싶어 한다.
- **STORY-03**: 운영자는 사용하지 않는 외부 연동(k3d)이 Compose 서비스에 연결되어 있지 않기를 원한다.

## Functional Requirements

- **REQ-0023-FR-0001**: 모든 활성 서비스는 실제로 사용하는 상대가 있는 네트워크에만 연결되어야 하며, 상대가 없으면 프로젝트 기본 네트워크를 사용한다.
- **REQ-0023-FR-0002**: 각 네트워크의 서브넷은 root Compose에 `10.250.x.0/24`로 명시되어야 함.
- **REQ-0023-FR-0003**: 어떤 서비스도 `k3d-hyhome` 네트워크에 연결하지 않는다(2026-09-23 소유자 결정으로 k3d 연동 제거).

## Non-functional Requirements

No separately numbered non-functional requirement was identified in the source package.

## Interface Requirements

No separately numbered solution-independent external interface requirement was identified in the source package.

## Acceptance Criteria

- **REQ-0023-FR-0001**: `docker-compose config` 결과에서 각 서비스의 네트워크가 선언된 흐름과 일치함.
- **REQ-0023-FR-0002**: 각 네트워크의 IPAM 설정이 선언된 `10.250.x.0/24` 대역을 가리킴.

## Constraints

- **In Scope**:
  - 루트 `docker-compose.yml` 및 `include`된 모든 `docker-compose` 파일 수정.
  - 분리된 네트워크의 서브넷 표준화.
- **Out of Scope**:
  - repository가 소유하지 않는 네트워크(예: `project_net`, `k3d-hyhome`)의 서브넷 변경.
  - 컨테이너 내부 서비스 로직 수정.

### AI Agent Requirements

N/A

## Risks

- **Risks**: IP 충돌 가능성 (기존에 수동으로 할당된 IP가 있을 경우).
- **Dependencies**: Root `docker-compose.yml`의 `networks` 기본 정의에 의존.
- **Assumptions**: `docker compose` V2의 `include` 기능을 사용하여 설정이 병합됨.

## Traceability

- **Architecture Description**: [Compose network segmentation architecture description](../02.architecture/descriptions/0026-standardize-infra-net.md)
- **ADR**: [infra_net standardization decision (superseded single-mesh model)](../02.architecture/decisions/0026-standardize-infra-net.md)
- **Spec**: [infra_net technical specification](../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md)
- **Plan**: infra_net implementation plan
- **Task**: infra_net task evidence
