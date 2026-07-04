---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/alloy.md -->

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
   rg -n 'service: template-infra-med|image: grafana/alloy:v1.17.1|container_name: infra-alloy|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

2. Pipeline component boundary를 확인한다.

   ```bash
   rg -n 'discovery.docker|project_net\\|infra_net|loki.source.docker|loki.write|prometheus.remote_write|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy
   ```

3. 현재 pipeline 구조를 이해한다.

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

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alloy`
- `docker logs --tail=100 infra-alloy`
- `rg -n 'discovery.docker|loki.source.docker|prometheus.remote_write|otelcol.receiver.otlp|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy`
- `rg -n 'ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/alloy.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/alloy.md)
- [Recovery runbook](../../runbooks/06-observability/alloy.md)
