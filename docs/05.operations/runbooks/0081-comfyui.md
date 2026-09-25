---
title: "ComfyUI Runbook"
version: "0.2.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "RUN-0081"
parent_ids:
- "GDE-0081"
created: "2026-09-19"
---

# ComfyUI Runbook

## When to Use

Use for an approved ComfyUI deployment, unavailable UI, failed healthcheck, or
planned data/image/custom-node recovery. Record the commit, selected service,
mount locations, image identity and backup evidence before a runtime mutation.

## Procedure

1. Confirm the source boundary without rendering private environment values:

   ```bash
   rg -n 'profiles:|ai-image|gpus: all|COMFYUI_ARGS|comfyui-(models|custom-nodes|output|input|user)|system_stats|middlewares' infra/08-ai/comfyui/docker-compose.yml
   ```

2. On an approved running target, check only the selected service and capture the
   exit status:

   ```bash
   docker compose --profile ai --profile ai-image ps comfyui
   curl --fail --silent --output /dev/null http://127.0.0.1:${COMFYUI_HOST_PORT:-8188}/system_stats
   ```

   A response means the service endpoint answered. Check GPU visibility and an
   approved representative workflow separately; neither is currently claimed by
   this document as executed evidence.

3. If an image or custom-node update caused the failure, stop new workflow work,
   retain the previous image identity and custom-node revision inventory, and
   return the tracked configuration to the reviewed version. Do not delete model
   directories or caches as a first response.

4. For recovery, stop queue intake and active jobs, then protect `models`,
   `custom_nodes`, `user`, `input`, and `output` as a consistent set.
   Restore to isolated mounts first, validate that expected nodes and a
   representative workflow load, then obtain approval before replacing live
   data. Model and cache downloads are rebuildable only when source, digest,
   license, and compatibility have been recorded.

### Planned isolated restore rehearsal

Status: **planned and not executed**. No successful ComfyUI restore evidence is claimed here.

1. Record image digest, CUDA/driver versions, profiles, mount identities, workflow dependency inventory, custom-node revisions, and model/input checksums/licenses. Pause queue intake and finish or cancel active work, stop ComfyUI, then create an approved consistent snapshot.
2. Restore the complete set to new paths in a separate Compose project/network with no public route. Keep the source snapshot immutable.
3. Start the pinned image, verify `/system_stats`, GPU visibility, model checksums, expected custom nodes, workflow loading, and one representative generation whose inputs and output invariant are safe to record.
4. On any mismatch, stop the isolated service and retain logs/checksums. Return to untouched source artifacts; production mount or route replacement needs a separate approved change.

## Evidence

Record sanitized command output, time, commit, selected profile, image identity,
mount names and resulting state in the current Task. Do not record user assets,
workflow contents, private environment, tokens or remote download credentials.

## Rollback or Recovery

Return only tracked configuration to the reviewed version; preserve persistent mounts. Restore to isolated storage before an approved replacement.

## Escalation

Escalate unavailable backups, custom-node provenance gaps, unexpected exposure,
GPU failures or any destructive operation to @buenhyden.

## Traceability

- Governing architecture: [AD-0008](../../02.architecture/descriptions/0008-ai-architecture.md)
- Subject peers: [Guide](../guides/0081-comfyui.md) and [Policy](../policies/0081-comfyui.md)

## Related Documents

- [Guide](../guides/0081-comfyui.md), [Policy](../policies/0081-comfyui.md)
- Runtime pins are owned by [ComfyUI Compose](../../../infra/08-ai/comfyui/docker-compose.yml); the [derived Compose image projection](../../../infra/tech-stack.versions.json) verifies drift.
- [Central backup policy](../policies/0021-backup-and-restore.md)
