---
title: "Alloy Operations Policy"
version: "1.2.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-18"
layer: "operations"
artifact_id: "POL-0040"
parent_ids:
- "AD-0006"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# Alloy Operations Policy

## Purpose and Scope

### Objective

이 정책은 Grafana Alloy collector의 telemetry ingestion, discovery, relabeling, exporter, route, health, 설정 경계를 정의한다. 사용 흐름은 [GDE-0040](../../guides/07-observability/0040-alloy.md)이, 장애 대응 절차는 [RUN-0040](../../runbooks/07-observability/0040-alloy.md)이 맡는다.

#### Authority

- Declared parent: [Observability Architecture Description](../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)

- [Runtime image declarations](../../../../infra/06-observability/docker-compose.yml)

### Applies To

이 정책은 `infra/06-observability`의 Alloy Compose 서비스와 두 설정 파일에 선언된 운영 기준을 다룬다.

- **Systems**: compose service `alloy`, container `alloy`, image [Compose image declaration](../../../../infra/06-observability/docker-compose.yml), 설정 `infra/06-observability/alloy/config/config.alloy`(기본 pipeline)와 `config.home.alloy`(기본 pipeline에 품질 metric 수신기 추가), secret `quality_otlp_token`, volume `alloy-data`, Docker socket/container log 읽기 전용 mount
- **Environments**: 로컬, 개발, 홈랩 운영

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0040-R1 | 항상 | 필수: 설정은 `ALLOY_CONFIG_FILE`이 선택하는 tracked `config.alloy` 또는 `config.home.alloy`에서 관리하고 두 지원 파일을 각각 검증 | none | none |
| POL-0040-R2 | 항상 | 필수: `template-infra-med`, tmpfs `/tmp`/`/run`, 읽기 전용 config mount, 읽기 전용 Docker container/socket mount, 영속 `alloy-data` volume 유지 | none | none |
| POL-0040-R3 | 항상 | 필수: OTLP 입력은 gRPC `4317`/HTTP `4318`이며 trace만 수신 | none | none |
| POL-0040-R4 | `config.home.alloy` 품질 metric 수신기 사용 시 | 필수: HTTP `4319`와 bearer token secret `quality_otlp_token` 사용 | none | none |
| POL-0040-R5 | `config.home.alloy` 품질 metric 수신기 사용 시 | 금지: 품질 metric 수신기를 host에 publish | none | none |
| POL-0040-R6 | `config.home.alloy` 품질 metric 수신기 사용 시 | 필수: 식별 속성(`project_id`/`environment`/`service_name`/`instance`)과 k6 `condition` 등 허용 label만 유지 | none | none |
| POL-0040-R7 | 항상 | 필수: run별 relay는 internal network `quality_otlp_net`으로만 `alloy:4319`에 접근 | none | none |
| POL-0040-R8 | 항상 | 금지: 수신기를 host나 다른 tier로 노출 | none | none |
| POL-0040-R9 | 항상 | 필수: `quality_otlp_net`에는 Alloy와 relay controller가 붙인 relay만 배치 | none | none |
| POL-0040-R10 | 항상 | 필수: UI/health는 `${ALLOY_PORT:-12345}`와 `/-/healthy` healthcheck 기준 | none | none |
| POL-0040-R11 | 항상 | 필수: route는 `gateway-standard-chain@file,sso-errors@file,sso-auth@file` middleware chain 유지 | none | none |
| POL-0040-R12 | 항상 | 필수: Docker discovery는 Compose project `hy-home-infra` label의 target만 유지 | none | none |
| POL-0040-R13 | 항상 | 금지: network 이름 matching으로 Docker discovery 경계 대체 | none | none |
| POL-0040-R14 | 항상 | 필수: Docker log label은 `service_name`/`container_name`/`compose_project`/`env`/`scope` 기준이며 observability infrastructure 서비스는 `scope=infra`로 relabel | none | none |
| POL-0040-R15 | 항상 | 필수: 로그는 `loki.source.docker`에서 `loki.write.local_loki`(`http://loki:3100/loki/api/v1/push`)로 전달 | none | none |
| POL-0040-R16 | 항상 | 필수: Alloy 자체 metric은 Prometheus job `alloy` 한 곳에서 scrape | none | none |
| POL-0040-R17 | 항상 | 금지: 중복 self remote-write로 같은 series 생성 | none | none |
| POL-0040-R18 | 항상 | 필수: trace pipeline `otelcol.receiver.otlp` → `otelcol.processor.batch` → `otelcol.exporter.otlp.tempo`(`tempo:4317`) 유지 | none | none |
| POL-0040-R19 | 항상 | 필수: Pyroscope forwarding은 `pyroscope.write.local_pyroscope`(`http://pyroscope:4040`)로 선언 | none | none |
| POL-0040-R20 | 항상 | 필수: 두 설정의 Go/SeaweedFS scrape source를 유지하고 추가나 변경은 config와 evidence 변경으로 처리 | none | none |
| POL-0040-R21 | 항상 | 필수: node-exporter는 host network에서 실행하고 Alloy는 `extra_hosts`의 `node-exporter:10.250.5.1`로 pprof 대상 이름 유지 | none | none |
| POL-0040-R22 | 새 application instrumentation 시 | 필수: OTLP를 우선 사용 | none | none |
| POL-0040-R23 | 새 Docker relabel rule이나 exporter 추가 시 | 필수: guide/runbook 영향과 downstream backend readiness를 함께 검증 | none | none |
| POL-0040-R24 | 항상 | 허용: Alloy UI에서 pipeline graph 확인 | none | none |
| POL-0040-R25 | 항상 | 필수: 변경 승인 기준은 git diff와 로컬 검증 evidence | none | git diff / 로컬 검증 evidence |
| POL-0040-R26 | 항상 | 금지: Docker socket이나 container log mount를 read-write로 변경 | 수동 | none |
| POL-0040-R27 | 항상 | 금지: high-cardinality 또는 secret이 담긴 값을 label로 승격 | 수동 | none |
| POL-0040-R28 | 항상 | 금지: 승인 없이 OTLP port/exporter endpoint/route middleware/Docker discovery project filter/image version을 runtime에서 변경 | 수동 | none |
| POL-0040-R29 | 항상 | 금지: profile source가 연결되지 않았는데 profiling ingestion이 active라고 선언 | 수동 | none |
| POL-0040-R30 | 항상 | 필수: Alloy를 HOME으로 유지하고 socket 읽기 전용과 선언된 network/gateway 경계 보존 | none | none |
| POL-0040-R31 | 항상 | 필수: 설정이 영속 기준이며 사용 component를 확인한 상태만 백업 | none | none |
| POL-0040-R32 | 항상 | 금지: 전송 중 telemetry의 정확한 복구 약속 | none | none |
| POL-0040-R33 | upgrade 전 | 필수: 대상 버전 config/허용 손실/각 backend 전달 검증 | none | none |
| POL-0040-R34 | 항상 | 금지: writer만으로 profile 수집을 증명 | none | none |
| POL-0040-R35 | 제거 시 | 필수: producer 이전, 관측 공백 승인, route/port 폐쇄, 확인된 WAL/checkpoint 처리 | 수동 | none |

