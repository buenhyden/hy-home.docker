---
title: Syncthing Operations Policy
version: 1.0.0
type: operation/policy
layer: operations
status: active
owner: "@buenhyden"
artifact_id: POL-0067
parent_ids:
  - AD-0009
created: 2026-05-17
updated: 2026-08-11
---
<!-- Target: docs/05.operations/catalog/09-tooling/0067-syncthing/policy.md -->

# Syncthing Operations Policy

<!-- [ID:09-tooling:syncthing] -->
> Governance for P2P data synchronization and integrity.

## Overview

This policy defines the operational standards for the Syncthing service. It ensures that decentralized data synchronization is reliable, secure, and performs optimally across all paired devices.

## Policy Scope

- **Governance**: Data sync patterns, conflict resolution rules.
- **Maintenance**: Database health, version upgrades.
- **Security**: Device pairing approval, encrypted transfer enforcement.

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

### Operational Standards

#### 1. Data Integrity and Conflicts

- **Conflict Handling**: If a sync conflict occurs, Syncthing generates a `.sync-conflict-` file. Operators/Users must manually resolve these to ensure data consistency.
- **Ignore Patterns**: Use `.stignore` files to prevent synchronization of temporary or large log files that do not require P2P distribution.
- **Folder Type**: Use "Send Only" for master nodes (e.g., a central backup server) and "Receive Only" for immutable mirrors where appropriate.

#### 2. Routine Maintenance

| Frequency | Task | Owner |
| :--- | :--- | :--- |
| **Weekly** | Check for "Out of Sync" alerts in GUI. | Operators |
| **Monthly** | Database consistency check (`-verify-db`). | Operators |
| **Quarterly** | Device pairing audit (remove stale devices). | Security |

#### 3. Resource Optimization

- **CPU Usage**: Enable "Low Priority" for the scanning process on low-resource nodes.
- **Memory**: Monitor the `syncthing` process; large folder structures may require higher JVM/RAM allocation via `stateful-med` optimizations.

### Monitoring Strategy

- **Health Check**: REST API `/rest/noauth/health` returns `OK`.
- **Key Metrics**:
  - `folder_state` (Idle, Syncing, Error).
  - `device_count` (Online vs Total).
  - `throughput` (Inbound/Outbound).


## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- Review this policy with its matching guide, runbook, and linked infra/config documents before material operations changes.
- Run `python3 scripts/validation/run-ci-gate.py --profile changed` after policy or linked operations document updates.
- Run `python3 scripts/validation/check-document-links.py --mode traceability` when execution or operations links change.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Traceability

- Declared parent: [Tooling Tier Architecture Description](../../../../02.architecture/descriptions/0009-tooling-architecture.md) (`AD-0009`)
- Subject peers: [Guide](guide.md) (`GDE-0067`), [Runbook](runbook.md) (`RUN-0067`)

## Related Documents

- [Operations index](../../../README.md)
- [Usage guide](guide.md)
- [Recovery runbook](runbook.md)
