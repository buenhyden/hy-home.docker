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

## How to Work

### 1. Initial Setup

1. Deploy the stack: `docker compose up -d`.
2. Access `https://redisinsight.${DEFAULT_URL}`.
3. Accept the EULA and set up your initial connection to a Redis instance.

### 2. Basic Usage

- Add a new database by providing the hostname (e.g., `redis` for local containers) and port (6379).
- Use the 'Browser' tab to explore keys and values.
- Use 'Memory Analysis' to find memory-intensive keys.

## Implementation Snippet

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

## Related Documentation

- **System Guide**: [RedisInsight Guide](../../../docs/07.guides/11-laboratory/redisinsight.md)
- **Operations Policy**: [RedisInsight Operations](../../../docs/08.operations/11-laboratory/redisinsight.md)
- **Runbook**: [RedisInsight Runbook](../../../docs/09.runbooks/11-laboratory/redisinsight.md)

---

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.
