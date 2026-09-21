---
title: "Alloy Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "GDE-0040"
parent_ids:
- "POL-0040"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - alloy
created: "2026-05-10"
---

# Alloy Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Grafana Alloy 사용 맥락과 설정 확인 방법을 설명한다. Alloy는 Docker discovery/log collection, Prometheus remote write, OTLP trace gateway, and Pyroscope writer endpoint를 `infra/06-observability/alloy/config/config.alloy`에서 선언해 Prometheus, Loki, Tempo, Pyroscope로 telemetry를 전달한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Alloy compose service, Docker discovery, relabeling, exporter endpoint, and OTLP ingress boundary를 빠르게 파악한다.
- Logs, metrics, traces, and profiling writer pipeline이 어떤 backend로 향하는지 확인한다.
- 복구, restart, endpoint 장애 대응, config rollback은 runbook으로 넘긴다.

### Prerequisites

- `config.alloy` HCL 설정 문법과 OTLP 기본 개념.
- Docker container label and network metadata 확인 권한.
- Alloy UI `https://alloy.${DEFAULT_URL}` 접근 권한.
- Docker socket and container log mount는 read-only로 유지한다.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/alloy:|container_name: infra-alloy|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

2. Pipeline component boundary를 확인한다.

   ```bash
   rg -n 'discovery.docker|project_net\\|infra_net|loki.source.docker|loki.write|prometheus.remote_write|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy
   ```

3. 현재 pipeline 구조를 이해한다. `ALLOY_CONFIG_FILE`이 두 독립 파일 중 하나를
   `/etc/alloy/config.alloy`로 mount한다. 두 파일은 합쳐 읽히지 않으므로 각각 따로
   검사한다(`alloy fmt <file>`).

   | 파일 | 선택 | 포함 pipeline | 빠진 것 |
   | --- | --- | --- | --- |
   | `config.home.alloy` | `.env.example` 기본값 | Docker 로그 → Loki, Alloy self-metrics → Prometheus | OTLP receiver, Tempo exporter, Pyroscope writer |
   | `config.alloy` | 변수 미설정 시 Compose 기본값 | 아래 전체 목록 | 없음 |

   `tracing`/`profiling` profile은 Alloy·Tempo·Pyroscope를 기동하지만 home 설정에서는
   OTLP 4317/4318 host port가 열려도 받는 receiver가 없다. trace·profile 수집이
   필요하면 `ALLOY_CONFIG_FILE=config.alloy`로 전환한다. profile 선택은 수신을
   증명하지 않으며 profile → config → receiver → source → backend → Grafana 조회를
   각각 확인한다. 아래 목록은 전체 설정(`config.alloy`) 기준이다.

   - **Discovery**: `discovery.docker`를 사용하여 컨테이너 정보를 수집한다.
   - **Relabeling**: `discovery.relabel`이 `service_name`, `container_name`, `compose_project`, `env`, `scope` labels를 주입한다.
   - **Logs**: `loki.source.docker` -> `loki.write.local_loki` -> `http://loki:3100/loki/api/v1/push`.
   - **Metrics**: `prometheus.exporter.self` -> `prometheus.scrape.alloy_scrape` -> `prometheus.remote_write.local_prom` -> `http://prometheus:9090/api/v1/write`.
   - **Traces**: `otelcol.receiver.otlp` (`4317`, `4318`) -> `otelcol.processor.batch` -> `otelcol.exporter.otlp.tempo` -> `tempo:4317`.
   - **Profiling writer**: `pyroscope.write.local_pyroscope` endpoint `http://pyroscope:4040` is declared. Profile source 추가 여부는 별도 config evidence로 확인한다.

4. 애플리케이션 instrumentation은 가능한 OTLP endpoint를 사용한다.

   - gRPC: `alloy:4317`
   - HTTP: `alloy:4318`

