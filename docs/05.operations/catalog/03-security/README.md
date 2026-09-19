---
title: "Operations — 03 Security"
version: "1.0.0"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "operations"
---

# Operations — 03 Security

> Canonical OpenBao and legacy Vault operations grouped by stable subject.

## Overview

OpenBao (`0085-openbao`) is the canonical HOME secret service with Raft,
AppRole Agent rendering, and native Keycloak OIDC. Vault (`0016-vault`) is
retained only under `legacy-vault` for migration and recovery. Their data paths,
seal material, snapshots, and consumers remain separate.

## Audience

- Operators, SREs, security officers, developers, and AI agents.

## Scope

- OpenBao current operation and legacy Vault migration/recovery.
- No secret values, runtime change, credential rotation, restore execution, or
  unauthenticated root recovery is authorized by this index.

## Structure

| Subject | Available documents |
| --- | --- |
| [Vault](0016-vault/guide.md) | [Guide](0016-vault/guide.md), [Policy](0016-vault/policy.md), [Runbook](0016-vault/runbook.md) |

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
