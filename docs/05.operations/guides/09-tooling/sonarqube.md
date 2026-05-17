# SonarQube Usage Guide

<!-- [ID:07-tooling:sonarqube] -->
## Usage
>
> Usage for performing code quality and security scans using SonarQube.

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

### Overview (KR)

이 문서는 `docs/05.operations/09-tooling/sonarqube.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- AI Agent

### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/09-tooling/sonarqube.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/09-tooling/sonarqube.md)
- [Recovery runbook](../../runbooks/09-tooling/sonarqube.md)
- [Operations template](../../../99.templates/operation.template.md)
