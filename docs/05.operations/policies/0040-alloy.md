---
title: "Alloy Operations Policy"
version: "1.0.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0040"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Alloy Operations Policy

## Overview

이 정책은 Grafana Alloy collector의 telemetry ingestion, discovery,
relabeling, exporter, route, health, configuration boundary를 정의한다.
사용 흐름은 Alloy guide가, 장애 대응 절차는 Alloy runbook이 담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/alloy` compose와
`config/config.alloy`에 선언된 Alloy 운영 기준을 다룬다.

- **Systems**: compose service `alloy`, container `infra-alloy`, image [Compose image declaration](../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/alloy/config/config.alloy`, volume `alloy-data`, Docker socket/container log read-only mounts
- **Environments**: 로컬·개발·홈랩 운영

## Controls

- **Required**:
  - Alloy configuration은
    `ALLOY_CONFIG_FILE`이 선택하는 tracked `config.alloy` 또는
    `config.home.alloy`에서 관리한다. 두 지원 파일을 각각 검증한다.
  - Alloy service는 `template-infra-med`, image [Compose image declaration](../../../infra/06-observability/docker-compose.yml),
    tmpfs `/tmp` and `/run`, read-only config mount, read-only Docker
    container/socket mounts, persistent `alloy-data` volume을 유지한다.
  - OTLP ingress는 gRPC `4317`과 HTTP `4318`을 사용한다.
  - Alloy UI/health endpoint는 `${ALLOY_PORT:-12345}`와 `/-/healthy`
    healthcheck를 기준으로 한다.
  - Docker discovery는 Compose project `hy-home-infra` label의 targets만 유지한다. Network-name matching으로 이 경계를 대체하지 않는다.
  - Docker log labels는 `service_name`, `container_name`, `compose_project`,
    `env`, `scope`를 기준으로 하고, observability infrastructure services는
    `scope=infra`로 relabel한다.
  - Logs pipeline은 `loki.source.docker`에서 `loki.write.local_loki`로
    전달하고, Loki endpoint는 `http://loki:3100/loki/api/v1/push`를 사용한다.
  - Alloy self metrics는 Prometheus job `alloy` 한 곳에서 scrape한다.
    중복 self remote-write로 동일 series를 생성하지 않는다.
  - Traces pipeline은 `otelcol.receiver.otlp` -> `otelcol.processor.batch` ->
    `otelcol.exporter.otlp.tempo` 흐름을 유지하고, Tempo endpoint는
    `tempo:4317`을 사용한다.
  - Pyroscope forwarding은 `pyroscope.write.local_pyroscope` endpoint
    `http://pyroscope:4040`로 선언한다. 현재 두 config 선택지의 Go/SeaweedFS
    scrape sources를 유지하고 추가·변경은 config/evidence 변경으로 처리한다.
  - Alloy route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`
    middleware chain을 유지한다.
- **Allowed**:
  - 새 application instrumentation은 OTLP를 우선 사용한다.
  - 새 Docker relabel rule이나 exporter 추가는 guide/runbook 영향과 downstream
    backend readiness를 함께 검증한다.
  - Pipeline graph 확인은 Alloy UI에서 수행하되, 변경 승인 기준은 git diff와
    local validation evidence로 둔다.
- **Disallowed**:
  - Docker socket/container log mount를 read-write로 전환하는 행위
  - high-cardinality 또는 secret-bearing 값을 label로 승격하는 행위
  - 승인 없이 OTLP ports, exporter endpoints, route middleware, Docker
    discovery project filter, image version을 runtime에서 변경하는 행위
  - profile source가 연결되지 않았는데 profiling ingestion이 active라고
    선언하는 행위

### Lifecycle and data controls

- Alloy를 HOME으로 유지하고 socket 읽기 전용과 선언 network/gateway 경계를 보존한다.
- 설정이 영속 기준이다. 사용 component를 확인한 상태만 백업하며 전송 중 telemetry의 정확한 복구를 약속하지 않는다.
- Upgrade 전에 대상 버전 config, 허용 손실과 각 backend 전달을 검증한다. Writer만으로 profile 수집을 증명하지 않는다.
- 제거에는 producer 이전, 관측 공백 승인, route/port 폐쇄와 확인된 WAL/checkpoint 처리가 필요하다.

## Exceptions

- Pipeline, exporter, Docker discovery, route, mount 예외는 사용자 승인과
  관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Alloy runbook에서 최소 조치와 rollback
  evidence를 기록한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-infra-med|image: grafana/alloy:|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`
- Alloy pipeline config:
  `rg -n 'discovery.docker|hy-home-infra|loki.source.docker|loki.write|pyroscope.scrape|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy`
- Repository contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Review Cadence

- Alloy image, config, Docker discovery, relabel rules, exporter endpoint,
  mounted paths, OTLP ports, route, healthcheck가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0040-alloy.md) (`GDE-0040`), [Runbook](../runbooks/0040-alloy.md) (`RUN-0040`)

## Related Documents

- [Runtime image declarations](../../../infra/06-observability/docker-compose.yml)
- [Operations index](../README.md)
- [Usage guide](../guides/0040-alloy.md)
- [Recovery runbook](../runbooks/0040-alloy.md)
