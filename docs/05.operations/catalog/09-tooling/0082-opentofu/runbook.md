---
title: "OpenTofu Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0082"
parent_ids:
- "POL-0082"
created: "2026-09-19"
---

# OpenTofu Runbook

## When to Use

Use for `opentofu` readiness checks and approved targeted deployment or recovery. Work from the repository root. Confirm configuration commit, image source, existing data location and a protected backup before runtime changes.

## Procedure

1. Validate the selected profile with the existing Compose validator; never print a private rendered model.
2. Run this bounded read-only check:

```bash
docker compose --profile iac config --services
```

1. This command verifies selection only. After authorizing the exact workspace, run init/validate and a reviewed plan using the operational account; inspect resources locally and record counts, not plan payloads.
2. If deployment is approved, name only these services and verify initialization jobs and daemon readiness separately. Stop on an unexpected mount or failed check; do not broaden to the whole stack.

[Implementation](../../../../../infra/09-tooling/opentofu/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Evidence

Record date, configuration commit, service names, exit statuses and sanitized health/resource results in the current Task. Do not capture secret values, raw environment, state, token files or message/database contents. No runtime validation is claimed by this document.

## Rollback or Recovery

Preserve encrypted state backups and lock ownership. Reverting a configuration commit does not revert remote resources; recovery requires a separately reviewed plan. Never force-unlock another active operator.

## Escalation

Stop and contact @buenhyden when credentials, destructive storage changes, remote mutations or unavailable backups prevent safe progress.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://opentofu.org/docs/cli/commands/plan/)
