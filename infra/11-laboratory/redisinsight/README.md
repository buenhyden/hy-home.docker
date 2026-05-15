# Laboratory RedisInsight

> Redis visualization, analysis, and management tool.

## Overview

RedisInsight is a powerful GUI for Redis that allows you to visualize, analyze, and manage your Redis data. It provides features like key browsing, memory profiling, and real-time monitoring.

## Audience

- **Operators**: Monitoring Redis health and memory usage.
- **Developers**: Analyzing data structures and debugging application state.
- **Data Engineers**: Profiling Redis performance and identifying bottlenecks.

## Scope

- **Included**: Redis key browsing, stream analysis, memory profiling, and CLI access via web UI.
- **Excluded**: Direct Redis server OS management, hardware-level performance tuning.

## Structure

```text
.
├── docker-compose.yml       # Service definition
└── README.md                # Entry point
```

## How to Work in This Area

### 1. Initial Setup

1. Deploy the stack: `docker compose up -d`.
2. Access `https://redisinsight.${DEFAULT_URL}`.
3. Accept the EULA and set up your initial connection to a Redis instance.

### 2. Basic Usage

- Add a new database by providing the hostname (e.g., `redis` for local containers) and port (6379).
- Use the 'Browser' tab to explore keys and values.
- Use 'Memory Analysis' to find memory-intensive keys.

## Implementation Details

### Service Configuration

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Image | `redis/redisinsight:3.2.0` | Specific stable version |
| Port | `5540` (Internal) | Managed by Traefik |
| Storage | `redisinsight_data` | Persistent volume for connections |

### Traefik Integration

```yaml
labels:
  traefik.enable: 'true'
  traefik.http.routers.redisinsight.rule: Host(`redisinsight.${DEFAULT_URL}`)
  traefik.http.routers.redisinsight.middlewares: sso-auth@file
```

## Available Scripts

- `docker compose up -d`: Start the service.
- `docker compose down`: Stop the service.
- `docker compose logs -f`: View service logs.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect RedisInsight.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with `docker compose config` to confirm RedisInsight network, volume, and label references render.
- Check RedisInsight logs and the linked runbook before changing admin routing or connection settings.

## Related Documents

- **System Guide**: [RedisInsight Guide](../../../docs/05.operations/guides/11-laboratory/redisinsight.md)
- **Operations Policy**: [RedisInsight Operations](../../../docs/05.operations/guides/11-laboratory/redisinsight.md)
- **Runbook**: [RedisInsight Runbook](../../../docs/05.operations/guides/11-laboratory/redisinsight.md)
