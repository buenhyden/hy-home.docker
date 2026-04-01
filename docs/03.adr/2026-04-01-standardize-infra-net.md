# ADR-2026-04-01-01: Standardized Dictionary-Based Network Infrastructure

## Overview (KR)

이 문서는 모든 Docker Compose 서비스의 `infra_net` 설정을 딕셔너리 기반의 고정 IP 할당 방식(`ipv4_address`)으로 표준화하기 위한 결정 사항을 기록한다.

## Context

그동안 일부 서비스들이 단순 리스트 형태(`- infra_net`)의 네트워크 설정을 사용하여 동적 IP를 할당받거나, 딕셔너리 형태 내에서도 불일치하는 IP 대역을 사용하는 문제가 있었다. 이는 컨테이너 재시작 시 IP가 변경되어 특정 서비스 간 통신 장애를 유발하고 네트워크 관리를 복잡하게 만들었다.

## Decision

모든 서비스 구성에서 다음 규칙을 준수하도록 강제한다.

- `networks:` 섹션 하위에서 `infra_net:`은 반드시 딕셔너리 형태로 사용함.
- `ipv4_address:` 속성을 통해 `172.19.0.0/16` 서브넷 내 고정 IP를 부여함.
- 서비스 성격에 따라 정의된 IP 그룹(Lake, NoSQL, Tooling 등)을 따름.

## Explicit Non-goals

- `k3d-hyhome` 브릿지 네트워크 설정을 고정 IP로 변경하는 것 (외부 관리는 기존 유지).
- 모든 포트의 Host 노출화.

## Consequences

- **Positive**:
  - 일관된 서비스 주소 체계 확보.
  - 컨테이너 재시작 후에도 서비스 연결성 보장.
  - 가시성 있는 IP 관리 테이블 운영 가능.
- **Trade-offs**:
  - IP 충돌 가능성에 대한 사전 대역 관리 오버헤드 발생.
  - Compose 파일의 줄 수가 다소 증가함.

## Alternatives

### Alternative 1: Dynamic DNS (Docker Internal DNS)

- Good: 자동 관리로 인해 충돌 방지 필요 없음.
- Bad: 특정 커스텀 이미지나 특수한 네트워크 환경 내에서 해석 지연 및 불안정성 발생 가능.

### Alternative 2: External IPAM Service

- Good: 독립적인 전담 관리 툴 사용으로 전문성 향상.
- Bad: 소규모 로컬 개발 환경(docker-compose)에서 과도한 구성 및 복잡도 증가.

## Related Documents

- **PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`
- **ARD**: `[../02.ard/2026-04-01-standardize-infra-net.md]`
- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **Plan**: `[../05.plans/2026-04-01-standardize-infra-net.md]`
