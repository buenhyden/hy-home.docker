---
title: "LGTM Stack Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0042"
created: "2026-03-25"
---

# LGTM Stack Usage Guide

## Overview

### Overview

## Audience and Goal

### Audience and Goal

## Usage

### Usage

### Overview

이 가이드는 `hy-home.docker`의 `06-observability` tier가 제공하는 통합 관측성 stack을 설명한다. 현재 stack은 Prometheus, Loki, Tempo, Grafana에 Alloy, Alertmanager, Pushgateway, cAdvisor, Pyroscope를 더해 metrics, logs, traces, alerts, profiles를 연결한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- `06-observability` tier의 service role, data path, storage boundary를 빠르게 파악한다.
- Grafana에서 metrics/logs/traces/profiles/alerts를 탐색할 때 어떤 datasource와 backend를 확인해야 하는지 연결한다.
- 개별 서비스 장애 대응은 service별 runbook으로 넘긴다.

### Prerequisites

- `infra/06-observability/docker-compose.yml`과 service README를 읽을 수 있는 권한.
- Grafana UI `https://grafana.${DEFAULT_URL}` 접근 권한.
- Secret 값은 문서, 로그, task evidence에 기록하지 않는다.

### Step-by-step Instructions

1. Tier service inventory를 확인한다.

   ```bash
   rg -n '^  (prometheus|loki|tempo|alloy|grafana|cadvisor|pyroscope|alertmanager|pushgateway):' infra/06-observability/docker-compose.yml
   ```

2. Data path를 기준으로 각 component 역할을 확인한다.

   - **Metrics**: Prometheus가 exporter를 scrape하고 TSDB 데이터를 `prometheus-data`에 저장한다.
   - **Logs**: Alloy가 Docker 로그를 `http://loki:3100/loki/api/v1/push`로 Loki에 보내며, Loki는 chunk/index를 SeaweedFS bucket `loki-bucket`에 저장한다.
   - **Traces**: Alloy가 `4317/4318`에서 OTLP를 받아 Tempo로 trace를 export하며, Tempo는 block을 SeaweedFS bucket `tempo-bucket`에 저장한다.
   - **Visualization**: Grafana가 Prometheus, Loki, Tempo, Alertmanager, Pyroscope를 위한 datasource를 provision한다.
   - **Alerting**: Prometheus가 `alertmanager:9093`으로 alert를 보낸다.
   - **Batch metrics**: Pushgateway가 단기 job을 위해 metric을 버퍼링한다.
   - **Container metrics**: cAdvisor가 container 리소스 metric을 노출한다.
   - **Profiles**: Pyroscope가 profile backend와 Grafana datasource를 제공한다.

3. Grafana datasource wiring을 확인한다.

   ```bash
   rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

4. Storage와 retention boundary를 확인한다.

   ```bash
   rg -n 'bucketnames: loki-bucket|retention_period: 168h|bucket: tempo-bucket|storage.tsdb|pyroscope-data' infra/06-observability/loki/config/loki-config.yaml infra/06-observability/tempo/config/tempo.yaml infra/06-observability/docker-compose.yml
   ```

5. Service-specific 문서로 이동한다.

   - Prometheus: metric과 alert rule
   - Loki: log와 SeaweedFS storage
   - Tempo: trace와 SeaweedFS storage
   - Grafana: dashboard, datasource, SSO
   - Alloy: telemetry 수집 pipeline
   - Alertmanager: alert routing과 silence
   - Pushgateway: ephemeral/batch metric
   - Pyroscope: profile

### Common Pitfalls

- **Single-pane assumption**: Grafana UI가 정상이어도 backend datasource가 unhealthy이면 일부 panels만 실패할 수 있다.
- **Retention assumption**: Loki `168h` 요구에는 marker persistence gap이 있고 Tempo `24h` 요구는 source에서 설정되지 않았다. [POL-0048](../policies/0048-telemetry-retention.md)의 미준수 구분과 Pyroscope capacity 경계를 따른다. 다른 항목의 regex match는 retention 검증이 아니다.
- **Collector assumption**: Alloy pipeline이 실패하면 Loki/Tempo/Prometheus/Grafana가 정상이어도 telemetry가 비어 보일 수 있다.
- **Secret evidence**: SeaweedFS, Grafana, Alertmanager, Prometheus secret 값은 기록하지 않는다.
- **Runbook scope**: 이 stack guide는 복구 절차가 아니다. 장애 대응은 service별 runbook을 따른다.

### Common Checks

- `docker compose --profile obs ps`
- `rg -n '^  (prometheus|loki|tempo|alloy|grafana|cadvisor|pyroscope|alertmanager|pushgateway):' infra/06-observability/docker-compose.yml`
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`
- `bash scripts/validation/validate-docker-compose.sh`

### Runbook Handoff

N/A — 이 가이드는 stack overview이며, 반복 실행 절차와 장애 대응은 service별 runbook을 따른다.

### Traceability

- Governing authority: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: none — no Policy or Runbook shares number `0042`.

## Related Documents

- Runtime pins: Compose/Dockerfile 선언이 authoritative하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift 검증을 제공한다.

- [Operations index](../README.md)
- [Prometheus guide](0045-prometheus.md)
- [Loki guide](0043-loki.md)
- [Tempo guide](0049-tempo.md)
- [Grafana guide](0041-grafana.md)
- [Alloy guide](0040-alloy.md)
- [Alertmanager guide](0039-alertmanager.md)
- [Pushgateway guide](0046-pushgateway.md)
- [Pyroscope guide](0047-pyroscope.md)
- [Runbook index](../README.md)