- 설정은 `ALLOY_CONFIG_FILE`이 선택하는 tracked `config.alloy` 또는 `config.home.alloy`에서 관리한다. 두 지원 파일을 각각 검증한다.
- 서비스는 `template-infra-med`, image [Compose image declaration](../../../../infra/06-observability/docker-compose.yml), tmpfs `/tmp`와 `/run`, 읽기 전용 config mount, 읽기 전용 Docker container/socket mount, 영속 `alloy-data` volume을 유지한다.
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

#### Lifecycle and data controls

- Alloy를 HOME으로 유지하고 socket 읽기 전용과 선언된 network, gateway 경계를 보존한다.
- 설정이 영속 기준이다. 사용 component를 확인한 상태만 백업하며 전송 중 telemetry의 정확한 복구를 약속하지 않는다.
- Upgrade 전에 대상 버전 config, 허용 손실, 각 backend 전달을 검증한다. writer만으로 profile 수집을 증명하지 않는다.
- 제거에는 producer 이전, 관측 공백 승인, route/port 폐쇄, 확인된 WAL/checkpoint 처리가 필요하다.

### Exceptions

#### Exception Conditions

pipeline, exporter, Docker discovery, route, mount 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다. 장애 대응 중 임시 조치가 필요하면 [RUN-0040](../../runbooks/07-observability/0040-alloy.md)에서 최소 조치와 rollback evidence를 기록한다.

