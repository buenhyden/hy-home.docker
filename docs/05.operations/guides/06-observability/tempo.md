---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/tempo.md -->

# Tempo Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Tempo 사용 맥락과 설정 확인 방법을 설명한다. Tempo는 Alloy가 전달한 OTLP trace를 수집하고, MinIO S3 backend의 `tempo-bucket`에 저장하며, `metrics_generator`를 통해 span metrics와 service graphs를 Prometheus remote write endpoint로 전송한다.

### Usage Type

`system-guide`

### Target Audience

- Backend Developer
- SRE
- Operator
- AI Agent

### Purpose

- Tempo compose service, OTLP receiver, MinIO storage, retention, metrics generator boundary를 빠르게 파악한다.
- Grafana에서 TraceQL, span metrics, service graph를 확인하는 진입점을 제공한다.
- 복구, restart, WAL symptom triage, storage 장애 대응은 runbook으로 넘긴다.

### Prerequisites

- [Grafana Alloy](./alloy.md)가 OTLP `4317`/`4318` receiver를 열고 `tempo:4317` exporter로 trace를 전달해야 한다.
- [MinIO](../../../../infra/04-data/lake-and-object/minio/README.md)에 `tempo-bucket`이 준비되어 있어야 한다.
- [Grafana](./grafana.md)에 Tempo datasource URL `http://tempo:3200`이 provisioning되어 있어야 한다.
- Docker Secret value는 열람하지 않는다. `minio_app_user_password` secret ID와 file reference만 문서화한다.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-high|image: hy/tempo:3.0.2-custom|container_name: infra-tempo|user: .10001:10001.|tempo-data|TEMPO_PORT|minio_app_user_password|tempo.middlewares' infra/06-observability/docker-compose.yml
   ```

2. Tempo config의 ingestion, retention, storage, metrics generator boundary를 확인한다.

   ```bash
   rg -n 'endpoint: 0.0.0.0:4317|endpoint: 0.0.0.0:4318|block_retention: 24h|compacted_block_retention: 1h|metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: minio:9000' infra/06-observability/tempo/config/tempo.yaml
   ```

3. Alloy에서 Tempo exporter가 `tempo:4317`을 가리키는지 확인한다.

   ```bash
   rg -n 'otelcol.exporter.otlp "tempo"|endpoint = "tempo:4317"|traces  = \\[otelcol.exporter.otlp.tempo.input\\]' infra/06-observability/alloy/config/config.alloy
   ```

4. Grafana의 `Explore` 메뉴에서 `Tempo` datasource를 선택하고 `TraceQL`로 trace를 조회한다.

   ```text
   { duration > 100ms && resource.service.name = "api-gateway" }
   ```

5. Grafana service graph와 span metrics가 비어 있으면 Tempo `metrics_generator`와 Prometheus remote write 상태를 runbook 기준으로 점검한다.

### Common Pitfalls

- **Instrumentation 누락**: trace propagation이 끊기면 전체 요청 흐름을 볼 수 없다. 애플리케이션 공통 라이브러리나 middleware의 context 전달을 확인한다.
- **Storage assumption**: Tempo는 MinIO S3 backend와 local WAL을 함께 사용한다. WAL 삭제나 bucket 변경은 guide 범위가 아니라 runbook escalation 대상이다.
- **Metrics generator assumption**: Service graph와 span metrics는 `metrics_generator`와 Prometheus remote write가 모두 정상이어야 보인다.
- **Secret exposure**: MinIO secret value를 로그나 문서에 기록하지 않는다.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps tempo`
- `docker logs --tail=100 infra-tempo`
- `docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready`
- `rg -n 'block_retention: 24h|compacted_block_retention: 1h|bucket: tempo-bucket|url: http://prometheus:9090/api/v1/write' infra/06-observability/tempo/config/tempo.yaml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/tempo.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/tempo.md)
- [Recovery runbook](../../runbooks/06-observability/tempo.md)
