---
title: "ComfyUI Runbook"
version: "0.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "RUN-0081"
parent_ids:
- "POL-0081"
created: "2026-09-19"
---

# ComfyUI Runbook

## When to Use

Use for `comfyui` readiness checks and approved targeted deployment or recovery. Work from the repository root. Confirm configuration commit, image source, existing data location and a protected backup before runtime changes.

## Procedure

1. Validate the selected profile with the existing Compose validator; never print a private rendered model.
2. Run this bounded read-only check:

```bash
curl --fail --silent --output /dev/null http://127.0.0.1:${COMFYUI_HOST_PORT:-8188}/system_stats
```

1. Check system_stats, GPU visibility and an approved small synthetic workflow. Confirm output persistence across a separately approved restart; do not download models during a read-only check.
2. If deployment is approved, name only these services and verify initialization jobs and daemon readiness separately. Stop on an unexpected mount or failed check; do not broaden to the whole stack.

[Implementation](../../../../../infra/08-ai/comfyui/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Evidence

Record date, configuration commit, service names, exit statuses and sanitized health/resource results in the current Task. Do not capture secret values, raw environment, state, token files or message/database contents. No runtime validation is claimed by this document.

## Rollback or Recovery

Back up user workflows, custom-node revision inventory and irreplaceable input/output. Keep model cache rebuild separate from data recovery. Restore compatible nodes and workflows on an isolated copy before switching mounts.

## Escalation

Stop and contact @buenhyden when credentials, destructive storage changes, remote mutations or unavailable backups prevent safe progress.

## Traceability

- Governing architecture: [AD-0008](../../../../02.architecture/descriptions/0008-ai-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://docs.comfy.org/installation/system_requirements)
