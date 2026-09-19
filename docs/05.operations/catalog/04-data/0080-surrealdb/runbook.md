---
title: "SurrealDB Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0080"
parent_ids:
- "POL-0080"
created: "2026-09-19"
---

# SurrealDB Runbook

## When to Use

Use for `surrealdb` readiness checks and approved targeted deployment or recovery. Work from the repository root. Confirm configuration commit, image source, existing data location and a protected backup before runtime changes.

## Procedure

1. Validate the selected profile with the existing Compose validator; never print a private rendered model.
2. Run this bounded read-only check:

```bash
docker compose exec -T surrealdb /usr/local/bin/surreal isready --conn http://127.0.0.1:8000
```

1. Readiness proves reachability only. An authenticated isolated fixture must verify namespace access and persistence before promotion; record result without query data or credentials.
2. If deployment is approved, name only these services and verify initialization jobs and daemon readiness separately. Stop on an unexpected mount or failed check; do not broaden to the whole stack.

[Implementation](../../../../../infra/04-data/specialized/surrealdb/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Evidence

Record date, configuration commit, service names, exit statuses and sanitized health/resource results in the current Task. Do not capture secret values, raw environment, state, token files or message/database contents. No runtime validation is claimed by this document.

## Rollback or Recovery

Take a consistent approved export or quiesced storage backup. Restore to a separate directory and verify with the matching engine before selecting recovered data.

## Escalation

Stop and contact @buenhyden when credentials, destructive storage changes, remote mutations or unavailable backups prevent safe progress.

## Traceability

- Governing architecture: [AD-0004](../../../../02.architecture/descriptions/0004-data-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://surrealdb.com/docs/surrealdb/cli/start)
