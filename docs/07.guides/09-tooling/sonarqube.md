<!-- [ID:07-tooling:sonarqube] -->
# SonarQube System Guide

> Guide for performing code quality and security scans using SonarQube.

## Overview

SonarQube is the platform's central hub for static application security testing (SAST) and code quality management. It provides a visual dashboard for identifying technical debt, vulnerabilities, and code smells across all projects.

## Architecture Context

- **Endpoint**: `https://sonarqube.${DEFAULT_URL}`
- **Persistence**: External PostgreSQL (`mng-db`)
- **Indexing**: Integrated ElasticSearch
- **Authentication**: Keycloak SSO

## How-to Procedures

### 1. Access and Authentication

1. Navigate to `https://sonarqube.${DEFAULT_URL}`.
2. Click **Log in**.
3. Select **Keycloak** (if configured) or use your platform credentials.
4. Developers should automatically have "Execute Analysis" permissions for their designated projects.

### 2. Creating a New Project

1. Click **Create Project** -> **Manually**.
2. Enter a **Project key** (e.g., `hy-home:my-service`).
3. Set the **Main branch name** (usually `main`).
4. Generate a **Project Token** for CI/CD integration.

### 3. Running a Local Scan

Standard scan using the `sonar-scanner` CLI:

```bash
# Set environment variables
export SONAR_TOKEN="your_project_token"
export SONAR_HOST_URL="https://sonarqube.${DEFAULT_URL}"

# Execute scan
sonar-scanner \
  -Dsonar.projectKey=hy-home:my-service \
  -Dsonar.sources=. \
  -Dsonar.host.url=${SONAR_HOST_URL} \
  -Dsonar.login=${SONAR_TOKEN}
```

## Troubleshooting & Pitfalls

### elasticsearch.max_map_count

**Symptom**: SonarQube fails to start or crashes during startup.

**Solution**: Ensure the host has `vm.max_map_count=262144`.

```bash
sysctl -w vm.max_map_count=262144
```

### Memory Exhaustion

**Symptom**: "Quality Gate" background tasks failing with `OutOfMemoryError`.

**Solution**: Adjust `SONAR_SEARCH_JAVAOPTS` and `SONAR_WEB_JAVAOPTS` in `docker-compose.yml`.

## Related References

- **Infrastructure**: [SonarQube Service](../../../infra/09-tooling/sonarqube/README.md)
- **Operation**: [SonarQube Operations Policy](../../08.operations/09-tooling/sonarqube.md)
- **Runbook**: [SonarQube Recovery Runbook](../../09.runbooks/09-tooling/sonarqube.md)
