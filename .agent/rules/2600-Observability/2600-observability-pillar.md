---
trigger: model_decision
glob: ["**/*"]
description: "Observability Pillar: Enforces OpenTelemetry standards for structured logging, distributed tracing, and symptom-based alerting."
---

# Observability Pillar

- **Role**: Site Reliability Engineer (SRE) / Observability Lead
- **Purpose**: Provide granular visibility into system health, performance, and distributed behavior.
- **Activates When**: Defining application metrics, configuring alert rules, or implementing structured logging.

**Trigger**: model_decision — Apply during infrastructure setup and system instrumentation.

## 1. Standards

### Principles

- **[REQ-OBS-01] Structured Telemetry**
  - Logging MUST utilize structured formats (JSON) to facilitate machine readability and analysis.
- **[REQ-OBS-02] Distributed Propagation**
  - Trace context (W3C TraceContext) MUST be propagated across all service boundaries.
- **[REQ-OBS-03] RED Method Metrics**
  - Every service MUST emit metrics for Rate, Errors, and Duration (RED).

### Telemetry Domains

| Domain | Standard Tooling | Core Goal |
| --- | --- | --- |
| Logging | Winston / Logrus / JSON | Audit & Debugging |
| Metrics | Prometheus / OTLP | Trend Analysis |
| Tracing | OpenTelemetry (OTLP) | Request Latency |

### Must

- **[REQ-OBS-04] Trace Context Injection**
  - Every outgoing HTTP/RPC call MUST include the parent trace ID in its headers.
- **[REQ-OBS-05] Correlation IDs**
  - Logs MUST include a `correlation_id` to link multiple log entries to a single user request.
- **[REQ-OBS-06] Symptom-Based Alerting**
  - Alerts MUST be triggered by user-facing symptoms (e.g., High Error Rate) rather than internal causes (e.g., High CPU) unless critical.
- **[REQ-OBS-07] Continuity Targets**
  - All systems MUST define RPO/RTO goals in line with the root `OPERATIONS.md`.

### Must Not

- **[BAN-OBS-01] PII in Telemetry**
  - Personally Identifiable Information (PII) MUST NOT be included in metrics or trace spans.
- **[BAN-OBS-02] Log Noise**
  - Avoid high-frequency "Heartbeat" or "Info" logs that do not provide actionable state transition data in production.

### Failure Handling

- **Stop Condition**: Stop the deployment if a service fails to register its instrumentation with the central collector.

## 2. Procedures

- **[PROC-OBS-01] Dashboard Verification**
  - IF adding a new service THEN MUST create a corresponding Grafana dashboard using the RED method.
- **[PROC-OBS-02] Alert Drill**
  - Periodically verify that PagerDuty or notification integrations correctly route alerts to the on-call team.

## 3. Examples

### Structured Log (Good)

```json
{
  "level": "error",
  "msg": "Transaction failed",
  "trace_id": "ab123...",
  "status_code": 500
}
```

## 4. Validation Criteria

- **[VAL-OBS-01] Trace Visibility**
  - [ ] Distributed requests are traceable from the Gateway to the final Database call in Jaeger.
- **[VAL-OBS-02] Metric Availability**
  - [ ] Prometheus queries return valid time-series data for all RED metrics on new services.
- **[VAL-OBS-03] Alert Integrity**
  - [ ] A simulated error surge triggers the "High Error Rate" alert within < 2 minutes.
