---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/pyroscope.md -->

# Pyroscope Usage Guide

## Usage

### Overview

이 가이드는 `06-observability` 계층의 Pyroscope 사용 맥락과 설정 확인 방법을 설명한다. Pyroscope는 profiling data를 local filesystem backend `/var/lib/pyroscope`에 저장하고, Grafana Pyroscope datasource와 Alloy `pyroscope.write` endpoint를 통해 flamegraph 분석 경로를 제공한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- SRE
- Operator
- AI Agent

### Purpose

- Pyroscope compose service, config, storage, ingestion limit, and Grafana/Alloy integration boundary를 빠르게 파악한다.
- Grafana에서 flamegraph, diff view, profile labels를 확인하는 진입점을 제공한다.
- 복구, restart, capacity pressure, storage mutation 판단은 runbook으로 넘긴다.

### Prerequisites

- [Grafana Alloy](./alloy.md)에 `pyroscope.write "local_pyroscope"` endpoint `http://pyroscope:4040`이 있어야 한다.
- [Grafana](./grafana.md)에 Pyroscope datasource URL `http://pyroscope:4040`이 provisioning되어 있어야 한다.
- Profile labels에는 request ID, user ID, token, credential 같은 high-cardinality or secret-bearing 값을 넣지 않는다.

### Step-by-step Instructions

1. Compose service boundary를 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/pyroscope:2.1.0|container_name: infra-pyroscope|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml
   ```

2. Pyroscope config의 storage, ingestion limit, and privacy boundary를 확인한다.

   ```bash
   rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml
   ```

3. Alloy와 Grafana가 Pyroscope endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'pyroscope.write "local_pyroscope"|url = "http://pyroscope:4040"|type: grafana-pyroscope-datasource|url: http://pyroscope:4040' infra/06-observability/alloy/config/config.alloy infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

4. Grafana의 `Explore` 메뉴에서 `Pyroscope` datasource를 선택하고 `Application` 또는 service label 기준으로 최근 profile을 조회한다.

5. Flamegraph에서 CPU hot path 또는 allocation-heavy path를 확인한다. 성능 저하 전후를 비교해야 하면 Grafana diff view를 사용한다.

### Common Pitfalls

- **Profiling overhead**: 수집 빈도와 profile type은 애플리케이션 성능에 영향을 줄 수 있다. 고빈도 profiling은 policy approval과 rollback note가 필요하다.
- **Label cardinality**: request ID, user ID, random run ID를 label로 올리면 index와 storage pressure가 커진다.
- **Storage assumption**: 현재 backend는 local filesystem이다. 오래된 profile data 삭제나 retention 변경은 guide 범위가 아니라 runbook escalation 대상이다.
- **Language support**: 언어와 runtime에 따라 CPU, memory, goroutine, mutex, block profile 지원 범위가 다르다.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps pyroscope`
- `docker logs --tail=100 infra-pyroscope`
- `docker exec infra-pyroscope wget -q --spider http://localhost:4040/ready`
- `rg -n 'ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/pyroscope.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/pyroscope.md)
- [Recovery runbook](../../runbooks/06-observability/pyroscope.md)
