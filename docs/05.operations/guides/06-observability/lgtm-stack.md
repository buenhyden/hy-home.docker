---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/lgtm-stack.md -->

# LGTM Stack Usage Guide

## Usage

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

   - **Metrics**: Prometheus scrapes exporters and stores TSDB data in `prometheus-data`.
   - **Logs**: Alloy sends Docker logs to Loki at `http://loki:3100/loki/api/v1/push`; Loki stores chunks/indexes in MinIO bucket `loki-bucket`.
   - **Traces**: Alloy accepts OTLP on `4317/4318` and exports traces to Tempo; Tempo stores blocks in MinIO bucket `tempo-bucket`.
   - **Visualization**: Grafana provisions datasources for Prometheus, Loki, Tempo, Alertmanager, and Pyroscope.
   - **Alerting**: Prometheus sends alerts to Alertmanager at `alertmanager:9093`.
   - **Batch metrics**: Pushgateway buffers metrics for short-lived jobs.
   - **Container metrics**: cAdvisor exposes container resource metrics.
   - **Profiles**: Pyroscope provides the profile backend and Grafana datasource.

3. Grafana datasource wiring을 확인한다.

   ```bash
   rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

4. Storage and retention boundary를 확인한다.

   ```bash
   rg -n 'bucketnames: loki-bucket|retention_period: 168h|bucket: tempo-bucket|block_retention: 24h|storage.tsdb|pyroscope-data' infra/06-observability/loki/config/loki-config.yaml infra/06-observability/tempo/config/tempo.yaml infra/06-observability/docker-compose.yml
   ```

5. Service-specific 문서로 이동한다.

   - Prometheus: metrics and alert rules
   - Loki: logs and MinIO storage
   - Tempo: traces and MinIO storage
   - Grafana: dashboards, datasources, SSO
   - Alloy: telemetry collection pipelines
   - Alertmanager: alert routing and silences
   - Pushgateway: ephemeral/batch metrics
   - Pyroscope: profiles

### Common Pitfalls

- **Single-pane assumption**: Grafana UI가 정상이어도 backend datasource가 unhealthy이면 일부 panels만 실패할 수 있다.
- **Retention assumption**: Loki `168h`, Tempo `24h`, Pyroscope local filesystem boundary는 각 service policy와 config를 확인해야 한다.
- **Collector assumption**: Alloy pipeline이 실패하면 Loki/Tempo/Prometheus/Grafana가 정상이어도 telemetry가 비어 보일 수 있다.
- **Secret evidence**: MinIO, Grafana, Alertmanager, Prometheus secret 값은 기록하지 않는다.
- **Runbook scope**: 이 stack guide는 복구 절차가 아니다. 장애 대응은 service별 runbook을 따른다.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps`
- `rg -n '^  (prometheus|loki|tempo|alloy|grafana|cadvisor|pyroscope|alertmanager|pushgateway):' infra/06-observability/docker-compose.yml`
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`
- `bash scripts/validation/validate-docker-compose.sh`

## Runbook Handoff

N/A — 이 가이드는 stack overview이며, 반복 실행 절차와 장애 대응은 service별 runbook을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Prometheus guide](./prometheus.md)
- [Loki guide](./loki.md)
- [Tempo guide](./tempo.md)
- [Grafana guide](./grafana.md)
- [Alloy guide](./alloy.md)
- [Alertmanager guide](./alertmanager.md)
- [Pushgateway guide](./pushgateway.md)
- [Pyroscope guide](./pyroscope.md)
- [Runbook index](../../runbooks/06-observability/README.md)
