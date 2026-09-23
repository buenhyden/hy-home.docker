---
title: "Operations — 12 Infra Net"
version: "1.0.1"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
---

# Operations — 12 Infra Net

> Compose network membership and address operations grouped by stable subject and role.

## Overview

This domain co-locates the existing guide, policy, and runbook under the current
`0077-ip-address-management` subject directory. The three roles preserve their
separate usage, control, and procedure responsibilities.

## Audience

- Operators, SREs, platform engineers, developers, and AI agents.

## Scope

- Compose network membership context, address controls,
  non-destructive validation, recovery boundaries, and escalation.
- No live network recreation, static-IP mutation, service restart, or
  credential access is authorized by this index.

## Structure

| Subject | Available documents |
| --- | --- |
| [Compose network membership](0077-ip-address-management/guide.md) | [Guide](0077-ip-address-management/guide.md), [Policy](0077-ip-address-management/policy.md), [Runbook](0077-ip-address-management/runbook.md) |

## How to Work in This Area

Use the guide for mapping context and common checks, the policy for allocation
and exception controls, and the runbook for ordered validation and recovery.
Runtime-changing network actions remain separately approval-gated.

## Related Documents

- [Operations index](../../README.md)
- [Infrastructure index](../../../../infra/README.md)
- [Compose network segmentation architecture](../../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [Incident records](../../incidents/README.md)
