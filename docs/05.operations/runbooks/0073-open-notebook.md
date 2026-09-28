---
title: "Open Notebook Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "RUN-0073"
parent_ids:
- "GDE-0073"
created: "2026-05-17"
---

# Open Notebook Recovery Runbook

## When to Use

app/DB readiness failure, 읽을 수 없는 provider key, missing notebook content,
API exposure concern, backup/restore, 또는 승인된 upgrade에 사용한다.

## Procedure

1. 루트에서 validate하고 점검한다.

   ```bash
   docker compose --profile notebook config --quiet
   docker compose --profile notebook ps surrealdb open_notebook
   docker compose --profile notebook logs --tail=200 surrealdb open_notebook
   ```

2. app password, encryption key, DB credential, database, app-data, gateway/UI,
   API, provider 증상을 구분한다. key 값이나 content는 절대 출력하지 않는다.
3. provider key를 읽을 수 없게 되었으면 write를 중지하고 encryption-key secret
   identity/custody를 확인한다. replacement key로 key를 덮어쓰거나 다시 저장하지
   않는다.
4. database를 먼저 재시작하고 readiness를 확인한 뒤 app만 재시작한다. content와
   credential 점검이 통과할 때까지 provider/model egress를 비활성화 상태로 유지한다.

### Backup and isolated restore

1. consistent logical export를 위해 SurrealDB를 사용 가능한 상태로 유지하면서 app
   write를 차단하거나 `open_notebook`을 중지한다. 설정된 namespace/database를
   command line에 password를 넣지 않고 protected SurrealQL file로 export한다.
2. 남은 writer를 중지하고, `/app/data`를 복사하고, export/app-data checksum,
   source commit, namespace/database, protected key/credential receipt를
   기록한다.
3. isolated SurrealDB로 import한다. 복사된 app-data 디렉터리를 mount하고, 동일한
   encryption key를 private하게 제공한다. 외부 provider/network 호출을
   비활성화한다.
4. notebook/source/settings count와 synthetic notebook 하나를 확인하고 credential
   decryptability는 boolean으로 확인한다. 검토 후에만 promote한다.

### Upgrade

backup을 반복하고 release/migration/security note를 점검하고 복원된 copy에서
target image를 테스트하고 content와 credential decryption을 확인한다.
실패 시에는 target을 중지하고 이전 image와 두 data scope를 모두 복원한다.

## Evidence

exit, source commit, export/app-data checksum, count, auth/decryption boolean,
API boundary, 최종 상태를 기록한다. content나 secret 값은 절대 기록하지 않는다.

## Rollback or Recovery

backup/restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다.
encryption key 손실은 database restore만으로는 복구되지 않는다.

## Escalation

encryption key 누락·불일치, DB export 실패, 예기치 않은 API exposure, 민감한
content 유출, migration error, 알 수 없는 provider 활동이 있으면 중단한다.

## Traceability

- [Guide](../guides/0073-open-notebook.md) (`GDE-0073`)
- [Policy](../policies/0073-open-notebook.md) (`POL-0073`)
- [Open Notebook Compose](../../../infra/11-laboratory/open-notebook/docker-compose.yml)
- [SurrealDB Operations](../guides/0080-surrealdb.md) (`GDE-0080`)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [Open Notebook security](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
