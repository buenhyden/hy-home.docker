---
title: "ComfyUI Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0081"
parent_ids:
- "AD-0008"
created: "2026-09-19"
---

# ComfyUI Policy

## Overview

HOME image workflow UI, explicitly required always-on by the owner.

## Policy Scope

`infra/08-ai/comfyui` and services `comfyui` under profiles `ai / ai-image`.

## Controls

Use authenticated gateway ingress and loopback direct access. The current image exception is owned in image-tag-policy.exceptions.json. Review custom-node code before installation. The 4 GiB container budget and shared GPU need measured inference tests; always-on does not authorize concurrent heavy Ollama and image workloads.

[Implementation](../../../../../infra/08-ai/comfyui/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Exceptions

Owner @buenhyden must record scope, risk, expiry and exit condition before any deviation. Static configuration is not evidence of live backup or recovery.

## Verification

Compose/profile validation and the [runbook](runbook.md) provide separate static and runtime evidence. Stop on unexpected service, mount, authentication or readiness state.

## Review Cadence

Review monthly and before image, persistence, authentication or exposure changes.

## Traceability

- Governing architecture: [AD-0008](../../../../02.architecture/descriptions/0008-ai-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://docs.comfy.org/installation/system_requirements)
