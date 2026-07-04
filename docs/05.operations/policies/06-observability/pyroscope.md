---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/pyroscope.md -->

# Pyroscope Operations Policy

## Overview

이 정책은 Pyroscope continuous profiling service의 ingestion, filesystem
storage, capacity boundary, label/cardinality, route, health 기준을 정의한다.
사용 흐름은 Pyroscope guide가, 장애 대응 절차는 Pyroscope runbook이
담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/pyroscope` compose와
`config/pyroscope.yaml`에 선언된 Pyroscope 운영 기준을 다룬다.

- **Systems**: compose service `pyroscope`, container `infra-pyroscope`, image `grafana/pyroscope:2.1.0`, config `infra/06-observability/pyroscope/config/pyroscope.yaml`, volume `pyroscope-data`
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Pyroscope service는 `template-infra-med`, image
    `grafana/pyroscope:2.1.0`, read-only config mount, persistent
    `pyroscope-data` volume을 유지한다.
  - Runtime command는 `-config.file=/etc/pyroscope/pyroscope.yaml`와
    `-config.expand-env=true`를 유지한다.
  - HTTP/query/health surface는 `${PYROSCOPE_PORT:-4040}`와 `/ready`
    healthcheck를 기준으로 한다.
  - Storage backend는 local filesystem backend
    `storage.filesystem.dir: /var/lib/pyroscope`를 사용한다.
  - Compactor data directory는 `/var/lib/pyroscope/compactor`를 유지한다.
  - Analytics reporting은 `reporting_enabled: false`를 유지한다.
  - `self_profiling.disable_push: true`와 `multitenancy_enabled: false`를
    유지한다.
  - Ingestion limits are `ingestion_rate_mb: 16`,
    `ingestion_burst_size_mb: 32`, `max_label_name_length: 1024`,
    `max_label_value_length: 2048`, and `max_label_names_per_series: 30`.
  - Profile labels must avoid high-cardinality or secret-bearing values.
  - Pyroscope route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
  - 고정 retention 기간은 현재 `pyroscope.yaml`에 선언되어 있지 않다. 보관
    기간 변경은 config/capacity 검증과 [retention policy](./01.retention.md)
    갱신을 함께 요구한다.
- **Allowed**:
  - Development/debug 상황에서 임시 고빈도 profiling을 사용할 수 있으나,
    CPU/storage 영향과 rollback note를 남긴다.
  - 새 profile source 또는 Alloy forwarding 변경은 Pyroscope/Grafana
    datasource 확인과 함께 검증한다.
- **Disallowed**:
  - PII, password, token, credential 값을 profile labels 또는 profile payload에
    기록하는 행위
  - Request ID, user ID 같은 high-cardinality 값을 label로 승격하는 행위
  - 승인 없이 route, storage backend, ingestion limits, image version,
    persistent volume, config path를 runtime에서 변경하는 행위
  - 운영 환경에서 근거 없이 high-overhead block/mutex profiling을 상시 활성화하는 행위

## Exceptions

- Retention, storage backend, ingestion limits, profile source, route 예외는
  사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Pyroscope runbook에서 최소 조치와
  rollback evidence를 기록한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-infra-med|image: grafana/pyroscope:2.1.0|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml`
- Pyroscope config:
  `rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml`
- Repository contracts:
  `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Pyroscope image, config, storage backend, ingestion limits, profile source,
  route, healthcheck, retention/capacity policy가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/pyroscope.md)
- [Recovery runbook](../../runbooks/06-observability/pyroscope.md)
- [Retention policy](./01.retention.md)
