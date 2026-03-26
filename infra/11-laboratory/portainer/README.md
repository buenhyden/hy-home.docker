# Laboratory Portainer

> Docker environment management and container orchestration UI.

## Overview

Portainer is a lightweight management UI which allows you to easily manage your different Docker environments (Docker hosts or Swarm clusters). It provides a high-level overview of your containers, images, networks, and volumes.

## Audience

- **Operators**: Managing local and remote Docker environments.
- **Developers**: Monitoring container logs and performance.
- **SREs**: Ensuring resource isolation and security compliance.

## Scope

- **Included**: Local Docker socket management, stack deployments, volume/network administration.
- **Excluded**: Direct host-level OS management, underlying hardware monitoring.

## Structure

```text
.
├── docker-compose.yml       # Service definition
└── README.md                # Entry point
```

## How to Work

### 1. Initial Setup
1. Deploy the stack: `docker compose up -d`.
2. Access `https://portainer.${DEFAULT_URL}`.
3. Set the initial admin password.

### 2. Environment Management
- Use the local endpoint to manage containers on the current host.
- Add remote agents for multi-host management.

## Implementation Snippet

### Service Configuration

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Image | `portainer/portainer-ce:sts` | Short Term Support version |
| Port | `9443` (Internal) | Managed by Traefik |
| Storage | `portainer_data` | Persistent volume for config |

### Traefik Integration

```yaml
labels:
  traefik.enable: 'true'
  traefik.http.routers.portainer.rule: Host(`portainer.${DEFAULT_URL}`)
  traefik.http.routers.portainer.middlewares: sso-auth@file
```

## Available Scripts

- `docker compose up -d`: Start the service.
- `docker compose down`: Stop the service.
- `docker compose logs -f`: View service logs.

## Related Documentation

- **System Guide**: [Portainer Guide](../../../docs/07.guides/11-laboratory/portainer.md)
- **Operations Policy**: [Portainer Operations](../../../docs/08.operations/11-laboratory/portainer.md)
- **Runbook**: [Portainer Runbook](../../../docs/09.runbooks/11-laboratory/portainer.md)
