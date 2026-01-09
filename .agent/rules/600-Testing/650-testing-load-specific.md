---
trigger: always_on
glob: "**/*.{js,py}"
description: "Load Testing: k6, Locust, Thresholds, and Cloud Integration."
---
# Load Testing Standards

## 1. Tools

- **k6**: Preferred for CI/CD integration (JS-based). Best for developers.
- **Locust**: Preferred for Python-heavy teams (Python-based).

## 2. Scenarios

- **Smoke**: Minimal load (~1 VU) to verify system health.
- **Load**: Expected production load to find bottlenecks.
- **Soak**: Long duration (hours) to find memory leaks.
- **Spike**: Sudden surge to test auto-scaling behavior.

### Example: k6 Thresholds

**Good**

```javascript
export const options = {
  vus: 50,
  duration: '5m',
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'], // Error rate < 1%
  },
};
```

**Bad**

```javascript
// No assertions, just spamming requests with no pass/fail criteria
```

## 3. Environment

- **Isolation**: NEVER load test Production (unless strict protocols). Use Staging.
- **Data**: Use synthetic data that mirrors production volume.

## 4. Integration

- **k6 Cloud / Grafana Cloud**: For distributed load generation and analytics.
- **CI**: Integrate into CI/CD to catch performance regressions on every deploy.
