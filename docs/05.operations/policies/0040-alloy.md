---
title: "Alloy Operations Policy"
version: "1.1.3"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "operations"
artifact_id: "POL-0040"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Alloy Operations Policy

## Overview

이 정책은 Grafana Alloy collector의 telemetry ingestion, discovery, relabeling, exporter, route, health, 설정 경계를 정의한다. 사용 흐름은 [GDE-0040](../guides/0040-alloy.md)이, 장애 대응 절차는 [RUN-0040](../runbooks/0040-alloy.md)이 맡는다.

## Scope

이 정책은 `infra/06-observability`의 Alloy Compose 서비스와 두 설정 파일에 선언된 운영 기준을 다룬다.

- **Systems**: compose service `alloy`, container `alloy`, image [Compose image declaration](../../../infra/06-observability/docker-compose.yml), 설정 `infra/06-observability/alloy/config/config.alloy`(기본 pipeline)와 `config.home.alloy`(기본 pipeline에 품질 metric 수신기 추가), secret `quality_otlp_token`, volume `alloy-data`, Docker socket/container log 읽기 전용 mount
- **Environments**: 로컬, 개발, 홈랩 운영

## Rules

- 설정은 `ALLOY_CONFIG_FILE`이 선택하는 tracked `config.alloy` 또는 `config.home.alloy`에서 관리한다. 두 지원 파일을 각각 검증한다.
- 서비스는 `template-infra-med`, image [Compose image declaration](../../../infra/06-observability/docker-compose.yml), tmpfs `/tmp`와 `/run`, 읽기 전용 config mount, 읽기 전용 Docker container/socket mount, 영속 `alloy-data` volume을 유지한다.
- OTLP 입력은 gRPC `4317`과 HTTP `4318`이며 trace만 받는다.
- `config.home.alloy`의 품질 metric 수신기는 HTTP `4319`와 bearer token secret `quality_otlp_token`을 쓰고 host에 publish하지 않는다. 식별 속성(`project_id`, `environment`, `service_name`, `instance`)과 k6 `condition` 등 허용 label만 남긴다.
- run별 relay는 internal network `quality_otlp_net`으로만 `alloy:4319`에 닿는다. 이 구간은 평문 HTTP hop이므로 수신기를 host나 다른 tier로 노출하지 않는다. `quality_otlp_net`에는 Alloy와 relay controller가 붙인 relay만 둔다.
- Alloy UI와 health endpoint는 `${ALLOY_PORT:-12345}`와 `/-/healthy` healthcheck를 기준으로 한다. Alloy route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware chain을 유지한다.
- Docker discovery는 Compose project `hy-home-infra` label의 target만 유지한다. network 이름 matching으로 이 경계를 대체하지 않는다.
- Docker log label은 `service_name`, `container_name`, `compose_project`, `env`, `scope`를 기준으로 하고 observability infrastructure 서비스는 `scope=infra`로 relabel한다.
- 로그 pipeline은 `loki.source.docker`에서 `loki.write.local_loki`로 전달하고 endpoint는 `http://loki:3100/loki/api/v1/push`를 쓴다.
- Alloy 자체 metric은 Prometheus job `alloy` 한 곳에서 scrape한다. 중복 self remote-write로 같은 series를 만들지 않는다.
- trace pipeline은 `otelcol.receiver.otlp` → `otelcol.processor.batch` → `otelcol.exporter.otlp.tempo`를 유지하고 Tempo endpoint는 `tempo:4317`을 쓴다.
- Pyroscope forwarding은 `pyroscope.write.local_pyroscope`(`http://pyroscope:4040`)로 선언한다. 두 설정의 Go/SeaweedFS scrape source를 유지하고, 추가나 변경은 config와 evidence 변경으로 처리한다.
- node-exporter는 SPEC-0225부터 host network에서 실행한다. Alloy는 `extra_hosts`의 `node-exporter:10.250.5.1`로 pprof 대상 이름을 유지한다.

허용:

- 새 application instrumentation은 OTLP를 우선 쓴다.
- 새 Docker relabel rule이나 exporter 추가는 guide, runbook 영향과 downstream backend readiness를 함께 검증한다.
- Pipeline graph 확인은 Alloy UI에서 하되, 변경 승인 기준은 git diff와 로컬 검증 evidence다.

금지:

- Docker socket이나 container log mount를 read-write로 바꾸는 행위
- high-cardinality 또는 secret이 담긴 값을 label로 승격하는 행위
- 승인 없이 OTLP port, exporter endpoint, route middleware, Docker discovery project filter, image version을 runtime에서 바꾸는 행위
- profile source가 연결되지 않았는데 profiling ingestion이 active라고 선언하는 행위

### Lifecycle and data controls

- Alloy를 HOME으로 유지하고 socket 읽기 전용과 선언된 network, gateway 경계를 보존한다.
- 설정이 영속 기준이다. 사용 component를 확인한 상태만 백업하며 전송 중 telemetry의 정확한 복구를 약속하지 않는다.
- Upgrade 전에 대상 버전 config, 허용 손실, 각 backend 전달을 검증한다. writer만으로 profile 수집을 증명하지 않는다.
- 제거에는 producer 이전, 관측 공백 승인, route/port 폐쇄, 확인된 WAL/checkpoint 처리가 필요하다.

## Exceptions

pipeline, exporter, Docker discovery, route, mount 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다. 장애 대응 중 임시 조치가 필요하면 [RUN-0040](../runbooks/0040-alloy.md)에서 최소 조치와 rollback evidence를 기록한다. 책임 소유자는 **@buenhyden**이다. 예외와 통제 변경에는 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Verification

- Compose 경계, pipeline 경계, 품질 metric 수신기 확인 명령은 [GDE-0040 Common Checks](../guides/0040-alloy.md#common-checks)와 [RUN-0040 절차](../runbooks/0040-alloy.md#procedure)가 소유한다.
- Repository contracts: 원격 PR public `changed` 검사 ([quality policy](../../../.agents/governance/quality-standards.md#canonical-delivery-phase-matrix))

### Review Cadence

- Alloy image, config, Docker discovery, relabel rule, exporter endpoint, mount 경로, OTLP port, route, healthcheck가 바뀔 때 검토한다.
- 정기 검토는 분기마다 한다.

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0040-alloy.md) (`GDE-0040`), [Runbook](../runbooks/0040-alloy.md) (`RUN-0040`)

## Related Documents

- [Runtime image declarations](../../../infra/06-observability/docker-compose.yml)
- [Operations index](../README.md)
- [Usage guide](../guides/0040-alloy.md)
- [Recovery runbook](../runbooks/0040-alloy.md)
