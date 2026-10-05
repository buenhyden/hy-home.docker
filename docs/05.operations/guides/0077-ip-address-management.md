---
title: "Compose Network Membership Usage Guide"
version: "1.2.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0077"
parent_ids:
- "POL-0077"
created: "2026-05-17"
---

# Compose Network Membership Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

이 가이드는 개발자·운영자·AI Agent가 실제 호출 흐름에 맞는 network를 선택하도록
돕는다. 구조적 할당은 [AD-0026 Networks](../../02.architecture/descriptions/0026-standardize-infra-net.md#networks-spec-0180-s05),
선언은 [루트 Compose](../../../docker-compose.yml)와 해당 service fragment가
소유한다. 서비스가 여러 network를 공유해도 개별 인증·권한 검증을 대신하지 않는다.

### Flow and membership

Traefik이 route하는 backend는 `edge_net`, Prometheus scrape 대상은 `obs_net`,
관리 PostgreSQL/Valkey 소비자는 `mng_data_net`, S3 소비자는 `object_net`처럼
실제 peer가 있는 network만 사용한다. peer가 없으면 project default network를
사용한다. 서비스 membership은 dictionary로 적는다.

```yaml
networks:
  edge_net: {}
  obs_net: {}
```

고정 주소는 다른 곳이 해당 주소를 신뢰하는 경우에만 부여하고 Compose 주석으로
이유를 남긴다. Traefik trusted-proxy 주소와 OpenSearch node announce 주소가
현재 예다. 대부분의 서비스는 dynamic 주소를 받는다. 고정 주소는 같은 network의
subnet 안, dynamic pool 밖이어야 하며 다른 service와 겹치지 않아야 한다.

root include는 파일을 읽고 profile·직접 service target은 실행 대상을 정한다.
모든 선언을 검토했다고 모든 서비스를 기동한 것은 아니다. root의 external network,
leaf 소유 isolated network와 root 생성 network를 구분한다. k3d와 Compose는
Docker network를 공유하지 않으며 기존 LAN endpoint 연동은
[0096](0096-k8s-integration.md)이 소유한다.

### Common pitfalls

- 다중 network 서버가 자기 DNS 이름의 한 주소에만 bind하면 다른 network의
  client가 닿지 못할 수 있다. 해당 listener는 승인된 container 내부
  `0.0.0.0` bind와 명시적 membership을 사용하며 host 공개 범위는 별도 통제한다.
- DNS 실패는 공통 network 누락 외에도 미선택·중단 service나 alias 차이가 원인일
  수 있다. 실제 target과 선언부터 확인하고 network를 무작정 추가하지 않는다.
- 다른 network에서 같은 주소를 쓰는 것과 같은 network 안의 중복을 구분한다.
  단순 검색은 중복 검증이 아니며 YAML 들여쓰기와 subnet도 함께 확인한다.
- 필요한 Compose 기능은 [개발환경 Guide](0002-developer-environment.md)를 따른다.
  쓰기·runtime 권한이 없어도 공개 선언을 읽을 수 있지만 변경·조회 승인은 별도다.

### Common Checks

root/leaf network 선언, peer와 endpoint, static 주소 이유, host 노출과 profile을
함께 대조한다. [RUN-0077](../runbooks/0077-ip-address-management.md)의 승인된
공개 구성 검증은 live 연결이나 static-IP 무충돌의 완전한 증거가 아니다.
선택·준비 상태의 차이는 [시스템 Guide](0099-system-operations.md)를 따른다.

### Runbook Handoff

membership·주소 변경, 충돌 진단과 scoped rollback은
[RUN-0077](../runbooks/0077-ip-address-management.md)이 소유한다.

### Traceability

- 상위 Policy: [POL-0077](../policies/0077-ip-address-management.md)
- 구조: [AD-0026](../../02.architecture/descriptions/0026-standardize-infra-net.md)
- 같은 주제: [Policy](../policies/0077-ip-address-management.md), [Runbook](../runbooks/0077-ip-address-management.md)

## Related Documents

- [Operations index](../README.md)
- [hy-home.k8s 통합](0096-k8s-integration.md)
