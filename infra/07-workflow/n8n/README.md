# n8n Low-code Automation

> Rapid workflow automation and third-party integrations.

## Overview

n8n provides a visual interface for building automation workflows. It is used for connecting various APIs, handling webhooks, and automating simple business processes that do not require the full complexity of an Airflow DAG.

## Audience

- Developers (Rapid prototyping)
- Operators (Integration logic)

## Structure

```text
n8n/
├── Dockerfile          # Custom n8n build with extra dependencies
├── docker-compose.yml  # n8n service configuration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [n8n Automation Guide](../../../docs/07.guides/07-workflow/02.n8n-automation.md).
2. Access the UI at `http://n8n.${DEFAULT_URL}`.

## Tech Stack

| Component | Technology | Version |
| :--- | :--- | :--- |
| Automation | n8n | v1.64.3 |
| DB | PostgreSQL | Persistence |

## AI Agent Guidance

1. Use `Sub-workflows` to modularize complex automation logic.
2. Credentials should be securely stored in n8n's internal encrypted database.
3. Regularly export and version-control critical workflows as JSON.
