# Standardize `infra_net` Implementation Plan

## Overview (KR)

이 문서는 모든 인프라 서비스에 `infra_net` 네트워크를 적용하고 서브넷을 `172.19.0.0/16`으로 표준화하기 위한 구체적인 실행 계획을 정의한다. 문서화, 구현, 검증의 3단계로 진행한다.

## Context

인프라 서비스 간의 통신 표준을 확립하고, IP 관리의 복잡도를 낮추기 위해 개별적으로 운영되던 네트워크 설정을 `infra_net`으로 통합한다.

## Goals & In-Scope

- **Goals**:
  - 모든 활성 인프라 서비스의 `infra_net` 연결.
  - `172.19.0.0/16` 서브넷 강제.
  - 기존 `k3d-hyhome` 설정 유지.
- **In Scope**: `docker-compose.yml` 및 하위 21개 `include` 파일 수정.

## Non-Goals & Out-of-Scope

- **Non-goals**: 서비스 포트 변경이나 내부 로직 수정.
- **Out of Scope**: 클러스터 외부(Host) 네트워크 설정 변경.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | SSoT 문서 작성 (9개 폴더) | `docs/01-09/` | REQ-GOV | 모든 템플릿 준수 및 링크 완료 |
| PLN-002 | 루트 Compose 네트워크 정의 수정 | `docker-compose.yml` | REQ-FUN-02 | `docker compose config` 서브넷 확인 |
| PLN-003 | 개별 서비스 네트워크 할당 수정 | `infra/**/docker-compose.yml` | REQ-FUN-01 | 서비스별 `infra_net` 존재 여부 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Merge 결과 검증 | `docker compose config` | 에러 없이 유효한 YAML 출력 |
| VAL-PLN-002 | Network | Subnet/IP 검증 | `docker compose config \| grep -E "subnet\|infra_net"` | `172.19.0.0/16` 확인 |
| VAL-PLN-003 | Persistence | k3d-hyhome 유지 검증 | `grep "k3d-hyhome" infra/**/docker-compose.yml` | 기존 설정 보존 확인 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| YAML 문법 오류 | High | 각 파일 수정 후 개별적으로 `docker compose config` 실행 |
| IP 대역 충돌 | Medium | 기존에 수동 할당된 IP 리스트를 먼저 스캔하여 확인 |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed (`docker compose config` success)
- [x] Required docs updated (9-directory governance)
- [x] Post-hoc IP assignments synced (e.g., oauth2-proxy-valkey: .5)

## Related Documents

- **PRD**: `[../01.prd/2026-04-01-standardize-infra-net.md]`
- **ARD**: `[../02.ard/0026-standardize-infra-net.md]`
- **Spec**: `[../04.specs/standardize-infra-net/spec.md]`
- **ADR**: `[../03.adr/0026-standardize-infra-net.md]`
- **TASK**: `[../06.tasks/2026-04-01-standardize-infra-net.md]`
