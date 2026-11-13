---
title: "LGTM Stack Usage Guide"
version: "1.1.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "GDE-0042"
created: "2026-03-25"
---

# LGTM Stack Usage Guide

## Purpose

### Outcome

이 가이드는 `hy-home.docker`의 `06-observability` tier가 제공하는 통합 관측성 stack을 설명한다. 현재 stack은 Prometheus, Loki, Tempo, Grafana에 Alloy, Alertmanager, Pushgateway, node-exporter, cAdvisor, Pyroscope, Gatus, `obs-gpu` 전용 dcgm-exporter, 일회성 `grafana-db-provision`을 더해 metrics, logs, traces, alerts, profiles, availability를 연결한다. OPTIONAL admin 로그 뷰어 Dozzle은 `infra/06-observability/dozzle/docker-compose.yml`에 따로 있다.

대상 독자: 개발자, 운영자, SRE, AI Agent.

- `06-observability` tier의 service role, data path, storage boundary를 빠르게 파악한다.
- Grafana에서 metrics/logs/traces/profiles/alerts를 탐색할 때 어떤 datasource와 backend를 확인해야 하는지 연결한다.
- 개별 서비스 장애 대응은 service별 runbook으로 넘긴다.

### Boundaries

- Governing authority: [Observability Architecture Description](../../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: 없음. 번호 `0042`를 공유하는 Policy나 Runbook은 없다.

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.
- [Prometheus guide](0045-prometheus.md)
- [Loki guide](0043-loki.md)
- [Tempo guide](0049-tempo.md)
- [Grafana guide](0041-grafana.md)
- [Alloy guide](0040-alloy.md)
- [Alertmanager guide](0039-alertmanager.md)
- [Pushgateway guide](0046-pushgateway.md)
- [Pyroscope guide](0047-pyroscope.md)

## Prerequisites

### Environment

사용 전에 다음을 확인한다.

- Secret 값은 문서, 로그, task evidence에 기록하지 않는다.

### Permissions

- `infra/06-observability/docker-compose.yml`과 service README를 읽을 수 있는 권한.
- Grafana UI `https://grafana.${DEFAULT_URL}` 접근 권한.

## Procedure

### Actions

일반 순서는 다음과 같다.

1. Tier service inventory를 [Common Checks](#common-checks)의 첫 `rg` 명령으로 확인한다.

2. Data path를 기준으로 각 component 역할을 확인한다.

   - **Metrics**: Prometheus가 exporter를 scrape하고 TSDB 데이터를 `prometheus-data`에 저장한다.
   - **Logs**: Alloy가 Docker 로그를 `http://loki:3100/loki/api/v1/push`로 Loki에 보내며, Loki는 chunk/index를 SeaweedFS bucket `loki-bucket`에 저장한다.
   - **Traces**: Alloy가 `4317/4318`에서 OTLP를 받아 Tempo로 trace를 export하며, Tempo는 block을 SeaweedFS bucket `tempo-bucket`에 저장한다.
   - **Visualization**: Grafana가 Prometheus, Loki, Tempo, Alertmanager, Pyroscope를 위한 datasource를 provision한다.
   - **Alerting**: Prometheus가 `alertmanager:9093`으로 alert를 보낸다.
   - **Batch metrics**: Pushgateway가 단기 job을 위해 metric을 버퍼링한다.
   - **Container metrics**: cAdvisor가 container 리소스 metric을 노출한다.
   - **Host metrics**: node-exporter는 SPEC-0225부터 host network namespace에서 실행하며 `obs_net` gateway 주소에 listen한다. Prometheus와 Alloy는 `extra_hosts`의 `node-exporter:10.250.5.1`로 접근한다.
   - **Profiles**: Pyroscope가 profile backend와 Grafana datasource를 제공한다.
   - **Availability**: Gatus가 선언된 endpoint를 probe하고 history를 SQLite `gatus-data`에 저장한다.
   - **GPU metrics**: dcgm-exporter는 `obs-gpu`에서만 선택되며 Prometheus가 `dcgm-exporter:9400`을 scrape한다.

3. Grafana datasource wiring을 확인한다.

   명령은 [Common Checks](#common-checks)에 있다.

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
   - Gatus: availability probe
   - Dozzle: admin 로그 조회

### Exceptions

예외와 제한 사항은 아래 항목에 정리한다.

#### 운영 시 주의점

- **Single-pane assumption**: Grafana UI가 정상이어도 backend datasource가 unhealthy이면 일부 panels만 실패할 수 있다.
- **Retention assumption**: Loki `168h` 요구에는 marker persistence gap이 있고 Tempo `24h` 요구는 source에서 설정되지 않았다. [POL-0048](../../policies/07-observability/0048-telemetry-retention.md)의 미준수 구분과 Pyroscope capacity 경계를 따른다. 다른 항목의 regex match는 retention 검증이 아니다.
- **Collector assumption**: Alloy pipeline이 실패하면 Loki/Tempo/Prometheus/Grafana가 정상이어도 telemetry가 비어 보일 수 있다.
- **Secret evidence**: SeaweedFS, Grafana, Alertmanager, Prometheus secret 값은 기록하지 않는다.
- **Runbook scope**: 이 stack guide는 복구 절차가 아니다. 장애 대응은 service별 runbook을 따른다.

## Verification

### Expected Result

확인 항목과 기대 결과는 아래와 같다.

#### Common Checks

- `docker compose --profile obs ps`
- `rg -n '^  (prometheus|loki|tempo|alloy|grafana|grafana-db-provision|node-exporter|cadvisor|gatus|pyroscope|alertmanager|pushgateway|dcgm-exporter|dozzle):' infra/06-observability/docker-compose.yml infra/06-observability/dozzle/docker-compose.yml`
- `rg -n 'uid: Prometheus|uid: Loki|uid: Tempo|uid: alertmanager|type: grafana-pyroscope-datasource' infra/06-observability/grafana/provisioning/datasources/datasource.yml`
- `bash scripts/validation/validate-docker-compose.sh`

### Troubleshooting

위 점검 결과가 기대와 다르면 증상별 진단, 재시작과 rollback은 [RUN-0045](../../runbooks/07-observability/0045-prometheus.md)으로 넘긴다.

#### Runbook Handoff

stack 전체를 다루는 runbook은 없다. 반복 실행 절차와 장애 대응은 서비스별 runbook을 따른다: [Prometheus](../../runbooks/07-observability/0045-prometheus.md), [Loki](../../runbooks/07-observability/0043-loki.md), [Tempo](../../runbooks/07-observability/0049-tempo.md), [Grafana](../../runbooks/07-observability/0041-grafana.md), [Alloy](../../runbooks/07-observability/0040-alloy.md), [Alertmanager](../../runbooks/07-observability/0039-alertmanager.md), [Pushgateway](../../runbooks/07-observability/0046-pushgateway.md), [Pyroscope](../../runbooks/07-observability/0047-pyroscope.md).

- [Operations index](../../README.md)
- [Runbook index](../../README.md)
