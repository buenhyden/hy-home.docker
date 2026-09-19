---
title: "Mailpit Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0084"
parent_ids:
- "POL-0084"
created: "2026-09-19"
---

# Mailpit Runbook

## When to Use

Use for `mailpit` readiness checks and approved targeted deployment or recovery. Work from the repository root. Confirm configuration commit, image source, existing data location and a protected backup before runtime changes.

## Procedure

1. Validate the selected profile with the existing Compose validator; never print a private rendered model.
2. Run this bounded read-only check:

```bash
docker compose --profile mail-dev exec -T mailpit /mailpit readyz
curl --fail --silent --output /dev/null http://127.0.0.1:${MAILPIT_UI_HOST_PORT:-8025}/
```

1. Native readiness and UI reachability are not SMTP delivery evidence. Send an approved synthetic message from a test consumer, confirm capture, then remove the fixture through the UI. Do not print message bodies in audit logs.
2. If deployment is approved, name only these services and verify initialization jobs and daemon readiness separately. Stop on an unexpected mount or failed check; do not broaden to the whole stack.

[Implementation](../../../../../infra/10-communication/mailpit/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Evidence

Record date, configuration commit, service names, exit statuses and sanitized health/resource results in the current Task. Do not capture secret values, raw environment, state, token files or message/database contents. No runtime validation is claimed by this document.

## Rollback or Recovery

For durable test mail, back up the quiesced database and restore on isolated storage. Otherwise document approved discard of disposable mail. Do not delete the volume as a default troubleshooting action.

## Escalation

Stop and contact @buenhyden when credentials, destructive storage changes, remote mutations or unavailable backups prevent safe progress.

## Traceability

- Governing architecture: [AD-0010](../../../../02.architecture/descriptions/0010-communication-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://mailpit.axllent.org/docs/configuration/runtime-options/)
