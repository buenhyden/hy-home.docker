---
title: "Crawl4AI Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "RUN-0091"
parent_ids:
- "GDE-0091"
created: "2026-09-21"
---

# Crawl4AI Recovery Runbook

## When to Use

Start failure, token exposure, memory pressure, or connecting/disconnecting a consumer.

## Procedure

1. Inspect:

   ```bash
   docker compose --profile crawl4ai config --quiet
   docker compose --profile crawl4ai ps -a crawl4ai
   docker compose --profile crawl4ai logs --tail=100 crawl4ai
   ```

2. Exit `64` means the token secret is missing or shorter than 16 characters.
3. On token exposure: stop the service, replace
   `secrets/tools/crawl4ai_api_token.txt`, update the consumer's token, start again.
4. On repeated out-of-memory restarts, lower crawl concurrency at the caller
   before raising `mem_limit`.
5. To remove the service, stop it, delete the include and package in one
   reviewed change, and retire the AI-006 secret row; it holds no data.

## Evidence

Record exit codes, image and source commit; not the token or crawled content.

## Rollback or Recovery

No persistent state exists; rollback is a Compose revert and restart.

## Escalation

Stop on any request to attach the crawler to `infra_net` or expose it publicly.

## Traceability

- [Guide](guide.md) (`GDE-0091`)
- [Policy](policy.md) (`POL-0091`)
- [Crawl4AI Compose](../../../../../infra/08-ai/crawl4ai/docker-compose.yml)

## Related Documents

- [Crawl4AI self-hosting](https://docs.crawl4ai.com/core/self-hosting/)
