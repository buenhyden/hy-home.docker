# Gateway (01-gateway)

This category manages the ingress traffic and edge routing for the entire infrastructure.

## Services

| Service | Profile | Path        | Purpose                                             |
| ------- | ------- | ----------- | --------------------------------------------------- |
| Traefik | (core)  | `./traefik` | Primary reverse proxy, TLS, routing, SSO middleware |
| Nginx   | `nginx` | `./nginx`   | Optional standalone proxy (path-based routing)      |

## Notes

- **Traefik and Nginx both use static IP `172.19.0.13`** on `infra_net`. Do not run them together unless you change one of the IPs.
- TLS assets are shared from `secrets/certs`.

## File Map

| Path        | Description                        |
| ----------- | ---------------------------------- |
| `traefik/`  | Traefik router and dynamic config. |
| `nginx/`    | Optional standalone Nginx gateway. |
| `README.md` | Category overview.                 |

> **Note**: This component's local documentation has been migrated to the global repository standards to enforce Spec-Driven Development boundaries.

Please refer to the following global documentation directories for information regarding this service:

- **Architecture & Topology**: [docs/architecture](../../docs/architecture)
- **Configuration & Setup Guides**: [docs/guides](../../docs/guides)
- **Routine Operations**: [operations/](../../operations)
- **Troubleshooting & Recovery**: [runbooks/](../../runbooks)
