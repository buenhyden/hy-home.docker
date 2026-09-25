---
title: "WireMock Operations Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0092"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# WireMock Operations Policy

## Overview

WireMock answers HTTP requests with tracked stubs and records what it received.
Its admin API is unauthenticated, so exposure and stub content are the controls.

## Policy Scope

Selection, network exposure, stub content, the request journal and removal.

## Controls

- Select only through `api-mock`; never add it to HOME or to a domain profile.
- Publish the host port on `127.0.0.1` only and add no Traefik route. Exposing
  the admin API needs a reviewed change that adds authentication first.
- The project default network is the container-side trust boundary: any
  container in it has full admin rights. A named consumer gets a scoped network
  when it is added.
- Tracked mappings are the only durable stubs. Stub bodies are synthetic: no
  captured production response, credential, token or personal data.
- Recording or proxying to a real upstream is prohibited by policy. The
  read-only mount only blocks persisting a recording; starting one, or a stub
  with `proxyBaseUrl`, through the admin API is not technically prevented.
- Keep the request journal bounded; requests sent to the stub may carry test
  credentials and are readable through the admin API while it runs.

## Exceptions

None. A consumer that needs a stub reachable from another network joins the
project default network instead of widening the host binding.

## Verification

Compose rendering, the operations catalog check, and an isolated run proving
health, the tracked stub, a non-root user and a read-only root filesystem.

## Review Cadence

Review on a WireMock major upgrade, on a new consumer, and whenever exposure
beyond loopback is proposed.

## Traceability

- [Guide](../guides/0092-wiremock.md) (`GDE-0092`)
- [Runbook](../runbooks/0092-wiremock.md) (`RUN-0092`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [WireMock Compose source](../../../infra/09-tooling/wiremock/docker-compose.yml)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
