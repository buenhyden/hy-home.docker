# Observability Stack (LGTM + Alloy) Runbook

## Maintenance & Troubleshooting

### Reloading Configurations

Configurations can be reloaded without service restarts via HTTP POST:

```bash
# Reload Prometheus configuration and alert rules
curl -X POST https://prometheus.${DEFAULT_URL}/-/reload

# Reload Alertmanager configuration
curl -X POST https://alertmanager.${DEFAULT_URL}/-/reload
```

### Checking Scraping Status

- **Metric Targets**: Navigate to `https://prometheus.${DEFAULT_URL}/targets`.
- **Collector Status**: Navigate to `https://alloy.${DEFAULT_URL}` to view the internal component graph.
