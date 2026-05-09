# Tempo Distributed Tracing

> High-scale distributed tracing backend within the `06-observability` tier.

## Overview

Tempo stores trace data in an S3-compatible backend (MinIO). It enables "TraceQL" for powerful querying and allows correlation between metrics, logs, and traces starting from a Span ID. It also generates span metrics and service graphs automatically.

## Audience

이 README의 주요 독자:

- Backend Developers (Latency analysis)
- SRE / DevOps Engineers (System bottleneck identification)
- AI Agents

## Scope

### In Scope

- Tempo service configuration and deployment.
- OTLP trace data ingestion and storage.
- Span metrics and Service Graph generation.

### Out of Scope

- Application-level instrumentation (handled by OpenTelemetry SDKs).
- Long-term trace archival (governed by [Retention Policy](../../../docs/08.operations/06-observability/tempo.md)).

## Structure

```text
tempo/
├── README.md           # This file
├── config/
│   └── tempo.yaml      # Main configuration file
└── Dockerfile          # Custom Tempo image build
```

## Tech Stack

| Category | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| Tracing | [Grafana Tempo](https://github.com/grafana/tempo) | v2.10.1-custom | Distributed Tracing Backend |
| Storage | [MinIO](../../04-data/lake-and-object/minio/README.md) | latest | S3-Compatible Object Store |
| Ingestion | [Grafana Alloy](../alloy/README.md) | v1.13.1 | OTLP Receiver & Forwarder |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d tempo` | Start Tempo service |
| `docker compose logs -f tempo` | Follow Tempo logs |

## Configuration

- **Ingestion**: Supports OTLP via gRPC (4317) and HTTP (4318).
- **Persistence**: Bucket `tempo-bucket` in MinIO.
- **WAL**: Local disk used for write-ahead logging (`/var/tempo/wal`).

## Operational Status

> [!IMPORTANT]
> Tempo is configured with a **24-hour block retention policy**. Ensure critical performance issues are investigated within this timeframe or exported.

## AI Agent Guidance

1. **TraceQL Analysis**: Use TraceQL to correlate high-latency spans with specific service names and status codes.
2. **Service Graphs**: Verify `metrics_generator` is active to visualize service dependency maps in Grafana.
3. **Storage Health**: Monitor MinIO bucket availability if trace ingestion gaps occur.

## Related References

- [System Guide](../../../docs/07.guides/06-observability/tempo.md)
- [Operational Policy](../../../docs/08.operations/06-observability/tempo.md)
- [Recovery Runbook](../../../docs/09.runbooks/06-observability/tempo.md)

---

Copyright (c) 2026. Licensed under the MIT License.

---

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
