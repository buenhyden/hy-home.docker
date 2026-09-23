---
title: "06-Observability Optimization Hardening Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
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

## Usage

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
- Traefik `gateway-standard-chain` and proxy `sso-*` middleware 준비,
  plus native Keycloak clients for Grafana and Gatus

### Step-by-step Instructions

1. 변경 전 정적 상태 점검
   - root context: `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
   - service-local context: root networks/secrets를 선언한 임시 validation overlay를 함께 사용한다.
2. Gateway/SSO 경계 정렬
   - Native OIDC routers `grafana` and `gatus` use
     `gateway-standard-chain@file`; authentication stays in each application.
   - Proxy-protected routers `prometheus`, `alloy`, `alertmanager`,
     `pushgateway`, `loki`, `tempo`, `pyroscope`, and `cadvisor` use
     `gateway-standard-chain@file,sso-errors@file,sso-auth@file`.
3. 의존성/헬스 보강
   - Alloy/Grafana의 Loki/Tempo 의존성을 `service_healthy`로 설정한다.
   - cAdvisor healthcheck(`/healthz`)를 추가한다.
4. 커스텀 이미지 하드닝
   - Loki/Tempo Dockerfile에 non-root user(`10001`)를 강제한다.
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

- **Purpose/classification/source**: `node-exporter` and `cadvisor` are `HOME` host/container metric exporters selected by `obs`/`obs-host`/`dev`; [Compose](../../../../../infra/06-observability/docker-compose.yml) is authoritative.
- **Flow/security**: Prometheus scrapes both over the declared networks. node-exporter uses host PID and read-only root/proc/sys mounts; cAdvisor is privileged with host filesystem/device mounts including `/dev/kmsg`. These grants are the security boundary and must not be generalized as non-root isolation. cAdvisor's route remains protected; node-exporter is internal-only.
- **State/secrets/resources**: neither exporter owns durable application data or Docker Secrets. Host metrics are observations, not backup content. CPU/memory declarations are source limits, not measured headroom.
- **Normal use/lifecycle**: render from root, verify metrics endpoints internally, confirm Prometheus targets/labels, and compare cardinality/scrape cost before changing collectors. Upgrade one image at a time and verify host/container series continuity.
- **Backup/recovery**: rebuild from tracked Compose; no service-state restore is required. Preserve dashboards/rules elsewhere and capture the pre-change target/series baseline.
- **Upstream/license**: use [node_exporter](https://github.com/prometheus/node_exporter) and [cAdvisor](https://github.com/google/cadvisor) upstream release/security guidance. Both are Apache-2.0 licensed.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=obs bash scripts/validation/validate-docker-compose.sh`
- Service-local compose 검증은 root network/secret context 또는 임시 overlay 포함
- `bash scripts/hardening/check-all-hardening.sh 06-observability`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Observability Optimization Hardening Policy](policy.md) (`POL-0044`)
- Governing authority: [Observability Architecture Description](../../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](policy.md) (`POL-0044`), [Runbook](runbook.md) (`RUN-0044`)

## Related Documents

- [Observability Compose](../../../../../infra/06-observability/docker-compose.yml)

- [Official cAdvisor deployment and host access](https://github.com/google/cadvisor)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
