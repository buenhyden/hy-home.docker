---
status: active
---
<!-- Target: docs/05.operations/runbooks/09-tooling/sonarqube.md -->

# SonarQube Runbook

<!-- [ID:09-tooling:sonarqube] -->

## Overview (KR)

이 런북은 `docs/05.operations/runbooks/09-tooling/sonarqube.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

## Procedure: SonarQube Service Recovery (P2)

> Procedures for recovering from SonarQube service failures and index corruption.

### Symptoms

- Web UI returning 500 or 503 errors.
- Authentication failures (SonarQube uses its own user DB stored in Postgres).
- ElasticSearch initialization loops or "Search index is corrupted" in logs.
- Scan tasks (Background Tasks) stuck in "Pending".

### Diagnostic Steps

#### 1. Check Service Status

```bash
cd ${DEFAULT_TOOLING_DIR}/sonarqube
docker compose ps
docker compose logs --tail=100 -f sonarqube
```

#### 2. Verify Database Connectivity

SonarQube depends on the shared `mng-db`. Check if the container can reach the DB.

```bash
docker exec -it sonarqube \
  psql -h ${POSTGRES_MNG_HOSTNAME} -U ${SONARQUBE_DB_USER} -d ${SONARQUBE_DBNAME}
```

### Recovery Procedures

#### 1. Elasticsearch Index Reconstruction

If ES fails to start or search results are inconsistent, clear the data directory to trigger a full re-analysis.

```bash
## 1. Stop the service
docker compose stop sonarqube

## 2. Clear ES data (Requires root to delete ES lock files)
sudo rm -rf ${DEFAULT_TOOLING_DIR}/sonarqube/data/es7

## 3. Restart service
docker compose start sonarqube
```

> [!NOTE]
> This will trigger a full re-analysis on the next scan for all projects. This is normal and expected.

### 2. JVM Memory Adjustment

If logs show `OutOfMemoryError`, increase the JVM heap in `docker-compose.yml`.

```yaml
## Update these values in docker-compose.yml
- SONAR_WEB_JAVAOPTS=-Xmx1024m -Xms1024m
- SONAR_SEARCH_JAVAOPTS=-Xmx1024m -Xms1024m
```

### 3. Log Inspection

Monitor these files for specific error patterns:

- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/web.log`: Web server and API issues.
- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/ce.log`: Compute Engine (scan task) issues.
- `${DEFAULT_TOOLING_DIR}/sonarqube/logs/es.log`: ElasticSearch internal issues.

### Escalation Policy

- **P1**: Total UI outage affecting all PR merges -> Notify SRE Team.
- **P2**: Intermittent scan failures -> Investigate Compute Engine limits.

### Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

### Canonical References

- [../README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)
- [../../05.operations/README.md](../../README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Steps

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

### Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

### Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

### Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- Capture command output, timestamps, and operator/agent actions for any execution of this runbook.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/09-tooling/sonarqube.md)
- [Operations policy](../../policies/09-tooling/sonarqube.md)
- [Operations template](../../../99.templates/operation.template.md)

## Rollback or Recovery

- Use only recovery or rollback steps already documented in this runbook, including any `Safe Rollback or Recovery Procedure` subsection above.
- N/A for additional verified recovery steps: this file does not validate a broader service-specific rollback beyond the documented procedure.
- If the observed failure does not match the documented steps, stop changes, preserve evidence, and escalate under `## Escalation`.

## Escalation

- Stop and escalate to the owning operator with captured evidence when the documented procedure does not match the observed failure.
