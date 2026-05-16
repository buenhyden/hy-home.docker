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
2. 가이드 문서는 [docs/05.operations/11-laboratory/dozzle.md](../../../docs/05.operations/guides/11-laboratory/dozzle.md)를 참조한다.
3. 운영 정책은 [docs/05.operations/11-laboratory/dozzle.md](../../../docs/05.operations/guides/11-laboratory/dozzle.md)를 확인한다.
4. 장애 조치 지침은 [docs/05.operations/11-laboratory/dozzle.md](../../../docs/05.operations/guides/11-laboratory/dozzle.md)를 따른다.

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

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh` before marking documentation ready.
- Verify log streaming by checking `docker logs dozzle` and confirming the Docker socket mount is accessible.
- Confirm service visibility by verifying target containers appear in the Dozzle UI after startup.

## Troubleshooting

- Start with `docker compose config` to confirm network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For Docker socket errors: confirm the socket path (`/var/run/docker.sock`) is correctly mounted and Dozzle has read access.
- For missing containers: verify Dozzle's filter configuration and that target containers share the same Docker host.

## Related Documents

- **Guide**: [../docs/05.operations/11-laboratory/dozzle.md](../../../docs/05.operations/guides/11-laboratory/dozzle.md)
- **Operation**: [../docs/05.operations/11-laboratory/dozzle.md](../../../docs/05.operations/guides/11-laboratory/dozzle.md)
- **Runbook**: [../docs/05.operations/11-laboratory/dozzle.md](../../../docs/05.operations/guides/11-laboratory/dozzle.md)
