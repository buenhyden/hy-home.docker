---
title: "Compose Network Membership Usage Guide"
version: "1.3.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-08"
layer: "operations"
artifact_id: "GDE-0077"
parent_ids:
- "POL-0077"
created: "2026-05-17"
---

# Compose Network Membership Usage Guide

## Overview

이 가이드는 Compose 서비스의 Docker network 소속과 고정 주소 사용 기준을 설명한다.

## Scope

### Audience and Goal

대상 독자는 개발자, 운영자, AI Agent다. 목표는 실제 호출 흐름에 맞는 network를 고르고
불필요한 고정 주소를 만들지 않는 것이다.

## Concepts

구조적 할당은 [AD-0026 Networks](../../../02.architecture/descriptions/0026-standardize-infra-net.md#networks),
선언은 [루트 Compose](../../../../docker-compose.yml)와 해당 service fragment가
소유한다. 서비스가 여러 network를 공유해도 개별 인증·권한 검증을 대신하지 않는다.

## Usage

### Flow and membership

Traefik이 route하는 backend 중 자체 인증이 있는 것은 `edge_net`, `sso-auth`만으로 보호되는 것은
Traefik만 함께 붙는 `<service>_ingress_net`(`10.250.24.0/24`–`10.250.40.0/24`, SPEC-0266)을 쓰고
`traefik.docker.network`로 그 망을 지정한다. `seaweedfs-s3` 메트릭은 `seaweedfs_s3_metrics_net`
(`10.250.41.0/24`)에서 scrape한다. ComfyUI만 붙는 비내부 `comfyui_egress_net`(`10.250.42.0/24`)은 모델·custom node 설치용 유지보수 overlay `infra/08-ai/comfyui/docker-compose.egress.yml`을 붙일 때만 쓰며, 기본 구성의 ComfyUI는 이 망과 host port 없이 `comfyui_ingress_net`에만 붙는다(SPEC-0268). 자체 인증이 없는 보조 listener는 소비자만 붙는 내부 망의 고정 주소 `.2`에만 bind한다(SPEC-0267): `oauth2_proxy_metrics_net`(`10.250.43.0/24`), `keycloak_management_net`(`10.250.44.0/24`), `grafana_pprof_net`(`10.250.45.0/24`), `traefik_metrics_net`(`10.250.46.0/24`), 그리고 기존 `seaweedfs_s3_metrics_net`의 `10.250.41.2`와 `n8n_main_runner_net`·`n8n_worker_runner_net`의 `10.250.22.2`·`10.250.23.2`. 이 망들은 동적 범위를 `.128/25`로 둔다. 퇴역한 망이 쓰던 `10.250.9.0/24`·`10.250.12.0/24`는 재사용하지 않는다.
Prometheus scrape 대상은 `obs_net`,
관리 PostgreSQL/Valkey 소비자는 `mng_data_net`, S3 소비자는 `object_net`처럼
실제 peer가 있는 network만 사용한다. peer가 없으면 project default network를
사용한다. 서비스 membership은 dictionary로 적는다.

```yaml
networks:
  edge_net: {}
  obs_net: {}
```

고정 주소는 다른 곳이 해당 주소를 신뢰하는 경우에만 부여하고 Compose 주석으로
이유를 남긴다. 현재 예는 Traefik trusted-proxy 주소(`edge_net` `10.250.1.2`),
RedisInsight의 `RI_APP_HOST`·healthcheck 주소(`redisinsight_ingress_net` `10.250.18.3`),
Crawl4AI egress gateway·crawler 주소(`crawl4ai_egress_net` `10.250.200.2`/`.3`)다. 대부분의 서비스는 dynamic 주소를 받는다. 고정 주소는 같은 network의
subnet 안, dynamic pool 밖이어야 하며 다른 service와 겹치지 않아야 한다.

root include는 파일을 읽고 profile·직접 service target은 실행 대상을 정한다.
모든 선언을 검토했다고 모든 서비스를 기동한 것은 아니다. root의 external network,
leaf 소유 isolated network와 root 생성 network를 구분한다. k3d와 Compose는
Docker network를 공유하지 않으며 기존 LAN endpoint 연동은
[0096](../10-platform-and-backup/0096-k8s-integration.md)이 소유한다.

### 흔한 함정

- 다중 network 서버가 자기 DNS 이름의 한 주소에만 bind하면 다른 network의
  client가 닿지 못할 수 있다. 해당 listener는 승인된 container 내부
  `0.0.0.0` bind와 명시적 membership을 사용하며 host 공개 범위는 별도 통제한다.
- DNS 실패는 공통 network 누락 외에도 미선택·중단 service나 alias 차이가 원인일
  수 있다. 실제 target과 선언부터 확인하고 network를 무작정 추가하지 않는다.
- 다른 network에서 같은 주소를 쓰는 것과 같은 network 안의 중복을 구분한다.
  단순 검색은 중복 검증이 아니며 YAML 들여쓰기와 subnet도 함께 확인한다.
- 필요한 Compose 기능은 [개발환경 Guide](../10-platform-and-backup/0002-developer-environment.md)를 따른다.
  쓰기·runtime 권한이 없어도 공개 선언을 읽을 수 있지만 변경·조회 승인은 별도다.

### Common Checks

root/leaf network 선언, peer와 endpoint, static 주소 이유, host 노출과 profile을
함께 대조한다. [RUN-0077](../../runbooks/02-gateway-and-networking/0077-ip-address-management.md)의 승인된
공개 구성 검증은 live 연결이나 static-IP 무충돌의 완전한 증거가 아니다.
선택·준비 상태의 차이는 [시스템 Guide](../01-common/0099-system-operations.md)를 따른다.

### Runbook Handoff

membership·주소 변경, 충돌 진단과 scoped rollback은
[RUN-0077](../../runbooks/02-gateway-and-networking/0077-ip-address-management.md)이 소유한다.

### Traceability

- 상위 Policy: [POL-0077](../../policies/02-gateway-and-networking/0077-ip-address-management.md)
- 구조: [AD-0026](../../../02.architecture/descriptions/0026-standardize-infra-net.md)
- 같은 주제: [Policy](../../policies/02-gateway-and-networking/0077-ip-address-management.md), [Runbook](../../runbooks/02-gateway-and-networking/0077-ip-address-management.md)

## Troubleshooting

위 "흔한 함정"의 DNS·bind·중복 주소 증상부터 확인하고, 변경이나 충돌 진단은
[RUN-0077](../../runbooks/02-gateway-and-networking/0077-ip-address-management.md)로 넘긴다.

## Related Documents

- [Operations index](../../README.md)
- [hy-home.k8s 통합](../10-platform-and-backup/0096-k8s-integration.md)
