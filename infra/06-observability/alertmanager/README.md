# Alertmanager Notification Routing

> Centralized alert routing, deduplication, and notification gateway.

## Overview

Alertmanager handles alerts sent by client applications such as Prometheus. It takes care of deduplicating, grouping, and routing them to the correct receiver integration (Slack, E-mail, PagerDuty, etc.). Its primary responsibility is ensuring that the right people get the right alerts at the right time while minimizing alert fatigue.

## Audience

이 README의 주요 독자:

- SREs (Alert routing & integration)
- On-call Engineers (Silencing & troubleshooting)
- DevOps Engineers (Configuration management)
- AI Agents (Automated silence management)

## Scope

### In Scope

- Alertmanager runtime configuration (`config.yml`).
- Notification routing rules and receiver integrations.
- Silencing and inhibition rules.
- Local deployment and connectivity settings.

### Out of Scope

- Alert rule definitions (Managed in Prometheus/Loki).
- Global telemetry collection (Managed in Grafana Alloy).
- Persistent storage for metrics (Managed in Prometheus TSDB).

## Structure

```text
alertmanager/
├── config/
│   └── config.yml    # Main routing and receiver configuration
└── README.md         # This file
```

## How to Work in This Area

1. **Understand Routing**: Review `config/config.yml` to understand how alerts are grouped and dispatched.
2. **Configuration Updates**: Always use `config.yml.template` for changes involving secrets (Slack webhooks, SMTP).
3. **Secret Integration**: Ensure Docker Secrets for SMTP and Slack webhook are mounted before deployment.
4. **Silence Management**: Use the Alertmanager UI/API for temporary alert silences during maintenance.

## Tech Stack

| Category     | Technology   | Version | Notes                          |
| :----------- | :----------- | :------ | :----------------------------- |
| Alerting     | Alertmanager | v0.32.1 | Single compose service with Docker Secret-rendered config |
| Integrations | Slack / SMTP | -       | Webhook and SMTP relay         |

## Available Scripts

| Command                  | Description                 |
| :----------------------- | :-------------------------- |
| `docker compose --profile obs up -d alertmanager` | Start Alertmanager service |
| `docker compose --profile obs restart alertmanager` | Apply configuration changes |

## Configuration

### Environment Variables

| Variable            | Required | Description                                 |
| :------------------ | :------- | :------------------------------------------ |
| `SLACK_WEBHOOK_URL` | Yes      | Slack incoming webhook endpoint             |
| `SMTP_PASSWORD`     | Yes      | SMTP authentication password (App Password) |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify routing tree syntax by checking `docker logs infra-alertmanager | grep -i "error\|warn"` after `config.yml` changes.
- Confirm receiver connectivity by triggering a test alert and verifying the notification reaches the target channel.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For routing tree errors: validate `config.yml` YAML syntax and check that all referenced receivers are defined.
- For notification failures: confirm `slack_webhook`, `smtp_username`, and `smtp_password` Docker Secrets are mounted.
- For inhibition rule issues: review `inhibit_rules` in `config.yml` to ensure source and target match labels are correct.

## Related Documents

- **Guides**: [docs/05.operations/06-observability/alertmanager.md](../../../docs/05.operations/guides/06-observability/alertmanager.md)
- **Policy**: [docs/05.operations/policies/06-observability/alertmanager.md](../../../docs/05.operations/policies/06-observability/alertmanager.md)
- **Runbook**: [docs/05.operations/runbooks/06-observability/alertmanager.md](../../../docs/05.operations/runbooks/06-observability/alertmanager.md)

---

## AI Agent Guidance

1. **Silences**: Proactively create silences during planned infrastructure maintenance to prevent alert fatigue.
2. **Grouping**: Group alerts by `alertname` and `service` to minimize notification noise.
3. **Secret Rotation**: Trigger a service restart whenever `SLACK_WEBHOOK_URL` or `SMTP` credentials are rotated in Vault.
