# Alertmanager

Alertmanager handles alerts sent by client applications such as Prometheus server. It takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, Slack, PagerDuty, or OpsGenie.

## 🚀 Overview

- **Service**: `alertmanager`
- **Docker Image**: `prom/alertmanager:v0.30.0`
- **Port**: `9093` (Web UI/API)

## ⚙️ Configuration

The configuration file is located at `config/config.yml`.

### Setup

1. **Copy the example configuration:**

   ```bash
   cp config.yml.example config.yml
   ```

2. **Edit `config.yml`:**
   - Update email settings (`smtp_auth_username`, `smtp_auth_password`) if you want email notifications.
   - Slack Webhook은 파일에 직접 넣지 않고 `SLACK_ALERTMANAGER_WEBHOOK_URL`로 주입합니다.
   - Ensure the `route.receiver` matches your desired default receiver.

### Key Settings

- **`global`**: Contains SMTP configuration for email alerts.
- **`route`**: Defines how alerts are grouped and routed.
- **`receivers`**: Defines notification channels (Email, Slack, etc.).

## 🔐 Secrets Management

**⚠️ CAUTION:** `config.yml` may contain sensitive information (SMTP passwords).

- **Do not commit `config.yml` to Git.**
- The `.gitignore` should already exclude `config.yml`.
- Slack Webhook은 `SLACK_ALERTMANAGER_WEBHOOK_URL` 환경변수로 주입됩니다.

## 🔗 Integration

- **Prometheus**: Sends fired alerts to Alertmanager.
- **Traefik**: Exposed via `alertmanager.${DEFAULT_URL}` (HTTPS).

## 🛠 Directory Structure

```text
alertmanager/
├── config/
│   ├── config.yml          # Template (SLACK_ALERTMANAGER_WEBHOOK_URL 치환)
│   └── config.yml.example  # Template configuration
└── README.md
```
