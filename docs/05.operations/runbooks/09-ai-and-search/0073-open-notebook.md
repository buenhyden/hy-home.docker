---
title: "Open Notebook Recovery Runbook"
version: "1.1.5"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
layer: "operations"
artifact_id: "RUN-0073"
parent_ids:
- "GDE-0073"
created: "2026-05-17"
---

# Open Notebook Recovery Runbook

## Purpose

### Trigger and Outcome

이 런북은 OPTIONAL Open Notebook(`open_notebook`, `surrealdb`, profile `notebook`)의 장애 진단, 백업·격리 복원, 업그레이드 절차를 다룬다. 데이터베이스와 앱 데이터, 암호화 키가 하나의 복구 세트다.

앱 또는 DB readiness 실패, 읽을 수 없는 provider key, 사라진 노트북 콘텐츠, API 노출 우려, 백업·복원, 승인된 업그레이드가 있을 때 사용한다.

### Scope

- [Guide](../../guides/09-ai-and-search/0073-open-notebook.md) (`GDE-0073`)
- [Policy](../../policies/09-ai-and-search/0073-open-notebook.md) (`POL-0073`)
- [Open Notebook Compose](../../../../infra/08-ai/open-notebook/docker-compose.yml)
- [SurrealDB Operations](../../guides/05-databases-and-storage/0080-surrealdb.md) (`GDE-0080`)

