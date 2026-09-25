---
title: "Dozzle Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0072"
parent_ids:
- "POL-0072"
implementation_services:
  infra/11-laboratory/dozzle/docker-compose.yml:
  - dozzle
created: "2026-05-10"
---

# Dozzle Usage Guide

## Usage

### Purpose and classification

Dozzle is an OPTIONAL admin log viewer under `admin` and `admin-logs`. It is not
a log archive; container logs remain owned by Docker/logging backends. Dozzle
persists UI/user settings in `${DEFAULT_MANAGEMENT_DIR}/dozzle`, but not a second
authoritative copy of the viewed logs.

### Current implementation and risk

- [Dozzle Compose](../../../infra/11-laboratory/dozzle/docker-compose.yml)
  owns profiles, OIDC, route, IP allowlist, secret, health, and mounts.
- It uses native OIDC against Keycloak via `DOZZLE_AUTH_*` and the
  `dozzle_client_secret`. Traefik applies the gateway standard chain and an admin
  CIDR allowlist, not OAuth2 Proxy ForwardAuth.
- The Docker socket is mounted `:ro`, but upstream warns that read-only file mode
  does not restrict Docker API methods; compromise can be root-equivalent. Current
  source declares no socket proxy.
- `/data` persists settings. The CA file supports issuer trust. The health command
  proves Dozzle process health, not OIDC, socket authorization, or log coverage.

### Normal use, backup, and upgrade

Validate `docker compose --profile admin-logs config --quiet`, confirm CIDRs and
OIDC client/claims, then start only Dozzle. Verify login with a least-privilege
test identity and confirm shell/actions remain disabled unless explicitly
configured and approved. Sanitize logs before evidence capture.

Back up `/data` only for settings continuity; it does not back up container logs.
Stop Dozzle for a consistent copy. Restore the settings copy against an isolated
Dozzle connected to a non-production Docker endpoint or no socket. Before upgrade,
review security advisories/release notes and test OIDC plus filtered log access.
No backup, restore, or upgrade ran here.

## Common Checks

- `docker compose --profile admin-logs config --quiet`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`

## Runbook Handoff

Use the [runbook](../runbooks/0072-dozzle.md) for OIDC, socket, log-stream, settings, and upgrade recovery.

## Traceability

- [Policy](../policies/0072-dozzle.md) (`POL-0072`)
- [Runbook](../runbooks/0072-dozzle.md) (`RUN-0072`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Dozzle authentication and socket security](https://dozzle.dev/guide/authentication)
- [Dozzle getting started](https://dozzle.dev/guide/getting-started)
- [Dozzle MIT license](https://github.com/amir20/dozzle#license)
