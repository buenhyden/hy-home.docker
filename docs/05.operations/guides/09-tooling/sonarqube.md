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

- **Infrastructure**: [SonarQube Service](../../../../infra/09-tooling/sonarqube/README.md)
- **Usage**: [SonarQube System Usage](./sonarqube.md)
- **Procedure**: [SonarQube Recovery Procedure](./sonarqube.md)

---

## Overview (KR)

이 문서는 `docs/05.operations/09-tooling/sonarqube.md` 주제의 운영 정책을 정의한다. 기존 운영 내용을 유지하면서 적용 범위, 통제, 검증 기준을 명시한다.

## Policy Scope

이 정책은 관련 서비스의 운영 기준, 변경 통제, 검증 방법을 다룬다.

## Applies To

- **Systems**: 관련 Docker Compose 서비스와 문서화된 운영 자산
- **Agents**: repo-local governance를 따르는 AI agents
- **Environments**: local, development, homelab operations

## Controls

- **Required**: 변경 전 관련 README, guide, runbook 확인
- **Allowed**: 문서와 검증 절차의 in-place 보강
- **Disallowed**: secret 값 노출, 승인 없는 runtime 변경, 정책과 절차의 중복 SSoT 생성

## Exceptions

- 정책 예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.

## Verification

- 관련 repository validation script와 문서 heading audit로 준수 여부를 확인한다.

## Review Cadence

- 서비스 구성 변경 시 검토
- 문서 템플릿 변경 시 검토
- 주요 운영 정책 변경 시 검토

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: agent runtime 변경은 이 문서에서 직접 수행하지 않고 governance 문서로 분리한다.
- **Eval / Guardrail Threshold**: 문서 변경 후 관련 validation을 통과해야 한다.
- **Log / Trace Retention**: 검증 evidence는 task 문서나 대화 요약에 남긴다.
- **Safety Incident Thresholds**: secret 노출 또는 승인 없는 runtime 변경 징후가 있으면 즉시 중단한다.

## Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Usage

> Migrated from `docs/05.operations/09-tooling/sonarqube.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:07-tooling:sonarqube] -->
### SonarQube System Usage

> Usage for performing code quality and security scans using SonarQube.

#### Overview

SonarQube is the platform's central hub for static application security testing (SAST) and code quality management. It provides a visual dashboard for identifying technical debt, vulnerabilities, and code smells across all projects.

#### Architecture Context

- **Endpoint**: `https://sonarqube.${DEFAULT_URL}`
- **Persistence**: External PostgreSQL (`mng-db`)
- **Indexing**: Integrated ElasticSearch
- **Authentication**: Keycloak SSO

#### How-to Procedures

##### 1. Access and Authentication

1. Navigate to `https://sonarqube.${DEFAULT_URL}`.
2. Click **Log in**.
3. Select **Keycloak** (if configured) or use your platform credentials.
4. Developers should automatically have "Execute Analysis" permissions for their designated projects.

##### 2. Creating a New Project

1. Click **Create Project** -> **Manually**.
2. Enter a **Project key** (e.g., `hy-home:my-service`).
3. Set the **Main branch name** (usually `main`).
4. Generate a **Project Token** for CI/CD integration.

##### 3. Running a Local Scan

Standard scan using the `sonar-scanner` CLI:

```bash
### Set environment variables
read -rsp "Sonar token: " SONAR_TOKEN; echo
export SONAR_TOKEN
export SONAR_HOST_URL="https://sonarqube.${DEFAULT_URL}"

### Execute scan
sonar-scanner \
  -Dsonar.projectKey=hy-home:my-service \
  -Dsonar.sources=. \
  -Dsonar.host.url=${SONAR_HOST_URL}

unset SONAR_TOKEN
```

#### Troubleshooting & Pitfalls

##### elasticsearch.max_map_count

**Symptom**: SonarQube fails to start or crashes during startup.

**Solution**: Ensure the host has `vm.max_map_count=262144`.

```bash
sysctl -w vm.max_map_count=262144
```

##### Memory Exhaustion

**Symptom**: "Quality Gate" background tasks failing with `OutOfMemoryError`.

**Solution**: Adjust `SONAR_SEARCH_JAVAOPTS` and `SONAR_WEB_JAVAOPTS` in `docker-compose.yml`.

#### Related References

- **Infrastructure**: [SonarQube Service](../../../../infra/09-tooling/sonarqube/README.md)
- **Operation**: [SonarQube Operations Policy](./sonarqube.md)
- **Procedure**: [SonarQube Recovery Procedure](./sonarqube.md)

