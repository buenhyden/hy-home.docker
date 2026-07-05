---
status: active
---
<!-- Target: docs/05.operations/runbooks/11-laboratory/open-notebook.md -->

# Open Notebook Recovery Runbook

## Open Notebook Recovery Procedure

> Scope: root-active Open Notebook and SurrealDB service evidence, route hardening, secret-file boundary, and non-destructive diagnosis.

### Overview

이 런북은 `open-notebook` UI 접속 실패, SurrealDB 의존성 장애, secret-file 주입 오류, 데이터 볼륨 경계 문제를 진단하고 복구 범위를 판단하는 절차를 정의한다.

### Purpose

Open Notebook 관리/실험 작업 환경의 가용성을 확인하되, secret 값 출력, 데이터 볼륨 삭제, credential storage 재초기화 같은 파괴적 조치를 승인 없는 복구 절차로 수행하지 않는다.

### Canonical References

- **Spec**: [Laboratory spec](../../../03.specs/012-laboratory/spec.md)
- **Policy**: [Open Notebook policy](../../policies/11-laboratory/open-notebook.md)
- **Guide**: [Open Notebook guide](../../guides/11-laboratory/open-notebook.md)

## When to Use

- `https://open-notebook.${DEFAULT_URL}` 접속이 실패할 때.
- `open_notebook` 또는 `surrealdb` 컨테이너가 unhealthy/restarting 상태일 때.
- login, credential storage, encryption key, SurrealDB health 오류가 의심될 때.
- hardening check에서 Open Notebook route, secret-file, dependency, healthcheck drift가 감지될 때.

## Procedure

### Checklist

- [ ] root `admin` profile에서 `open_notebook`과 `surrealdb`가 포함되는지 기록한다.
- [ ] `open_notebook_password`, `open_notebook_encryption_key`, `surreal_db_password` secret 파일 존재 여부만 확인한다.
- [ ] `SURREALDB_USERNAME`, `SURREALDB_NAMESPACE`, `SURREALDB_DATABASE` key 이름과 값 존재 여부를 확인하되 secret 값은 출력하지 않는다.
- [ ] host-bound API/DB ports 노출이 target environment에서 승인된 상태인지 기록한다.

### Steps

1. root-active admin profile을 확인한다: `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`.
2. tier hardening을 확인한다: `bash scripts/hardening/check-all-hardening.sh 11-laboratory`.
3. 실행 중이면 상태와 로그를 기록한다: `docker ps --format '{{.Names}}\t{{.Status}}'`, `docker logs --tail 100 open_notebook`, `docker logs --tail 100 surrealdb`.
4. route drift가 있으면 Open Notebook route chain을 `gateway-standard-chain@file,open-notebook-admin-ip@docker,large-body@file,sso-errors@file,sso-auth@file`로 복구한다.
5. dependency drift가 있으면 `depends_on.surrealdb.condition: service_healthy`와 `surrealdb` healthcheck를 복구한다.
6. secret-file drift가 있으면 `OPEN_NOTEBOOK_PASSWORD_FILE`과 `OPEN_NOTEBOOK_ENCRYPTION_KEY_FILE` 경계를 복구한다.
7. credential storage, encryption key rotation, volume reset, host-port exposure changes가 필요하면 중단하고 `## Escalation`으로 이동한다.

### Verification Steps

- `HYHOME_COMPOSE_PROFILES=admin bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 11-laboratory`
- 활성화된 runtime에서 UI login과 notebook save evidence를 secret 값 없이 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail 100 open_notebook`, `docker logs --tail 100 surrealdb`
- **Static config**: [Open Notebook compose](../../../../infra/11-laboratory/open-notebook/docker-compose.yml)
- **Runtime signals**: container status, SurrealDB health, Traefik route response

### Safe Rollback or Recovery Procedure

N/A — no verified image rollback, encryption-key rollback, credential storage reset, or data-volume restore procedure is documented for autonomous execution.

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: stop if secret values, notebook private content, or credential storage values may be exposed.
- **Eval Re-run**: hardening, root profile validation, doc traceability.

## Evidence

- Record command names, validation results, service states, redacted log snippets, and whether escalation was required.
- Do not record secret values, notebook private content, encryption keys, or credential storage contents.

## Rollback or Recovery

If encryption key changes, credential storage reset, data volume restore/delete, host firewall changes, or direct port exposure changes are required, stop and escalate.

## Escalation

Escalate to the owning operator when verification fails, secret exposure risk appears, host-bound API/DB exposure needs change, destructive data actions are required, or Open Notebook content governance is implicated.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/11-laboratory/open-notebook.md)
- [Operations policy](../../policies/11-laboratory/open-notebook.md)
