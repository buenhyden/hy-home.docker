---
trigger: always_on
glob: "**/*.{yml,yaml,prometheus,rules}"
description: "Prometheus: Metrics Design, Alerting, and best practices."
---
# Prometheus Standards

## 1. Metric Types

- **Counter**: For monotonically increasing values (requests, errors). Use `rate()`.
- **Gauge**: For values that go up/down (memory, queue depth).
- **Histogram**: For distributions (latency, size). Use buckets.

### Example: Metrics

**Good**

```python
# Counter
requests_total = Counter('http_requests_total', 'Total HTTP requests', ['method', 'status'])
# Gauge
active_connections = Gauge('active_connections', 'Active TCP connections')
```

## 2. Naming & Labels

- **Snake Case**: `http_response_time_seconds`.
- **Units**: Suffix with unit (e.g., `_seconds`, `_bytes`, `_total`).
- **Cardinality**: Avoid high-cardinality labels (e.g., User IDs, IP addresses).

### Example: Labels

**Good**
`http_requests_total{method="POST", status="200"}`

**Bad**
`http_requests_total{user_id="12345"}` # Explodes metric count

## 3. PromQL Best Practices

- **Rates**: Always use `rate()` or `irate()` with Counters.
- **Windows**: Use aligned windows (e.g., `[5m]`).

## 4. Alerting

- **Symptoms**: Alert on symptoms (latency high, errors high), not causes (CPU high).
- **Fatigue**: Group alerts to avoid storms. Use `for: 5m` clauses.
