---
title: "ComfyUI Implementation"
version: "0.1.1"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
---

# ComfyUI

## Overview

Image workflow service required always-on. Shared GPU workload concurrency must be measured with Ollama; the runtime image exception has a separate owner.

Lifecycle: **HOME**. Root Compose includes this definition; explicit profiles control activation.

## Audience

Operators and developers reviewing implementation, configuration and validation.

## Scope

Local service definitions and implementation navigation. Operational controls and recovery belong to `OPS-0081` in the operations catalog, reached through the [documentation index](../../../docs/README.md).

## Structure

- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)

## Tech Stack

Runtime pins belong to [Compose](docker-compose.yml) and its referenced build sources. The [version registry](../../../infra/tech-stack.versions.json) is a curated projection, not a deployment manifest.

## Configuration

| Service | Profiles | Networks | `edge_net` | Secret references |
| --- | --- | --- | --- | --- |
| `comfyui` | `ai, ai-image` | `ai_net` | `127.0.0.1:${COMFYUI_HOST_PORT:-8188}:${COMFYUI_PORT:-8188}` | No Compose Secret grant; inspect configured bootstrap file metadata |

Persistence:

- `comfyui-models`: `${DEFAULT_AI_MODEL_DIR}/comfyui/models`
- `comfyui-custom-nodes`: `${DEFAULT_AI_MODEL_DIR}/comfyui/custom_nodes`
- `comfyui-output`: `${DEFAULT_AI_MODEL_DIR}/comfyui/output`
- `comfyui-input`: `${DEFAULT_AI_MODEL_DIR}/comfyui/input`
- `comfyui-user`: `${DEFAULT_AI_MODEL_DIR}/comfyui/user`
- `comfyui-hf-cache`: `${DEFAULT_AI_MODEL_DIR}/comfyui/cache/huggingface`
- `comfyui-torch-cache`: `${DEFAULT_AI_MODEL_DIR}/comfyui/cache/torch`

Environment key names and defaults are declared in Compose and the [public environment example](../../../.env.example). Mount grants and healthcheck commands in Compose describe the implementation; a passing config check does not prove runtime readiness. Do not print private environment values, credential files or raw rendered configuration.

## Validation

From the repository root, select the documented profiles and use `scripts/validation/validate-docker-compose.sh`. Use the owning operations Runbook for targeted runtime checks and recovery after approval. Stop on missing mounts, unexpected exposure or failed initialization.

## How to Work in This Area

Keep Compose, build sources, public environment keys and secret references consistent. Review gateway authentication, persistence, resource budgets and version exceptions before changing them. Update the existing operations subject instead of duplicating commands here.

### Convergence contract

- Classification: **HOME**. Exact profiles: `ai`, `ai-image`.
- Source authority: this package Compose and its selected image/build inputs; `infra/tech-stack.versions.json` is a derived projection.
- Root preflight: `docker compose --profile ai config --quiet`. Root targeted start: `docker compose --profile ai up -d comfyui`.
- Stable entry point: [docs/README.md](../../../docs/README.md). Exact Stage 05 path `docs/05.operations/guides/0081-comfyui.md`; IDs `GDE-0081`, `POL-0081`, `RUN-0081`.
- The subject runbook's isolated recovery is planned and unexecuted. Preserve model/content provenance and never use a live filesystem copy as restore evidence.

## Related Documents

- [Infrastructure index](../../../infra/README.md)
- [Documentation index](../../../docs/README.md)
- [Public secret contract](../../../secrets/README.md)
