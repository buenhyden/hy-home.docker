# n8n (Workflow Automation)

## Overview

n8n is an extendable workflow automation tool. This deployment is configured in **Queue Mode** (Scalable Architecture) to handle high-volume workloads by separating the Editor/Webhook handling from the actual execution processing.

## Services

- **Service Name**: `n8n`
- **Image**: `n8nio/n8n:2.3.0`
- **Role**: Main Node (Editor/Webhook Receiver/Coordinator)
- **Restart Policy**: `unless-stopped`

- **Service Name**: `n8n-worker`
- **Image**: `n8nio/n8n:2.3.0`
- **Role**: Worker Node (Job Executor)
- **Restart Policy**: `unless-stopped`

- **Service Name**: `n8n-valkey`
- **Image**: `valkey/valkey:9.0.1-alpine`
- **Role**: Job Queue (Redis)
- **Restart Policy**: `unless-stopped`

- **Service Name**: `n8n-valkey-exporter`
- **Image**: `oliver006/redis_exporter:v1.80.1-alpine`
- **Role**: Prometheus Metrics Exporter for Queue
- **Restart Policy**: `unless-stopped`

## Custom Build

This directory contains a `Dockerfile` that allows building n8n from source/npm directly, enabling:

- **Private Nodes**: Installing custom nodes during the build process.
- **System Dependencies**: Adding tools like `pandoc`, `ffmpeg`, or `python3`.
- **Custom Fonts**: Installing Microsoft fonts for better PDF/Image generation.
- **Architecture Control**: Building specifically for the target architecture.

### How to use

1. Open `docker-compose.yml`.
2. Comment out the `image` instruction.
3. Add/Uncomment the `build` instruction:

```yaml
services:
  n8n:
    # image: n8nio/n8n:2.3.0
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - N8N_VERSION=2.3.0
```

1. Rebuild: `docker-compose up -d --build n8n`.

## Networking

All services run on the `infra_net` network with **Static IPs**:

| Service | Role | Static IPv4 | Port |
| :--- | :--- | :--- | :--- |
| `n8n` | Editor / Webhooks | `172.19.0.14` | `${N8N_PORT}` |
| `n8n-worker` | Job Executor | `172.19.0.17` | - |
| `n8n-valkey` | Job Queue | `172.19.0.15` | `${VALKEY_PORT}` |
| `n8n-valkey-exporter` | Queue Metrics | `172.19.0.16` | `${VALKEY_EXPORTER_PORT}` |

## Persistence

- **`n8n-data`** → `/home/node/.n8n`: Persistent storage for n8n user data, workflows, and configuration.
- **`n8n-valkey-data`** → `/data`: Persistent storage for the Valkey queue.

## Configuration

### Core & Security

| Variable | Description | Default |
| :--- | :--- | :--- |
| `EXECUTIONS_MODE` | Execution Mode | `queue` |
| `N8N_ENCRYPTION_KEY` | Encryption Key | `${N8N_ENCRYPTION_KEY}` |
| `WEBHOOK_URL` | Public URL | `https://n8n.${DEFAULT_URL}` |
| `GENERIC_TIMEZONE` | Timezone | `${DEFAULT_TIMEZONE}` |

### Database & Queue

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DB_TYPE` | Database Type | `postgresdb` |
| `DB_POSTGRESDB_HOST` | DB Host | `${POSTGRES_HOSTNAME}` |
| `QUEUE_BULL_REDIS_HOST`| Redis/Valkey Host | `${MNG_VALKEY_HOST}` |
| `QUEUE_BULL_PREFIX` | Redis Key Prefix | `n8n` |

### Metrics

| Variable | Description | Default |
| :--- | :--- | :--- |
| `N8N_METRICS` | Enable Metrics | `true` |
| `N8N_METRICS_PREFIX` | Metric Prefix | `n8n_` |

## Traefik Integration

- **Domain**: `n8n.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service Port**: `${N8N_PORT}`

## Usage

### Web Editor

- **URL**: `https://n8n.${DEFAULT_URL}`
- **Login**: Setup your admin account on first access.

### Worker Scaling

To scale processing power, you can increase the replicas of the worker service (requires Swarm or distinct naming in Compose):

```bash
# Example concept
docker-compose up -d --scale n8n-worker=3
```
