---
title: Retention and Performance Policies
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0048
parent_ids:
  - AD-0006
created: 2026-03-25
updated: 2026-09-01
---
<!-- Target: docs/05.operations/catalog/06-observability/0048-telemetry-retention/policy.md -->

# Retention and Performance Policies

## Overview

이 정책은 `06-observability` tier의 metrics, logs, traces, profiles 보관
경계와 performance guardrail을 정의한다. 현재 compose/config에 선언된
storage와 retention만 active 기준으로 관리하며, external long-term archive
또는 S3 Glacier 같은 미구현 보관 계층은 승인된 config 변경과 task evidence
없이는 active 요구사항으로 취급하지 않는다.

## Policy Scope

이 정책은 observability stack의 storage, retention, cardinality, resource,
backup 책임 경계를 다룬다.

- **Systems**: Prometheus local TSDB, Loki MinIO bucket `loki-bucket`, Tempo MinIO bucket `tempo-bucket`, Pyroscope local filesystem backend `/var/lib/pyroscope`, Grafana dashboard JSON assets
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Prometheus metrics는 local TSDB와 Prometheus policy의 retention/volume
    boundary를 따른다. External long-term metric storage는 현재 tracked
    compose에 선언되어 있지 않다.
  - Loki logs는 `infra/06-observability/loki/config/loki-config.yaml`의
    `retention_enabled: true`와 `retention_period: 168h`를 기준으로 한다.
  - Tempo traces는 `infra/06-observability/tempo/config/tempo.yaml`의
    `block_retention: 24h`와 `compacted_block_retention: 1h`를 기준으로 한다.
  - Pyroscope profiles는 local filesystem backend를 사용한다. 현재
    `pyroscope.yaml`에는 고정 retention period가 선언되어 있지 않으므로
    capacity 추이와 storage usage를 점검한다.
  - Grafana dashboard backup은 `infra/06-observability/grafana/dashboards/`
    JSON assets를 version-controlled source로 유지한다.
  - High-cardinality labels(user IDs, IP addresses, request IDs 등)는
    metrics/log labels에 직접 추가하지 않는다.
- **Allowed**:
  - Loki/Tempo MinIO snapshot 또는 replication은 MinIO owning policy와
    runbook evidence가 있을 때 검토한다.
  - Retention, resource, storage 변경은 관련 config diff, capacity impact,
    rollback evidence를 포함한 승인된 active Plan과 Task가 있을 때 수행한다.
- **Disallowed**:
  - 문서만 수정해서 runtime retention이 변경된 것처럼 선언하는 행위
  - 구현되지 않은 external archive를 active control로 표기하는 행위
  - secret 값, credential, token, certificate 원문을 정책 문서나 검증
    evidence에 기록하는 행위

## Exceptions

- Retention, archive, resource cap 예외는 사용자 승인과 관련 plan/task
  evidence가 있을 때만 허용한다.
- 긴급 장애 대응으로 임시 보관 또는 삭제 정책을 조정한 경우, 변경 후
  incident 또는 task evidence에 원인, 범위, rollback 상태를 기록한다.

## Verification

- Loki retention config:
  `rg -n 'retention_enabled: true|retention_period: 168h' infra/06-observability/loki/config/loki-config.yaml`
- Tempo retention config:
  `rg -n 'block_retention: 24h|compacted_block_retention: 1h' infra/06-observability/tempo/config/tempo.yaml`
- Pyroscope no-fixed-retention boundary:
  `rg -n 'fixed retention period is not declared|고정 7일 retention 설정이 없다' infra/06-observability/pyroscope/README.md docs/05.operations/catalog/06-observability/0047-pyroscope/guide.md`
- Documentation contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

## Review Cadence

- 서비스 storage, retention, resource cap, MinIO bucket, dashboard provisioning
  config가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Traceability

- Declared parent: [Observability Architecture Description](../../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: none — `06-observability/0048-telemetry-retention` holds this document alone.

## Related Documents

- [Operations index](../../../README.md)
- [Observability policy index](../../../README.md)
- [Prometheus policy](../0045-prometheus/policy.md)
- [Loki policy](../0043-loki/policy.md)
- [Tempo policy](../0049-tempo/policy.md)
- [Pyroscope policy](../0047-pyroscope/policy.md)
- [Loki guide](../0043-loki/guide.md)
- [Tempo runbook](../0049-tempo/runbook.md)
