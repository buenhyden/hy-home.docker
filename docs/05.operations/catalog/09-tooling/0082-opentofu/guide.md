---
title: "OpenTofu Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0082"
parent_ids:
- "POL-0082"
created: "2026-09-19"
---

# OpenTofu Guide

## Usage

DEV operator job; excluded from HOME automatic startup.

Profiles: `iac / tooling`. Services: `opentofu`. Root Compose owns inclusion.

The inline Dockerfile owns the OpenTofu source image. The workspace bind mount contains configuration and state; cloud credential directories are read-only inputs but still grant remote authority. No daemon readiness is expected.

[Implementation](../../../../../infra/09-tooling/opentofu/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Common Checks

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://opentofu.org/docs/cli/commands/plan/)
