---
title: "Compose Network Membership Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0077"
parent_ids:
- "POL-0077"
created: "2026-05-17"
---

# Compose Network Membership Usage Guide

## Usage

### Overview

이 문서는 인프라 서비스를 실제 흐름에 맞는 network에 연결하는 가이드다. 프로젝트의 일관성을 유지하기 위해 표준 딕셔너리 기반의 네트워크 정의 방식을 따른다.

### Usage Type

`how-to | system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

이 가이드는 시스템 관리자나 개발자가 신규 서비스 또는 기존 서비스를 `hy-home.docker`의 분리된 network 구조에 올바르게 연결하는 것을 돕는다.

### Prerequisites

- `hy-home.docker` 프로젝트 루트 디렉터리에 대한 쓰기 권한.
- Docker Compose v2.0 이상.
- `docs/02.architecture/descriptions/0026-standardize-infra-net.md`의 current
  structural allocation table.

### Step-by-step Instructions

1. **필요한 flow 확인**:
   - 서비스가 실제로 호출하는 상대를 확인한다. Traefik route가 있으면 `edge_net`,
     Prometheus가 scrape하면 `obs_net`, `mng-pg`/`mng-valkey`를 쓰면 `mng_data_net`,
     S3를 쓰면 `object_net`이다. 전체 표는
     `docs/02.architecture/descriptions/0026-standardize-infra-net.md`의 **Networks**가 소유한다.
2. **Compose 파일 수정**:
   - `services:` 하위의 대상 서비스에서 사용하는 network만 딕셔너리 형태로 적는다.

   ```yaml
   networks:
     edge_net: {}
     obs_net: {}
   ```

   - 고정 주소는 다른 곳이 그 주소를 신뢰할 때만 부여하고 사유를 주석으로 남긴다.
     상대가 없는 서비스는 `networks:` 자체를 생략해 프로젝트 기본 network를 쓴다.
   - (선택 사항) K3s 연동으로 `k3d-hyhome`이 필요한 경우 기존 값을 유지한다.
3. **루트 Docker Compose 수정**:
   - 프로젝트 루트의 `docker-compose.yml` 내 `include:` 섹션에 해당 파일이 있는지 확인한다. include는 무조건 병합되므로, 실제 기동 여부는 선택한 profile로 판단한다.
4. **구성 검증**:
   - repository root에서 `bash scripts/validation/validate-docker-compose.sh`를 실행하여 기본 compose 구조와 root network 컨텍스트를 검증한다.
   - 특정 tier profile을 변경한 경우 해당 profile을 `HYHOME_COMPOSE_PROFILES`에 지정해 동일 검증을 반복한다.

### Common Pitfalls

- **IP Conflict**: 고정 주소를 부여할 때 `rg -n "ipv4_address:" infra docker-compose.yml`로 중복을 확인한다.
- **Indentation Error**: YAML 딕셔너리 구조에서의 들여쓰기 오류 주의.
- **Network Scope**: 해당 network의 선언된 `10.250.x.0/24` 밖 주소를 쓰면 배포가 실패한다.
- **Multi-homed bind**: 여러 network에 붙은 서버는 `0.0.0.0`에 bind한다. 자기 이름은 한
  network에서만 해석되므로 그 주소에 bind하면 다른 network의 client가 닿지 못한다.
- **Missing peer network**: 이름이 해석되지 않으면 대개 두 서비스가 공유하는 network가 없다는 뜻이다.

## Common Checks

- `bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES="workflow" bash scripts/validation/validate-docker-compose.sh` (변경한 profile 값으로 대체)
- `rg -n "ipv4_address:" infra docker-compose.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Compose Network Membership Operations Policy](policy.md) (`POL-0077`)
- Governing authority: [Compose Network Segmentation Architecture Description](../../../../02.architecture/descriptions/0026-standardize-infra-net.md) (`AD-0026`)
- Subject peers: [Policy](policy.md) (`POL-0077`), [Runbook](runbook.md) (`RUN-0077`)

## Related Documents

- [Operations index](../../../README.md)
- [Compose network segmentation architecture](../../../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
