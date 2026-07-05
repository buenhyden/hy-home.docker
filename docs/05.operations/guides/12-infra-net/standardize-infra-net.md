---
status: active
---
<!-- Target: docs/05.operations/guides/12-infra-net/standardize-infra-net.md -->

# 0012 Standardize Infra Net Usage Guide

## Usage

### Overview

이 문서는 모든 인프라 서비스에 `infra_net` 공통 네트워크와 고정 IP를 할당하는 가이드다. 프로젝트의 일관성을 유지하기 위해 표준 딕셔너리 기반의 네트워크 정의 방식을 따른다.

### Usage Type

`how-to | system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

이 가이드는 시스템 관리자나 개발자가 신규 서비스 또는 기존 서비스를 `hy-home.docker`의 표준 네트워크 구조인 `infra_net`에 올바르게 통합하는 것을 돕는다.

### Prerequisites

- `hy-home.docker` 프로젝트 루트 디렉터리에 대한 쓰기 권한.
- Docker Compose v2.0 이상.
- `docs/03.specs/098-standardize-infra-net/spec.md`의 authoritative IP mapping table.

### Step-by-step Instructions

1. **IP 대역 확인**:
   - `docs/03.specs/098-standardize-infra-net/spec.md`의 **Assigned IP Mapping Table (Authoritative)** 섹션에서 서비스 그룹에 맞는 IP 가용 범위를 확인한다.
2. **Compose 파일 수정**:
   - `services:` 하위의 대상 서비스에서 `networks:` 섹션을 다음과 같이 딕셔너리 형태로 수정한다.

   ```yaml
   networks:
     infra_net:
       ipv4_address: 172.19.0.7 # registry example from the authoritative table
   ```

   - 실제 대상 서비스에는 위 예시를 그대로 복사하지 말고 authoritative table의 해당 서비스 IP를 사용한다.
   - (선택 사항) 만약 K3s 연동을 위해 기존 `k3d-hyhome` 네트워크가 이미 필요한 경우 기존 값을 유지한다.
3. **루트 Docker Compose 수정**:
   - 프로젝트 루트의 `docker-compose.yml` 내 `include:` 섹션에서 해당 파일이 주석 처리되어 있지 않은지 확인한다.
4. **구성 검증**:
   - repository root에서 `bash scripts/validation/validate-docker-compose.sh`를 실행하여 기본 compose 구조와 root `infra_net` 컨텍스트를 검증한다.
   - 특정 tier profile을 변경한 경우 해당 profile을 `HYHOME_COMPOSE_PROFILES`에 지정해 동일 검증을 반복한다.

### Common Pitfalls

- **IP Conflict**: 이미 할당된 IP를 중복 부여하지 않도록 `rg -n "ipv4_address:" infra docker-compose.yml`로 전체 조사를 수행해야 함.
- **Indentation Error**: YAML 딕셔너리 구조에서의 들여쓰기 오류 주의.
- **Network Scope**: 지정된 주소 대역(`172.19.0.0/16`) 외부의 IP를 입력할 경우 배포 실패.

## Common Checks

- `bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES="workflow" bash scripts/validation/validate-docker-compose.sh` (변경한 profile 값으로 대체)
- `rg -n "ipv4_address:|infra_net:" infra docker-compose.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/12-infra-net/standardize-infra-net.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [infra_net spec](../../../03.specs/098-standardize-infra-net/spec.md)
- [Operations policy](../../policies/12-infra-net/standardize-infra-net.md)
- [Recovery runbook](../../runbooks/12-infra-net/standardize-infra-net.md)
