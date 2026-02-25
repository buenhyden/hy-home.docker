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

## Documentation References

- **Architecture Principles**: [ARCHITECTURE.md](../../ARCHITECTURE.md)
- **Gateway Blueprints**: [docs/context/01-gateway](../../docs/context/01-gateway)
- **Platform Guides**: [docs/guides/README.md](../../docs/guides/README.md)
- **Runbooks (Gateway)**: [runbooks/01-gateway](../../runbooks/01-gateway)
- **Operations History**: [operations/README.md](../../operations/README.md)
