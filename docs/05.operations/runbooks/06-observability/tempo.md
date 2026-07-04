---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/tempo.md -->

# Tempo Readiness and Recovery Runbook

## Tempo Readiness and Recovery Procedure

> Scope: Tempo readiness checks, OTLP ingestion triage, MinIO storage evidence, metrics generator verification, restart, and WAL symptom escalation.

### Overview

이 런북은 Tempo trace ingestion failure, MinIO-backed storage error, metrics generator failure, query latency, and WAL corruption symptom을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-tempo`의 상태를 확인하고 Alloy → Tempo → MinIO → Prometheus remote write 경로를 검증하며, 데이터 손실 가능성이 있는 WAL or bucket 조치를 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Tempo operations policy](../../policies/06-observability/tempo.md)
- **Guide**: [Tempo usage guide](../../guides/06-observability/tempo.md)
- **Infrastructure**: [Tempo infra README](../../../../infra/06-observability/tempo/README.md)

## When to Use

- Grafana Tempo datasource에서 최근 trace가 검색되지 않을 때.
- Alloy는 trace를 수신하지만 Tempo에 trace가 도착하지 않는다고 의심될 때.
- Tempo log에 S3, bucket, access denied, compaction, WAL 관련 오류가 보일 때.
- Service graph or span metrics가 Prometheus/Grafana에서 보이지 않을 때.
- Config 변경 후 readiness, route, storage, remote write evidence가 필요할 때.

## Procedure

### Checklist

- [ ] `tempo` service, `infra-tempo` container, and `tempo-data` volume 상태를 확인한다.
- [ ] Secret values를 열람하지 않는다. `minio_app_user_password` ID만 evidence에 기록한다.
- [ ] 문제 유형을 readiness, ingestion, storage, metrics generator, query, WAL symptom 중 하나로 분류한다.
- [ ] WAL deletion, bucket mutation, retention change, or secret rotation이 필요해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태, ready endpoint, 최근 로그를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps tempo
   docker logs --tail=200 infra-tempo
   docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready
   ```

2. Compose and config boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-high|image: hy/tempo:3.0.2-custom|container_name: infra-tempo|user: .10001:10001.|tempo-data|TEMPO_PORT|minio_app_user_password|tempo.middlewares' infra/06-observability/docker-compose.yml
   rg -n 'endpoint: 0.0.0.0:4317|endpoint: 0.0.0.0:4318|block_retention: 24h|compacted_block_retention: 1h|metrics_generator:|remote_write:|url: http://prometheus:9090/api/v1/write|bucket: tempo-bucket|endpoint: minio:9000|secret_key: \\$\\{MINIO_APP_USER_PASSWORD\\}' infra/06-observability/tempo/config/tempo.yaml
   ```

3. Alloy exporter가 Tempo endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'otelcol.exporter.otlp "tempo"|endpoint = "tempo:4317"|traces  = \\[otelcol.exporter.otlp.tempo.input\\]' infra/06-observability/alloy/config/config.alloy
   ```

4. Storage or secret symptom은 로그 문구와 bucket/config boundary만 캡처한다. Secret value를 출력하지 않는다.

   ```bash
   docker logs --tail=500 infra-tempo | grep -Ei 's3|bucket|tempo-bucket|minio|access denied|secret|wal|compact|block'
   ```

5. Metrics generator failure가 의심되면 Tempo config의 `remote_write` endpoint와 Prometheus readiness를 확인한다.

   ```bash
   rg -n 'metrics_generator:|span_metrics:|service_graphs:|remote_write:|url: http://prometheus:9090/api/v1/write' infra/06-observability/tempo/config/tempo.yaml
   docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy
   ```

6. Readiness or ingestion state가 config와 맞지만 회복되지 않으면 Tempo를 재시작한다. Alloy exporter state도 함께 의심될 때만 Alloy를 같이 재시작한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart tempo
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart tempo alloy
   ```

7. WAL corruption or local-block corruption이 의심되면 삭제하지 말고 evidence만 수집한다.

   ```bash
   docker logs --tail=500 infra-tempo | grep -Ei 'wal|corrupt|local block|compactor|failed to replay'
   docker compose -f infra/06-observability/docker-compose.yml config | grep -n 'tempo-data'
   ```

   이 런북은 WAL 삭제, bucket mutation, or volume file mutation을 검증된 복구 절차로 제공하지 않는다. 데이터 손실 가능성이 있는 조치는 별도 incident/task approval과 backup evidence가 필요하다.

### Verification Steps

- [ ] `docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready`가 성공한다.
- [ ] Grafana Tempo datasource에서 최근 trace가 조회된다.
- [ ] Service graph or span metrics가 필요한 경우 Prometheus remote write와 Grafana dashboard timestamp가 갱신된다.
- [ ] Storage symptom이면 `tempo-bucket`, MinIO endpoint, secret reference boundary가 policy와 일치한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-tempo`
- **Health**: Tempo `/ready`, Grafana Tempo datasource, Grafana service graph dashboards
- **Config**: `tempo.yaml`, Alloy Tempo exporter, Prometheus `/-/healthy`
- **Storage**: `tempo-bucket` boundary, MinIO endpoint `minio:9000`, `tempo-data` volume
- **Evidence to Capture**: failing symptom, log excerpt without secrets, affected route or endpoint, restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed `tempo.yaml`, Alloy exporter, or Compose 변경이 원인이면 직전 Git diff 단위로 되돌리고 readiness를 다시 확인한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- WAL deletion, bucket deletion, object mutation, retention change, or secret rotation은 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret values는 기록하지 않는다.
- Trace ingestion 장애는 Alloy exporter check, Tempo ready state, Grafana datasource result를 함께 기록한다.
- Storage/WAL symptom은 로그 발췌, `tempo-data` volume boundary, approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. 데이터 손실 가능성이 있는 WAL, bucket, object, retention 조치는 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, destructive data change가 필요하거나, WAL/bucket/object mutation이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/tempo.md)
- [Operations policy](../../policies/06-observability/tempo.md)
