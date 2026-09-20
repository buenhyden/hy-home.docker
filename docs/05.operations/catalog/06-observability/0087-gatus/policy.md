---
title: "Gatus Policy"
version: "0.2.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0087"
parent_ids:
- "AD-0031"
created: "2026-09-19"
---

# Gatus Policy

## Overview

Gatus is the HOME availability monitor with native OIDC and persistent probe history.

## Policy Scope

Keep the local Gatus image, native OIDC configuration, read-only config mount,
`gatus-data` SQLite state, status UI, metrics boundary and probes within the HOME
availability capability.

## Controls

- Keep direct host ports unpublished, the configured non-root identity, read-only root filesystem and the writable data mount exactly as the Compose source declares.
- Use native `home-gatus` OIDC and `gateway-standard-chain@file` for the UI. Do not add `sso-auth@file`, local-password fallback or a broad subject allowlist. Keep `/metrics` outside the browser route and do not expose it externally without an approved monitoring design.
- Do not record probe URLs, response bodies, credential material or raw SQLite data in Task evidence. A probe success is endpoint evidence, not application acceptance.
- Treat SQLite as stateful: create a coordinated consistent backup and isolated restore proof before replacement. Never delete the volume to resolve a probe or login symptom.
- Upgrade only after reviewing the Dockerfile source, upstream release/security notes, license and the local hardening patch. Keep the previous image/configuration until approved login, health and probe checks complete.

### Lifecycle and data controls

- Keep Gatus `HOME`; native Keycloak OIDC, root-CA validation, session controls, and least-privilege endpoint credentials are required.
- SQLite/data, endpoint configuration, local patch/image identity, and matching OIDC secret form the recovery set. Stop writes or use SQLite-native backup; never live-copy `gatus.db`.
- Rehearse in an isolated project with test routes/credentials and verify schema, history, endpoints, OIDC, session behavior, and metrics without exposing private response data.
- Upgrade/removal requires patch compatibility, endpoint-owner coordination, retained history decision, client/route revocation, and explicit data-deletion approval.

## Exceptions

Exceptions require owner, scope, risk, expiry and recovery condition.

## Verification

Static source and catalog checks verify declarations only. Container health,
native login, session expiry, probe coverage, backup and restore remain runtime
evidence requiring a separately approved target.

## Review Cadence

Review monthly and when authentication, probe inventory, source or storage changes.

## Traceability

- Governing architecture: [AD-0031](../../../../02.architecture/descriptions/0031-home-development-host.md)
- Subject peers: [Guide](guide.md) and [Runbook](runbook.md)

## Related Documents

- [Guide](guide.md), [Runbook](runbook.md)
- Runtime pins are owned by [observability Compose](../../../../../infra/06-observability/docker-compose.yml) and the selected [Gatus Dockerfile](../../../../../infra/06-observability/gatus/Dockerfile); the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) verifies drift.
- [Gatus upstream security policy](https://github.com/TwiN/gatus/security/policy)
