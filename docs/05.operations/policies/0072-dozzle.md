---
title: "Dozzle Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0072"
parent_ids:
- "AD-0011"
created: "2026-05-17"
---

# Dozzle Operations Policy

## Overview

Dozzle is an OPTIONAL privileged admin viewer. Native OIDC and CIDR restriction
are mandatory compensating controls for its direct Docker API access.

## Policy Scope

Activation, OIDC/CIDR, Docker socket authority, log privacy, settings data,
upgrade, backup, and removal.

## Controls

- Use only `admin`/`admin-logs`; keep Dozzle outside HOME.
- Preserve native OIDC, secret-file delivery, TLS issuer trust, and the admin
  CIDR allowlist. Verify roles/filters; login alone is not least privilege.
- Treat the socket as root-equivalent despite `:ro`. Shell/actions remain off
  unless an approved requirement and socket restriction design say otherwise.
- Do not use Dozzle as retention. Apply redaction and least access to logs that
  may contain credentials, personal data, or private requests.
- Stop Dozzle before backing up/restoring `/data`; use an isolated/non-production
  Docker endpoint for restore testing.
- Review upstream advisories and OIDC behavior before upgrade. Remove socket and
  revoke the OIDC client/secret before deleting settings at retirement.

## Exceptions

No exception may expose Dozzle without auth/CIDR controls or treat a read-only
socket mount as Docker API authorization.

## Verification

Verify health, OIDC claims/roles, CIDR denial, expected container visibility,
and absence of unapproved shell/actions. Runtime evidence remains separate.

## Review Cadence

Review on image/security advisory, OIDC/CIDR, socket, or settings changes.

## Traceability

- [Guide](../guides/0072-dozzle.md) (`GDE-0072`)
- [Runbook](../runbooks/0072-dozzle.md) (`RUN-0072`)
- [Laboratory architecture](../../02.architecture/descriptions/0011-laboratory-architecture.md)

## Related Documents

- [Dozzle Compose source](../../../infra/11-laboratory/dozzle/docker-compose.yml)
- [Dozzle security considerations](https://dozzle.dev/guide/authentication#security-considerations)
