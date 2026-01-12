# n8n (Workflow Automation)

## Overview

n8n is an extendable workflow automation tool. This deployment runs in **Queue Mode** for scalability.

## Service Details

### Components

- **Main**: `n8n` (Editor & Webhook handler)
- **Worker**: `n8n-worker` (Job processor)
- **Queue**: `n8n-valkey` (Redis for job queue)

### Configuration

- **Image**: `n8nio/n8n:2.3.0`
- **Database**: Connects to `mng-pg` (PostgreSQL).
- **Encryption Key**: Managed via `${N8N_ENCRYPTION_KEY}`. Do not change once set.
- **Metrics**: Enabled (`N8N_METRICS=true`).

## Traefik Configuration

- **Domain**: `n8n.${DEFAULT_URL}`
- **Entrypoint**: `websecure`
- **TLS**: Enabled
- **Port**: `${N8N_PORT}` (5678)
