---
trigger: model_decision
glob: ["**/*"]
description: "Observability Strategy: Enforces the three pillars of telemetry (Metrics, Logs, Tracing) and cross-domain correlation standards."
---

# Observability Strategy Standard

- **Role**: Site Reliability Engineer (SRE)
- **Purpose**: Define the foundational strategy for system visibility and rapid root-cause analysis through holistic telemetry.
- **Activates When**: Architecting observability pipelines, instrumenting new services, or configuring telemetry correlation.

**Trigger**: model_decision — Apply during the design of system monitoring and observability capabilities.

## 1. Standards

### Principles

- **[REQ-OBS-01] The Telemetry Triad**
  - All production systems MUST implement the three pillars of observability: Metrics (for status), Logs (for context), and Tracing (for causality).
- **[REQ-OBS-02] Transactional Correlation**
  - Telemetry assets MUST share a unified correlation ID (TraceID) to enable seamless navigation between logs, traces, and metrics.
- **[REQ-OBS-03] User-Centric Measurement**
  - Observability efforts MUST prioritize metrics that directly reflect user experience (e.g., Latency, Error Rate, Saturation).

### Observability Domains

| Domain | Requirement ID | Critical Requirement |
| --- | --- | --- |
| Metrics | [REQ-OBS-04] | Count requests & Measure latency (Histograms) |
| Logging | [REQ-OBS-05] | Structured JSON with severity levels |
| Tracing | [REQ-OBS-06] | Context propagation via `traceparent` headers |

### Must

- **[REQ-OBS-07] Structured Telemetry**
  - All logs and events MUST be emitted in a machine-readable structured format (JSON).
- **[REQ-OBS-08] Correlation Propagation**
  - Distributed services MUST propagate trace context across asynchronous boundaries (e.g., Message Queues, Webhooks).
- **[REQ-OBS-09] Baseline Dashboarding**
  - Every critical service MUST have a standard dashboard displaying the "Four Golden Signals" (Latency, Traffic, Errors, Saturation).

### Must Not

- **[BAN-OBS-01] PII Leakage**
  - Telemetry data (Logs/Traces) MUST NOT contain Personally Identifiable Information (PII) or secrets.
- **[BAN-OBS-02] High-Cardinality Logging**
  - Avoid logging excessively large blobs or high-cardinality fields that cause storage explosion or performance degradation.

### Failure Handling

- **Stop Condition**: Stop deployment if a critical path service is identified to lack trace context propagation.

## 2. Procedures

- **[PROC-OBS-01] SLI Identification**
  - IF defining observability for a new service THEN MUST identify the top 3 Service Level Indicators (SLIs) first.
- **[PROC-OBS-02] PII Scrubbing Audit**
  - Perform weekly automated scans of logging sinks to detect and redact accidentally leaked PII.

## 3. Examples

### Correlated Telemetry (Conceptual)

```json
{
  "timestamp": "2024-01-26T12:00:00Z",
  "level": "INFO",
  "trace_id": "a1b2c3d4-e5f6-7890",
  "span_id": "b1b2b3b4",
  "msg": "Order processed successfully",
  "order_id": "ord_777"
}
```

## 4. Validation Criteria

- **[VAL-OBS-01] Correlation Integrity**
  - [ ] Distributed tracing confirms that a single request can be followed across all service boundaries.
- **[VAL-OBS-02] PII Audit Pass**
  - [ ] Automated security scanners confirm zero PII patterns in the central logging aggregator.
- **[VAL-OBS-03] Golden Signal Presence**
  - [ ] Monitoring system confirms that all 4 Golden Signals are being reported for every production service.
