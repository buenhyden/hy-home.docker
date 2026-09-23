---
title: "Operations — 12 Infra Net"
version: "1.1.0"
type: "operation/domain-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
---

# Operations — 12 Infra Net

> Compose network membership and address operations grouped by stable subject and role.

## Overview

This domain co-locates the guide, policy, and runbook of the Compose network
membership subject (`0077`) and of the hy-home.k8s integration (`0096`), the
host-address contract with the k3d cluster. The three roles preserve their
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
| [hy-home.k8s integration](0096-k8s-integration/guide.md) | [Guide](0096-k8s-integration/guide.md), [Policy](0096-k8s-integration/policy.md), [Runbook](0096-k8s-integration/runbook.md) |

## How to Work in This Area

Use the guide for mapping context and common checks, the policy for allocation
and exception controls, and the runbook for ordered validation and recovery.
Runtime-changing network actions remain separately approval-gated.

## Related Documents

- [Operations index](../../README.md)
- [Infrastructure index](../../../../infra/README.md)
- [Compose network segmentation architecture](../../../02.architecture/descriptions/0026-standardize-infra-net.md)
- [Incident records](../../incidents/README.md)