5. Pipeline debugging은 Alloy UI에서 수행한다.

   - `https://alloy.${DEFAULT_URL}`에 접속한다.
   - **Graph View**에서 component 연결과 error state를 확인한다.
   - **Component Details**에서 target, receiver, exporter 상태를 확인한다.

### Common Pitfalls

- **Relabeling regex**: `service_name` 또는 `scope` label이 잘못 지정되면 logs/metrics/profile query가 분산된다.
- **Network filter**: Docker discovery는 `project_net|infra_net`만 keep한다. 다른 network의 container는 의도적으로 제외될 수 있다.
- **Exporter assumption**: Downstream backend가 unhealthy이면 Alloy pipeline이 정상이어도 telemetry가 보이지 않을 수 있다.
- **Profiling assumption**: `pyroscope.write` endpoint가 있다고 해서 profile source가 자동으로 수집되는 것은 아니다.
- **Docker socket boundary**: Docker socket and container log mounts는 read-only여야 한다.

### Source-backed operating contract

- **Purpose/classification/source**: `alloy` is the `HOME` telemetry collector selected by `obs`, `logs`, `tracing`, or `profiling`; [Compose](../../../../../infra/06-observability/docker-compose.yml) and [Alloy config](../../../../../infra/06-observability/alloy/config/config.alloy) are authoritative.
- **Flow/dependencies**: read-only Docker socket/container logs feed Loki, OTLP 4317/4318 feeds Tempo, Alloy self-metrics remote-write to Prometheus, and a Pyroscope write sink exists. Current config declares no profile source, so the sink alone does not prove profiles are collected. Loki, Tempo, Prometheus, Docker, and `infra_net` are dependencies.
- **State/security**: config and host log mounts are read-only; Docker socket access is security-sensitive. `alloy-data:/var/lib/alloy` is mounted and the command now passes `--storage.path=/var/lib/alloy/data`; the previous command override had dropped the image default, so positions and WAL lived in the container layer and were lost on recreate. The container runs as the image's `alloy` user (UID 473) with the host docker group (`DOCKER_GID`) because root without capabilities cannot write the 473-owned state directory; the first attempt as root crash-looped on `mkdir /var/lib/alloy/data: permission denied` on 2026-09-21 and was rolled back within about three minutes. The first recreate with the fix starts without the old positions, which can re-send or skip recent Docker log lines; Loki may reject out-of-order duplicates. Config edits apply through `POST /-/reload` only when the mounted file inode is unchanged; editors that replace the file need a container restart. Changing ports or mounts needs a recreate. In-flight telemetry can be lost and is not a guaranteed recovery asset.
- **Resources/normal use**: source CPU/memory limits are not headroom. Render at root with `docker compose --profile obs config --quiet`, run Alloy config validation, then verify downstream writes and bounded retry/WAL signals.
- **Lifecycle**: preserve config and any component-specific verified state; drain or accept documented in-flight loss, update one pinned version, validate component compatibility, then verify logs/traces/metrics and only claim profiling when a source is present.
- **Upstream/license**: use official [How Alloy works](https://grafana.com/docs/alloy/latest/introduction/how-alloy-works/) and [remote_write/WAL](https://grafana.com/docs/alloy/latest/reference/components/prometheus/prometheus.remote_write/) guidance. Grafana Alloy is Apache-2.0 licensed.

## Common Checks

- `docker compose --profile obs ps alloy`
- `docker logs --tail=100 infra-alloy`
- `rg -n 'discovery.docker|loki.source.docker|prometheus.remote_write|otelcol.receiver.otlp|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy`
- `rg -n 'ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

## Traceability

- Declared parent: [Alloy Operations Policy](policy.md) (`POL-0040`)
- Governing authority: [Observability Architecture Description](../../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Policy](policy.md) (`POL-0040`), [Runbook](runbook.md) (`RUN-0040`)

## Related Documents

- [Runtime image declarations](../../../../../infra/06-observability/docker-compose.yml)
- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
