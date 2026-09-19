---
title: "ComfyUI Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0081"
parent_ids:
- "POL-0081"
created: "2026-09-19"
---

# ComfyUI Guide

## Usage

HOME image workflow UI, explicitly required always-on by the owner.

Profiles: `ai / ai-image`. Services: `comfyui`. Root Compose owns inclusion.

Model, custom-node, output, input, user and cache directories are separate bind mounts beneath DEFAULT_AI_MODEL_DIR. COMFYUI_ARGS defaults its listener to COMFYUI_PORT; custom arguments must preserve listener agreement with health and ingress.

[Implementation](../../../../../infra/08-ai/comfyui/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Common Checks

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0008](../../../../02.architecture/descriptions/0008-ai-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://docs.comfy.org/installation/system_requirements)
