---
profile_id: operations-domain-readme
---

# Operations — 12 Infra Net

> `infra_net` standardization and static-address operations grouped by stable subject and role.

## Overview

This domain co-locates the existing guide, policy, and runbook under the current
`0077-ip-address-management` subject directory. The three roles preserve their
separate usage, control, and procedure responsibilities.

## Audience

- Operators, SREs, platform engineers, developers, and AI agents.

## Scope

- Existing `infra_net` mapping context, address-allocation controls,
  non-destructive validation, recovery boundaries, and escalation.
- No live network recreation, static-IP mutation, service restart, or
  credential access is authorized by this index.

## Structure

| Subject | Available documents |
| --- | --- |
| [`infra_net` standardization](0077-ip-address-management/guide.md) | [Guide](0077-ip-address-management/guide.md), [Policy](0077-ip-address-management/policy.md), [Runbook](0077-ip-address-management/runbook.md) |

## How to Work in This Area

Use the guide for mapping context and common checks, the policy for allocation
and exception controls, and the runbook for ordered validation and recovery.
Runtime-changing network actions remain separately approval-gated.

## Related Documents

- [Operations index](../../README.md)
- [Infrastructure index](../../../../infra/README.md)
- [`infra_net` specification](../../../03.specs/0098-standardize-infra-net/spec.md)
- [Incident records](../../incidents/README.md)
