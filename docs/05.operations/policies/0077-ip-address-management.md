---
title: "Compose Network Membership Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
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
- **Environments**: 현재 HOME/DEV와 명시적으로 선택한 OPTIONAL/LAB 환경. 미래 production을 검증된 대상으로 간주하지 않는다.

## Controls

- **Required**:
  - 서비스는 실제로 사용하는 peer가 있는 network에만 연결한다. peer가 없으면
    프로젝트 기본 network를 쓴다.
  - 고정 주소는 다른 곳이 그 주소를 신뢰할 때만 부여하고, 사유를 Compose 주석에
    남긴다(현재: Traefik의 `edge_net` 주소, OpenSearch node 간 announce 주소).
  - 고정 주소는 해당 network의 dynamic range 밖에 둔다.
- **Allowed**:
  - 새 flow가 생기면 해당 network membership을 추가한다.
  - 대부분의 서비스는 주소를 지정하지 않고 dynamic 주소를 받는다.
- **Disallowed**:
  - 같은 network 안의 중복된 고정 주소. 적용 전에 선언과 승인된 runtime 주소를 대조해야 한다.
  - 사용하지 않는 peer를 위한 network 연결.
  - 외부망 주소와의 브릿징 설정 수동 수정.

## Exceptions

현재 예외는 없다. `k3d-hyhome` 공유 membership 예외는 2026-09-23 종료되었다.
별도 LAN endpoint 연동은 [POL-0096](0096-k8s-integration.md)의 기존 경계를 따른다.

## Verification

- `bash scripts/validation/validate-docker-compose.sh`를 통한 root compose 구조 검증.
- 변경한 tier profile은 `HYHOME_COMPOSE_PROFILES`로 지정해 동일 검증을 반복한다.
- `rg -n "ipv4_address:" infra docker-compose.yml`로 고정 주소 선언을 확인한다.
- `python3 -m unittest tests.validation.test_compose_baseline_gates.NetworkSegmentationContractTests`로
  routed·scrape·trusted proxy·bind address 계약을 확인한다.
- 승인된 runtime에서는 [RUN-0077](../runbooks/0077-ip-address-management.md)의 값 없는 scoped 주소 출력만 선언과 비교한다.

현재 Compose validator의 명시적 충돌 검사는 host port이며 static-IP 유일성을
전부 검증하지 않는다. `rg`는 후보 목록일 뿐이다. subnet·dynamic pool·network별
중복은 별도로 검토한다. 이 구현 한계는 중복 금지 통제를 면제하지 않는다.
검사 입력·임시 파일 효과는 [RUN-0086](../runbooks/0086-dependency-version-management.md#static-configuration-validation)을 따른다.

## Review Cadence

책임 소유자는 @buenhyden이며, 주소·membership·노출 예외를 승인한다.

- **Monthly**: AD-0026 **Networks** 표와 현재 Compose 파일 사이의 실태를 점검한다.
- **On material change**: 신규 서비스, static IP 변경, profile include 변경, network gateway 변경 시 즉시 재검토한다.

## Traceability

- 상위 문서: [Compose Network Segmentation Architecture Description](../../02.architecture/descriptions/0026-standardize-infra-net.md) (`AD-0026`)
- 같은 주제: [Guide](../guides/0077-ip-address-management.md) (`GDE-0077`), [Runbook](../runbooks/0077-ip-address-management.md) (`RUN-0077`)

## Related Documents

- [Operations index](../README.md)
- [Usage guide](../guides/0077-ip-address-management.md)
- [Recovery runbook](../runbooks/0077-ip-address-management.md)
- [Compose network segmentation architecture](../../02.architecture/descriptions/0026-standardize-infra-net.md)
