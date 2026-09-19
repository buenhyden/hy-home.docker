---
title: "ComfyUI Guide"
version: "0.2.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "GDE-0081"
parent_ids:
- "POL-0081"
implementation_services:
  infra/08-ai/comfyui/docker-compose.yml:
  - comfyui
created: "2026-09-19"
---

# ComfyUI Guide

## Usage

ComfyUI is the always-on HOME image-workflow UI selected by `ai` and
`ai-image`. Root Compose includes [its implementation](../../../../../infra/08-ai/comfyui/docker-compose.yml); the service is reached through Traefik and also binds its declared loopback host port. `gateway-standard-chain@file,sso-errors@file,sso-auth@file` protects the public route.

The service uses the current upstream image declared in Compose. Its pinned
source, license, lifecycle and upgrade notes are owned by the upstream image
and [ComfyUI repository](https://github.com/Comfy-Org/ComfyUI); the local
[Dockerfile](../../../../../infra/08-ai/comfyui/Dockerfile) is a separate, currently unselected build authority. The [derived Compose image projection](../../../../../infra/tech-stack.versions.json) is only a drift view.

### Data and configuration boundary

| Mount | Contents | Recovery treatment |
| --- | --- | --- |
| `models` | downloaded model weights | replaceable only after recording source and checksum/licensing evidence |
| `custom_nodes` | third-party executable node code | preserve revision inventory; review before install or update |
| `user`, `input`, `output` | workflows, user settings, supplied and generated assets | back up as user data before destructive work |
| Hugging Face and Torch caches | downloaded artifacts | rebuildable cache, never a substitute for model provenance |

`COMFYUI_ARGS` must retain the listener and port matched by the healthcheck and
Traefik backend. `HF_HOME`, `TORCH_HOME`, NVIDIA compute/utility capabilities,
`gpus: all`, 4 GiB memory and two CPUs are declared source limits, not measured
headroom. Shared-GPU peak concurrency with Ollama is unverified.

### Normal operation

Use an approved workflow, record the required model and custom-node revisions,
then queue it through the UI. A successful `/system_stats` response shows that
the endpoint responds; it does not prove a model can load or a workflow is safe.
Use the [runbook](runbook.md) for approval-gated runtime checks and recovery.

### Source-backed lifecycle contract

- The selected `yanwk/comfyui-boot:cu126-slim` image is authoritative; the local Dockerfile is currently unselected. Record the image digest, CUDA/driver compatibility, model digests/licenses, workflow dependencies, and custom-node revisions before upgrade.
- `models`, `custom_nodes`, `user`, `input`, and `output` are the recovery set; caches are rebuildable only from recorded sources. Environment values include listener/port and cache paths; registry/download tokens, if introduced, remain secret-owner inputs.
- Traefik's standard/error/SSO chains protect the route; the loopback port is for local operations. Dependencies are NVIDIA runtime/driver, model storage, gateway/auth, root CA, and `infra_net`.
- Use `docker compose --profile ai --profile ai-image config --quiet` from root. Before upgrade, stop queue intake and active jobs, make a consistent stopped snapshot, test the new image/nodes/models on isolated mounts, and verify `/system_stats`, GPU visibility, expected nodes, and a representative workflow.
- ComfyUI is GPL-3.0 licensed; custom nodes and models carry separate licenses. Use the [official repository](https://github.com/Comfy-Org/ComfyUI) and [Manager guidance](https://docs.comfy.org/manager/overview).

## Common Checks

- Inspect profiles, route, mounts, resources and healthcheck in the [Compose source](../../../../../infra/08-ai/comfyui/docker-compose.yml).
- Inspect actual custom-node and model provenance before an upgrade; do not trust a cache directory as provenance.
- Use the central [backup policy](../../04-data/0021-backup-and-restore/policy.md) before changing persistent content.

## Runbook Handoff

Use the [ComfyUI Runbook](runbook.md) for approval-gated diagnosis and recovery.

## Traceability

- Governing architecture: [AD-0008](../../../../02.architecture/descriptions/0008-ai-architecture.md)
- [Policy](policy.md) and [Runbook](runbook.md)
- [Official custom-node management guidance](https://docs.comfy.org/manager/overview)

## Related Documents

- [ComfyUI Compose](../../../../../infra/08-ai/comfyui/docker-compose.yml)
- [Policy](policy.md), [Runbook](runbook.md)
