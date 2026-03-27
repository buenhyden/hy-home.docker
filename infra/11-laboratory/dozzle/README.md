# Dozzle

> Real-time log viewer for Docker containers.

## Overview

Dozzle is a small and lightweight application that provides a web-based interface for viewing Docker container logs in real-time. It is part of the `11-laboratory` tier, used for monitoring and debugging services within the infrastructure.

## Audience

이 README의 주요 독자:

- Operators (Log monitoring and debugging)
- Developers (Service health check)
- AI Agents (Log analysis and error detection)

## Scope

### In Scope

- Dozzle service configuration (`docker-compose.yml`)
- Log aggregation and display for local Docker containers
- Access control via SSO Auth middleware

### Out of Scope

- Centralized log storage (e.g., Elasticsearch, Loki)
- Log rotation policies (managed by Docker daemon)
- External log shipping

## Structure

```text
dozzle/
├── docker-compose.yml    # Service definition
└── README.md             # This file
```

## How to Work in This Area

1. [docker-compose.yml](./docker-compose.yml)을 통해 서비스 구성을 확인한다.
2. 가이드 문서는 [docs/07.guides/11-laboratory/dozzle.md](../../../docs/07.guides/11-laboratory/dozzle.md)를 참조한다.
3. 운영 정책은 [docs/08.operations/11-laboratory/dozzle.md](../../../docs/08.operations/11-laboratory/dozzle.md)를 확인한다.
4. 장애 조치 지침은 [docs/09.runbooks/11-laboratory/dozzle.md](../../../docs/09.runbooks/11-laboratory/dozzle.md)를 따른다.

## Tech Stack

| Category   | Technology   | Notes                     |
| ---------- | ------------ | ------------------------- |
| Image      | amir20/dozzle| v10.2.0                   |
| Interface  | Web UI       | Real-time streaming       |
| Monitoring | Docker Logs  | via `/var/run/docker.sock`|

## Configuration

### Environment Variables

| Variable               | Required | Description                        |
| ---------------------- | -------: | ---------------------------------- |
| `DOZZLE_PORT`          |       No | Web UI port (default: 8080)        |
| `DEFAULT_URL`          |      Yes | Base URL for Traefik routing       |
| `DEFAULT_MANAGEMENT_DIR`|      Yes | Path for persistent data storage   |

## Related References

- **Guide**: [../docs/07.guides/11-laboratory/dozzle.md](../../../docs/07.guides/11-laboratory/dozzle.md)
- **Operation**: [../docs/08.operations/11-laboratory/dozzle.md](../../../docs/08.operations/11-laboratory/dozzle.md)
- **Runbook**: [../docs/09.runbooks/11-laboratory/dozzle.md](../../../docs/09.runbooks/11-laboratory/dozzle.md)
