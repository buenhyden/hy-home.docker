---
status: active
---

<!-- Target: examples/sample-web-service/README.md -->

# sample-web-service

> Copyable best-practice service seed for `hy-home.docker`. Copy this folder as
> the starting point for a new containerized service, then adapt names, image,
> ports, and configuration.

## Overview

A minimal static web service that demonstrates the repository's container
hardening and Compose conventions: pinned images, non-root runtime, read-only
root filesystem, dropped capabilities, healthcheck, resource limits, and
secret-free configuration. The Compose definition deliberately omits a fixed
top-level project name and `container_name`, so callers can isolate copies with
`docker compose --project-name`.

## Audience

This README is for:

- Developers
- Operations/SRE Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- Copyable static web service scaffold files.
- Container hardening, healthcheck, resource-limit, and log-retention examples.
- Non-secret local environment setup through `.env.example`.
- Links to the current README and service scaffold templates.

### Out of Scope

- Production service ownership, SLA, or incident response records.
- TLS termination, ingress routing, and persistent data services.
- Secret values, credentials, tokens, private keys, raw logs, shell history, or
  `.env` values.

## Structure

```text
sample-web-service/
├── .env.example       # Non-secret environment template; copy to .env.
├── Dockerfile         # Multi-stage build and unprivileged nginx runtime.
├── README.md          # This scaffold README.
├── docker-compose.yml # Hardened service definition.
├── nginx.conf         # Nginx config listening on port 8080.
├── service.md         # Filled service scaffold example.
└── site/index.html    # Static content served by the service.
```

## How to Work in This Area

1. Copy this folder when starting a new containerized service example.
2. Update names, image tags, ports, healthchecks, and non-secret environment
   keys for the new service.
3. Keep `service.md` aligned with the registered Service metadata and section
   contract.
4. Select an explicit project name when parallel local instances are required.
5. Validate Compose before using the service.

## Files

| File                 | Role                                                            |
| -------------------- | --------------------------------------------------------------- |
| `Dockerfile`         | Multi-stage build; unprivileged nginx runtime with HEALTHCHECK. |
| `nginx.conf`         | Listens on `8080` (non-root port).                              |
| `site/index.html`    | Static content served by the service.                           |
| `docker-compose.yml` | Hardened service definition.                                    |
| `.env.example`       | Non-secret environment template; copy to `.env`.                |
| `service.md`         | Sample-specific instance of the canonical Service contract.     |

## Service Readiness

| Control              | Status | Evidence                                                   |
| -------------------- | ------ | ---------------------------------------------------------- |
| Pinned image tag     | Ready  | `nginxinc/nginx-unprivileged:1.31.3-alpine3.24-slim`, `alpine:3.21` |
| Non-root runtime     | Ready  | unprivileged image (uid 101), no `privileged`              |
| Read-only rootfs     | Ready  | `read_only: true` + `tmpfs` for writable paths             |
| Dropped capabilities | Ready  | `cap_drop: [ALL]`, `no-new-privileges:true`                |
| Healthcheck          | Ready  | `HEALTHCHECK` + Compose `healthcheck`                      |
| Resource limits      | Ready  | `deploy.resources.limits` (cpu/memory)                     |
| Secret handling      | Ready  | `env_file` only; no plaintext secrets in compose           |
| Log rotation         | Ready  | `json-file` with `max-size`/`max-file`                     |
| Project isolation    | Ready  | no fixed project or container identity                    |

## Operations

```bash
cp .env.example .env
docker compose config        # validate
docker compose up -d --build # start
docker compose ps            # health status
docker compose down          # stop
```

The Spec 127 delivery rehearsal uses separate task-owned project names, the
loopback ports `18080` and `18081`, and immutable local image config digests.
Its merged runtime topology resets the build path and uses
`pull_policy: never`; the wrapper also requires an exact local image-object ID
for each accepted digest and starts with `--pull never --no-build`.
Its accepted verdict fixtures are contract tests only. They never authorize an
actual project start; the runtime command fails closed until the canonical
Spec 126 baseline/candidate pair exists and passes every upstream gate.

## Validation

- `docker compose config` parses without error.
- `docker compose ps` reports `healthy` after `start_period`.
- `python3 -m unittest tests.validation.test_sample_service_delivery_rehearsal`
  verifies the local delivery contract without starting Docker resources.

## Troubleshooting

- Port already in use: change `WEB_HOST_PORT` in `.env`.
- Container restarts: inspect `docker compose logs web` for nginx permission or
  tmpfs path errors under the read-only root filesystem.

## Related Documents

- [README template](../../docs/99.templates/templates/common/readme.template.md)
- [Service scaffold template](../../docs/99.templates/templates/spec-contracts/service.template.md)
- [New-service onboarding guide](../../docs/05.operations/catalog/00-workspace/ops-0008-new-service-onboarding/guide.md)
- [Release management runbook](../../docs/05.operations/catalog/00-workspace/ops-0009-release-management/runbook.md)
