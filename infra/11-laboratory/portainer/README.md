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

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Laboratory Portainer service leaf in `11-laboratory`; services: `portainer`; root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/portainer/docker-compose.yml` |
| Config files | `docker-compose.yml` |
| Config values | profiles: `admin` |
| Compose linkage | root include optional/commented in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-laboratory/portainer/docker-compose.yml` |
| Networks | `infra_net` |
| Volumes | `/var/run/docker.sock:/var/run/docker.sock`, `portainer-data:/data`, `portainer-data` |
| Ports | Not declared |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.portainer.rule`, `traefik.http.routers.portainer.entrypoints`, `traefik.http.routers.portainer.tls`, `traefik.http.middlewares.portainer-admin-ip.ipallowlist.sourcerange`, `traefik.http.routers.portainer.middlewares`, `traefik.http.services.portainer.loadbalancer.server.port` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `portainer` |
| Operations | [Guide](../../../docs/05.operations/guides/11-laboratory/portainer.md), [Policy](../../../docs/05.operations/policies/11-laboratory/portainer.md), [Runbook](../../../docs/05.operations/runbooks/11-laboratory/portainer.md) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh) tier `11-laboratory`; [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh) after root include promotion; [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with the hardening check, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

### 1. Initial Setup

1. Confirm the root Portainer include is intentionally enabled; it is optional/commented by default.
2. Validate the static boundary with `bash scripts/hardening/check-all-hardening.sh 11-laboratory`.
3. Access `https://portainer.${DEFAULT_URL}` only after approved runtime promotion and set the initial admin password.

### 2. Environment Management

- Use the local endpoint to manage containers on the current host.
- Add remote agents for multi-host management.

## Implementation Details

### Service Configuration

| Category | Technology | Notes |
| :--- | :--- | :--- |
| Image | `portainer/portainer-ce:sts` | Short Term Support version |
| Port | `9443` (Internal) | Managed by Traefik |
| Storage | `portainer-data` | Persistent volume for config |

### Traefik Integration

```yaml
labels:
  traefik.enable: 'true'
  traefik.http.routers.portainer.rule: Host(`portainer.${DEFAULT_URL}`)
  traefik.http.routers.portainer.middlewares: gateway-standard-chain@file,portainer-admin-ip@docker,sso-errors@file,sso-auth@file
```

## Available Scripts

- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`: validate Portainer static boundary with the rest of the laboratory tier.
- `docker logs --tail 100 portainer`: inspect logs when the optional service is running.

## Validation

- Run `bash scripts/validation/validate-docker-compose.sh` after README or Compose reference changes that affect Portainer.
- Run `bash scripts/validation/check-repo-contracts.sh` to keep service documentation and operation links synchronized.

## Troubleshooting

- Start with the hardening check to confirm Portainer socket, volume, and label references.
- Check Portainer logs and the linked runbook before changing admin routing or Docker access settings.

## Related Documents

- **Guide**: [Portainer usage guide](../../../docs/05.operations/guides/11-laboratory/portainer.md)
- **Policy**: [Portainer operations policy](../../../docs/05.operations/policies/11-laboratory/portainer.md)
- **Runbook**: [Portainer recovery runbook](../../../docs/05.operations/runbooks/11-laboratory/portainer.md)
