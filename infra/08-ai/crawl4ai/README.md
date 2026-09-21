---
title: "AI Crawl4AI Crawler"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-21"
created: "2026-09-21"
---

# AI Crawl4AI Crawler

> Token-protected web crawler that renders pages with Chromium and returns LLM-ready Markdown.

## Overview

Crawl4AI fetches arbitrary URLs on request, so it can be abused for server-side
request forgery (SSRF). It is therefore isolated on its own `crawl4ai_net`
egress network and never joins `infra_net`. Its intended consumer is Open
Notebook's remote-crawler setting, which is currently commented out; no service
consumes it today. Lifecycle: **OPTIONAL**, selected only by `crawl4ai`.

## Audience

- **Operators** deciding whether to enable the crawler and connect a consumer.
- **AI agents** changing this package under the owning Guide, Policy and Runbook.

## Scope

- **Included**: pinned upstream image, token handling, network isolation, resource limits.
- **Excluded**: LLM provider keys (the former tracked `.llm.env` was removed), consumer wiring.

## Structure

```text
.
├── docker-compose.yml  # crawl4ai service and crawl4ai_net
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `crawl4ai` | Upstream image declared in [Compose](docker-compose.yml) | Crawl API with headless Chromium |

Runtime pins are owned by the Compose declaration; the
[derived Compose image projection](../../tech-stack.versions.json) provides drift verification.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `crawl4ai` only; not selected by `ai`, `notebook` or HOME |
| Network / port | `crawl4ai_net` only; internal `11235` via `expose`; no host port, no Traefik route |
| Authentication | Secret `crawl4ai_api_token` (AI-006) exported as `CRAWL4AI_API_TOKEN`; upstream then requires `Authorization: Bearer` on every endpoint except `GET /health` |
| Hardening | `template-infra-high`, `cap_drop: ALL`, `no-new-privileges`, read-only root with tmpfs work paths, `mem_limit: 4g`, `pids_limit: 512`, private `shm_size` |
| Persistence | None; outputs and caches are tmpfs |
| Health | `GET /health` (unauthenticated by design); proves the API answers, not browser rendering |

## Validation

- `HYHOME_COMPOSE_PROFILES=crawl4ai bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/validation/check-template-security-baseline.sh`

## How to Work in This Area

1. Create `secrets/tools/crawl4ai_api_token.txt` through the registered secret workflow.
2. Start only with an approved target: `docker compose --profile crawl4ai up -d crawl4ai`.
3. To connect Open Notebook, add `crawl4ai_net` to that service and set `CRAWL4AI_API_URL` and the
   token in one reviewed change; do not add the crawler to `infra_net`.

## Related Documents

- **Guide**: Crawl4AI usage guide (`docs/05.operations/catalog/08-ai/0091-crawl4ai/guide.md`)
- **Policy**: Crawl4AI operations policy (`docs/05.operations/catalog/08-ai/0091-crawl4ai/policy.md`)
- **Runbook**: Crawl4AI recovery runbook (`docs/05.operations/catalog/08-ai/0091-crawl4ai/runbook.md`)
- [Documentation index](../../../docs/README.md)
