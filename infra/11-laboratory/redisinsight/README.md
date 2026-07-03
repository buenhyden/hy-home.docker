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

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Laboratory RedisInsight service leaf in `11-laboratory`; services: `redisinsight`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/redisinsight/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | profiles: `admin`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/redisinsight/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `redisinsight-data:/data:rw`, `redisinsight-data` |
| Ports | Not declared |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.redisinsight-static.rule`, `traefik.http.routers.redisinsight-static.entrypoints`, `traefik.http.routers.redisinsight-static.tls`, `traefik.http.routers.redisinsight-static.priority`, `traefik.http.routers.redisinsight-static.service`, `traefik.http.routers.redisinsight.rule`, plus 7 more |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `redisinsight` |
| Operations | [Guide](../../../docs/05.operations/guides/11-laboratory/redisinsight.md), [Policy](../../../docs/05.operations/policies/11-laboratory/redisinsight.md), [Runbook](../../../docs/05.operations/runbooks/11-laboratory/redisinsight.md) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) tier `11-laboratory`; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) root `admin` profile; [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

### 1. Initial Setup

1. Validate the root-active admin profile with `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`.
2. Access `https://redisinsight.${DEFAULT_URL}` only in an approved running environment.
3. Accept the EULA and set up your initial connection to a Redis/Valkey instance.

### 2. Basic Usage

- Add a new database by providing the hostname (e.g., `redis` for local containers) and port (6379).
- Use the 'Browser' tab to explore keys and values.
- Use 'Memory Analysis' to find memory-intensive keys.

## Implementation Details

### Service Configuration

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Image | `redis/redisinsight:3.6.0` | Current compose tag |
| Port | `5540` (Internal) | Managed by Traefik |
| Storage | `redisinsight-data` | Persistent volume for connections |

### Traefik Integration

```yaml
labels:
  traefik.enable: 'true'
  traefik.http.routers.redisinsight.rule: Host(`redisinsight.${DEFAULT_URL}`)
  traefik.http.routers.redisinsight.middlewares: gateway-standard-chain@file,redisinsight-admin-ip@docker,sso-errors@file,sso-auth@file
```

## Available Scripts

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`: validate RedisInsight route, image, static IP, and healthcheck.
- `docker logs --tail 100 redisinsight`: inspect logs when the service is running.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect RedisInsight.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with the hardening check to confirm RedisInsight network, volume, and label references.
- Check RedisInsight logs and the linked runbook before changing admin routing or connection settings.

## Related Documents

- **System Guide**: [RedisInsight Guide](../../../docs/05.operations/guides/11-laboratory/redisinsight.md)
- **Operations Policy**: [RedisInsight Operations](../../../docs/05.operations/policies/11-laboratory/redisinsight.md)
- **Runbook**: [RedisInsight Runbook](../../../docs/05.operations/runbooks/11-laboratory/redisinsight.md)
