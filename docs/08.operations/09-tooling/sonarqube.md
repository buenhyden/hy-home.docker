<!-- [ID:08-tooling:sonarqube] -->
# SonarQube Operations Policy

> Governance for code quality, security standards, and SonarQube lifecycle.

## Overview

This policy defines the operational standards for the SonarQube service. It ensures that code quality scanning is consistent across all platform components and that the infrastructure remains healthy and high-performing.

## Scope

- **Governance**: Quality gate enforcement, branch analysis rules.
- **Maintenance**: Plug-in life-cycle, database optimization.
- **Reporting**: Security hotspots and vulnerability tracking.

## Operational Standards

### 1. Quality Gate Enforcement

- All platform-level projects **MUST** pass the "Sonar way" Quality Gate before merging into `main`.
- Critical issues and high-severity security vulnerabilities **MUST** be remediated or officially "Acknowledged" with a technical rationale.
- Test coverage requirements: Minimum 80% for new code (recommended).

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

## Related References

- **Infrastructure**: [SonarQube Service](../../../infra/09-tooling/sonarqube/README.md)
- **Guide**: [SonarQube System Guide](../../07.guides/09-tooling/sonarqube.md)
- **Runbook**: [SonarQube Recovery Runbook](../../09.runbooks/09-tooling/sonarqube.md)
