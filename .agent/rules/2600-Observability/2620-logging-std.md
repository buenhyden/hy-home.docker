---
trigger: model_decision
glob: ["**/logger/**", "**/monitoring/**", "**/telemetry/**", "**/*log*"]
description: "Logging Standards: Enforces structured JSON formatting, correlation IDs, and severity-driven event reporting."
---

# Observability Logging Standard

- **Role**: Platform Engineer / Developer
- **Purpose**: Define standards for emitting high-quality, structured log events that enable rapid debugging and automated analysis.
- **Activates When**: Implementing logging logic, configuring logger middleware, or handling application exceptions.

**Trigger**: model_decision — Apply during the implementation of logging and error-tracking mechanisms.

## 1. Standards

### Principles

- **[REQ-LOG-01] Machine Readability (JSON)**
  - All production logs MUST be output in structured JSON format. Unstructured "wall of text" logs are STRICTLY PROHIBITED.
- **[REQ-LOG-02] Traceability (Correlation ID)**
  - Every log entry generated within a transaction MUST include a persistent `correlation_id` or `trace_id` to enable request stitching.
- **[REQ-LOG-03] Contextual Exhaustiveness**
  - Logs MUST include sufficient metadata (e.g., service version, host, environment) to localize the origin of the event.

### Log Severity Matrix

| Level | Use Case | Action Required |
| --- | --- | --- |
| FATAL | System crash / Unrecoverable | Immediate On-call Page |
| ERROR | Functional failure (e.g., 5xx) | Ticket / Sentry Alert |
| WARN | Unusual but non-fatal (e.g., 4xx) | Monitor trends |
| INFO | State transitions (e.g., Start/Stop) | None (Searchable) |
| DEBUG | Detailed diagnostic | None (Development only) |

### Must

- **[REQ-LOG-04] Explicit Exception Logging**
  - Exceptions MUST be logged with their full stack trace and associated contextual variables.
- **[REQ-LOG-05] Correlation Propagation**
  - The `correlation_id` MUST be injected into the logging context at the earliest possible entry point of the application.
- **[REQ-LOG-06] Atomic Log Writing**
  - Logs SHOULD be written as single, complete JSON objects per event to prevent interleaving in buffered outputs.

### Must Not

- **[BAN-LOG-01] Secret Exposure**
  - Logs MUST NOT contain passwords, API keys, tokens, or unmasked credit card numbers.
- **[BAN-LOG-02] Silent Catches**
  - Code MUST NOT catch exceptions silently without at least a `WARN` or `ERROR` level log entry.

### Failure Handling

- **Stop Condition**: Stop feature deployment if logging middleware is found to strip `trace_id` from downstream events.

## 2. Procedures

- **[PROC-LOG-01] Logger Configuration Audit**
  - IF creating a new microservice THEN MUST verify the logger is configured with the standard JSON formatter and severity filtering.
- **[PROC-LOG-02] Secret Scrubbing Pass**
  - Define and maintain a global redaction list for the logger to automatically mask sensitive field keys.

## 3. Examples

### Structured Error Log (Good)

```json
{
  "level": "ERROR",
  "msg": "Database connection timeout",
  "correlation_id": "req-999",
  "service": "user-api",
  "stack": "Error: ETIMEDOUT at ..."
}
```

## 4. Validation Criteria

- **[VAL-LOG-01] Schema Compliance**
  - [ ] Automated log audit confirms that 100% of production logs are valid JSON objects.
- **[VAL-LOG-02] Traceability Check**
  - [ ] Log aggregator dashboard confirms that search by `correlation_id` returns the complete lifecycle of a request.
- **[VAL-LOG-03] Privacy Scrub Verification**
  - [ ] Penetration test confirms that dummy password strings are correctly masked in the logging output.
