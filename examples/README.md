# Developer & Integration Examples (`examples/`)

This directory provides **functional patterns** for integrating applications with the platform's infrastructure tiers.

## 1. Core Integration Hub

Use these examples to connect your application to the core infrastructure capabilities.

### Telemetry & Observability

- **[OTLP Application Integration](app-compose-telemetry.yml)**: How to push traces and metrics to **Grafana Alloy** (`alloy:4317`).
- **[Custom Alerts](prometheus-custom-alerts.yml)**: Define Prometheus alerting rules for application-specific SLOs.

### Infrastructure Configuration

- **[Infrastructure Environment Variables](.env.infra.example)**: Reference for core stack tuning (Ports, Memory Limits).

## 2. Documentation Examples

Reference formats for maintaining the platform's "Infrastructure-as-Documentation" standard.

- **[Architecture Decision (ADR)](example-adr.md)**: Decision template (`Why`).
- **[Product Requirements (PRD)](example-prd.md)**: Feature template (`What`).
- **[Procedural Manual (Runbook)](example-runbook.md)**: Recovery template (`How`).

## 3. Quick-Start: Connecting to Tiers

| Capability | Integration Endpoint | Context Link |
| --- | --- | --- |
| **Object Storage**| `minio:9000` | [MinIO Guide](../docs/context/04-data/minio-s3-guide.md) |
| **Pub/Sub**      | `kafka-1:19092` | [Kafka Guide](../docs/context/05-messaging/kafka-kraft-guide.md) |
| **Secrets**      | `/run/secrets/*` | [Identity Guide](../docs/context/02-auth/keycloak-idp-guide.md) |
| **Telemetry**    | `alloy:4317` | [LGTM Blueprint](../docs/context/06-observability/lgtm-stack-blueprint.md) |

---
> [!TIP]
> Always check the [Technical Context](../docs/context/README.md) for precise port mappings and service labels before configuring your `docker-compose.yml`.
