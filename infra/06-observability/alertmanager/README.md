# Alertmanager Notification Routing

> Centralized alert routing, deduplication, and notification gateway.

## Overview

Alertmanager handles alerts sent by client applications such as Prometheus. It takes care of deduplicating, grouping, and routing them to the correct receiver integration such as Slack or E-mail. It also takes care of silencing and inhibition of alerts.

## Audience

- SREs (Alert routing & integration)
- On-call Engineers (Silencing & troubleshooting)

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Alerting | Alertmanager | v0.30.0 |

## Configuration

- **Routing**: Defined in `alertmanager/config/config.yml.template`.
- **Integrations**: Slack Webhooks and SMTP credentials (injected via secrets).

## AI Agent Guidance

1. Use `Silences` during planned maintenance to prevent alert fatigue.
2. Group alerts by `alertname` and `service` to minimize notification noise.
3. Ensure the `slack_webhook` secret is updated in Vault before deployment.
