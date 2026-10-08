---
title: "Tempo Usage Guide"
version: "1.0.5"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0049"
parent_ids:
- "POL-0049"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - tempo
created: "2026-05-10"
---

# Tempo Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 가이드는 `06-observability` 계층의 Tempo 사용 맥락과 설정 확인 방법을 설명한다. Tempo는 Alloy가 전달한 OTLP trace를 수집하고, SeaweedFS S3 backend의 `tempo-bucket`에 저장하며, `metrics_generator`를 통해 span metrics와 service graphs를 Prometheus remote write endpoint로 전송한다.

### Usage Type

`system-guide`

### Target Audience

- Backend Developer
- SRE
- Operator
- AI Agent

### Purpose

- Tempo compose service, OTLP receiver, SeaweedFS storage, retention, metrics generator boundary를 빠르게 파악한다.
- Grafana에서 TraceQL, span metrics, service graph를 확인하는 진입점을 제공한다.
- 복구, restart, WAL symptom triage, storage 장애 대응은 runbook으로 넘긴다.

### Prerequisites

- [Grafana Alloy](0040-alloy.md)가 OTLP `4317`/`4318` receiver를 열고 `tempo:4317` exporter로 trace를 전달해야 한다.
- [SeaweedFS](../../../infra/04-data/seaweedfs/README.md)에 `tempo-bucket`이 준비되어 있어야 한다.
- [Grafana](0041-grafana.md)에 Tempo datasource URL `http://tempo:3200`이 provisioning되어 있어야 한다.
- Docker Secret value는 열람하지 않는다. `seaweedfs_s3_tempo_secret_key` secret ID와 file reference만 문서화한다.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-high|image: hy/tempo:|container_name: tempo|user: .10001:10001.|tempo-data|TEMPO_PORT|seaweedfs_s3_tempo_secret_key|tempo.middlewares' infra/06-observability/docker-compose.yml
   ```

2. Tempo config의 ingestion, retention, storage, metrics generator boundary를 확인한다.

   ```bash
   rg -n 'endpoint: 0.0.0.0:4317|endpoint: 0.0.0.0:4318|metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: seaweedfs-s3:8333' infra/06-observability/tempo/config/tempo.yaml
   ```

3. Alloy에서 Tempo exporter가 `tempo:4317`을 가리키는지 확인한다.

   ```bash
   rg -n 'otelcol.exporter.otlp "tempo"|endpoint = "tempo:4317"|traces  = \\[otelcol.exporter.otlp.tempo.input\\]' infra/06-observability/alloy/config/config.alloy
   ```

4. Grafana의 `Explore` 메뉴에서 `Tempo` datasource를 선택하고 `TraceQL`로 trace를 조회한다.

   ```text
   { duration > 100ms && resource.service.name = "api-gateway" }
   ```

5. Grafana service graph와 span metrics가 비어 있으면 Tempo `metrics_generator`와 Prometheus remote write 상태를 runbook 기준으로 점검한다.

### Common Pitfalls

- **Instrumentation 누락**: trace propagation이 끊기면 전체 요청 흐름을 볼 수 없다. 애플리케이션 공통 라이브러리나 middleware의 context 전달을 확인한다.
- **Storage assumption**: Tempo는 SeaweedFS S3 backend와 local WAL을 함께 사용한다. WAL 삭제나 bucket 변경은 guide 범위가 아니라 runbook escalation 대상이다.
- **Metrics generator assumption**: Service graph와 span metrics는 `metrics_generator`와 Prometheus remote write가 모두 정상이어야 보인다.
- **Secret exposure**: SeaweedFS secret value를 로그나 문서에 기록하지 않는다.

### Source-backed operating contract

- **목적/분류/출처**: `tempo`는 `obs`/`tracing`이 선택하는 `HOME` trace store다. [Compose](../../../infra/06-observability/docker-compose.yml)와 [Tempo config](../../../infra/06-observability/tempo/config/tempo.yaml)가 authoritative하다.
- **Flow/state**: Alloy가 OTLP를 수신해 Tempo로 trace를 전송한다. 내구성 있는 block은 SeaweedFS bucket `tempo-bucket`에 있고, `tempo-data:/var/tempo`는 ingest WAL, metrics-generator WAL, local temporary block을 보관한다. Grafana가 Tempo를 query한다.
- **Secrets/dependencies/security**: `S3_ACCESS_KEY`와 `seaweedfs_s3_tempo_secret_key`로 object storage에 접근한다. SeaweedFS, Alloy, Grafana, gateway auth, root CA와 선언된 network가 dependency다. Credential을 render하거나 OTLP/query route를 선언된 통제 이상으로 노출하지 않는다.
- **Resources/normal use**: source의 limit은 headroom이 아니다. Root에서 render하고, readiness를 validate하고, Alloy를 통해 labeled test trace를 보내 query한 뒤 WAL/object-store error를 monitor한다.
- **Lifecycle**: trace intake를 quiesce하고, SeaweedFS owner와 함께 `tempo-bucket`의 consistent backup을 조율하며, local WAL/temp state/config를 같은 recovery point에 보존한다. 지원되는 version으로 upgrade하고 WAL replay와 historical/new trace를 검증한다.
- **Upstream/license**: 공식 [object storage architecture](https://grafana.com/docs/tempo/latest/reference-tempo-architecture/object-storage/)와 [recommended versions](https://grafana.com/docs/tempo/latest/set-up-for-tracing/setup-tempo/recommended-versions/) 가이드를 따른다. Tempo는 AGPL-3.0 라이선스다.

### Retention enforcement gap

[POL-0048](../policies/0048-telemetry-retention.md)은 block 24h, compacted block 1h를 요구하지만 현재 설정에는 둘 다 없다. 선언된 Tempo 기본값은 336h/1h이므로 24h 준수가 입증되지 않는다. Bucket/receiver에 일치한 `rg`를 retention 검증으로 간주하지 않는다. 별도로 확인하고 누락은 통제 실패로 기록한다. 버전에 맞는 별도 구현 수정이 필요하다. Tempo 3은 backend scheduler/worker compaction 설정을 사용하므로 Tempo 2의 `compactor` 블록을 복사하지 않는다. 소스 검증은 실제 삭제나 trace 복원 증거가 아니다.

### Approved LAN integration boundary

Traefik hostname에는 TLS/SSO middleware를 유지한다. 별도로 [POL-0096](../policies/0096-k8s-integration.md#controls)의 기존 k3d 예외에 따라 Tempo HTTP `3200`을 `HOST_LAN_BIND_IP`(공개 기본값 `192.168.0.13`)에 gateway 인증·서비스 TLS 없이 게시한다. 완료된 SPEC-0188 Task의 2026-09-29 owner 승인에 따른 것으로 W5가 만든 예외가 아니다. Loki `auth_enabled: false`는 사용자 인증이 아니며 Tempo에도 native 인증 계층이 없다. Gateway middleware는 직접 포트를 보호하지 않는다.

예외는 지정 cluster 통합 목적과 설정된 LAN 인터페이스로 한정한다. 소스에는 k3d만 식별하는 인증이 없으며 비공개 override, bind 성공, routing/firewall과 실제 도달성은 관찰하지 않았다. 사람은 보호된 hostname을, 기계 검증은 [GDE-0096](../guides/0096-k8s-integration.md)을 따른다. 실제 log/trace payload 대신 상태와 시험 ID만 남긴다. 재바인딩·제거·인증/TLS 추가·노출 확대는 통합 소유자와 조정한 별도 승인 변경이다.

### Common Checks

- `docker compose --profile obs ps tempo`
- `docker logs --tail=100 tempo`
- `docker exec tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready`
- `rg -n 'bucket: tempo-bucket|url: http://prometheus:9090/api/v1/write' infra/06-observability/tempo/config/tempo.yaml`

### Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../runbooks/0049-tempo.md)을 따른다.

### Traceability

- Declared parent: [Tempo Operations Policy](../policies/0049-tempo.md) (`POL-0049`)
- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](../policies/0049-tempo.md) (`POL-0049`), [Runbook](../runbooks/0049-tempo.md) (`RUN-0049`)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Operations policy](../policies/0049-tempo.md)
- [Recovery runbook](../runbooks/0049-tempo.md)
