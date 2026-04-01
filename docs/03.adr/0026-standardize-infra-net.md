# ADR-20260401: Standardize `infra_net` Subnet

## Overview (KR)

이 문서는 모든 인프라 서비스용 네트워크(`infra_net`)의 서브넷을 `172.19.0.0/16`으로 표준화하기로 한 결정에 대한 기록이다.

## Context

현재 여러 Docker Compose 파일이 `include`되면서 각각 개별적인 네트워크 설정을 가질 수 있는 위험이 있다. 특히 인프라 전반에서 사용하는 `infra_net`의 대역이 불명확하거나 충돌할 경우 서비스 간 통신 장애나 IP 관리의 어려움이 발생한다. 따라서 모든 인프라 서비스가 동일한 가상 네트워크 평면에서 동작하도록 강제할 필요가 있다.

## Decision

- **결성 사항 1**: 루트 `docker-compose.yml`에서 `infra_net`의 서브넷을 `${INFRA_SUBNET:-172.19.0.0/16}`으로 고정 정의한다.
- **결정 사항 2**: `include`되는 모든 개별 설정 파일의 서비스에 `infra_net`을 명시적으로 선언한다.
- **결정 사항 3**: 서비스가 이미 `k3d-hyhome` 등 다른 네트워크에 연결되어 있을 경우, 이를 제거하지 않고 `infra_net`을 추가하는 방식으로 구성한다.

## Explicit Non-goals

- 사용자 애플리케이션용 네트워크(`project_net`)의 서브넷 변경은 포함하지 않는다.
- 데이터베이스 클러스터 내부의 전용 인터커넥트 네트워크 구성 방식 변경은 다루지 않는다.

## Consequences

- **Positive**:
  - 예측 가능한 IP 대역 관리 (`172.19.0.0/16`).
  - 서비스 간 통신 시 DNS 및 IP 참조의 안정성 확보.
- **Trade-offs**:
  - 서브넷이 겹치는 다른 로컬 네트워크 환경과의 충돌 가능성이 미세하게 존재할 수 있음.

## Alternatives

### 대안 1: Docker Default Bridge (Automatic CIDR)

- Good: 별도의 설정 없이 Docker가 알아서 할당함.
- Bad: 서비스 배치 순서에 따라 IP가 바뀌어 Static IP 기반의 설정이 불가능함.

## Related Documents

- **PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`
- **ARD**: `[../02.ard/0026-standardize-infra-net.md]`
- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
