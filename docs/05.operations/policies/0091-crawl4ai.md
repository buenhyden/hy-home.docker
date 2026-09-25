---
title: "Crawl4AI Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "POL-0091"
parent_ids:
- "AD-0008"
created: "2026-09-21"
---

# Crawl4AI Operations Policy

## Overview

Crawl4AI is an SSRF-capable service. It stays isolated, authenticated and
unused until a reviewed consumer needs it.

## Policy Scope

Activation, network placement, authentication, consumers, provider keys and removal.

## Controls

- Select only through `crawl4ai`; never add it to `ai`, `notebook` or HOME.
- Never attach it to the declared networks, publish a host port or add a public route.
- Always run with the token secret; never pass provider keys through a tracked file.
- Connect a consumer only by adding that consumer to `crawl4ai_net` in a
  reviewed change that also sets its token.

## Exceptions

`GET /health` is unauthenticated upstream behavior.

## Verification

Static rendering and template baseline; live: `/health` 200, other endpoints 401
without token, and no resolution of `mng-pg` or `openbao` from the container.

## Review Cadence

Review on image upgrade, consumer connection, and at each service
rationalization review; remove the package if it still has no consumer.

## Traceability

- [Guide](../guides/0091-crawl4ai.md) (`GDE-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI Compose source](../../../infra/08-ai/crawl4ai/docker-compose.yml)
