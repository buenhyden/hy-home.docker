---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/loki.md -->

# Loki Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Loki 사용 맥락과 설정 확인 방법을 설명한다. Loki는 Alloy가 수집한 Docker logs를 `http://loki:3100/loki/api/v1/push`로 수신하고, MinIO S3 backend의 `loki-bucket`에 chunks/index를 저장하며, Grafana datasource `Loki`를 통해 LogQL query를 제공한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- SRE
- AI Agent

### Purpose

- Loki compose service, custom image, MinIO storage, retention, compactor, label cardinality, Alloy ingestion, and Grafana query boundary를 빠르게 파악한다.
- LogQL 검색과 readiness 확인에 필요한 구현 위치를 연결한다.
- 장애 대응, restart, storage/ingestion triage, config rollback은 runbook으로 넘긴다.

### Prerequisites

- `infra/06-observability/loki/config/loki-config.yaml` 설정을 읽을 수 있는 권한.
- Docker Secret ID `minio_app_user_password`와 environment reference `MINIO_APP_USERNAME`이 준비되어 있어야 한다. Secret 값은 문서, 로그, task evidence에 기록하지 않는다.
- Alloy pipeline과 Grafana datasource가 현재 compose network에서 `loki:3100`을 가리켜야 한다.
- Grafana UI `https://grafana.${DEFAULT_URL}` 접근 권한.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-stateful-high|image: hy/loki:3.7.3-custom|container_name: infra-loki|loki-data|MINIO_APP_USERNAME|minio_app_user_password|LOKI_HOST_PORT|LOKI_PORT|/ready|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

2. Loki config boundary를 확인한다.

   ```bash
   rg -n 'bucketnames: loki-bucket|access_key_id: \\$\\{MINIO_APP_USERNAME\\}|secret_access_key: \\$\\{MINIO_APP_USER_PASSWORD\\}|retention_enabled: true|retention_period: 168h|compaction_interval: 10m|retention_delete_delay: 2h|alertmanager_url: http://alertmanager:9093' infra/06-observability/loki/config/loki-config.yaml
   ```

3. Custom image and secret expansion boundary를 확인한다.

   ```bash
   rg -n 'FROM grafana/loki:3.7.3|ENTRYPOINT \\[\"/docker-entrypoint.sh\"\\]|-config.expand-env=true|MINIO_APP_USER_PASSWORD|/run/secrets/minio_app_user_password|exec /usr/bin/loki' infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh
   ```

4. Log ingestion and query path를 확인한다.

   ```bash
   rg -n 'loki.source.docker|loki.write|url = \"http://loki:3100/loki/api/v1/push\"|project_net\\|infra_net' infra/06-observability/alloy/config/config.alloy
   rg -n 'name: Loki|uid: Loki|url: http://loki:3100' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

5. Grafana Explore에서 LogQL query를 실행한다.

   - UI: `https://grafana.${DEFAULT_URL}`
   - Datasource: `Loki`
   - 예시 selection: `{service_name="grafana"}`
   - 예시 filter: `{service_name="grafana"} |= "error"`
   - 예시 aggregation: `count_over_time({service_name="grafana"}[5m])`

### Common Pitfalls

- **Label cardinality**: request ID, user ID, IP address 같은 동적 값을 label로 승격하면 index 비용과 query latency가 급증한다.
- **Secret evidence**: `MINIO_APP_USER_PASSWORD` 값이나 rendered env를 로그/evidence에 남기지 않는다.
- **Retention assumption**: 현재 retention은 `168h`이며 문서만 바꿔 보관 기간이 바뀐 것처럼 선언하지 않는다.
- **Alloy assumption**: Loki가 healthy여도 Alloy `loki.write`가 실패하면 Grafana에서 logs가 비어 보일 수 있다.
- **Direct access assumption**: 외부 UI route는 `https://loki.${DEFAULT_URL}`로 보호되고, 내부 compose network에서는 `loki:3100`를 사용한다.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps loki`
- `docker logs --tail=100 infra-loki`
- `docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready`
- `rg -n 'loki.source.docker|loki.write|http://loki:3100/loki/api/v1/push' infra/06-observability/alloy/config/config.alloy`
- `rg -n 'retention_enabled: true|retention_period: 168h|bucketnames: loki-bucket' infra/06-observability/loki/config/loki-config.yaml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/loki.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/loki.md)
- [Recovery runbook](../../runbooks/06-observability/loki.md)
