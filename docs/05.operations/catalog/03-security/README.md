---
title: "Operations — 03 Security"
version: "1.0.1"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
---

# Operations — 03 Security

> Canonical OpenBao operations grouped by stable subject.

## Overview

OpenBao (`0085-openbao`) is the canonical HOME secret service with Raft,
AppRole Agent rendering, and native Keycloak OIDC. Vault was removed in
SPEC-0180 S08; its preserved data path and seal material stay separate and out
of service.

## Audience

- Operators, SREs, security officers, developers, and AI agents.

## Scope

- OpenBao current operation.
- No secret values, runtime change, credential rotation, restore execution, or
  unauthenticated root recovery is authorized by this index.

## Structure

| Subject | Available documents |
| --- | --- |
| [OpenBao](0085-openbao/guide.md) | [Guide](0085-openbao/guide.md), [Policy](0085-openbao/policy.md), [Runbook](0085-openbao/runbook.md) |

## How to Work in This Area

Read the guide for routine context and policy for control boundaries. Execute
only the existing runbook procedure, including its stated safety, evidence,
rollback or recovery, and escalation conditions.

## Related Documents

- [Operations index](../../README.md)
- [Security infrastructure](../../../../infra/03-security/README.md)
- [Guides index](../../README.md)
- [Policies index](../../README.md)
- [Runbooks index](../../README.md)
