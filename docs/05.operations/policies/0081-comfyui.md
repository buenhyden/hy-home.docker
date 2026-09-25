---
title: "ComfyUI Policy"
version: "0.2.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0081"
parent_ids:
- "AD-0008"
created: "2026-09-19"
---

# ComfyUI Policy

## Overview

ComfyUI is the always-on HOME image-workflow interface.

## Policy Scope

Keep `comfyui` as an always-on HOME capability under `ai` and `ai-image`.
Compose owns service selection, gateway labels, GPU request, resources and mounts.

## Controls

- Keep gateway authentication and loopback-only direct publication. Exposure or gateway changes require an approved exception with scope, expiry and rollback.
- Treat custom nodes as third-party executable code. Review provenance, revision, dependencies and license before install or update; keep an inventory sufficient to reproduce the known-good node set.
- Preserve `user`, `input` and `output` as user data. Preserve model source/checksum and custom-node revision inventory. Hugging Face and Torch caches are rebuildable, but do not delete them while diagnosing without an approved recovery plan.
- Back up persistent user data before migration and restore only to isolated storage first. A static Compose check does not establish a backup, GPU capacity, restart recovery or restore.
- Review upstream release notes and image compatibility before upgrade. Hold the prior image and data inventory until health and an approved representative workflow succeed; the current image tag is a source declaration, not a tested upgrade claim.

### Lifecycle and data controls

- ComfyUI remains owner-confirmed `HOME`. Route auth, loopback binding, GPU access, and source resource limits must remain explicit; limits are not measured headroom.
- Back up workflows/user settings, inputs/outputs required for recovery, custom-node revision inventory, and exact model provenance as one release set. Treat caches as disposable only when every artifact is reproducible.
- Pause queue intake and wait for or cancel active jobs before backup, restore, image upgrade, custom-node change, or model migration. Do not install executable nodes directly into the live recovery set.
- Restore/rehearse on isolated mounts/project with no public route and verify health, GPU, required nodes, model checksums/licenses, and a representative workflow before replacement.
- Removal requires user-data disposition, artifact provenance export, route shutdown, credential revocation, and explicit approval before deleting mounts.

## Exceptions

Exceptions require owner, scope, risk, expiry and recovery condition.

## Verification

Use source and metadata checks before deployment. Runtime starts, model downloads,
workflow runs, GPU utilization and restores need a separately approved target and
sanitized evidence. Escalate missing backup/provenance, unexpected port exposure,
or an unreviewed custom node.

## Review Cadence

Review monthly and before an image, custom-node, persistent-data, exposure or GPU policy change.

## Traceability

- Governing architecture: [AD-0008](../../02.architecture/descriptions/0008-ai-architecture.md)
- Subject peers: [Guide](../guides/0081-comfyui.md) and [Runbook](../runbooks/0081-comfyui.md)

## Related Documents

- [Guide](../guides/0081-comfyui.md), [Runbook](../runbooks/0081-comfyui.md)
- Runtime pins are owned by [ComfyUI Compose](../../../infra/08-ai/comfyui/docker-compose.yml); its declared image is selected instead of the local Dockerfile, and the [derived Compose image projection](../../../infra/tech-stack.versions.json) verifies drift.
- [Central backup policy](0021-backup-and-restore.md)
