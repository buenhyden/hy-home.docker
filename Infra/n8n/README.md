# n8n (Workflow Automation)

## Overview

n8n is an extendable workflow automation tool. This deployment is configured in **Queue Mode** (Scalable Architecture) to handle high-volume workloads by separating the Editor/Webhook handling from the actual execution processing.

## Architecture

- **Main Node (`n8n`)**: Handles the Web Editor, API, and incoming Webhooks. Delegates execution to the queue.
- **Worker Node (`n8n-worker`)**: Picks up jobs from Redis and executes them. Can be scaled horizontally.
- **Queue (`n8n-valkey`)**: A dedicated Valkey (Redis) instance acting as the job broker.

## Custom Build

This directory contains a `Dockerfile` intended for building n8n from source (requires a `./compiled` directory).

> [!NOTE]
> **Advanced Usage Only**: This Dockerfile is not for simple extensions (like adding Python packages). It expects pre-compiled n8n source code. For standard deployments, use the official image defined in `docker-compose.yml`.

### How to use (Advanced)

1. Ensure you have compiled n8n source code in `./compiled`.
2. Uncomment the `build` section in `docker-compose.yml` (if added) or run:

   ```bash
   docker build -t custom-n8n .
   ```

## Services & Networking

All services run on the `infra_net` network with **Static IPs**:

| Service | Role | Static IPv4 | Port |
| :--- | :--- | :--- | :--- |
| `n8n` | Editor / Webhooks | `172.19.0.14` | `${N8N_PORT}` (5678) |
| `n8n-worker` | Job Executor | `172.19.0.17` | - |
| `n8n-valkey` | Job Queue | `172.19.0.15` | `${VALKEY_PORT}` |
| `n8n-valkey-exporter` | Queue Metrics | `172.19.0.16` | `${VALKEY_EXPORTER_PORT}` |

## Key Configuration

## Environment Variables

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

## Traefik Configuration

- **Domain**: `n8n.${DEFAULT_URL}`
- **Entrpoint**: `websecure` (TLS Enabled)
- **Service**: Points to the Main Node (`n8n`) on port `${N8N_PORT}`.

## Data Persistence

- **n8n Data**: `n8n-data` (Mapped to `/home/node/.n8n`)
- **Queue Data**: `n8n-valkey-data` (Mapped to `/data`)

## Usage

### Web Editor

- **URL**: `https://n8n.<your-domain>`
- **Login**: Setup your admin account on first access.

### Worker Scaling

To scale processing power, you can increase the replicas of the worker service (requires Swarm or distinct naming in Compose):

```bash
# Example concept
docker-compose up -d --scale n8n-worker=3
```
