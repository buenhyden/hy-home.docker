---
title: "Crawl4AI Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0091"
parent_ids:
- "POL-0091"
implementation_services:
  infra/08-ai/crawl4ai/docker-compose.yml:
  - crawl4ai
created: "2026-09-21"
---

# Crawl4AI Usage Guide

## Usage

### Purpose and classification

Crawl4AI is an OPTIONAL crawler selected only by `crawl4ai`. Its planned
consumer is Open Notebook's remote-crawler setting, which is still commented
out, so no service uses it today. Keeping it costs nothing until selected;
remove it if no consumer is connected by the next review.

### Current implementation

- [Crawl4AI Compose](../../../infra/08-ai/crawl4ai/docker-compose.yml)
  pins the upstream image, extends `template-infra-high` with a 4 GiB memory
  and 512 PID limit, and runs read-only with tmpfs work paths.
- The server needs `crawl4ai_api_token`; with a token upstream requires
  `Authorization: Bearer` on every endpoint except `GET /health`.
- It joins only `crawl4ai_net`. There is no host port and no Traefik route.
- The previously tracked empty `.llm.env` and the unused local build block were
  removed; provider keys must never be committed.

### SSRF boundary

A crawler fetches whatever URL a caller sends. Because it is not on the declared networks,
internal databases, OpenBao, Kafka Connect and admin APIs are unreachable by
container name. The host and LAN remain reachable through the default route, so
restrict callers and do not treat network separation as a URL allowlist.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`

## Runbook Handoff

Use the [runbook](../runbooks/0091-crawl4ai.md) for token, start and consumer-connection work.

## Traceability

- [Policy](../policies/0091-crawl4ai.md) (`POL-0091`)
- [Runbook](../runbooks/0091-crawl4ai.md) (`RUN-0091`)
- [AI architecture](../../02.architecture/descriptions/0008-ai-architecture.md)

## Related Documents

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
- [Open Notebook guide](0073-open-notebook.md)