---

#### Overview (KR)

이 문서는 `docs/05.operations/09-tooling/sonarqube.md` 주제의 사용 가이드다. 기존 본문을 기준으로 작업자가 필요한 배경, 절차, 주의사항을 빠르게 찾도록 보강한다.

#### Usage Type

`system-guide`

#### Target Audience

- Developer
- Operator
- AI Agent

#### Purpose

관련 인프라 서비스나 문서 영역을 이해하고 안전하게 변경 또는 운영할 수 있도록 돕는다.

#### Prerequisites

- Repository root README 확인
- 관련 `infra/` 서비스 README 확인
- 필요한 경우 대응 operation/runbook 문서 확인

#### Step-by-step Instructions

1. 관련 README와 기존 본문을 먼저 읽는다.
2. 실제 compose/config 경로와 문서 설명이 일치하는지 확인한다.
3. 변경이 필요하면 대응 템플릿과 상위 README 링크를 함께 갱신한다.
4. 관련 검증 스크립트 또는 문서 audit를 실행한다.

#### Common Pitfalls

- guide 문서에 운영 정책이나 incident timeline을 섞지 않는다.
- secret 값, token, 인증서 원문을 열람하거나 문서화하지 않는다.
- runtime 변경이 필요한 경우 문서 보강과 별도 작업으로 분리한다.

#### Related Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## Procedure

> Migrated from `docs/05.operations/09-tooling/sonarqube.md` during the 2026-05-10 operations taxonomy consolidation.

<!-- [ID:09-tooling:sonarqube] -->
### Procedure: SonarQube Service Recovery (P2)

> Procedures for recovering from SonarQube service failures and index corruption.

#### Symptoms

- Web UI returning 500 or 503 errors.
- Authentication failures (SonarQube uses its own user DB stored in Postgres).
- ElasticSearch initialization loops or "Search index is corrupted" in logs.
- Scan tasks (Background Tasks) stuck in "Pending".

#### Diagnostic Steps

##### 1. Check Service Status

```bash
cd ${DEFAULT_TOOLING_DIR}/sonarqube
docker compose ps
docker compose logs --tail=100 -f sonarqube
```

##### 2. Verify Database Connectivity

SonarQube depends on the shared `mng-db`. Check if the container can reach the DB.

```bash
docker exec -it sonarqube \
  psql -h ${POSTGRES_MNG_HOSTNAME} -U ${SONARQUBE_DB_USER} -d ${SONARQUBE_DBNAME}
```

#### Recovery Procedures

##### 1. Elasticsearch Index Reconstruction

If ES fails to start or search results are inconsistent, clear the data directory to trigger a full re-analysis.

```bash
### 1. Stop the service
docker compose stop sonarqube

### 2. Clear ES data (Requires root to delete ES lock files)
sudo rm -rf ${DEFAULT_TOOLING_DIR}/sonarqube/data/es7

### 3. Restart service
docker compose start sonarqube
```

> [!NOTE]
> This will trigger a full re-analysis on the next scan for all projects. This is normal and expected.

##### 2. JVM Memory Adjustment

If logs show `OutOfMemoryError`, increase the JVM heap in `docker-compose.yml`.

```yaml
### Update these values in docker-compose.yml
- SONAR_WEB_JAVAOPTS=-Xmx1024m -Xms1024m
- SONAR_SEARCH_JAVAOPTS=-Xmx1024m -Xms1024m
```

##### 3. Log Inspection

Monitor these files for specific error patterns:

- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/web.log`: Web server and API issues.
- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/ce.log`: Compute Engine (scan task) issues.
- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/es.log`: ElasticSearch internal issues.

#### Escalation Policy

- **P1**: Total UI outage affecting all PR merges -> Notify SRE Team.
- **P2**: Intermittent scan failures -> Investigate Compute Engine limits.

#### Related References

- **Infrastructure**: [SonarQube Service](../../../../infra/09-tooling/sonarqube/README.md)
- **Usage**: [SonarQube System Usage](./sonarqube.md)
- **Operation**: [SonarQube Operations Policy](./sonarqube.md)

---

#### Overview (KR)

이 런북은 `docs/05.operations/09-tooling/sonarqube.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

#### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

#### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

#### When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

#### Procedure or Checklist

##### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

##### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

#### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

#### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

#### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

#### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

#### Related Operational Documents

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/incidents/README.md](../../incidents/README.md)
