---
title: "Tempo Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "POL-0049"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Tempo Operations Policy

## Overview

이 정책은 Tempo distributed tracing backend의 trace ingestion, SeaweedFS S3
storage, block retention, metrics generator, secret boundary, protected route를
정의한다. 사용 흐름은 Tempo guide가, 장애 대응 절차는 Tempo runbook이
담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/tempo` compose와
`config/tempo.yaml`에 선언된 Tempo 운영 기준을 다룬다.

- **Systems**: compose service `tempo`, container `infra-tempo`, image [hy/tempo image declaration](../../../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/tempo/config/tempo.yaml`, volume `tempo-data`, SeaweedFS bucket `tempo-bucket`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Tempo service는 `template-stateful-high`, image
    [hy/tempo image declaration](../../../../../infra/06-observability/docker-compose.yml), user `10001:10001`, read-only config mount,
    persistent `tempo-data` volume을 유지한다.
  - Custom Tempo image는 upstream [grafana/tempo image declaration](../../../../../infra/06-observability/tempo/Dockerfile), non-root user
    `10001:10001`, and `/docker-entrypoint.sh` secret guard를 유지한다.
  - OTLP receiver는 internal gRPC `4317`과 HTTP `4318` endpoints를 유지한다.
  - HTTP/query/health surface는 `${TEMPO_PORT:-3200}`와 `/ready` healthcheck를
    기준으로 한다.
  - Trace storage는 SeaweedFS S3 backend, bucket `tempo-bucket`, endpoint
    `seaweedfs-s3:8333`, `insecure: true`를 사용한다.
  - `S3_ACCESS_KEY`은 environment reference로, `S3_SECRET_KEY`는
    Docker Secret `seaweedfs_s3_tempo_secret_key`로만 주입한다.
  - Block retention은 `block_retention: 24h`,
    `compacted_block_retention: 1h`를 기준으로 한다.
  - Metrics generator는 `span_metrics`, `service_graphs`, `local_blocks`를
    활성화하고 Prometheus `http://prometheus:9090/api/v1/write`로
    `remote_write` 한다.
  - Tempo route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
- **Allowed**:
  - Development/debug 상황의 sampling 또는 log-level 변경은 plan/task
    evidence와 rollback note가 있을 때만 허용한다.
  - 장기 분석이 필요하면 retention policy와 SeaweedFS owning policy/runbook을
    함께 갱신한다.
- **Disallowed**:
  - PII, password, token, credential 값을 trace attributes에 기록하는 행위
  - Secret guard 없이 SeaweedFS-backed Tempo image 또는 entrypoint를 변경하는 행위
  - 승인 없이 bucket, retention, metrics generator processors, remote_write
    endpoint, route middleware, image version을 runtime에서 변경하는 행위

### Lifecycle and data controls

- Keep Tempo `OPTIONAL`; runtime presence does not reclassify it. A future HOME-only transition must explicitly stop preexisting Tempo.
- Treat `tempo-bucket`, local WAL/temp state, config, and matching SeaweedFS credentials as a coordinated recovery set; the object-store owner performs bucket backup/restore.
- Quiesce OTLP ingestion before consistency capture. Rehearse with isolated bucket/path and verify WAL replay, historical/new trace queries, metrics-generator behavior, and Alloy/Grafana integration.
- Removal requires producer/exporter migration, retention decision, credentials/route cleanup, and explicit approval before deleting object or local data.

## Exceptions

- Retention, bucket, sampling, remote_write, route, secret reference 예외는
  사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Tempo runbook에서 최소 조치와 rollback
  evidence를 기록한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: hy/tempo:|user: .10001:10001.|tempo-data|TEMPO_PORT|seaweedfs_s3_tempo_secret_key|tempo.middlewares' infra/06-observability/docker-compose.yml`
- Tempo config:
  `rg -n 'block_retention: 24h|compacted_block_retention: 1h|metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: seaweedfs-s3:8333|secret_key: \\$\\{S3_SECRET_KEY\\}' infra/06-observability/tempo/config/tempo.yaml`
- Custom image secret guard:
  `rg -n 'FROM grafana/tempo:|USER 10001:10001|missing secret: S3_SECRET_KEY_FILE' infra/06-observability/tempo/{Dockerfile,docker-entrypoint.sh}`
- Repository contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- Tempo image, config, retention, SeaweedFS bucket, metrics generator,
  remote_write, route, secret reference, OTLP receiver가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Traceability

- Declared parent: [Observability Architecture Description](../../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](guide.md) (`GDE-0049`), [Runbook](runbook.md) (`RUN-0049`)

## Related Documents

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
