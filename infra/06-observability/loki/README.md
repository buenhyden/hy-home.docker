# Loki Log Aggregation System

> Cloud-native log aggregation system inspired by Prometheus.

## Audience

- **Developers**: Application log debugging and correlation.
- **SREs**: Retention policy management and performance tuning.
- **AI Agents**: Automated log analysis and root cause identification.

## Scope

- **In-Scope**:
  - Log ingestion via Alloy (OTLP/Docker).
  - Log storage and indexing in MinIO.
  - Log querying using LogQL.
- **Out-of-Scope**:
  - Direct syslog ingestion (handled by collectors).
  - Long-term audit archiving beyond 90 days.

## Tech Stack

| Component | Technology | Version | Backend |
| :--- | :--- | :--- | :--- |
| Logging | Loki | v3.6.6 | MinIO (S3) |

## Available Scripts

### 1. Management

- `docker compose up -d loki`: Start Loki service.
- `docker compose logs -f loki`: Follow Loki internal logs.

### 2. Verification

- `wget -qO- http://localhost:3100/ready`: Check Loki readiness.
- `curl http://localhost:3100/metrics`: View Loki internal metrics.

## Usage

### Direct Search

1. In Grafana, select the **Loki** datasource.
2. Use the `Explore` tab for ad-hoc LogQL queries.

### Trace Context

1. Locate a trace in **Tempo**.
2. Click the **Logs for this span** button to jump to Loki with the correct time range and labels.

### Alerting

1. Prometheus Alertmanager monitors Loki via recorded rules.
2. High-priority log patterns trigger Slack/Discord notifications.

## Configuration

### 1. Storage Integration

Loki is configured to use MinIO as its primary storage backend for both index and chunks.

- **Bucket**: `loki-bucket`
- **Primary URL**: `https://loki.${DEFAULT_URL}`
- **Storage Backend**: MinIO (S3 compatible)
- **Retention Strategy**: 7-day automated deletion via Compactor.
- **Log Source**: Grafana Alloy (OTLP/Loki push)
- **Auth**: REST API restricted to internal network; visualize via Grafana.

### 2. Retention Policy

Retention is enabled and currently set to **7 days (168h)** by default.

- **Compactor**: Automatically cleans up expired logs in MinIO.

## AI Agent Guidance

### 1. Querying Strategy

- Use **LogQL** for structured log analysis.
- Filter by `app` or `container_name` to reduce query load.

### 2. Troubleshooting

- If logs are missing, check **Alloy** collector status first.
- For high latency queries, check **Ingester** memory usage.

### 3. Contextual Retrieval

- Correlate logs with metrics using common labels (e.g., `service_name`).

---
[System Guide](../../../docs/05.operations/guides/06-observability/loki.md) | [Operational Policy](../../../docs/05.operations/guides/06-observability/loki.md) | [Recovery Runbook](../../../docs/05.operations/guides/06-observability/loki.md)

---

## Overview

`infra/06-observability/loki`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.

## Structure

```text
infra/06-observability/loki/
├── config/  # 하위 구성 영역
├── docker-entrypoint.sh  # 구성 파일
├── Dockerfile  # 구성 파일
└── README.md  # This file
```

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

## Related Documents

- [infra/README.md](../../README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
- [docs/05.operations/README.md](../../../docs/05.operations/README.md)
