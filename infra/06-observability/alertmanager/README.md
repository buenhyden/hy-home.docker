# Alertmanager

> Alert routing and notification management engine.

## Overview

Alertmanager handles alerts sent by Prometheus, grouping and routing them to the appropriate notification channels (Slack, Email).

## Structure

```text
alertmanager/
├── config/
│   └── config.yml       # Alert routing & receiver configuration
└── README.md           # This file
```

## Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| Routing | prom/alertmanager:v0.30.0 | Alert grouping & delivery |
| Receivers | Slack, SMTP | Notification channels |

## Configuration

- **Config File**: `config/config.yml`.
- **Integrations**: Uses Docker Secrets for SMTP and Slack credentials.
- **Routes**: Grouped by severity and service, routing to `team-notifications` by default.

## Persistence

- **State**: Persistent volume (not explicitly defined in the provided scope, typically handles silence/notification state internally).

## Operational Status

> [!WARNING]
> Ensure SMTP credentials and Slack webhooks are correctly configured in Docker Secrets to prevent silence on critical failures.

---

Copyright (c) 2026. Licensed under the MIT License.
