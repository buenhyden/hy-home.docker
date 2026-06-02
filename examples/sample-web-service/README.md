# sample-web-service

> Copyable best-practice service seed for `hy-home.docker`. Copy this folder as
> the starting point for a new containerized service, then adapt names, image,
> ports, and configuration.

## Purpose

A minimal static web service that demonstrates the repository's container
hardening and Compose conventions: pinned images, non-root runtime, read-only
root filesystem, dropped capabilities, healthcheck, resource limits, and
secret-free configuration.

## Files

| File                 | Role                                                            |
| -------------------- | --------------------------------------------------------------- |
| `Dockerfile`         | Multi-stage build; unprivileged nginx runtime with HEALTHCHECK. |
| `nginx.conf`         | Listens on `8080` (non-root port).                              |
| `site/index.html`    | Static content served by the service.                           |
| `docker-compose.yml` | Hardened service definition.                                    |
| `.env.example`       | Non-secret environment template; copy to `.env`.                |
| `service.md`         | Filled instance of `service.template.md`.                       |

## Service Readiness

| Control              | Status | Evidence                                                   |
| -------------------- | ------ | ---------------------------------------------------------- |
| Pinned image tag     | Ready  | `nginxinc/nginx-unprivileged:1.27.3-alpine`, `alpine:3.21` |
| Non-root runtime     | Ready  | unprivileged image (uid 101), no `privileged`              |
| Read-only rootfs     | Ready  | `read_only: true` + `tmpfs` for writable paths             |
| Dropped capabilities | Ready  | `cap_drop: [ALL]`, `no-new-privileges:true`                |
| Healthcheck          | Ready  | `HEALTHCHECK` + Compose `healthcheck`                      |
| Resource limits      | Ready  | `deploy.resources.limits` (cpu/memory)                     |
| Secret handling      | Ready  | `env_file` only; no plaintext secrets in compose           |
| Log rotation         | Ready  | `json-file` with `max-size`/`max-file`                     |

## Operations

```bash
cp .env.example .env
docker compose config        # validate
docker compose up -d --build # start
docker compose ps            # health status
docker compose down          # stop
```

## Validation

- `docker compose config` parses without error.
- `docker compose ps` reports `healthy` after `start_period`.

## Troubleshooting

- Port already in use: change `WEB_HOST_PORT` in `.env`.
- Container restarts: inspect `docker compose logs web` for nginx permission or
  tmpfs path errors under the read-only root filesystem.

## Related Documents

- [Service scaffold template](../../docs/99.templates/service.template.md)
- [New-service onboarding guide](../../docs/05.operations/guides/new-service-onboarding.md)
