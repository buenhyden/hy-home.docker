---
title: "SonarQube Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0066"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# SonarQube Operations Policy

## Overview

This policy governs the tracked SonarQube Community Build deployment without
assuming paid-edition features, native Keycloak integration, or a universal CI gate.

## Policy Scope

Activation, gateway/application auth, tokens, database/index/log data, resource
limits, backup/restore, upgrades, and removal.

## Controls

- **Activation:** use `sast` or general `tooling`; keep it outside HOME.
- **Authentication:** gateway ForwardAuth protects entry, while SonarQube owns
  application users, groups, permissions, and tokens. Native delegated auth is
  absent until configured and tested. IdP deactivation does not by itself revoke
  existing SonarQube tokens; revoke them in SonarQube.
- **Tokens:** issue minimum-scope expiring tokens, store them in approved CI secret
  owners, and rotate/revoke without logging values.
- **Data:** PostgreSQL is authoritative. Local search indexes are rebuildable;
  logs follow incident/evidence retention. Do not treat the data volume alone as backup.
- **Backup/restore:** use database-native backup, verify it, and rehearse isolated
  restore plus reindex. Capture tracked config and external plugin inventory.
- **Resources:** respect the tracked heap and stateful-high limits. Change them
  only from measured queue/heap/index evidence and host capacity.
- **Upgrade:** review edition/version compatibility, DB/host requirements, and
  plugin compatibility; test on restored data. Rollback image and DB together.
- **Removal:** preserve or explicitly dispose of projects, settings, issues,
  users, tokens, and backup evidence before deleting the database/schema or volumes.

## Exceptions

Paid features, native SAML/OIDC provisioning, or broader quality-gate mandates
require their owning requirement/policy and cannot be inferred here.

## Verification

Health is partial. Runtime acceptance includes DB access, gateway plus app
authorization, background task completion, representative analysis, and backup/
restore evidence where claimed.

## Review Cadence

Review on release, DB/plugin/auth/token, resource, or retention changes.

## Traceability

- [Guide](../guides/0066-sonarqube.md) (`GDE-0066`)
- [Runbook](../runbooks/0066-sonarqube.md) (`RUN-0066`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [SonarQube Compose source](../../../infra/09-tooling/sonarqube/docker-compose.yml)
- [Community Build authentication](https://docs.sonarsource.com/sonarqube-community-build/instance-administration/authentication/overview)
- [Managing SonarQube tokens](https://docs.sonarsource.com/sonarqube-community-build/user-guide/managing-tokens)
