<!-- Target: docs/90.references/kubernetes/README.md -->
# Kubernetes References

> Kubernetes and k3s/k3d migration reference material

## Overview

`docs/90.references/kubernetes` stores stable Kubernetes reference material used by architecture, operations, and migration planning. It explains durable interpretation and migration-analysis context without replacing active architecture decisions, execution plans, or runtime configuration.

This folder is not the source of truth for current deployment state. Runtime truth remains in `infra/`, `docker-compose.yml`, and validation scripts. Active migration decisions belong in `docs/02.architecture/`; implementation sequencing belongs in `docs/04.execution/`.

## Category Role

Use this category for slow-changing Kubernetes migration context, k3s/k3d evaluation notes, and source-backed background facts. Do not use it for rollout steps, task evidence, or incident recovery.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- System Architects
- AI Agents

## Scope

### In Scope

- Kubernetes migration reference analysis
- k3s/k3d background and evaluation criteria
- Stable service migration suitability notes
- Links to active architecture, execution, and operations docs

### Out of Scope

- Current runtime configuration
- Active migration execution plans
- Rollout, rollback, or incident runbooks
- Secret values, credentials, tokens, private keys

## Structure

```text
docs/90.references/kubernetes/
├── README.md                             # This file
└── docker-compose-to-k3s-migration.md    # Docker Compose to k3s/k3d migration reference
```

## Current References

- [docker-compose-to-k3s-migration.md](./docker-compose-to-k3s-migration.md) - Docker Compose to k3s/k3d migration suitability snapshot

## Reference Rules

1. Treat Kubernetes migration analysis as reference until an ADR or ARD accepts an active migration decision.
2. Keep execution sequencing in `docs/04.execution/plans/`, not in this category.
3. Re-check runtime facts against `infra/`, root `docker-compose.yml`, and validators before using this reference for current planning.
4. Update this category README when adding, moving, or archiving Kubernetes reference docs.

## How to Work in This Area

1. Confirm the content is stable reference context, not an active plan or runbook.
2. Use [reference.template.md](../../99.templates/reference.template.md) for new non-README reference docs.
3. Link to active architecture and execution docs instead of duplicating decisions or task status.
4. Run `bash scripts/validation/check-repo-contracts.sh` after changing Kubernetes reference docs.

## Related Documents

- [references index](../README.md)
- [reference template](../../99.templates/reference.template.md)
- [architecture index](../../02.architecture/README.md)
- [execution index](../../04.execution/README.md)
- [operations index](../../05.operations/README.md)
