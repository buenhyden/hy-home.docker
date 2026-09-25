---
title: "Gatus Guide"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0087"
parent_ids:
- "POL-0087"
implementation_services:
  infra/06-observability/docker-compose.yml:
  - gatus
created: "2026-09-19"
---

# Gatus Guide

## Usage

Gatus is an always-on HOME availability monitor selected by `obs`,
`availability`, or `dev`. Root Compose owns its inclusion; [the observability
Compose source](../../../../../infra/06-observability/docker-compose.yml) owns its local build, UID/GID, `GATUS_PORT`, read-only configuration, healthcheck, network, `gatus-data` mount and Traefik labels.

The active mount is `config.oidc.yaml`: Gatus authenticates with the confidential
`home-gatus` Keycloak authorization-code client and allows the configured subject
only. The UI route has TLS plus `gateway-standard-chain@file`; it does not use
`sso-auth@file`. The router excludes `/metrics`, so metrics are an internal
monitoring boundary rather than an authenticated browser UI. Gatus’s session is
configured locally for one hour; a Keycloak logout does not establish immediate
Gatus-session revocation without an observed test.

SQLite history persists in `/data/gatus.db` through `gatus-data`. Probe results
are operational data. The configuration and database do not prove that the
probed application is fully accepted; they record the declared endpoint check.

### Normal operation and lifecycle

Review probe names and status outcomes through an authorized UI session; do not
put response bodies, credentials or tokens in evidence. To upgrade the local
image, review the Dockerfile’s upstream source and patch first, retain the prior
image and configuration, then use the [runbook](../runbooks/0087-gatus.md) after runtime
approval. Gatus uses an Apache-2.0 upstream license according to its
[repository](https://github.com/TwiN/gatus); verify any new source release and
patch compatibility rather than inferring features from the local image name.

SQLite backup requires coordinated quiescence or an engine-supported consistent
snapshot. Copying a live database file alone can omit WAL state. Restore first
to isolated storage, verify the expected history and a new probe, then obtain
approval before replacement. The central [backup policy](../policies/0021-backup-and-restore.md) owns shared retention and custody controls.

### Source-backed operating contract

- **Purpose/classification/source**: `gatus` is a `HOME` availability dashboard selected by `obs`/`availability`/`dev`; [Compose](../../../infra/06-observability/docker-compose.yml), [local Dockerfile](../../../infra/06-observability/gatus/Dockerfile), entrypoint, and OIDC config are authoritative.
- **Flow/dependencies/security**: Gatus runs declared endpoint checks and publishes UI/metrics; native Keycloak OIDC protects the UI using `gatus_oidc_client_secret` and the mounted root CA. Session TTL is one hour. The metrics endpoint is not independently gateway-routed in current source.
- **State/resources**: `gatus-data:/data` contains SQLite `gatus.db` and application state. Source limits are not headroom. Endpoint configs can contain sensitive topology; do not log tokens or private response bodies.
- **Normal use/lifecycle**: render from root, validate config, verify health, OIDC login, expected endpoint results, and Prometheus scrape path. Stop Gatus or use SQLite-native consistency before backup; preserve config, database, OIDC secret reference, and root CA.
- **Upgrade**: rebuild the pinned local image/patch intentionally, review schema/OIDC compatibility, restore/test on isolated state, then verify history, endpoint checks, login, sessions, and metrics.
- **Upstream/license**: follow the official [Gatus repository/releases](https://github.com/TwiN/gatus). Gatus is Apache-2.0 licensed; retain patch provenance.

## Common Checks

- Inspect native OIDC, the `/metrics` router exclusion and healthcheck in the [Observability Compose](../../../infra/06-observability/docker-compose.yml).
- Review source and SQLite custody before an approved upgrade; health does not prove login or probe coverage.

## Runbook Handoff

Use the [Gatus Runbook](../runbooks/0087-gatus.md) for approval-gated diagnosis, restart and recovery.

## Traceability

- [Policy](../policies/0087-gatus.md), [Runbook](../runbooks/0087-gatus.md)
- [Gatus configuration reference](https://github.com/TwiN/gatus#configuration)

## Related Documents

- [Observability Compose](../../../infra/06-observability/docker-compose.yml)
