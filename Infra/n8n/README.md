# n8n - Workflow Automation

## Overview

n8n is an extendable workflow automation tool. This setup uses a Queue mode with dedicated main node and workers.

## Services

- **n8n**: Main server (Editor, Webhook handler).
  - URL: `https://n8n.${DEFAULT_URL}`
- **n8n-worker**: Worker node for executing workflows.
- **n8n-valkey**: Dedicated Redis/Valkey for job queue.
- **n8n-valkey-exporter**: Exporter for queue metrics.

## Configuration

### Environment Variables

- `EXECUTIONS_MODE`: `queue`
- `N8N_ENCRYPTION_KEY`: Encryption key for credentials.
- `DB_TYPE`: `postgresdb` (Connects to `mng-pg`)
- `QUEUE_BULL_REDIS_HOST`: `mng-valkey` (or local `n8n-valkey` depending on config)

### Volumes

- `n8n-data`: `/home/node/.n8n`
- `n8n-valkey-data`: `/data`

## Networks

- `infra_net`
  - n8n: `172.19.0.14`
  - n8n-valkey: `172.19.0.15`

## Traefik Routing

- **Domain**: `n8n.${DEFAULT_URL}`
