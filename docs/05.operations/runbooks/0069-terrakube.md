---
title: "Terrakube Recovery Runbook"
version: "1.1.2"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0069"
parent_ids:
- "GDE-0069"
created: "2026-05-17"
---

# Terrakube Recovery Runbook

## When to Use

API/UI/executor failure, stuck run, OIDC failure, missing state/output, 또는
승인된 backup/restore/upgrade에 사용한다. 저장소 루트에서 작업한다.

## Procedure

1. 새 Terrakube run을 동결한다. workspace/run ID, VCS ref, state key, component
   status, apply 진행 여부를 기록한다. remote effect와 recovery owner를 파악하기
   전에는 active apply를 중지하지 않는다.
2. bounded state를 validate하고 점검한다.

   ```bash
   docker compose --profile iac config --quiet
   docker compose --profile iac ps terrakube-api terrakube-ui terrakube-executor
   docker compose --profile iac logs --tail=200 terrakube-api terrakube-ui terrakube-executor
   ```

3. 재시작 전에 분류한다.
   - UI만: gateway와 OIDC redirect/claim을 점검한다.
   - API DB error: `mng-pg`를 점검한다. migration을 반복적으로 재시도하지 않는다.
   - missing state/output: state를 로그로 다운로드하지 않고 SeaweedFS bucket/key와
     DB reference를 점검한다.
   - stuck execution: Valkey coordination과 executor/Docker access를 점검하고,
     취소나 replay 전에 remote provider action을 확인한다.
4. dependency와 active-run check 후 실패한 component만 재시작한다. job이나 apply를
   replay하려면 별도 authorization이 필요하다.

### Coordinated backup and isolated restore

1. scheduling을 차단하고, active run을 대기하거나 안전하게 해결한 뒤, Terrakube
   writer가 남지 않도록 API/UI와 executor를 중지한다.
2. `tfstate`에 대해서는 PostgreSQL owner의 online logical/physical backup 절차와
   daily backup(RUN-0024)에 포함된 SeaweedFS set을 사용한다. DB backup ID, object
   snapshot/version inventory, source commit, Keycloak/client configuration을
   연결하는 recovery-point receipt 하나를 기록한다. secret/state 내용은 캡처하지 않는다.
3. 두 store를 모두 isolated target으로 복원한다. replacement secret을 사용하고
   provider, VCS webhook, executor egress를 비활성화한다.
4. isolated store에 대해서만 복원된 component set을 시작한다. organization/
   workspace/run count, 참조된 state/output key, OIDC role mapping, non-applying
   plan을 확인한다. 복원된 executor를 live account로 향하게 하지 않는다.
5. 검토 후에만 promote한다. 그렇지 않으면 isolated copy를 폐기하고 source를 그대로
   둔다.

### Upgrade

coordinated backup을 완료하고 모든 migration/release note를 검토하고 복원된
store에서 새 API/UI/executor를 테스트한 뒤, 호환되는 set을 upgrade한다. 실패
시에는 새 set을 중지하고 DB와 object를 이전 image로 함께 복원한다.

## Evidence

sanitized component health, run/workspace count, backup ID/checksum, state-key
count, release/source commit, non-applying plan 결과, 최종 상태를 기록한다.

## Rollback or Recovery

이 coordinated backup/restore와 upgrade 단계는 **계획되었으나 미실행** 상태이다.
component restart나 단일 store snapshot으로 recovery했다고 주장하지 않는다.

## Escalation

active/unknown apply, DB-object 불일치, Docker-socket 예기치 않은 access, auth
모호성, backup 불가, destructive migration이 있으면 중단한다.

## Traceability

- [Guide](../guides/0069-terrakube.md) (`GDE-0069`)
- [Policy](../policies/0069-terrakube.md) (`POL-0069`)
- [Terrakube Compose](../../../infra/09-tooling/terrakube/docker-compose.yml)

## Related Documents

- [Terrakube documentation](https://docs.terrakube.io/)
- [Operations index](../README.md)
