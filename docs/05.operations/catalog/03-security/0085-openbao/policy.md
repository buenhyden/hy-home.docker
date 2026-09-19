---
title: "OpenBao Policy"
version: "0.1.0"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "POL-0085"
parent_ids:
- "AD-0003"
created: "2026-09-19"
---

# OpenBao Policy

## Overview

HOME secret control plane; Vault remains a separate migration source.

## Policy Scope

`infra/03-security/openbao` and services `openbao openbao-agent` under profiles `core / security / secrets`.

## Controls

Keep unseal/recovery material offline. Never log token, role_id, secret_id or rendered files. Current status health accepts sealed state: container health alone does not prove secret delivery. Existing application Docker Secrets are not automatically replaced by Agent output.

[Implementation](../../../../../infra/03-security/openbao/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Exceptions

Owner @buenhyden must record scope, risk, expiry and exit condition before any deviation. Static configuration is not evidence of live backup or recovery.

## Verification

Compose/profile validation and the [runbook](runbook.md) provide separate static and runtime evidence. Stop on unexpected service, mount, authentication or readiness state.

## Review Cadence

Review monthly and before image, persistence, authentication or exposure changes.

## Traceability

- Governing architecture: [AD-0003](../../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
