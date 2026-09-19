---
title: "Renovate Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0083"
parent_ids:
- "POL-0083"
created: "2026-09-19"
---

# Renovate Guide

## Usage

DEV maintenance job; excluded from normal HOME and broad startup.

Profiles: `dependency-update`. Services: `renovate`. Root Compose owns inclusion.

renovate.json5 owns repository update policy; config/config.js owns the self-host execution allowlist. renovate_token is mounted as a Docker Secret. The cache volume is disposable; repository policy and generated registry updates are review artifacts.

[Implementation](../../../../../infra/09-tooling/renovate/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Common Checks

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0009](../../../../02.architecture/descriptions/0009-tooling-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://docs.renovatebot.com/self-hosted-configuration/#allowedcommands)
