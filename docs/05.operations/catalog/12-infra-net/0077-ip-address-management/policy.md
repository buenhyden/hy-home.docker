---
title: "Compose Network Membership Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0077"
parent_ids:
- "AD-0026"
created: "2026-04-01"
---


# Compose Network Membership Operations Policy

## Overview

이 문서는 `hy-home.docker` 시스템의 Docker network 소속과 주소 할당 정책을 정의한다. IP 충돌 방지 및 일관성 유지를 위한 통제 기준을 제공한다.

## Policy Scope

이 정책은 repository가 root Compose에서 소유하는 모든 network의 소속과 주소 할당 방식을 관할한다.

- **Systems**: `hy-home.docker` 기반 모든 서비스.
- **Agents**: 모든 인프라 관리 에이전트.
- **Environments**: Local (k3d/docker-compose) 및 Production (Future) 개발/운영 환경.

## Controls

- **Required**:
  - 서비스는 실제로 사용하는 peer가 있는 network에만 연결한다. peer가 없으면
    프로젝트 기본 network를 쓴다.
  - 고정 주소는 다른 곳이 그 주소를 신뢰할 때만 부여하고, 사유를 Compose 주석에
    남긴다(현재: Traefik의 `edge_net` 주소, OpenSearch node 간 announce 주소,
    `k3d-hyhome` 소속 서비스).
  - 고정 주소는 해당 network의 dynamic range 밖에 둔다.
- **Allowed**:
  - 새 flow가 생기면 해당 network membership을 추가한다.
  - 대부분의 서비스는 주소를 지정하지 않고 dynamic 주소를 받는다.
- **Disallowed**:
  - 중복된 고정 주소 (Compose 파일 병합 단계에서 검증 필수).
  - 사용하지 않는 peer를 위한 network 연결.
  - 외부망 주소와의 브릿징 설정 수동 수정.

## Exceptions

- **K3d-hyhome Compatibility**: `k3d-hyhome` 네트워크는 마스터 노드 및 외부 게이트웨이 영역과의 호환성을 위해 기존 IP 체계를 예외적으로 유지하거나 별도 할당 방식을 적용할 수 있음.

## Verification

- `bash scripts/validation/validate-docker-compose.sh`를 통한 root compose 구조 검증.
- 변경한 tier profile은 `HYHOME_COMPOSE_PROFILES`로 지정해 동일 검증을 반복한다.
- `rg -n "ipv4_address:" infra docker-compose.yml`로 고정 주소 선언을 확인한다.
- `python3 -m unittest tests.validation.test_compose_baseline_gates.NetworkSegmentationContractTests`로
  routed·scrape·trusted proxy·bind address 계약을 확인한다.
- 실행 중인 승인된 환경에서는 `docker network inspect <network>` 결과를 선언과 비교한다.

## Review Cadence

- **Monthly**: AD-0026 **Networks** 표와 현재 Compose 파일 사이의 실태를 점검한다.
- **On material change**: 신규 서비스, static IP 변경, profile include 변경, network gateway 변경 시 즉시 재검토한다.

## Traceability

- Declared parent: [Compose Network Segmentation Architecture Description](../../../../02.architecture/descriptions/0026-standardize-infra-net.md) (`AD-0026`)
- Subject peers: [Guide](guide.md) (`GDE-0077`), [Runbook](runbook.md) (`RUN-0077`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Compose network segmentation architecture](../../../../02.architecture/descriptions/0026-standardize-infra-net.md)
