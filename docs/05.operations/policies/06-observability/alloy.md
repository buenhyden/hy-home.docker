---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/alloy.md -->

# Alloy Operations Policy

## Overview

이 정책은 Grafana Alloy collector의 telemetry ingestion, discovery,
relabeling, exporter, route, health, configuration boundary를 정의한다.
사용 흐름은 Alloy guide가, 장애 대응 절차는 Alloy runbook이 담당한다.

## Policy Scope

이 정책은 current `infra/06-observability/alloy` compose와
`config/config.alloy`에 선언된 Alloy 운영 기준을 다룬다.

- **Systems**: compose service `alloy`, container `infra-alloy`, image `grafana/alloy:v1.17.1`, config `infra/06-observability/alloy/config/config.alloy`, volume `alloy-data`, Docker socket/container log read-only mounts
- **Agents**: Operators, SREs, AI agents following repo-local governance
- **Environments**: local, development, homelab operations

## Controls

- **Required**:
  - Alloy configuration은
    `infra/06-observability/alloy/config/config.alloy`에서 관리한다.
  - Alloy service는 `template-infra-med`, image `grafana/alloy:v1.17.1`,
    tmpfs `/tmp` and `/run`, read-only config mount, read-only Docker
    container/socket mounts, persistent `alloy-data` volume을 유지한다.
  - OTLP ingress는 gRPC `4317`과 HTTP `4318`을 사용한다.
  - Alloy UI/health endpoint는 `${ALLOY_PORT:-12345}`와 `/-/healthy`
    healthcheck를 기준으로 한다.
  - Docker discovery는 `project_net|infra_net` network targets만 유지한다.
  - Docker log labels는 `service_name`, `container_name`, `compose_project`,
    `env`, `scope`를 기준으로 하고, observability infrastructure services는
    `scope=infra`로 relabel한다.
  - Logs pipeline은 `loki.source.docker`에서 `loki.write.local_loki`로
    전달하고, Loki endpoint는 `http://loki:3100/loki/api/v1/push`를 사용한다.
  - Metrics pipeline은 `prometheus.exporter.self`와
    `prometheus.remote_write.local_prom`을 사용하고, Prometheus endpoint는
    `http://prometheus:9090/api/v1/write`를 사용한다.
  - Traces pipeline은 `otelcol.receiver.otlp` -> `otelcol.processor.batch` ->
    `otelcol.exporter.otlp.tempo` 흐름을 유지하고, Tempo endpoint는
    `tempo:4317`을 사용한다.
  - Pyroscope forwarding은 `pyroscope.write.local_pyroscope` endpoint
    `http://pyroscope:4040`로 선언하며, profile source 추가는 별도
    config/evidence 변경으로 처리한다.
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
    discovery network filter, image version을 runtime에서 변경하는 행위
  - profile source가 연결되지 않았는데 profiling ingestion이 active라고
    선언하는 행위

## Exceptions

- Pipeline, exporter, Docker discovery, route, mount 예외는 사용자 승인과
  관련 plan/task evidence가 있을 때만 허용한다.
- 장애 대응 중 임시 조치가 필요하면 Alloy runbook에서 최소 조치와 rollback
  evidence를 기록한다.

## Verification

- Compose service boundary:
  `rg -n 'service: template-infra-med|image: grafana/alloy:v1.17.1|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`
- Alloy pipeline config:
  `rg -n 'discovery.docker|project_net\\|infra_net|loki.source.docker|loki.write|prometheus.remote_write|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy`
- Repository contracts:
  `bash scripts/validation/check-repo-contracts.sh`

## Review Cadence

- Alloy image, config, Docker discovery, relabel rules, exporter endpoint,
  mounted paths, OTLP ports, route, healthcheck가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/alloy.md)
- [Recovery runbook](../../runbooks/06-observability/alloy.md)
