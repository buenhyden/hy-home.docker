---
layer: infra
---
# Gateway System and Service Context

The Gateway tier acts as the primary ingress point for the `hy-home` internal infrastructure, utilizing **Traefik** as the dynamic edge router and **Nginx** for static, path-based routing scenarios.

## 1. Network Architecture

The gateway sits at the boundary of the host network and the internal docker networks.

- **External Interface**: Listens on Host `80` and `443`.
- **Internal Interface**: Connects to `infra_net` to route traffic to backend containers.

## 2. Service Relations

- **Auth Layer**: Relies on `02-auth` (Keycloak/OAuth2 Proxy) for `sso-auth` middleware.
- **Monitoring**: Exports metrics to Prometheus and traces to Tempo via OTLP.
- **Storage**: Maps certificates from the `secrets/` directory.

## 3. High-Level Traffic Flow

1. **Host Request**: User visits `app.hy-home.local`.
2. **TLS Termination**: Gateway terminates HTTPS using local `mkcert` CA.
3. **Middleware**: Traefik applies `sso-auth` via forwardAuth (OAuth2 Proxy); Nginx uses `auth_request`.
4. **Backend Proxy**: Traffic is proxied to the target container over `infra_net`.
