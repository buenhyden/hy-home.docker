# Alertmanager Notification Routing

## Overview

Alertmanager handles alerts sent by Prometheus, then deduplicates, groups, inhibits, silences, and routes them to the configured receiver integrations. In this stack it runs as `infra-alertmanager`, uses `prom/alertmanager:v0.33.0`, stores runtime state in `alertmanager-data`, and renders Docker Secret values into an ephemeral `/tmp/config.yml` at startup.

## Audience

이 README의 주요 독자:

- SREs (Alert routing & integration)
- On-call Engineers (Silencing & troubleshooting)
- DevOps Engineers (Configuration management)
- AI Agents (Automated silence management)

## Scope

### In Scope

- Alertmanager source configuration (`config/config.yml`) and startup rendering into `/tmp/config.yml`.
- Notification routing rules and receiver integrations.
- Silencing and inhibition rules.
- Local deployment, protected route, readiness, and connectivity settings.

### Out of Scope

- Alert rule definitions (Managed in Prometheus/Loki).
- Global telemetry collection (Managed in Grafana Alloy).
- Persistent storage for metrics (Managed in Prometheus TSDB).

## Structure

```text
alertmanager/
├── config/
│   └── config.yml    # Git-managed routing config with secret placeholders
└── README.md         # This file
```

## How to Work in This Area

1. **Understand Routing**: Review `config/config.yml` to understand how alerts are grouped, inhibited, silenced, and dispatched.
2. **Configuration Updates**: Edit `config/config.yml`; Compose mounts it as `/etc/alertmanager/config.yml.template` and renders secrets into `/tmp/config.yml` at startup.
3. **Secret Integration**: Ensure Docker Secrets for SMTP and Slack webhook are mounted before deployment. Do not record rendered secret values.
4. **Silence Management**: Use the Alertmanager UI/API for temporary alert silences during maintenance, and always set an expiry.
5. **Runtime Checks**: Use the linked guide and runbook before changing route, receiver, inhibition, secret, or middleware policy.

## Tech Stack

| Category     | Technology   | Version | Notes                          |
| :----------- | :----------- | :------ | :----------------------------- |
| Alerting     | Alertmanager | v0.33.0 | Single compose service with Docker Secret-rendered config |
| Integrations | Slack / SMTP | -       | Webhook and SMTP relay         |

## Available Scripts

| Command                  | Description                 |
| :----------------------- | :-------------------------- |
| `docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d alertmanager` | Start Alertmanager from the repository root |
| `docker compose -f infra/06-observability/docker-compose.yml --profile obs restart alertmanager` | Apply configuration changes from the repository root |
| `docker compose -f infra/06-observability/docker-compose.yml --profile obs logs -f alertmanager` | Tail Alertmanager logs from the repository root |

## Configuration

### Docker Secrets

| Secret | Required | Description |
| :----- | :------- | :---------- |
| `slack_webhook` | Yes | Slack incoming webhook endpoint rendered into `__SLACK_WEBHOOK_URL__` |
| `smtp_username` | Yes | SMTP authentication username rendered into `__SMTP_USERNAME__` |
| `smtp_password` | Yes | SMTP authentication password rendered into `__SMTP_PASSWORD__` |

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify service readiness with `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alertmanager` and `docker exec infra-alertmanager wget -q --spider http://localhost:9093/-/ready`.
- Verify routing tree syntax by checking `docker logs --tail=200 infra-alertmanager` after `config.yml` changes.
- Confirm Prometheus delivery with `rg -n 'alertmanagers:|targets: \["alertmanager:9093"\]' infra/06-observability/prometheus/config/prometheus.yml`.
- Confirm receiver connectivity by triggering a test alert and verifying the notification reaches the expected Slack channel.

## Troubleshooting

- Start with `docker compose -f infra/06-observability/docker-compose.yml --profile obs config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For routing tree errors: validate `config.yml` YAML syntax and check that all referenced receivers are defined.
- For notification failures: confirm `slack_webhook`, `smtp_username`, and `smtp_password` Docker Secrets are mounted.
- For inhibition rule issues: review `inhibit_rules` in `config.yml` to ensure source and target match labels are correct.
- Do not capture `/tmp/config.yml` or secret values as troubleshooting evidence.

## Related Documents

- **Guides**: [docs/05.operations/guides/06-observability/alertmanager.md](../../../docs/05.operations/guides/06-observability/alertmanager.md)
- **Policy**: [docs/05.operations/policies/06-observability/alertmanager.md](../../../docs/05.operations/policies/06-observability/alertmanager.md)
- **Runbook**: [docs/05.operations/runbooks/06-observability/alertmanager.md](../../../docs/05.operations/runbooks/06-observability/alertmanager.md)

## AI Agent Guidance

1. **Silences**: Proactively create silences during planned infrastructure maintenance to prevent alert fatigue.
2. **Grouping**: Keep alert grouping aligned with `alertname`, `job`, `domain`, and `severity` unless the policy and config are changed together.
3. **Secret Rotation**: Trigger a service restart whenever the `slack_webhook`, `smtp_username`, or `smtp_password` Docker Secrets are rotated.
4. **Evidence Hygiene**: Record Secret IDs and command results only; never paste rendered webhook, SMTP username, or SMTP password values.
