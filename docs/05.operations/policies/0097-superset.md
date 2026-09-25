---
title: "Superset Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-24"
layer: "operations"
artifact_id: "POL-0097"
parent_ids:
- "AD-0004"
created: "2026-09-23"
---

# Superset Operations Policy

## Overview

Superset is a routed web application with its own login, metadata database
and access to lakehouse data. Authentication, role grants and credential
handling are the controls.

## Policy Scope

Selection, login, roles, secrets, metadata database, data connections and
upgrades.

## Controls

- Select only through `bi`; never add it to HOME.
- Login is native Keycloak OIDC with PKCE; the router uses
  `gateway-standard-chain@file` only and never OAuth2 Proxy ForwardAuth.
  The form login is not offered.
- Self-registration grants `Gamma` only. Admin and data roles are granted by
  an Admin to a named Keycloak user; record who and why in the Task.
- The signing key, database password and client secret come from Docker
  secret files; none is an environment variable, a command-line argument or a
  plain URI in configuration.
- The metadata database is feature-owned on `mng-pg` and reached only on
  `mng_data_net`; no host port.
- Data connections added in the UI use scoped identities; none uses an
  administrator login.

## Exceptions

None. Superset uses native OIDC, so the OAuth2 Proxy `/admins` allowlist does
not apply: any realm user can log in as `Gamma` (no data access) and an Admin
grants roles. The owner kept this on 2026-09-24 with the realm at one user.

## Verification

Compose rendering, hardening pins, and the rehearsal: provisioning,
idempotent migration, the registered `lakehouse` database, `/health`,
anonymous API `401`, the Keycloak login option, and no credential in the
container environment.

## Review Cadence

Review on a Superset or Flask-AppBuilder upgrade, a Keycloak client change,
and any new data connection.

## Traceability

- [Guide](../guides/0097-superset.md) (`GDE-0097`)
- [Runbook](../runbooks/0097-superset.md) (`RUN-0097`)
- [Application auth integration policy](0079-application-auth-integration.md)

## Related Documents

- [Superset Compose source](../../../infra/04-data/analytics/superset/docker-compose.yml) and [derived version projection](../../../infra/tech-stack.versions.json)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
