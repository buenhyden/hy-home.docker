---
title: "Gatus Implementation"
version: "0.2.1"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
---

# Gatus

## Overview

Monitors configured endpoint availability and stores SQLite history on
`gatus-data` at `/data/gatus.db`. Compose selects the native Keycloak OIDC
configuration without direct host publication. After the recorded native-login
acceptance, its router retains only the standard gateway chain; OAuth2 Proxy
ForwardAuth is removed. A healthy monitor does not prove every monitored
application works.

## Audience

Operators and developers reviewing service configuration.

## Scope

Lifecycle: **HOME**. Operational controls and recovery belong to `OPS-0087` through the [documentation index](../../../docs/README.md).

## Structure

[Compose](../docker-compose.yml) owns the service, mounts, network grants and entrypoint.

## Tech Stack

Upstream build pins belong to [Dockerfile](Dockerfile); runtime configuration belongs to [Compose](../docker-compose.yml); [version registry](../../../infra/tech-stack.versions.json) is a curated projection, not a deployment manifest.

## Configuration

Profiles: `availability / obs / dev`. Root Compose includes this definition; inclusion alone does not start a service. Networks are `edge_net` and `obs_net`. Review [public environment keys](../../../.env.example) and [secret references](../../../secrets/README.md) without printing private values.

The confidential client ID is `home-gatus`, and its exact callback is
`https://status.<domain>/authorization-code/callback`. The client secret is
read from a Docker Secret by the entrypoint. Gatus compares
`allowed-subjects` with the ID token's immutable `sub` claim, so
`GATUS_OIDC_ALLOWED_SUBJECT` must contain that exact Keycloak subject. The
entrypoint fails closed when the secret, subject, domain or CA inputs are absent.

The image builds the immutable upstream source selected in
[Dockerfile](Dockerfile), verifies its archive checksum and applies
[the local OIDC hardening patch](patches/oidc-hardening.patch) without fuzz.
The patch adds S256 PKCE, secure and HTTP-only cookies, one-time state/nonce/PKCE
cookie clearing, authenticated status-data routes and source-level regression
tests. This local patch is required because the pinned upstream implementation
lacks those controls; reassess it when changing the upstream source.

The external route boundary is explicit:

| Route | Boundary | Reason |
| --- | --- | --- |
| `/`, `/endpoints/*`, `/suites/*`, static assets | Public bootstrap | The SPA and login screen must load before a native session exists. |
| `/oidc/login`, `/authorization-code/callback` | OIDC protocol | Starts and completes the authorization-code flow. |
| `/api/v1/config` | Public minimal bootstrap | Returns `oidc` and `authenticated` flags plus UI announcements; announcements are empty until OIDC authentication succeeds. |
| `/health` | Public minimal probe | Container health checks require it; the response contains health state only. |
| `/metrics` | Internal network only | Prometheus scrapes the container directly; the Traefik router excludes this path, so the public hostname returns no matching Gatus route. |
| Endpoint and suite statuses, health badges, uptime, response-time badges/charts/history | Native OIDC session | These monitoring data routes use the same session middleware. |
| `POST /api/v1/endpoints/:key/external` | Per-endpoint bearer token | Machine ingestion keeps its independent token boundary. |

## Validation

From the repository root, select the documented profile and run
`scripts/validation/validate-docker-compose.sh`. The image build runs the
patched upstream security tests. Use the owning Runbook for runtime checks;
config validation does not prove native login, logout, denial, session expiry
or restored monitoring history.

## How to Work in This Area

Preserve data and credentials during changes. Review exact runtime targets before deployment. Keep operational procedures in the existing operations subject.

### Convergence contract

- Classification: **HOME**. Exact profiles: `obs`, `availability`, `dev`.
- Source authority: `infra/06-observability/docker-compose.yml` plus this package's tracked config/build inputs; image declarations are authoritative and `infra/tech-stack.versions.json` is derived.
- Root preflight: `docker compose --profile obs config --quiet`. Root targeted start: `docker compose --profile obs up -d gatus`.
- The stable entry point is [docs/README.md](../../../docs/README.md). Exact Stage 05 path: `docs/05.operations/guides/0087-gatus.md`; IDs `GDE-0087`, `POL-0087`, `RUN-0087`.
- Follow that runbook's planned isolated recovery. It is unexecuted unless dated evidence says otherwise; do not mutate live state from this README.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