#### Approval and Review

- Alloy image, config, Docker discovery, relabel rule, exporter endpoint, mount 경로, OTLP port, route, healthcheck가 바뀔 때 검토한다.
- 정기 검토는 분기마다 한다.

## Enforcement

### Mechanisms

- Compose 경계, pipeline 경계, 품질 metric 수신기 확인 명령은 [GDE-0040 Common Checks](../../guides/07-observability/0040-alloy.md#common-checks)와 [RUN-0040 절차](../../runbooks/07-observability/0040-alloy.md#steps)가 소유한다.
- Repository contracts: 원격 PR public `changed` 검사 ([quality policy](../../../00.workspace/03.quality/quality-standards.md#canonical-delivery-phase-matrix))

### Limits

정책 본문이 이름 붙인 검사로 강제하는 규칙은 일부이며 아래 항목은 기계적으로 강제되지 않는다.

- 설정/서비스 경계: `POL-0040-R1`, `POL-0040-R2`, `POL-0040-R10`, `POL-0040-R11`는 이름 붙은 검사가 지정되지 않았다.
- 수신기/네트워크 경계: `POL-0040-R3`, `POL-0040-R4`, `POL-0040-R5`, `POL-0040-R6`, `POL-0040-R7`, `POL-0040-R8`, `POL-0040-R9`는 이름 붙은 검사가 지정되지 않았다.
- pipeline 경계: `POL-0040-R12`, `POL-0040-R13`, `POL-0040-R14`, `POL-0040-R15`, `POL-0040-R16`, `POL-0040-R17`, `POL-0040-R18`, `POL-0040-R19`, `POL-0040-R20`, `POL-0040-R21`는 이름 붙은 검사가 지정되지 않았다.
- 변경 검증: `POL-0040-R22`, `POL-0040-R23`, `POL-0040-R24`, `POL-0040-R25`는 이름 붙은 검사가 지정되지 않았다.
- 금지 행위: `POL-0040-R26`, `POL-0040-R27`, `POL-0040-R28`, `POL-0040-R29`는 승인/검토 등 수동 절차에 의존한다.
- 수명주기/데이터: `POL-0040-R30`, `POL-0040-R31`, `POL-0040-R32`, `POL-0040-R33`, `POL-0040-R34`는 이름 붙은 검사가 지정되지 않았다.
- 수명주기/데이터: `POL-0040-R35`는 승인/검토 등 수동 절차에 의존한다.
- 정책 본문은 개별 확인 명령을 지정하지 않고 Compose/pipeline/수신기 확인 명령의 소유를 guide/runbook에 위임하므로, 이 정책이 직접 이름 붙인 검사는 없다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외와 통제 변경에는 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- Subject peers: [Guide](../../guides/07-observability/0040-alloy.md) (`GDE-0040`), [Runbook](../../runbooks/07-observability/0040-alloy.md) (`RUN-0040`)

- [Operations index](../../README.md)
- [Usage guide](../../guides/07-observability/0040-alloy.md)
- [Recovery runbook](../../runbooks/07-observability/0040-alloy.md)
