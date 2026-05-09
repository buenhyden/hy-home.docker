<!-- [ID:09-tooling:terrakube] -->
# Runbook: Terrakube Recovery (P2)

> Procedures for recovering the Terrakube platform from executor failures, sync drift, and database corruption.

## Symptoms

- UI shows jobs stuck in "Pending" or "Running" for hours.
- Login redirection loops between Terrakube and Keycloak.
- "Error: S3 Storage not reachable" in API logs.
- Workspace state is "Locked" permanently in the UI.

## Diagnostic Steps

### 1. Check API and Executor Health

Terrakube provides Spring Actuator endpoints for health checks.

```bash
curl -I https://terrakube-api.${DEFAULT_URL}/actuator/health
```

### 2. Verify Docker Socket Access

The executor requires a healthy Docker socket to spawn Terraform runs.

```bash
docker exec terrakube-executor docker info
```

## Recovery Procedures

### 1. Cleaning Up Hung Executors

If the UI shows a job as running but the host has no associated container:

1. Locate the `terrakube-executor` logs to find the orphan job ID.
2. Manually kill the subprocess if it exists on the host.
3. Restart the executor service to reset internal queue state:

   ```bash
   cd ${DEFAULT_TOOLING_DIR}/terrakube
   docker compose restart terrakube-executor
   ```

### 2. Resolving OIDC / DEX Auth Loops

If users cannot login despite valid Keycloak credentials:

1. Check the `terrakube-api` log for "Invalid Token" or "JWK extraction failure".
2. Ensure the `OAUTH2_PROXY_CLIENT_ID` and Secrets match between Keycloak and the `docker-compose.yml`.
3. Restart the API server to refresh the OIDC configuration.

### 3. Manual Workspace Unlock

If a workspace is stuck in a locked state and "Force Unlock" in the UI fails:

1. Connect to the `terrakube` database in PostgreSQL.
2. Update the workspace record status manually.

   ```sql
   UPDATE workspace SET locked = false WHERE name = '<workspace_name>';
   ```

> [!WARNING]
> Manual DB modifications are high-risk. Always back up the `terrakube` database before running raw SQL.

## Escalation Policy

- **P1**: Total loss of the `tfstate` bucket content in MinIO -> Follow Disaster Recovery Plan.
- **P2**: Intermittent executor failures or UI sync issues -> Follow manual restart and queue cleanup.

## Related References

- **Infrastructure**: [Terrakube Platform](../../../infra/09-tooling/terrakube/README.md)
- **Guide**: [Terrakube System Guide](../../07.guides/09-tooling/terrakube.md)
- **Operation**: [Terrakube Operations Policy](../../08.operations/09-tooling/terrakube.md)

---

## Overview (KR)

이 런북은 `docs/09.runbooks/09-tooling/terrakube.md` 주제의 실행 절차를 정의한다. 기존 절차를 유지하면서 검증, evidence, rollback 기준을 명확히 한다.

## Purpose

운영자가 관련 서비스나 문서 작업을 반복 가능하고 검증 가능한 방식으로 수행하도록 돕는다.

## Canonical References

- [../README.md](../README.md)
- [../../08.operations/README.md](../../08.operations/README.md)
- [../../07.guides/README.md](../../07.guides/README.md)

## When to Use

- 관련 서비스 점검, 재시작, 검증, 문서 보강이 필요할 때
- 운영 절차와 evidence capture가 필요한 변경을 수행할 때

## Procedure or Checklist

### Checklist

- [ ] 관련 operation policy를 확인한다.
- [ ] 현재 compose/config/docs 상태를 확인한다.
- [ ] 필요한 절차를 수행한다.
- [ ] 검증 결과와 evidence를 기록한다.

### Procedure

1. 관련 README와 operation 문서를 확인한다.
2. 작업 전 현재 상태를 기록한다.
3. 절차를 최소 변경으로 수행한다.
4. 검증 명령 또는 수동 확인을 실행한다.

## Verification Steps

- [ ] 관련 validation script를 실행한다.
- [ ] 문서 변경이면 template/heading audit를 확인한다.
- [ ] runtime 변경이 있었다면 compose validation을 확인한다.

## Observability and Evidence Sources

- **Signals**: command output, validation logs, service health status, documentation diff
- **Evidence to Capture**: 실행 명령, 결과 요약, 실패 시 원인과 조치

## Safe Rollback or Recovery Procedure

- [ ] 실패한 문서 변경은 직전 diff 단위로 되돌린다.
- [ ] runtime 변경이 필요한 경우 이 런북 범위를 벗어난 별도 승인 절차로 분리한다.

## Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Related Operational Documents

- [../README.md](../README.md)
- [../../08.operations/README.md](../../08.operations/README.md)
- [../../10.incidents/README.md](../../10.incidents/README.md)
