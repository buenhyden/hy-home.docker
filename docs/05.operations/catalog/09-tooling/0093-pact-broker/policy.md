---
title: "Pact Broker Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0093"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# Pact Broker Operations Policy

## Overview

The broker's verification results decide whether a version may be deployed, so
who can publish and verify, and where it is reachable, are the controls.

## Policy Scope

Provisioning, authentication, exposure, credentials, data retention and removal.

## Controls

- Select only through `contract-testing`; never add it to HOME.
- Provisioning lives in the feature SQL, not `mng-pg-init`. The role is
  `NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS` and owns only
  its database; the job refuses an administrator, a role it did not create, or a
  database with another owner.
- Basic auth stays enabled and `PACT_BROKER_ALLOW_PUBLIC_READ` stays `false`.
  Only the heartbeat is public.
- Publish the host port on `127.0.0.1` only. A route beyond loopback needs a
  reviewed change that adds TLS and single sign-on or token auth first.
- Credentials come from Docker secrets and never appear in Compose
  `environment`, argv, logs or published pacts. Pacts carry synthetic examples,
  not captured production payloads.
- Keep the analytics ping disabled.
- `PACT_BROKER_BASE_URL` stays unset: generated links follow the request
  `Host`, which is safe while the only listener is loopback and lets an
  in-network client work. Set it when a route is added.

## Exceptions

None. A second, read-only credential is added only when a consumer needs it.

## Verification

Static rendering and provisioning contract tests; an isolated run proving 401
without credentials, a public heartbeat, a publish and read-back with
credentials, a non-root read-only container and no secret in its environment or
logs.

## Review Cadence

Review on a broker major upgrade, on a new publishing pipeline, and whenever
exposure beyond loopback is proposed.

## Traceability

- [Guide](guide.md) (`GDE-0093`)
- [Runbook](runbook.md) (`RUN-0093`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Pact Broker Compose source](../../../../../infra/09-tooling/pact-broker/docker-compose.yml)
- [Management database policy](../../04-data/0028-management-database/policy.md)
