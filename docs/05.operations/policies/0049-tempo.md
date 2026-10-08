---
title: "Tempo Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "operations"
artifact_id: "POL-0049"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Tempo Operations Policy

## Overview

### Overview

이 정책은 Tempo distributed tracing backend의 trace ingestion, SeaweedFS S3
storage, block retention, metrics generator, secret boundary, protected route를
정의한다. 사용 흐름은 Tempo guide가, 장애 대응 절차는 Tempo runbook이
담당한다.

## Scope

### Policy Scope

이 정책은 current `infra/06-observability/tempo` compose와
`config/tempo.yaml`에 선언된 Tempo 운영 기준을 다룬다.

- **Systems**: compose service `tempo`, container `tempo`, image [hy/tempo image declaration](../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/tempo/config/tempo.yaml`, volume `tempo-data`, SeaweedFS bucket `tempo-bucket`
- **Environments**: 로컬·개발·홈랩 운영

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0049-tempo.md) (`GDE-0049`), [Runbook](../runbooks/0049-tempo.md) (`RUN-0049`)

## Rules

### Controls

- **Required**:
  - Tempo service는 `template-stateful-high`, image
    [hy/tempo image declaration](../../../infra/06-observability/docker-compose.yml), user `10001:10001`, read-only config mount,
    persistent `tempo-data` volume을 유지한다.
  - Custom Tempo image는 upstream [grafana/tempo image declaration](../../../infra/06-observability/tempo/Dockerfile), non-root user
    `10001:10001`, `/docker-entrypoint.sh` secret guard를 유지한다.
  - OTLP receiver는 internal gRPC `4317`과 HTTP `4318` endpoint를 유지한다.
  - HTTP/query/health surface는 `${TEMPO_PORT:-3200}`와 `/ready` healthcheck를
    기준으로 한다.
  - Trace storage는 SeaweedFS S3 backend, bucket `tempo-bucket`, endpoint
    `seaweedfs-s3:8333`, `insecure: true`를 사용한다.
  - `S3_ACCESS_KEY`는 environment reference로, `S3_SECRET_KEY`는
    Docker Secret `seaweedfs_s3_tempo_secret_key`로만 주입한다.
  - Block retention 값은 [POL-0048](0048-telemetry-retention.md)을 기준으로 한다.
  - Metrics generator는 현재 `span-metrics`, `service-graphs` processors와
    Prometheus `http://prometheus:9090/api/v1/write` remote_write를 유지한다.
    Tempo 3 TraceQL metrics는 이전 `local_blocks` processor 요구와 구분한다.
    검색/Drilldown capability를 processor 이름만으로 검증하지 않는다.
  - Tempo route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
- **Allowed**:
  - Development/debug 상황의 sampling 또는 log-level 변경은 plan/task
    evidence와 rollback note가 있을 때만 허용한다.
  - 장기 분석이 필요하면 retention policy와 SeaweedFS owning policy/runbook을
    함께 갱신한다.
- **Disallowed**:
  - PII, password, token, credential 값을 trace attributes에 기록하는 행위
  - Secret guard 없이 SeaweedFS-backed Tempo image나 entrypoint를 변경하는 행위
  - 승인 없이 bucket, retention, metrics generator processors, remote_write
    endpoint, route middleware, image version을 runtime에서 변경하는 행위

### Lifecycle and data controls

- Tempo는 `HOME`이다. SPEC-0182 W6에서 소유자가 `tracing`을 HOME에 추가했다(POL-0078). `tracing`을 빼는 대상으로 전환할 때는 `HOME up`이 이미 실행 중인 컨테이너를 제거하지 않으므로 Tempo를 명시적으로 중지한다.
- `tempo-bucket`, local WAL/temp state, config, 대응하는 SeaweedFS credential을 하나의 조율된 recovery set으로 취급한다; object-store owner가 bucket backup/restore를 수행한다.
- consistency 캡처 전에 OTLP ingestion을 멈춘다. isolated bucket/path로 rehearse하고 WAL replay, historical/new trace query, metrics-generator 동작, Alloy/Grafana integration을 검증한다.
- Removal은 producer/exporter migration, retention 결정, credential/route 정리, object나 local data를 삭제하기 전 명시적 승인이 필요하다.

### Retention enforcement gap

[POL-0048](../policies/0048-telemetry-retention.md)은 block 24h, compacted block 1h를 요구하지만 현재 설정에는 둘 다 없다. 선언된 Tempo 기본값은 336h/1h이므로 24h 준수가 입증되지 않는다. Bucket/receiver에 일치한 `rg`를 retention 검증으로 간주하지 않는다. 별도로 확인하고 누락은 통제 실패로 기록한다. 버전에 맞는 별도 구현 수정이 필요하다. Tempo 3은 backend scheduler/worker compaction 설정을 사용하므로 Tempo 2의 `compactor` 블록을 복사하지 않는다. 소스 검증은 실제 삭제나 trace 복원 증거가 아니다.

### Approved LAN integration boundary

Traefik hostname에는 TLS/SSO middleware를 유지한다. 별도로 [POL-0096](../policies/0096-k8s-integration.md#controls)의 기존 k3d 예외에 따라 Tempo HTTP `3200`을 `HOST_LAN_BIND_IP`(공개 기본값 `192.168.0.13`)에 gateway 인증·서비스 TLS 없이 게시한다. 완료된 SPEC-0188 Task의 2026-09-29 owner 승인에 따른 것으로 W5가 만든 예외가 아니다. Loki `auth_enabled: false`는 사용자 인증이 아니며 Tempo에도 native 인증 계층이 없다. Gateway middleware는 직접 포트를 보호하지 않는다.

예외는 지정 cluster 통합 목적과 설정된 LAN 인터페이스로 한정한다. 소스에는 k3d만 식별하는 인증이 없으며 비공개 override, bind 성공, routing/firewall과 실제 도달성은 관찰하지 않았다. 사람은 보호된 hostname을, 기계 검증은 [GDE-0096](../guides/0096-k8s-integration.md)을 따른다. 실제 log/trace payload 대신 상태와 시험 ID만 남긴다. 재바인딩·제거·인증/TLS 추가·노출 확대는 통합 소유자와 조정한 별도 승인 변경이다.

### Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: hy/tempo:|user: .10001:10001.|tempo-data|TEMPO_PORT|seaweedfs_s3_tempo_secret_key|tempo.middlewares' infra/06-observability/docker-compose.yml`
- Tempo config:
  `rg -n 'metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: seaweedfs-s3:8333|secret_key: \\$\\{S3_SECRET_KEY\\}' infra/06-observability/tempo/config/tempo.yaml`
- Custom image secret guard:
  `rg -n 'FROM grafana/tempo:|USER 10001:10001|missing secret: S3_SECRET_KEY_FILE' infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- Repository contracts:
  원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- Tempo image, config, retention, SeaweedFS bucket, metrics generator,
  remote_write, route, secret reference, OTLP receiver가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Exceptions

### Exceptions

- Retention, bucket, sampling, remote_write, route, secret reference 예외는
  사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Tempo runbook에서 최소 조치와 rollback
  evidence를 기록한다.

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0049-tempo.md)
- [Recovery runbook](../runbooks/0049-tempo.md)
