---
status: completed
---

<!-- Target: docs/03.specs/108-compose-profile-service-coverage-snapshot/README.md -->

# Compose Profile Service Coverage Snapshot

> Stage 90 generated Docker Compose profile/service inventory contract

## Overview

This folder defines the technical contract for generating a static reference
that maps tracked Docker Compose services to declared Compose profiles and
infrastructure stages.

The generator closes the `AEA-AUTO-005` audit candidate by making profile
coverage evidence reproducible instead of manually maintained in audit prose.

## Audience

This README is for:

- Infra/DevOps Engineers
- QA Engineers
- Documentation Specialists
- Repository Maintainers

## Scope

### In Scope

- Static parsing of tracked root and `infra/**/docker-compose*.yml` / `.yaml`
  files.
- Generated Stage 90 Docker data reference for service, profile, file, and
  stage coverage.
- Repository-contract freshness validation for the generated snapshot.
- Stage 04 evidence for implementation and verification.

### Out of Scope

- Running Docker Compose, starting containers, or inspecting live runtime state.
- Reading `.env` values, secret files, container logs, tokens, credentials,
  private keys, shell history, or raw logs.
- Changing Compose service behavior, profiles, CI workflows, or deployment
  procedures.

## Structure

```text
108-compose-profile-service-coverage-snapshot/
├── README.md
└── spec.md
```

## How to Work in This Area

1. Use [spec.md](./spec.md) as the implementation contract.
2. Keep generated inventory output under
   [Stage 90 Docker data](../../90.references/data/docker/compose-profile-service-coverage.md).
3. Re-run the generator after tracked Compose service or profile changes.
4. Keep execution ordering and evidence in the linked Stage 04 plan and task.

## Related Documents

- [Spec](./spec.md)
- [Implementation plan](../../04.execution/plans/2026-07-05-compose-profile-service-coverage-snapshot.md)
- [Task evidence](../../04.execution/tasks/2026-07-05-compose-profile-service-coverage-snapshot.md)
- [Generated Compose profile coverage reference](../../90.references/data/docker/compose-profile-service-coverage.md)
- [Automation candidates](../../90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/automation-candidates.md)
