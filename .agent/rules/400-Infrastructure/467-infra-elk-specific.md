---
trigger: always_on
glob: "**/*"
description: "ELK Stack: Structured Logging, Correlation IDs, and ILM."
---
# ELK Stack (Elasticsearch, Logstash, Kibana) Standards

## 1. Logging Strategy

- **Stdout**: Write logs to `stdout` (JSON format). Do NOT write to files.
- **Structured**: Use structured JSON. No implementation-specific string formats.
- **Schema**: Enforce `service.name`, `@timestamp`, `log.level`, `trace.id`.

### Example: Structured Log

**Good**

```json
{
  "@timestamp": "2023-10-27T10:00:00Z",
  "log.level": "INFO",
  "service.name": "payment-service",
  "trace.id": "abc-123",
  "message": "Payment processed",
  "amount": 100.00
}
```

**Bad**

```text
2023-10-27 10:00:00 INFO Payment processed for 100.00
```

## 2. Distributed Tracing

- **Correlation**: Inject `trace.id` and `span.id` into all logs.
- **Propagation**: Propagate headers (B3 or W3C) between microservices.

## 3. Index Lifecycle Management (ILM)

- **Policies**: Configure rollover, shrink, and delete phases.
- **Prevention**: Prevent "shard explosion" by managing index size/count.

## 4. Log Levels

- **Production**: `INFO` or `WARN`. Never `DEBUG`.
- **Sensitivity**: Scrub PII and secrets BEFORE logging.
