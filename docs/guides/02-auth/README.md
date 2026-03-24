---
layer: infra
---

# Identity and Access (02-auth)

Identity providers (Keycloak) and access proxies (OAuth2 Proxy) for the platform.

- [Procedural & Lifecycle Guide](./PROCEDURAL.md): How to manageauth services and Keycloak instances.
- [System & Service Context](./CONTEXT.md): Architectural context for authentication flows.
- [Setup & Installation Guide](./SETUP.md): Initial Keycloak and OAuth2 Proxy setup.
- [Usage & Troubleshooting Guide](./USAGE.md): Common authentication issues and operational steps.

## Service Deep Dives

- [Keycloak Customization](./keycloak-customization.md)
- [Keycloak IDP Guide](./keycloak-idp-guide.md)
- [SSO & OAuth2 Proxy Guide](./sso-oauth2-proxy-guide.md)

For technical configuration details (Docker Compose, Config files), see [infra/02-auth/](../../infra/02-auth/README.md).
