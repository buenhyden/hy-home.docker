---
title: "Retention and Performance Policies"
version: "1.0.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0048"
parent_ids:
- "AD-0006"
created: "2026-03-25"
---

# Retention and Performance Policies

## Overview

이 정책은 `06-observability` tier의 metrics, logs, traces, profiles 보관
경계와 performance guardrail을 정의한다. 현재 storage 구현과 요구되는 retention을 구분하며, external long-term archive
또는 S3 Glacier 같은 미구현 보관 계층은 승인된 config 변경과 task evidence
없이는 active 요구사항으로 취급하지 않는다.

## Policy Scope

이 정책은 observability stack의 storage, retention, cardinality, resource,
backup 책임 경계를 다룬다.

- **Systems**: Prometheus local TSDB, Loki SeaweedFS bucket `loki-bucket`, Tempo SeaweedFS bucket `tempo-bucket`, Pyroscope local filesystem backend `/var/lib/pyroscope`, Grafana dashboard JSON assets
- **Environments**: 로컬·개발·홈랩 운영

## Controls

- **Required**:
  - Prometheus metrics는 local TSDB와 Prometheus policy의 retention/volume
    boundary를 따른다. External long-term metric storage는 현재 tracked
    compose에 선언되어 있지 않다.
  - Loki logs는 `infra/06-observability/loki/config/loki-config.yaml`의
    `retention_enabled: true`와 `retention_period: 168h`를 기준으로 한다.
  - Tempo traces는 `block_retention: 24h`와 `compacted_block_retention: 1h`를
    요구한다. 현재 `tempo.yaml`에는 해당 설정이 없어 미준수다. 선언된
    upstream의 기본값은 24h 요구를 충족하지 않는다. 별도 승인된 구현 변경과
    실제 삭제 검증 전에는 retention compliant로 판정하지 않는다.
  - Pyroscope profiles는 local filesystem backend를 사용한다. 현재
    `pyroscope.yaml`에는 고정 retention period가 선언되어 있지 않으므로
    capacity 추이와 storage usage를 점검한다.
  - Grafana dashboard backup은 `infra/06-observability/grafana/dashboards/`
    JSON assets를 version-controlled source로 유지한다.
  - High-cardinality labels(user IDs, IP addresses, request IDs 등)는
    metrics/log labels에 직접 추가하지 않는다.
- **Allowed**:
  - Loki/Tempo SeaweedFS snapshot 또는 replication은 SeaweedFS owning policy (POL-0024)와
    runbook evidence가 있을 때 검토한다.
  - Retention, resource, storage 변경은 관련 config diff, capacity impact,
    rollback evidence를 포함한 승인된 active Plan과 Task가 있을 때 수행한다.
- **Disallowed**:
  - 문서만 수정해서 runtime retention이 변경된 것처럼 선언하는 행위
  - 구현되지 않은 external archive를 active control로 표기하는 행위
  - secret 값, credential, token, certificate 원문을 정책 문서나 검증
    evidence에 기록하는 행위

### Implementation and recovery gaps

Loki marker는 영속 `/loki` 밖의 `/tmp/loki/compactor`에 있고 object-store prefix도 없다. 재생성 시 marker가 사라질 수 있으며 `loki-data`만 백업하면 보존되지 않는다. 168h 요구와 지속적인 삭제 처리는 유지하되 이 결함은 별도 구현 변경으로 닫아야 한다. 동일 컨테이너 재시작과 재생성의 상태 영향을 구분한다.

Prometheus는 시간·크기 override가 없어 선언 릴리스의 15d 기본값을 따른다. 이는 실제 보존 이력을 관찰한 결과가 아니다. Pyroscope는 고정 기간이 없고 기본값·disk pressure 동작이 무기한 보존을 약속하지 않는다. Pushgateway는 process restart 때 metric을 잃는다. 어느 것도 승인된 backup/archive를 대신하지 않는다.

## Exceptions

- Retention, archive, resource cap 예외는 사용자 승인과 관련 plan/task
  evidence가 있을 때만 허용한다.
- 긴급 장애 대응으로 임시 보관 또는 삭제 정책을 조정한 경우, 변경 후
  incident 또는 task evidence에 원인, 범위, rollback 상태를 기록한다.

## Verification

- Loki retention config:
  `rg -n 'retention_enabled: true|retention_period: 168h' infra/06-observability/loki/config/loki-config.yaml`
- Tempo 필수값 점검(현재 일치하지 않으며 구현 결함으로 기록하고 PASS로 처리하지 않는다):
  `rg -n 'block_retention: 24h|compacted_block_retention: 1h' infra/06-observability/tempo/config/tempo.yaml`
- Pyroscope의 고정 retention 미선언 경계:
  `rg -n 'fixed retention period is not declared|고정 7일 retention 설정이 없다' infra/06-observability/pyroscope/README.md docs/05.operations/guides/0047-pyroscope.md`
- Documentation contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Review Cadence

- 서비스 storage, retention, resource cap, SeaweedFS bucket, dashboard provisioning
  config가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: none — no Guide or Runbook shares number `0048`.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Observability policy index](../README.md)
- [Prometheus policy](0045-prometheus.md)
- [Loki policy](0043-loki.md)
- [Tempo policy](0049-tempo.md)
- [Pyroscope policy](0047-pyroscope.md)
- [Loki guide](../guides/0043-loki.md)
- [Tempo runbook](../runbooks/0049-tempo.md)
