# n8n Low-Code Automation Context

> **Component**: `n8n`
> **Workflow Pattern**: Distributed Queue Mode
> **Message Broker**: `mng-redis` (Valkey)

## 1. Enterprise-Scale Workflow Engine

n8n is deployed using a distributed architecture to ensure reliability and performance.

- **Main URL**: `https://n8n.${DEFAULT_URL}`
- **Database**: SQLite (local dev) or Management PostgreSQL.
- **Queue Mode**: Enabled. Workloads are distributed to `n8n-worker` containers.

## 2. Webhook Infrastructure

To receive external events (Github, CircleCI, etc.):

1. Ensure `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false` is set for Docker mounts.
2. The `WEBHOOK_URL` must match the external Traefik entrypoint.

## 3. Persistent Storage

All custom nodes and credentials reside in `/home/node/.n8n` within the container, mapped to a host volume.

- **Migration Advice**: Before upgrading n8n major versions, take a binary snapshot of the SQLite database.
