---
trigger: always_on
glob: "**/*.json,**/*.yaml"
description: "Grafana: Dashboards as Code, Variables, USE/Golden Signals, and Linting."
---
# Grafana Standards

## 1. Observability as Code (OaC)

- **Git-Versioned**: Store dashboards as JSON/YAML in Git.
- **Provisioning**: Use Grafana's API for automated deployment.
- **Foundation SDK**: Use TypeScript/Python SDK for complex dashboards.

### Example: Declarative

**Good**

```json
{
  "title": "Service Overview",
  "uid": "service-overview",
  "panels": [ /* ... */ ]
}
```

**Bad**
> Manual UI configuration with no version history.

## 2. Templated Variables

- **Reusability**: Use variables for environment, instance, datacenter.
- **Dynamic Queries**: Use `label_values()` for auto-discovery.

### Example: Variables

**Good**

```json
"templating": {
  "list": [
    { "name": "instance", "type": "query", "query": "label_values(up, instance)" }
  ]
}
```

## 3. Diagnostic Frameworks

- **USE Method**: Utilization, Saturation, Errors for resources.
- **Four Golden Signals**: Rate, Errors, Duration, Saturation for services.
- **Y-Axis**: ALWAYS zero-based. Never auto-scale.

### Example: Metrics

**Good**

```json
{ "targets": [{ "expr": "sum(rate(http_requests_total[5m]))" }] }
```

**Bad**

```json
{ "targets": [{ "expr": "sum(http_requests_total)" }] } // Cumulative, not rate
```

## 4. Linting & CI/CD

- **dashboard-linter**: Integrate `grafana/dashboard-linter` in CI.
- **Peer Review**: Require PR review for all dashboard changes.
