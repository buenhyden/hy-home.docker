---
title: Valkey Cluster Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0022
parent_ids:
  - AD-0004
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/04-data/0022-valkey-cluster/policy.md -->

# Valkey Cluster Operations Policy

> This policy governs the current Valkey cluster services under `04-data/cache-and-kv`.

---

## Overview

이 정책은 `infra/04-data/cache-and-kv/valkey-cluster`의 6-node Valkey cluster, init job, exporter 운영 통제를 정의한다. 정책 기준은 현재 compose와 `infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf`, `infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-start.sh`, `infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh`에 실제로 선언된 service, network, secret, persistence surface다.

## Policy Scope

- **Systems**: `valkey-node-0`, `valkey-node-1`, `valkey-node-2`, `valkey-node-3`, `valkey-node-4`, `valkey-node-5`, `valkey-cluster-init`, `valkey-cluster-exporter`
- **Configs**: `docker-compose.yml`, [valkey.conf](../../../../../infra/04-data/cache-and-kv/valkey-cluster/config/valkey.conf), [valkey-start.sh](../../../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-start.sh), [valkey-cluster-init.sh](../../../../../infra/04-data/cache-and-kv/valkey-cluster/scripts/valkey-cluster-init.sh)
- **Networks**: `infra_net`
- **Profiles**: `data`, `service`
- **Agents**: AI agents reviewing or updating operations docs, compose references, validation evidence, or cache/kv runtime boundaries

## Controls

- **Required**:
  - Authentication and node-to-node `masterauth` use Docker Secret `service_valkey_password`.
  - The six data volumes are bound under `${DEFAULT_DATA_DIR}/valkey/data-0` through `data-5`.
  - Cluster initialization uses `valkey-cluster-init`; destructive re-initialization is not allowed as a documentation-only operation.
  - Compose-facing documentation must list the current service set and image family `valkey/valkey:9.1.0-alpine`.
  - Persistence controls must match current config evidence: RDB snapshots and AOF are enabled.
- **Allowed**:
  - Metadata-only compose validation with `docker compose ... config`.
  - Read-only status, cluster-info, and exporter metric checks that do not print secret values.
  - Approved node/config changes when guide, policy, runbook, infra README, and task evidence are updated together.
- **Disallowed**:
  - Recording secret values, generated passwords, tokens, or certificate material in documentation or task evidence.
  - Referencing old service names or a single `valkey-cluster` container as a command target.
  - Claiming `maxmemory-policy` or other runtime controls are enabled unless the current config declares them.
  - Deleting data volumes, forcing cluster recreation, or restoring RDB/AOF files without explicit owner approval and incident/task evidence.

## Exceptions

Exceptions require explicit owner or user approval and must record scope, affected services, commands, secret-safety considerations, validation output, and rollback/escalation state in related task or incident evidence.

## Verification

- Run `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml --profile data config` after changing compose-facing documentation.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` after policy, guide, runbook, README, or link updates.
- Run `python3 scripts/validation/check-document-links.py --mode alignment` when the change is part of implementation-vs-doc drift remediation.
- Search updated docs for stale service names, direct password variable examples, stale image tags, unsupported runtime controls, and single-container assumptions before committing.

## Review Cadence

Review on any change to Valkey compose services, image tags, ports, profiles, networks, secret refs, persistence config, init script behavior, exporter behavior, or linked operations documents. Otherwise review during the regular Stage 05 operations audit.

---

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0022`), [Runbook](runbook.md) (`RUN-0022`)

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0022`), [Runbook](runbook.md) (`RUN-0022`)

## Traceability

- Declared parent: [Data Tier (04-data) Architecture Description](../../../../02.architecture/descriptions/0004-data-architecture.md) (`AD-0004`)
- Subject peers: [Guide](guide.md) (`GDE-0022`), [Runbook](runbook.md) (`RUN-0022`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
- [Infrastructure service README](../../../../../infra/04-data/cache-and-kv/valkey-cluster/README.md)
