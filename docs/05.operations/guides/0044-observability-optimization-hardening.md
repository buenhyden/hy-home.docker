---
title: "06-Observability Optimization Hardening Usage Guide"
version: "1.0.4"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
layer: "operations"
artifact_id: "GDE-0044"
parent_ids:
- "POL-0044"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - cadvisor
created: "2026-05-17"
---

# 06-Observability Optimization Hardening Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 문서는 `06-observability` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 체인+SSO 정렬, health 기반 의존성, 커스텀 이미지 하드닝, CI 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Observability Maintainer

### Purpose

- 관측성 관리 경로를 게이트웨이 표준 정책에 정렬한다.
- 초기 기동 안정성과 회귀 차단 능력을 강화한다.
- 카탈로그 기반 확장(샘플링/retention/pipeline module) 준비 상태를 확보한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/06-observability` 및 `scripts/` 수정 권한
- Traefik `gateway-standard-chain`과 프록시 `sso-*` middleware, Grafana·Gatus의 Keycloak 네이티브 client 준비

### Step-by-step Instructions

1. 변경 전 정적 상태 점검
   - root context: `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
   - service-local context: root networks/secrets를 선언한 임시 validation overlay를 함께 사용한다.
2. Gateway/SSO 경계 정렬
   - 네이티브 OIDC router인 `grafana`·`gatus`는 `gateway-standard-chain@file`을 사용하며 각 애플리케이션이 인증을 담당한다.
   - 프록시로 보호하는 `prometheus`·`alloy`·`alertmanager`·`pushgateway`·`loki`·`tempo`·`pyroscope`·`cadvisor`는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을 사용한다.
3. 의존성/헬스 보강
   - Alloy/Grafana의 선언된 `service_healthy` 및 `required: false` 경계를 확인한다. Optional backend가 없을 때 전체 pipeline 수신을 주장하지 않는다.
   - 선언된 cAdvisor `/healthz`와 Prometheus scrape 결과를 구분한다.
4. 커스텀 이미지 하드닝
   - Loki/Tempo Dockerfile의 non-root user와 copied entrypoint를 확인한다. 변경 실행은 RUN-0044로 넘긴다.
   - entrypoint에서 S3 secret 파일(`S3_SECRET_KEY_FILE`)의 존재와 비어 있지 않음을 선검증한다.
5. 자동 검증 및 CI 반영
   - `bash scripts/hardening/check-all-hardening.sh 06-observability`
   - `.github/workflow-contract.yml`에 `leaf.infrastructure-hardening` gate가 등록되어 있는지 확인
6. 문서 추적성 동기화
   - PRD~Procedure optimization-hardening 문서 링크를 점검한다.

### Common Pitfalls

- Native and proxy-protected routers에 동일한 auth middleware를 일괄 적용해
  native OIDC를 중복하거나 proxy protection을 누락하는 실수
- `service_started` 의존성으로 부팅 race condition을 남기는 실수
- custom 이미지에 root 실행 경로를 재도입하는 실수
- 하드닝 스크립트/README 인덱스를 함께 갱신하지 않는 실수

### Source-backed operating contract

- **목적·분류·구현 소유권**: `cadvisor`는 `HOME` container metric exporter이며 `obs`/`obs-host`/`dev`로 선택한다. node-exporter의 소유 문서는 [GDE-0045](0045-prometheus.md#host-and-gpu-exporter-boundary)이며 [Compose](../../../infra/06-observability/docker-compose.yml)가 구현을 소유한다.
- **흐름·보안**: Prometheus는 선언된 network를 통해 두 exporter를 scrape한다. node-exporter는 host PID, host network namespace와 읽기 전용 root/proc/sys mount를 사용하며 `obs_net` gateway 주소에만 listen한다. cAdvisor는 privileged로 실행되며 `/dev/kmsg`를 포함한 host filesystem/device를 mount한다. 이 권한이 보안 경계이며 이를 non-root 격리로 일반화해서는 안 된다. cAdvisor route는 계속 보호된다. node-exporter는 Traefik route나 LAN 공개 포트가 없지만, internal이 아닌 bridge network의 container는 `obs_net` gateway 주소로 접근할 수 있다.
- **상태·secret·자원**: 두 exporter 모두 영속 application data나 Docker Secret을 소유하지 않는다. host metric은 관찰 결과이며 backup 내용이 아니다. CPU/memory 선언은 source limit이며 측정된 여유 용량이 아니다.
- **정상 사용·수명 주기**: 저장소 root에서 렌더링하고 내부 metric endpoint를 검증한 뒤 Prometheus target/label을 확인한다. collector를 변경하기 전에 cardinality/scrape 비용을 비교한다. image를 한 번에 하나씩 upgrade하고 host/container series의 연속성을 검증한다.
- **백업·복구**: 추적 중인 Compose로 다시 구성하며 service state 복구는 필요하지 않다. dashboard/rule은 해당 exporter 밖에서 보존하고 변경 전 target/series 기준값을 기록한다.
- **공식 문서·license**: [node_exporter](https://github.com/prometheus/node_exporter)와 [cAdvisor](https://github.com/google/cadvisor)의 upstream release/security 지침을 따른다. 두 도구 모두 Apache-2.0 license가 적용된다.

### cAdvisor and static-check limits

cAdvisor는 읽기 전용 filesystem/device mount와 `/dev/kmsg`를 사용하는 privileged 관측기다. 공통 template이 capability를 제거한다고 격리를 보장하지 않는다. Disk metric 등 제외 collector, container label/cardinality와 보호 route를 유지한다. Health는 process 응답만 확인하므로 Prometheus target과 예상 container series를 따로 검증한다. 자체 애플리케이션 데이터나 Docker Secret은 없고 복구 대상은 승인된 image/config와 telemetry 기준이다.

관측 hardening 함수는 일부 문자열·파일만 검사하며 모든 Dockerfile, retention 시행, 인증 거부, 전달, host 호환성이나 용량을 증명하지 않는다. Loki/Tempo LAN 접근은 POL-0096의 기존 예외이고 retention 결함은 POL-0048에 남는다. Grafana/Gatus native 인증에 일괄 proxy SSO를 붙이지 않는다. 검사 통과만으로 통제를 완료하거나 privileged 권한 확대를 승인하지 않는다.

### Common Checks

- `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
- Service-local compose 검증은 root network/secret context 또는 임시 overlay 포함
- `bash scripts/hardening/check-all-hardening.sh 06-observability`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0044-observability-optimization-hardening.md)을 따른다.

### Traceability

- Declared parent: [Observability Optimization Hardening Policy](../policies/0044-observability-optimization-hardening.md) (`POL-0044`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0044-observability-optimization-hardening.md) (`POL-0044`), [Runbook](../runbooks/0044-observability-optimization-hardening.md) (`RUN-0044`)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)

- [Official cAdvisor deployment and host access](https://github.com/google/cadvisor)

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0044-observability-optimization-hardening.md)
- [Recovery runbook](../runbooks/0044-observability-optimization-hardening.md)