- [SurrealDB export](https://surrealdb.com/docs/reference/cli/surrealdb-cli/commands/export)
- [Open Notebook security](https://github.com/lfnovo/open-notebook/blob/main/docs/5-CONFIGURATION/security.md)

## Preconditions

### Authority and Access

책임자는 `@buenhyden`이다. 작업 전에 승인자와 작업 대상을 기록하고 승인된 모델/provider endpoint와 키만 구성한다. secret 값은 어떤 증거에도 기록하지 않는다.

승인자와 작업 대상은 Safety Checks의 `작업 선택과 복구 전제`에서 기록하고, 승인된 모델/provider endpoint와 키 구성은 Actions의 `승인된 사용과 일관된 복구 세트`에 있다. 책임자 `@buenhyden`은 Escalation에 있으며 secret 값은 어떤 증거에도 기록하지 않는다.

### Safety Checks

작업 전 점검은 아래 항목에 따른다.

#### 작업 선택과 복구 전제

변경 전에 정확한 서비스·데이터 경로·승인자·중단 영향을 기록하고 [공통 복구 전제](../10-platform-and-backup/0021-backup-and-restore.md)를
적용한다. 격리 대상, 복구본 식별자·무결성, 여유 공간, 비밀 보관, 작성자 정지와
승격 승인 중 하나라도 불명확하면 중단한다. config·secret 교체는
[공통 수명주기 정책](../../policies/01-common/0006-infrastructure-optimization-governance.md)의
단일 파일 bind 재생성과 비밀 비노출 확인을 따른다. 재시작은 데이터 복원이나 자격 증명
폐기 검증을 대신하지 않는다.

## Steps

### Actions

절차는 아래 항목에 따른다.

#### 진단

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

#### 모델 등록 계약의 격리 점검

`notebook-models.py`의 `plan`, `apply`, `verify`는 product UI/API 계약을
점검하기 위한 P03 로컬 도구다. 기본 점검은 읽기 전용 `plan` 또는 `verify`로
시작한다. 실제 운영 endpoint, 자격 증명, 저장된 모델을 이 명령의 입력으로
사용하지 않는다.

`scripts/operations/notebook-models.py`는 정책·receipt 처리를
`scripts/lib/ops/notebook_models.py`에, 제한된 API 전송을
`scripts/lib/ops/_notebook_models_http.py`에 위임한다. 이 런북은 세 경로의
런타임 사용 경계를 함께 관리한다.

승인된 격리 fixture에서만 다음과 같이 값 없는 placeholder를 실제 소유한 합성
대상으로 바꾼다. password file은 단일 link이고 mode `0600`인 보호 파일이어야
하며, 명령행과 결과에 비밀번호 값을 넣지 않는다.

```bash
python3 scripts/operations/notebook-models.py plan \
  --endpoint http://127.0.0.1:<owned-port> \
  --policy infra/08-ai/open-notebook/config/notebook-model-policy.json \
  --password-file <owned-0600-single-link-file> \
  --receipt <owned-output.json>

python3 scripts/operations/notebook-models.py verify \
  --endpoint http://127.0.0.1:<owned-port> \
  --policy infra/08-ai/open-notebook/config/notebook-model-policy.json \
  --password-file <owned-0600-single-link-file> \
  --receipt <owned-output.json>
```

`apply`는 위 인수에 `--owned-isolated`를 추가하고 receipt 없이는 거부한다.
이 flag와 Task 기록은 구조적 제한일 뿐 인증 수단이 아니다. controller는 쓰기
전에 신뢰할 수 있는 사용자 승인과 정확한 소유 대상 검증을 별도로 수행해야 한다.
endpoint는 명시 포트가 있는 `http://127.0.0.1:<owned-port>` literal만 허용되며,
password file을 읽기 전에 검증된다. 이 런북은 이 예시를 실제로 실행한 수용
증거가 아니다.

충돌·부분 적용·중단 또는 receipt 출력 실패가 발생하면 추가 `apply`를 중지하고
기존 등록을 읽기 전용으로 대조한다. 지원 API가 null default 복원을 보장한다고
가정하지 않는다. 복구는 같은 SurrealDB 데이터, `/app/data` SQLite 상태와
대응하는 encryption key를 함께 갖춘 승인된 격리 복구 절차로만 재개한다.

#### Backup and isolated restore

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

#### Upgrade

backup을 반복하고 release/migration/security note를 점검하고 복원된 copy에서
target image를 테스트하고 content와 credential decryption을 확인한다.
실패 시에는 target을 중지하고 이전 image와 두 data scope를 모두 복원한다.

#### 승인된 사용과 일관된 복구 세트

`docker compose --profile notebook config --quiet`로 검증하고, 두 서비스를 모두
확인한 다음 app보다 먼저 데이터베이스를 시작한다. 애플리케이션 비밀번호와
게이트웨이 통제를 함께 사용한다. 승인된 모델/provider endpoint와 키만 구성한다.
노트북 콘텐츠, 소스 문서, embedding, provider 키는 민감 정보이다. SurrealDB는
v2로 유지하고 v3로 업그레이드하지 않는다.

백업·격리 복원과 업그레이드는 위 `Backup and isolated restore`와 `Upgrade` 절차를 따른다. 여기서는
백업, 복원, provider 호출, 업그레이드를 실행하지 않았다.

### Stop Conditions

encryption key 누락·불일치, DB export 실패, 예기치 않은 API exposure, 민감한
content 유출, migration error, 알 수 없는 provider 활동이 있으면 중단한다.

## Validation

### Service Checks

`docker compose --profile notebook ps surrealdb open_notebook`로 두 서비스 상태를 확인한다. 노트북·소스·설정 개수, 합성 노트북 하나, 자격 증명 복호화 가능 여부(boolean)를 확인한다.

### Evidence

종료 코드·source 커밋·export/app-data checksum·개수·인증/복호화 판정·API 경계와
최종 상태를 기록한다. content나 secret 값은 절대 기록하지 않는다.

## Recovery

### Rollback

backup/restore와 upgrade rehearsal은 **계획되었으나 미실행** 상태이다.
encryption key 손실은 database restore만으로는 복구되지 않는다.

### Escalation

책임자는 `@buenhyden`이다. 위 Stop Conditions의 중단 조건과 영향받은 서비스·대상 소유자를 함께 기록하고, 추가 변경 없이 보고한다.
