# Grafana Alloy Unified Collector

> Advanced telemetry pipeline and OTLP gateway.

## Overview

Alloy is the unified collection agent for the `hy-home.docker` platform. It replaces legacy agents by providing a programmable configuration (Alloy HCL) to collect, process, and export metrics, logs, and traces. It acts as the primary OTLP gateway for all applications within the infrastructure.

## Audience

이 README의 주요 독자:

- Developers (Data ingestion and instrumentation)
- Operators (Pipeline monitoring and tuning)
- SREs (Cross-tier telemetry governance)
- AI Agents (Automated troubleshooting and onboarding)

## Scope

### In Scope

- **Ingestion**: OTLP (gRPC/HTTP), Docker socket discovery.
- **Processing**: Target relabeling, metadata enrichment, batching.
- **Exporting**:
  - Metrics -> Prometheus
  - Logs -> Loki
  - Traces -> Tempo
  - Profiling -> Pyroscope
- **Status**: Live pipeline debugging via Alloy UI.

### Out of Scope

- **Storage**: Metric/Log/Trace persistence (managed by Prometheus/Loki/Tempo).
- **Visualization**: Dashboards (managed by Grafana).
- **Instrumentation**: Application-side SDK implementation.

## Structure

```text
alloy/
├── config/
│   └── config.alloy  # Telemetry pipeline definition (HCL)
└── README.md         # This file
```

## How to Work in This Area

1. Follow the [Alloy Guide](../../../docs/05.operations/guides/06-observability/alloy.md).
2. Modify `config.alloy` to add new pipeline components or relabeling rules.
3. Access the Alloy UI at `http://alloy.${DEFAULT_URL}` to debug pipelines and check component status.
4. Verify changes in the [Alloy Operation Policy](../../../docs/05.operations/guides/06-observability/alloy.md).

## Tech Stack

| Category  | Technology    | Version | Notes                    |
| :-------- | :------------ | :------ | :----------------------- |
| Collector | Grafana Alloy | v1.13.1 | Unified agent            |
| Protocol  | OTLP          | v1.x    | Standard interface       |
| Runtime   | Docker        | Latest  | Containerized deployment |

## Available Scripts

| Command                        | Description                 |
| :----------------------------- | :-------------------------- |
| `docker compose restart alloy` | Apply configuration changes |
| `docker compose logs -f alloy` | Tail collector logs         |

## Configuration

### Environment Variables

| Variable               | Required | Description                        |
| :--------------------- | :------: | :--------------------------------- |
| `ALLOY_PORT`           |    No    | UI listening port (Default: 12345) |
| `ALLOY_OTLP_GRPC_PORT` |    No    | OTLP gRPC port (Default: 4317)     |
| `ALLOY_OTLP_HTTP_PORT` |    No    | OTLP HTTP port (Default: 4318)     |

## AI Agent Guidance

1. **OTLP First**: Prefer `OTLP` ingestion for all new application instrumentation to ensure future-proof telemetry.
2. **Metadata Enrichment**: Use Alloy's `discovery.docker` for automatic container metadata enrichment (service_name, env, scope).
3. **Performance**: Monitor `batch` processing metrics via the Alloy UI to prevent data loss or latency during high load periods.
4. **Relabeling Rules**: When adding new services, ensure relabeling rules in `config.alloy` correctly assign the `scope` (infra vs app).

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify OTLP pipeline health by checking `docker logs alloy | grep -i "error\|warn"` after `config.alloy` changes.
- Confirm telemetry forwarding by verifying Prometheus, Loki, Tempo, and Pyroscope receive data from Alloy exporters.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For OTLP ingestion errors: verify port bindings (`ALLOY_OTLP_GRPC_PORT`, `ALLOY_OTLP_HTTP_PORT`) and check that applications target the correct Alloy endpoint.
- For collector config errors: validate `config.alloy` HCL syntax and check the Alloy UI at `http://alloy.${DEFAULT_URL}` for component status.
- For exporter errors: confirm downstream services (Prometheus, Loki, Tempo, Pyroscope) are reachable and their endpoints match `config.alloy` export targets.

## Related Documents

- **System Guide**: [docs/05.operations/06-observability/alloy.md](../../../docs/05.operations/guides/06-observability/alloy.md)
- **Operations**: [docs/05.operations/06-observability/alloy.md](../../../docs/05.operations/guides/06-observability/alloy.md)
- **Runbooks**: [docs/05.operations/06-observability/alloy.md](../../../docs/05.operations/guides/06-observability/alloy.md)
