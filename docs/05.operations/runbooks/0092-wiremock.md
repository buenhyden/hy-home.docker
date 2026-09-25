---
title: "WireMock Recovery Runbook"
version: "1.0.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "RUN-0092"
parent_ids:
- "GDE-0092"
created: "2026-09-23"
---

# WireMock Recovery Runbook

## When to Use

The service is unhealthy, a request returns 404 where a stub was expected, a
mapping file fails to load, or the container hits its memory limit.

## Procedure

1. Inspect:

   ```bash
   docker compose --profile api-mock config --quiet
   docker compose --profile api-mock ps wiremock
   docker compose --profile api-mock logs --tail=100 wiremock
   curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/health
   ```

2. A mapping that fails to parse is named in the log at start. Fix the JSON in
   `infra/09-tooling/wiremock/mappings/` and reload with
   `curl -s -X POST http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/mappings/reset`.
3. For an unexpected 404, compare the request with the stubs:
   `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/requests/unmatched` lists requests
   no stub matched, and `__admin/requests/unmatched/near-misses` shows the closest
   stub for each.
4. An `OOMKilled` state means the journal cap or a large stub body outgrew the
   limit. Lower `--max-request-journal-entries` or shrink the body before
   raising the template.

## Evidence

Record the health response, the mapping count from `__admin/mappings`, exit
codes and the source commit. Do not record request bodies or headers from the
journal: a test may have sent a credential.

## Rollback or Recovery

The service holds no durable state. Recreating it from the tracked image and
mappings is a full recovery; in-memory stubs and the journal are lost by design.

## Escalation

Stop on any request to publish the admin API beyond loopback, to enable
recording against a real upstream, or to commit a captured production response.

## Traceability

- [Guide](../guides/0092-wiremock.md) (`GDE-0092`)
- [Policy](../policies/0092-wiremock.md) (`POL-0092`)
- [WireMock Compose](../../../infra/09-tooling/wiremock/docker-compose.yml)

## Related Documents

- [WireMock package README](../../../infra/09-tooling/wiremock/README.md)
- [WireMock admin API](https://wiremock.org/docs/standalone/admin-api-reference/)
