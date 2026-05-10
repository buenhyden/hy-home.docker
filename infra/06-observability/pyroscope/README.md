# Pyroscope Continuous Profiling

> Continuous profiling platform for analyzing application performance within the `06-observability` tier.

## Overview

Pyroscope provides continuous profiling of applications to identify performance bottlenecks, CPU hot paths, and memory leaks. It collects profiling data (CPU, memory, etc.) and allows developers to visualize it over time using flamegraphs.

## Audience

이 README의 주요 독자:

- Backend Developers (Performance optimization)
- SRE / DevOps Engineers (Resource management)
- AI Agents

## Scope

### In Scope

- Pyroscope service configuration and deployment.
- Continuous profiling data ingestion and storage.
- Integration with Grafana for visualization.

### Out of Scope

- Application-level profiling agents (handled by [Grafana Alloy](../alloy/README.md)).
- Long-term archival of profiling data (governed by [Retention Policy](../../../docs/07.operations/06-observability/pyroscope.md)).

## Structure

```text
pyroscope/
├── README.md           # This file
└── config/
    └── pyroscope.yaml  # Main configuration file
```

## Tech Stack

| Category | Technology | Version | Role |
| :--- | :--- | :--- | :--- |
| Profiling | [Grafana Pyroscope](https://github.com/grafana/pyroscope) | v1.18.1 | Continuous Profiling Engine |
| Collector | [Grafana Alloy](../alloy/README.md) | v1.13.1 | Profile Scraping & Remapping |
| Visualization | [Grafana](../grafana/README.md) | v12.3.3 | Unified Dashboards |

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d pyroscope` | Start Pyroscope service |
| `docker compose restart pyroscope` | Apply configuration changes |

## Configuration

- **Ingestion**: Receives profiling data via Protobuf over HTTP (Port 4040).
- **Storage**: Local filesystem backend (`/var/lib/pyroscope`).
- **Retention**: Data is compacted and pruned according to system limits.

## Operational Status

> [!IMPORTANT]
> Pyroscope is configured with a 7-day retention policy to balance visibility and storage costs. For critical performance audits, ensure data is analyzed within this window.

## AI Agent Guidance

1. **Flamegraph Analysis**: Use the `traceqlEditor` feature toggle in Grafana to correlate profiles with traces.
2. **Resource Monitoring**: Profiling ingestion can be CPU-intensive; monitor `infra-pyroscope` container stats during peak loads.
3. **Traceability**: Refer to the dedicated system guide for remapping logic and custom labels.

## Related References

- [System Guide](../../../docs/07.operations/06-observability/pyroscope.md)
- [Operational Policy](../../../docs/07.operations/06-observability/pyroscope.md)
- [Recovery Runbook](../../../docs/07.operations/06-observability/pyroscope.md)

---

Copyright (c) 2026. Licensed under the MIT License.

---

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
