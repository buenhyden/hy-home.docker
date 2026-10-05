---
title: "Pyroscope Operations Policy"
version: "1.0.5"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0047"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Pyroscope Operations Policy

## Overview

### Overview

이 정책은 Pyroscope continuous profiling service의 ingestion, filesystem
storage, capacity boundary, label/cardinality, route, health 기준을 정의한다.
사용 흐름은 Pyroscope guide가, 장애 대응 절차는 Pyroscope runbook이
담당한다.

## Scope

### Policy Scope

이 정책은 current `infra/06-observability/pyroscope` compose와
`config/pyroscope.yaml`에 선언된 Pyroscope 운영 기준을 다룬다.

- **Systems**: compose service `pyroscope`, container `infra-pyroscope`, image [grafana/pyroscope image declaration](../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/pyroscope/config/pyroscope.yaml`, volume `pyroscope-data`
- **Environments**: 로컬·개발·홈랩 운영

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0047-pyroscope.md) (`GDE-0047`), [Runbook](../runbooks/0047-pyroscope.md) (`RUN-0047`)

## Rules

### Controls

- **Required**:
  - Pyroscope service는 `template-infra-med`, image
    [grafana/pyroscope image declaration](../../../infra/06-observability/docker-compose.yml), read-only config mount, persistent
    `pyroscope-data` volume을 유지한다.
  - Runtime command는 `-config.file=/etc/pyroscope/pyroscope.yaml`와
    `-config.expand-env=true`를 유지한다.
  - HTTP/query/health surface는 `${PYROSCOPE_PORT:-4040}`와 `/ready`
    healthcheck를 기준으로 하며, host port는 `127.0.0.1`에만 게시한다.
  - Storage backend는 local filesystem backend
    `storage.filesystem.dir: /var/lib/pyroscope`를 사용한다.
  - Compactor data directory는 `/var/lib/pyroscope/compactor`를 유지한다.
  - Analytics reporting은 `reporting_enabled: false`를 유지한다.
  - `self_profiling.disable_push: true`와 `multitenancy_enabled: false`를
    유지한다.
  - 입력 제한은 `ingestion_rate_mb: 16`, `ingestion_burst_size_mb: 32`, `max_label_name_length: 1024`, `max_label_value_length: 2048`, `max_label_names_per_series: 30`을 유지한다.
  - Profile label에 cardinality가 높은 값이나 secret이 포함된 값을 쓰지 않는다.
  - Pyroscope route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
  - 고정 retention 기간은 현재 `pyroscope.yaml`에 선언되어 있지 않다. 보관
    기간 변경은 config/capacity 검증과 [retention policy](0048-telemetry-retention.md)
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

### Lifecycle and data controls

- Pyroscope는 `HOME`이다. SPEC-0182 W6에서 소유자가 `profiling`을 HOME에 추가했다(POL-0078). `profiling`을 빼는 대상으로 전환할 때는 `HOME up`이 이미 실행 중인 컨테이너를 제거하지 않으므로 Pyroscope를 명시적으로 중지한다.
- Gateway 인증과 로컬 filesystem 경계를 유지한다. Profile source 없이 쓰기 대상만 설정한 것은 수집 증거가 아니다.
- 쓰기·서비스를 중지하거나 일관성을 검증한 snapshot으로만 백업한다. 격리 스토리지에서 rehearsal을 수행하며 과거·신규 조회와 producer label을 확인한다.
- 제거 전 producer·Grafana 참조를 정리하고 보존 여부를 결정하며 경로를 닫는다. `pyroscope-data` 삭제에는 명시적 승인이 필요하다.

### Profile storage and source limits

두 Alloy 설정에는 Go와 별도 SeaweedFS pprof source가 있다. 선택 파일·target과 제한된 profile query로 수신을 확인하며 writer/receiver readiness만으로 판정하지 않는다. Pyroscope는 선언 volume의 로컬 filesystem과 ingestion/cardinality 한도를 사용한다. 고정 retention은 없고 기본값·disk pressure 정리가 무기한 보존을 보장하지 않는다. 기간 요구는 별도 승인된 설정·용량 검토가 필요하다. wget 존재를 가정하지 않고 선언된 `profilecli ready` probe를 쓴다. Profile/config를 일관되게 보존하고 삭제는 POL-0048을 따른다.

### Verification

- Compose service boundary:
  `rg -n 'service: template-infra-med|image: grafana/pyroscope:|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml`
- Pyroscope config:
  `rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml`
- Repository contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- Pyroscope image, config, storage backend, ingestion limits, profile source,
  route, healthcheck, retention/capacity policy가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Exceptions

### Exceptions

- Retention, storage backend, ingestion limits, profile source, route 예외는
  사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Pyroscope runbook에서 최소 조치와
  rollback evidence를 기록한다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0047-pyroscope.md)
- [Recovery runbook](../runbooks/0047-pyroscope.md)
- [Retention policy](0048-telemetry-retention.md)
