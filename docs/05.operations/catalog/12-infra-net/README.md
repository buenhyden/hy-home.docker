# Operations — 12 Infra Net

> `infra_net` standardization and static-address operations grouped by stable subject and role.

## Overview

This domain co-locates the existing guide, policy, and runbook under the frozen
`ops-0077-standardize-infra-net` identity. The three roles preserve their
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
| [`infra_net` standardization](ops-0077-standardize-infra-net/guide.md) | [Guide](ops-0077-standardize-infra-net/guide.md), [Policy](ops-0077-standardize-infra-net/policy.md), [Runbook](ops-0077-standardize-infra-net/runbook.md) |

## How to Work in This Area

Use the guide for mapping context and common checks, the policy for allocation
and exception controls, and the runbook for ordered validation and recovery.
Runtime-changing network actions remain separately approval-gated.

## Related Documents

- [Operations index](../../README.md)
- [Infrastructure index](../../../../infra/README.md)
- [`infra_net` specification](../../../03.specs/spec-0098-standardize-infra-net/spec.md)
- [Incident records](../../incidents/README.md)
- [Release records](../../releases/README.md)
