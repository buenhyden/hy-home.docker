---
status: active
---
<!-- Target: docs/05.operations/guides/09-tooling/sonarqube.md -->

# SonarQube Usage Guide

<!-- [ID:09-tooling:sonarqube] -->

## Usage

### Overview

이 문서는 SonarQube를 사용해 코드 품질과 보안 분석을 수행하는 방법을 설명한다. 프로젝트 생성, 로컬 scan, quality gate 확인은 guide에서 다루고, 운영 통제와 복구 절차는 policy/runbook으로 분리한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Operators
- Developers
- Contributors
- AI Agents

### Purpose

- SonarQube Usage Guide의 운영 사용 맥락을 빠르게 파악한다.
- 반복 실행 절차와 장애 대응은 연결된 runbook으로 넘긴다.
- 통제 기준은 연결된 policy 문서와 분리해 유지한다.

### Prerequisites

- Repository checkout 접근 가능
- 관련 `docs/03.specs/` 또는 operations 문서 확인 가능
- 필요한 경우 Docker/Docker Compose 명령 실행 권한

### Step-by-step Instructions

1. 이 문서의 overview와 usage context를 확인한다.
2. 관련 service, configuration, 또는 documentation target을 식별한다.
3. `## Common Checks`의 검증 항목을 실행하거나 검토한다.
4. 반복 절차, 장애 대응, rollback, escalation이 필요하면 `## Runbook Handoff`의 runbook으로 이동한다.

### Common Pitfalls

- guide에 policy control이나 복구 절차를 직접 섞어 목적 프로파일을 흐리는 경우
- target-relative link를 템플릿 위치 기준으로 계산하는 경우
- 검증 명령 실행 결과 없이 운영 가능 상태를 단정하는 경우

### Overview

SonarQube is the platform's central hub for static application security testing (SAST) and code quality management. It provides a visual dashboard for identifying technical debt, vulnerabilities, and code smells across all projects.

### Architecture Context

- **Endpoint**: `https://sonarqube.${DEFAULT_URL}`
- **Persistence**: External PostgreSQL (`mng-db`)
- **Indexing**: Integrated ElasticSearch
- **Authentication**: Keycloak SSO

### How-to Procedures

#### 1. Access and Authentication

1. Navigate to `https://sonarqube.${DEFAULT_URL}`.
2. Click **Log in**.
3. Select **Keycloak** (if configured) or use your platform credentials.
4. Developers should automatically have "Execute Analysis" permissions for their designated projects.

#### 2. Creating a New Project

1. Click **Create Project** -> **Manually**.
2. Enter a **Project key** (e.g., `hy-home:my-service`).
3. Set the **Main branch name** (usually `main`).
4. Generate a **Project Token** for CI/CD integration.

#### 3. Running a Local Scan

Standard scan using the `sonar-scanner` CLI:

```bash

## Set environment variables
read -rsp "Sonar token: " SONAR_TOKEN; echo
export SONAR_TOKEN
export SONAR_HOST_URL="https://sonarqube.${DEFAULT_URL}"

## Execute scan
sonar-scanner \
  -Dsonar.projectKey=hy-home:my-service \
  -Dsonar.sources=. \
  -Dsonar.host.url=${SONAR_HOST_URL}

unset SONAR_TOKEN
```

### Troubleshooting & Pitfalls

#### elasticsearch.max_map_count

**Symptom**: SonarQube fails to start or crashes during startup.

**Solution**: Ensure the host has `vm.max_map_count=262144`.

```bash
sysctl -w vm.max_map_count=262144
```

#### Memory Exhaustion

**Symptom**: "Quality Gate" background tasks failing with `OutOfMemoryError`.

**Solution**: Adjust `SONAR_SEARCH_JAVAOPTS` and `SONAR_WEB_JAVAOPTS` in `docker-compose.yml`.

## Common Checks

- `bash scripts/hardening/check-all-hardening.sh 09-tooling`
- Runtime approval 후 service가 실행 중이면 `docker compose exec sonarqube curl -f http://localhost:${SONARQUBE_PORT:-9000}/api/system/status`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/sonarqube.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/sonarqube.md)
- [Recovery runbook](../../runbooks/09-tooling/sonarqube.md)
