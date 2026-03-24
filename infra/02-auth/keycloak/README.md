# Keycloak IAM

<!-- [ID:02-auth:keycloak] -->
: Identity and Access Management (IAM) provider based on Quarkus.

---

## Overview

Keycloak is the central identity provider for the `hy-home.docker` ecosystem. It handles user authentication, session management, and OIDC/SAML token issuance for protected applications.

### Service Details

| Service | Image / Build | Resources | Port |
| :--- | :--- | :--- | :--- |
| **keycloak** | `quay.io/keycloak/keycloak:26.5.4` | 1.0 CPU / 1GB RAM | 8080 (HTTP) |

## Features

- **SSO**: Centralized login for all services.
- **Realms**: Multi-tenancy support for organizing users and clients.
- **Metrics**: Prometheus-compatible metrics at `${MGMT_PORT}/metrics`.

## Networking

- **URL**: `https://keycloak.${DEFAULT_URL}`
- **Management Port**: `9000` (Health checks & Metrics)
- **Service Port**: `8080` (Internal API/Web)

## Persistence

Mounted from `${DEFAULT_AUTH_DIR}/keycloak/`:

| Path | Description |
| :--- | :--- |
| `/opt/keycloak/conf` | Quarkus static configuration. |
| `/opt/keycloak/providers` | Custom JARs/SPIs for extensions. |
| `/opt/keycloak/themes` | Custom UI/UX themes. |

---

## Operations

### Health Verification

```bash
# Verify readiness
docker exec keycloak curl -f http://localhost:9000/health/ready
```

### Key Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `KC_DB` | Database vendor | `postgres` |
| `KC_HOSTNAME` | Public access URL | `keycloak.${DEFAULT_URL}` |

## Related Documents

- **[Setup Guide](../../../docs/07.guides/02-auth/01.setup.md)**
- **[Operations Policy](../../../docs/08.operations/02-auth/README.md)**
- **[Auth Runbook](../../../docs/09.runbooks/02-auth/README.md)**
