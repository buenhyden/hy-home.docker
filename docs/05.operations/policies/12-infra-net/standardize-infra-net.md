---
status: active
---

<!-- Target: docs/05.operations/policies/12-infra-net/standardize-infra-net.md -->

# infra_net IP Management Operations Policy

## Overview

이 문서는 `hy-home.docker` 시스템의 네트워크 레이어인 `infra_net` 내 IP 할당 및 관리 정책을 정의한다. IP 충돌 방지 및 일관성 유지를 위한 통제 기준을 제공한다.

## Policy Scope

이 정책은 `infra_net` 브릿지 네트워크에 연결된 모든 Docker 컨테이너의 IP 할당 방식을 관할한다.

- **Systems**: `hy-home.docker` 기반 모든 서비스.
- **Agents**: 모든 인프라 관리 에이전트.
- **Environments**: Local (k3d/docker-compose) 및 Production (Future) 개발/운영 환경.

## Controls

- **Required**:
  - 모든 서비스의 `networks` 항목에 `ipv4_address` 속성 필수 부여.
  - 지정된 그룹별 IP 대역(Lake: 140-149, Tooling: 220-249 등) 내 할당.
- **Allowed**:
  - 그룹별 여유 공간 활용한 신규 서비스 추가.
  - 일시적인 테스트 목적의 유동 IP 할당 (단, 수동 고정으로 머지 필수).
- **Disallowed**:
  - 중복된 IP 할당 (Compose 파일 병합 단계에서 검증 필수).
  - 외부망 주소와의 브릿징 설정 수동 수정.

## Exceptions

- **K3d-hyhome Compatibility**: `k3d-hyhome` 네트워크는 마스터 노드 및 외부 게이트웨이 영역과의 호환성을 위해 기존 IP 체계를 예외적으로 유지하거나 별도 할당 방식을 적용할 수 있음.

## Verification

- `bash scripts/validation/validate-docker-compose.sh`를 통한 root compose 구조 검증.
- 변경한 tier profile은 `HYHOME_COMPOSE_PROFILES`로 지정해 동일 검증을 반복한다.
- `rg -n "ipv4_address:|infra_net:" infra docker-compose.yml`를 통한 고정 IP와 network 선언 상태 확인.
- 실행 중인 승인된 환경에서는 `docker network inspect infra_net` 결과를 authoritative mapping과 비교한다.

## Review Cadence

- **Monthly**: authoritative mapping table과 현재 Compose 파일 사이의 실태를 점검한다.
- **On material change**: 신규 서비스, static IP 변경, profile include 변경, network gateway 변경 시 즉시 재검토한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/12-infra-net/standardize-infra-net.md)
- [Recovery runbook](../../runbooks/12-infra-net/standardize-infra-net.md)
- [infra_net spec](../../../03.specs/standardize-infra-net/spec.md)
