---
layer: infra
---

# Identity and Access (02-auth)

Identity providers (Keycloak) and access proxies (OAuth2 Proxy) for the platform.

## Navigation Map

| View | Command | Focus |
| :--- | :--- | :--- |
| **Architecture** | `[LOAD:CONTEXT]` | Traffic flow and component roles |
| **Installation** | `[LOAD:SETUP]` | Initial bootstrap and verification |
| **Operations** | `[LOAD:USAGE]` | Daily tasks and connection strings |
| **Maintenance** | `[LOAD:PROCEDURAL]` | Lifecycle and recovery |

## Categorized Service Index

### Core Authentication

- **[CONTEXT.md](./CONTEXT.md)**: Architectural context for authentication flows.
- **[SETUP.md](./SETUP.md)**: Initial Keycloak and OAuth2 Proxy setup.
- **[USAGE.md](./USAGE.md)**: Common authentication issues and operational steps.
- **[PROCEDURAL.md](./PROCEDURAL.md)**: How to manage auth services and Keycloak instances.

## Service Deep Dives

- [Keycloak Customization](./keycloak-customization.md)
- [Keycloak IDP Guide](./keycloak-idp-guide.md)
- [SSO & OAuth2 Proxy Guide](./sso-oauth2-proxy-guide.md)

For technical configuration details (Docker Compose, Config files), see [infra/02-auth/](../../infra/02-auth/README.md).
