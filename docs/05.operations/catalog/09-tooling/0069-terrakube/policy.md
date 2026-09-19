---
title: "Terrakube Operations Policy"
version: "1.1.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-20"
layer: "operations"
artifact_id: "POL-0069"
parent_ids:
- "AD-0009"
created: "2026-05-17"
---

# Terrakube Operations Policy

## Overview

Terrakube is an explicit `iac` control plane. Its Apache-2.0 project license does
not establish support, SLA, enterprise features, or HA for this single-host deployment.

## Policy Scope

API/UI/executor activation, native/gateway authentication, Docker-socket and
provider authority, PostgreSQL/MinIO/Valkey data, coordinated recovery, upgrades,
and removal.

## Controls

- **Activation:** start only the three named Terrakube services under `iac`, with
  exact dependencies selected separately. It is excluded from HOME/tooling.
- **Authentication:** verify both the tracked gateway middleware and application
  OIDC behavior. Do not claim native OIDC or group authorization from env labels alone.
- **Execution:** executor Docker socket access and provider credentials are
  privileged. Plans and applies name repository/ref, workspace, account, expected
  resources, and approver. Apply/destroy remain separately approved.
- **Secrets:** use only declared secret files; no secret/state/plan output in
  logs, screenshots, Tasks, or support bundles.
- **Data:** PostgreSQL metadata and MinIO `tfstate` are jointly authoritative.
  Valkey is coordination state. Retention must cover a consistent recovery point.
- **Backup/recovery:** quiesce scheduling/execution, capture PostgreSQL and MinIO
  consistently, preserve config/client/custody metadata, and rehearse with
  external execution disabled. One-store recovery is incomplete.
- **Resources/availability:** treat this as a single-host, single-replica DEV
  deployment. Do not describe container restart as HA or disaster recovery.
- **Upgrade:** test migrations on restored copies and move API/UI/executor as a
  compatible set. Database/state rollback accompanies an incompatible downgrade.
- **Removal:** retain workspaces, runs, state, outputs, VCS mappings, and recovery
  custody until an approved successor owns them; deleting containers is insufficient.

## Exceptions

An exception cannot bypass provider/apply approval, Docker-socket review, secret
handling, or coordinated backup. Record expiry and recovery owner.

## Verification

Static Compose and component health are partial signals. End-to-end evidence
requires login/authorization, DB/object reachability, executor registration, and
a reviewed non-applying plan. Restore remains unverified until rehearsed.

## Review Cadence

Review before each release, auth change, storage/backend change, or Docker-socket
permission change.

## Traceability

- [Guide](guide.md) (`GDE-0069`)
- [Runbook](runbook.md) (`RUN-0069`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Terrakube Compose source](../../../../../infra/09-tooling/terrakube/docker-compose.yml)
- [Terrakube documentation](https://docs.terrakube.io/)
- [Terrakube license](https://github.com/terrakube-io/terrakube/blob/main/LICENSE)
- [Operations index](../../../README.md)
