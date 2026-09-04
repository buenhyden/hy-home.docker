---
title: "Operations Catalog"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "operations"
---

<!-- README Target: docs/05.operations/catalog/README.md -->

# Operations Catalog

## Overview

`docs/05.operations/catalog/`는 current Operations subject를 domain별로 찾는
canonical catalog다. Incident event record는 이 catalog에 속하지
않는다.

## Audience

- Operators
- Developers
- SREs
- Security Officers
- AI Agents

## Scope

- current Guide, Policy, Runbook subject 탐색
- stable four-digit subject identity와 domain owner routing
- domain README navigation

## Structure

| Domain | Route |
| --- | --- |
| 00 Workspace | [00-workspace](./00-workspace/README.md) |
| 01 Gateway | [01-gateway](./01-gateway/README.md) |
| 02 Auth | [02-auth](./02-auth/README.md) |
| 03 Security | [03-security](./03-security/README.md) |
| 04 Data | [04-data](./04-data/README.md) |
| 05 Messaging | [05-messaging](./05-messaging/README.md) |
| 06 Observability | [06-observability](./06-observability/README.md) |
| 07 Workflow | [07-workflow](./07-workflow/README.md) |
| 08 AI | [08-ai](./08-ai/README.md) |
| 09 Tooling | [09-tooling](./09-tooling/README.md) |
| 10 Communication | [10-communication](./10-communication/README.md) |
| 11 Laboratory | [11-laboratory](./11-laboratory/README.md) |
| 12 Infra Net | [12-infra-net](./12-infra-net/README.md) |

## How to Work in This Area

1. owning domain README에서 stable subject를 찾는다.
2. subject leaf의 기존 Guide, Policy, Runbook 역할만 사용한다.
3. subject README를 만들지 않는다.
4. Incident는 sibling `../incidents/`로 route한다.

## Related Documents

- [Operations](../README.md)
- [Incidents](../incidents/README.md)
- [Template catalog](../../99.templates/templates/README.md)
- [Stage authoring matrix](../../00.agent-governance/policies/stage-authoring-matrix.md)
