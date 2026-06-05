---
status: active
---
<!-- Target: docs/05.operations/policies/09-tooling/sonarqube.md -->

# SonarQube Operations Policy

<!-- [ID:09-tooling:sonarqube] -->
> Governance for code quality, security standards, and SonarQube lifecycle.

## Overview

This policy defines the operational standards for the SonarQube service. It ensures that code quality scanning is consistent across all platform components and that the infrastructure remains healthy and high-performing.

## Policy Scope

- **Governance**: Quality gate enforcement, branch analysis rules.
- **Maintenance**: Plug-in life-cycle, database optimization.
- **Reporting**: Security hotspots and vulnerability tracking.

## Operational Standards

### 1. Quality Gate Enforcement

- All platform-level projects **MUST** pass the "Sonar way" Quality Gate before merging into `main`.
- Critical issues and high-severity security vulnerabilities **MUST** be remediated or officially "Acknowledged" with a technical rationale.
- Test coverage requirements: Minimum 90% for new code (mandatory).

### 2. Routine Maintenance

| Frequency | Task | Owner |
| :--- | :--- | :--- |
| **Weekly** | Log rotation check (`ce.log`, `web.log`). | Operators |
| **Monthly** | Database index maintenance (Postgres). | DBAs |
| **Quarterly** | Plug-in compatibility audit (SonarLint). | Platform Team |

### 3. Backup and Persistence

- **Data**: All persistent configuration is stored in the `mng-db` cluster.
- **Indexing**: ElasticSearch indexes are located at `/opt/sonarqube/data/es7`.
- **Note**: Only the SQL database needs regular backups. ElasticSearch indexes can be rebuilt from the DB.

## Monitoring Strategy

- **Health Check**: `http://sonarqube:9000/api/system/health`.
- **Key Metrics**:
  - `sonar.web-jvm.max_heap_size`
  - `sonar.search-jvm.max_heap_size`
  - Number of pending Background Tasks.

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- Review this policy with its matching guide, runbook, and linked infra/config documents before material operations changes.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy or linked operations document updates.
- Run `bash scripts/validation/check-doc-traceability.sh` when execution or operations links change.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/sonarqube.md)
- [Recovery runbook](../../runbooks/09-tooling/sonarqube.md)
