---
status: active
---

# Syncthing Operations Policy

<!-- [ID:08-tooling:syncthing] -->
# Syncthing Operations Policy

> Governance for P2P data synchronization and integrity.

## Overview

This policy defines the operational standards for the Syncthing service. It ensures that decentralized data synchronization is reliable, secure, and performs optimally across all paired devices.

## Scope

- **Governance**: Data sync patterns, conflict resolution rules.
- **Maintenance**: Database health, version upgrades.
- **Security**: Device pairing approval, encrypted transfer enforcement.

## Operational Standards

### 1. Data Integrity and Conflicts

- **Conflict Handling**: If a sync conflict occurs, Syncthing generates a `.sync-conflict-` file. Operators/Users must manually resolve these to ensure data consistency.
- **Ignore Patterns**: Use `.stignore` files to prevent synchronization of temporary or large log files that do not require P2P distribution.
- **Folder Type**: Use "Send Only" for master nodes (e.g., a central backup server) and "Receive Only" for immutable mirrors where appropriate.

### 2. Routine Maintenance

| Frequency | Task | Owner |
| :--- | :--- | :--- |
| **Weekly** | Check for "Out of Sync" alerts in GUI. | Operators |
| **Monthly** | Database consistency check (`-verify-db`). | Operators |
| **Quarterly** | Device pairing audit (remove stale devices). | Security |

### 3. Resource Optimization

- **CPU Usage**: Enable "Low Priority" for the scanning process on low-resource nodes.
- **Memory**: Monitor the `syncthing` process; large folder structures may require higher JVM/RAM allocation via `stateful-med` optimizations.

## Monitoring Strategy

- **Health Check**: REST API `/rest/noauth/health` returns `OK`.
- **Key Metrics**:
  - `folder_state` (Idle, Syncing, Error).
  - `device_count` (Online vs Total).
  - `throughput` (Inbound/Outbound).

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/syncthing.md)
- [Recovery runbook](../../runbooks/09-tooling/syncthing.md)
- [Operations template](../../../99.templates/operation.template.md)
