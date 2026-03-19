# Gateway (01-gateway)

This category manages the ingress traffic and edge routing for the entire infrastructure.

## Services

| Service | Profile | Path        | Purpose                                             | Observability |
| ------- | ------- | ----------- | --------------------------------------------------- | ------------- |
| Traefik | (core)  | `./traefik` | Primary ingress, handles SSL/TLS and SSO.           | Metrics/Traces|
| Nginx   | `nginx` | `./nginx`   | Secondary proxy, path-based routing.                | Logs          |

## Notes

- Traefik and Nginx both compete for the same **host ports** (80/443).
- TLS assets are shared from `secrets/certs`.
- **Observability**: Traefik exports metrics to Prometheus and traces to Tempo (`tempo:4317`).

## File Map

| Path        | Description                        |
| ----------- | ---------------------------------- |
| `traefik/`  | Traefik router and dynamic config. |
| `nginx/`    | Optional standalone Nginx gateway. |
| `README.md` | Category overview.                 |

## Documentation References

- **Traffic Flow**: [Architecture Principles](../../ARCHITECTURE.md#31-network-model)
- **Ingress Guide**: [traefik-ingress-guide.md](../../docs/guides/01-gateway/traefik-ingress-guide.md)
- **Operations**: [gateway-operations.md](../../docs/guides/01-gateway/gateway-operations.md)
- **Recovery**: [2026-03-15-traefik-proxy-recovery.md](../../docs/runbooks/2026-03-15-traefik-proxy-recovery.md)
