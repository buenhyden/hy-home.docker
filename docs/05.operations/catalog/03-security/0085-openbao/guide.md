---
title: "OpenBao Guide"
version: "0.1.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0085"
parent_ids:
- "POL-0085"
created: "2026-09-19"
---

# OpenBao Guide

## Usage

HOME secret control plane; Vault remains a separate migration source.

Profiles: `core / security / secrets`. Services: `openbao openbao-agent`. Root Compose owns inclusion.

Raft data, AppRole bootstrap material and rendered output use separate bind volumes. Agent config must be mounted at the command path; rendered files must stay under /openbao/out. VAULT_ADDR overrides the HCL server address.

[Implementation](../../../../../infra/03-security/openbao/docker-compose.yml) and [version projection](../../../../../infra/tech-stack.versions.json) own runtime pins.

## Common Checks

Check selected services, declared mounts, published interfaces and container state before use. Readiness and data recovery remain unverified until the runbook evidence is collected.

## Runbook Handoff

[Runbook](runbook.md) owns commands, expected results and recovery. [Policy](policy.md) owns controls.

## Traceability

- Governing architecture: [AD-0003](../../../../02.architecture/descriptions/0003-security-architecture.md)
- [Guide](guide.md), [Policy](policy.md), [Runbook](runbook.md)

## Related Documents

- [Operations index](../../../README.md)
- [Upstream documentation](https://openbao.org/docs/agent-and-proxy/agent/)
