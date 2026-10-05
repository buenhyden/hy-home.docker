---
title: "Open Notebook Recovery Runbook"
version: "1.1.1"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0073"
parent_ids:
- "GDE-0073"
created: "2026-05-17"
---

# Open Notebook Recovery Runbook

## Overview

## Trigger and Preconditions

### Overview

### Trigger and Preconditions

### When to Use

app/DB readiness failure, 읽을 수 없는 provider key, missing notebook content,
API exposure concern, backup/restore, 또는 승인된 upgrade에 사용한다.

### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../policies/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Procedure

### Procedure

1. 루트에서 validate하고 점검한다.

   ```bash
   docker compose --profile notebook config --quiet
   docker compose --profile notebook ps surrealdb open_notebook
   docker compose --profile notebook logs --tail=200 surrealdb open_notebook
   ```

2. 앱 비밀번호·암호화 키·DB 자격 증명·데이터베이스·app-data·gateway/UI·API·
   provider 증상을 구분한다. key 값이나 content는 절대 출력하지 않는다.
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

### 승인된 사용과 일관된 복구 세트

`docker compose --profile notebook config --quiet`로 검증하고, 두 서비스를 모두
확인한 다음 app보다 먼저 데이터베이스를 시작한다. 애플리케이션 비밀번호와
게이트웨이 통제를 함께 사용한다. 승인된 모델/provider endpoint와 키만 구성한다.
노트북 콘텐츠, 소스 문서, embedding, provider 키는 민감 정보이다. SurrealDB는
v2로 유지하고 v3로 업그레이드하지 않는다.

백업할 때는 app write를 멈추고 `surreal export`로 구성된 SurrealDB
namespace/database를 export하고 `/app/data`를 복사하고 암호화 키와 DB
credential을 보호된 방식으로 보관한다. provider/network egress를 비활성화한
격리된 SurrealDB로 복원하고 export를 import하고 app data를 마운트하고 같은
암호화 키를 비공개로 제공한 다음, 개수와 합성 노트북 하나를 검증한다. 업그레이드
전에는 floating-tag/release 변경 사항을 검토하고 이 복원을 테스트한다. 여기서는
백업, 복원, provider 호출, 업그레이드를 실행하지 않았다.

## Verification

### Evidence

종료 코드·source 커밋·export/app-data checksum·개수·인증/복호화 판정·API 경계와
최종 상태를 기록한다. content나 secret 값은 절대 기록하지 않는다.

## Rollback and Escalation

### Rollback or Recovery

backup/restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다.
encryption key 손실은 database restore만으로는 복구되지 않는다.

### Escalation

책임자는 `@buenhyden`이다. 아래 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.

encryption key 누락·불일치, DB export 실패, 예기치 않은 API exposure, 민감한
content 유출, migration error, 알 수 없는 provider 활동이 있으면 중단한다.

### Traceability

- [Guide](../guides/0073-open-notebook.md) (`GDE-0073`)
- [Policy](../policies/0073-open-notebook.md) (`POL-0073`)
- [Open Notebook Compose](../../../infra/08-ai/open-notebook/docker-compose.yml)
- [SurrealDB Operations](../guides/0080-surrealdb.md) (`GDE-0080`)

## Related Documents

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [Open Notebook security](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)
