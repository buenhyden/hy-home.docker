# n8n Low-Code Automation Context

> **Component**: `n8n`
> **Workflow Pattern**: Distributed Queue Mode
> **Message Broker**: `n8n-valkey` (Valkey)

## 1. Enterprise-Scale Workflow Engine

n8n is deployed in a distributed queue mode for high dependability.

### Technical Specifications

| Attribute | Value |
| --- | --- |
| **Main URL** | `https://n8n.${DEFAULT_URL}` |
| **Database** | Management PostgreSQL (`mng-pg`) |
| **Execution Mode**| `queue` (via Valkey) |
| **Internal Port** | `5678` |

### Infrastructure Components

- **Main Engine**: `n8n` (Main UI and orchestration).
- **Workers**: `n8n-worker` (Executes large workflow payloads).
- **Task Runner**: `n8n-task-runner` (External script execution).
- **Message Broker**: `n8n-valkey` (Execution queue).

### Provisioning Verification

```bash
docker exec n8n curl -f http://localhost:5678/healthz
```

## 2. Webhook Infrastructure

To receive external events (Github, CircleCI, etc.):

1. Ensure `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false` is set for Docker mounts.
2. The `WEBHOOK_URL` must match the external Traefik entrypoint.

## 3. Persistent Storage

All custom nodes and credentials reside in `/home/node/.n8n` within the container, mapped to a host volume.

- **Migration Advice**: Before upgrading n8n major versions, take a binary snapshot of the SQLite database.
