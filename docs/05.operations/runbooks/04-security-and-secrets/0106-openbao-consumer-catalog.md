---
title: "OpenBao Consumer Migration and Secret Catalog"
version: "0.4.3"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "operations"
artifact_id: "RUN-0106"
parent_ids:
- "POL-0085"
created: "2026-10-28"
next_review_at: "2027-05-13"
---

# OpenBao Consumer Migration and Secret Catalog

## Purpose

### Trigger and Outcome

이 런북은 P06 소비자 이관 runtime의 운영 경계와 P02 공개 secret catalog 점검을 다룬다. 실제 소비자 전환 절차는 [consumer-migration README](../../../../infra/03-security/openbao/consumer-migration/README.md)가 소유한다.

소비자를 OpenBao Agent 출력으로 옮기거나, secret catalog를 점검·렌더·생성 점검하거나, SMTP01의 COMM-003 중복 퇴역을 수행할 때 사용한다.

### Scope

- 공통 OpenBao 운영: [RUN-0085](0085-openbao.md)
- [Implementation](../../../../infra/03-security/openbao/docker-compose.yml)과 [version projection](../../../../infra/tech-stack.versions.json)이 런타임 고정 버전을 소유한다.
- [Guide](../../guides/04-security-and-secrets/0085-openbao.md), [Policy](../../policies/04-security-and-secrets/0085-openbao.md)
- 관장 architecture: [AD-0003](../../../02.architecture/descriptions/0003-security-architecture.md)

- [운영 인덱스](../../README.md)

## Preconditions

### Authority and Access

저장소 루트에서 작업하고, 실제 copy·전환·삭제·회전은 P06 Task의 별도 입력·검토·수용을 거친다.

#### P06 Consumer Migration Boundary

이 Runbook은 [copy runtime](../../../../scripts/lib/ops/openbao_consumer_migration.py)과
[HTTPS transport](../../../../scripts/lib/ops/_openbao_copy_transport.py)의 운영 실행 경계를 소유합니다.
두 모듈은 controller가 현재 trusted user 또는 native authorization origin을 확인하고
고정 P02·P01·P03·P04 입력에 결속한 뒤에만 실행하는 runtime primitive입니다.
직접 library를 호출했다는 사실은 실행 승인이 아닙니다. 공개
`scripts/operations/openbao-consumer-migration.py` CLI는 validate-only이며 production catalog
adapter·controller factory·runtime copy CLI는 아직 제공하지 않습니다. 실제 private/native copy,
consumer 렌더·pilot·authority 전환·복구·삭제·회전의 새 실행은 별도 입력·검토·수용
전까지 **NOT_RUN**입니다. 기존 [P06 Task](../../../03.specs/0204-service-integration-security-and-operations/tasks/tsk-0014-p06-openbao-consumer-migration.md)는
2026-10-27–28에 별도 owner 절차로 수행한 선택 소비자의 전환과 되돌리기를 기록합니다.
이 과거 수용은 일반 copy API의 실행이나 현재 운영 동등성 증거가 아닙니다. source/unit
통과로 어느 실행 경계도 완료 처리하지 않습니다.

### Safety Checks

#### P06 Read-only Structure and SMTP Checks

현재 작업에서 private 읽기를 허용하고, 합성 값 누출 시험과 독립 보안 검토를
먼저 통과한 경우에만 운영자가 저장소 루트에서 다음 명령을 실행한다. 두 명령은
사설 파일을 쓰거나 권한을 바꾸지 않는다. 일반 CI에는 실제 private 입력 대신
합성 fixture만 사용한다. 현재 작업 경계의 root는 mode 0775이므로 같은 그룹의
비협조 작성자를 descriptor 재확인만으로 완전히 배제하거나 원자적 snapshot을
보장하지 않는다. 신뢰된 작성자와 해당 입력의 쓰기 중단을 확인한 뒤 검사한다.

```bash
python3 scripts/operations/secret-structure.py --root "$PWD" check --read-private
python3 scripts/operations/secret-structure.py --root "$PWD" smtp-equality --read-private
```

구조 검사의 `MATCH`/exit 0은 값 이외 구조 일치, `DRIFT`/exit 1은 차이,
`BLOCKED`/exit 2는 누락·권한·링크·형식·동시 변경 등 안전 거부다. SMTP 검사의
`EQUAL`/exit 0과 `DIFFERENT`/exit 1은 두 파일의 실제 비교 결과다. 역사 사본이
없으면 `OLD_ABSENT`, `comparison_performed=false`, exit 2이며 정본 내용도 읽지
않는다. 이 관측은 값 동일성이나 이번 삭제 성공이 아니다.

값·값 해시·길이·원문과 private 오류 payload는 출력하거나 영수증에 보관하지
않는다. `DRIFT`, `DIFFERENT`, `OLD_ABSENT` 또는 `BLOCKED`이면 운영 전환이나
삭제를 진행하지 않는다. 현재 서버 자격·reader·backup·data owner를 확인하고 별도
권한과 복구 경계를 갖춘 다음 해당 소비자 소유자에게 인계한다. 소스 되돌리기는
도구 코드만 되돌리며 실제 credential의 서버 유효성 복원을 뜻하지 않는다.

## Steps

### Actions

#### SMTP 전환 확인과 중복 퇴역

Supabase LAB은 2026-11-06 owner 결정으로 제거되어 COMM-003 alias의 Auth 소비자는 남아 있지 않습니다(SPEC-0263 W8).

1. SMTP01의 root 단일 source, COMM-002/003 alias와 파일 소비
   증거를 확인합니다. 공용 username·host·account와 Alertmanager는 변경하지 않습니다.
2. 실제 정확한 호스트 checkout에서 old path의 source, 모든 container mount,
   정기 job, backup/restore 및 외부 소비를 확인해 owning Task에 기록합니다.
   비선택 profile이나 최근 무트래픽만으로 소비자 부재를 판단하지 않습니다.
3. 제한된 로컬 비교는 다음 check mode를 사용합니다. 값·hash·길이는 출력하지 않으며
   exit 0은 이미 퇴역, 1은 변경 대기, 2는 불안전/불일치입니다. 실제 비밀 접근은
   정확한 대상에 대한 현재 사용자 권한과 owning Task 기록이 있어야 합니다.

   ```bash
   bash scripts/operations/gen-secrets.sh --retire-supabase-smtp-check
   ```

4. 총괄이 선행 전환과 SMTP01의 폐기·복구 경계를 수용한 뒤에만 현재 호스트,
   Git SHA, 공개 Compose source hash, 동일 root identity, old mount 부재,
   job/backup/external 확인, canonical restore mapping과 아래 두 quiescence
   사실을 담은 값 없는 audit receipt로 적용합니다.
   receipt 자체는 권한을 발급하지 않습니다. 다음 명령은 현재 SMTP01에서 실행하지 않습니다.

   ```bash
   umask 077
   smtp_proof_dir="$(mktemp -d /tmp/smtp01.XXXXXXXX)" || exit 1
   install -m 600 "${operator_receipt:?}" "$smtp_proof_dir/smtp01-audit.json"
   bash scripts/operations/gen-secrets.sh --retire-supabase-smtp \
     --smtp-audit-proof "$smtp_proof_dir/smtp01-audit.json"
   ```

5. helper는 canonical 파일을 보존하고 COMM-003 private 값 행과 정확한 중복 파일만
   처리합니다. 동시 변경·불일치·불명확한 mount는 거부합니다. `.env`와 LAB은 읽거나
   수정하지 않습니다. SMTP01 helper가 exact COMM-003 행과 파일, 이미 비어 있는 old
   folder만 처리하며 다른 entry가 있으면 보존합니다. 재실행으로 idempotency와 활성 old
   source/path 참조 0을 확인합니다.

복구는 canonical 파일과 특정 소비자의 source 설정만 복원합니다.
기존 암호화 Restic host snapshot은 비밀 자료의 보관이지 old path의 live 소비자가
아닙니다. snapshot에서 옛 layout을 복원할 때 현재 canonical mapping을 다시 적용하며
평문 중복을 영구 유지하지 않습니다. 실제 backup/restore 검증은 별도 Task 증거이고,
source revert나 격리 SMTP 성공으로 HOME 복구를 PASS로 기록하지 않습니다. 전체 up/down,
volume 초기화와 일괄 credential 회전은 이 절차에 포함되지 않습니다.

#### SMTP01의 root·lock·증거 계약

receipt의 필수 필드는 `host`, `git_sha`, `source_sha256`,
`root_identity: {st_dev, st_ino}`, `old_mount_consumers: []`,
`job_backup_external_verified: true`, `canonical_restore_mapping_verified: true`,
`consumer_creation_quiesced: true`, `source_private_mutation_quiesced: true`, 정확한
`operation: retire-supabase-smtp`, `target: COMM-003`, 안전한 식별자인
`observation_id`와 `approval_record`, UTC `Z` 형식의 `observed_at`과 `expires_at`입니다.
`approval_record`는 설명용 기록 식별자이며 승인 진위나 실행 권한을 증명하지 않습니다.
receipt는 관찰 후 5분 이내여야 하고 30초를 넘는 미래 시각을 거부하며, 관찰부터 만료까지
최대 15분입니다. 세 번의 verifier 각각에서 만료까지 최소 5분이 남아야 합니다. 위 준비와
적용 명령, 현재 HOME 사실과 receipt 발급은 NOT_RUN입니다.

`source_sha256`은 값이나 private 환경이 아니라 tracked public source 파일의
상대경로→SHA-256 map이며 root Compose include graph의 public source digest를 묶습니다.
SMTP delivery, HOME activation 또는 credential rotation을 증명하지 않습니다.

proof는 repository root 밖의 절대 경로에 둡니다. 정확한 parent는 현재 실행 UID 소유의
0700 directory, 파일은 같은 UID 소유의 단일 regular file·단일 link·0600이어야 하며
32 KiB를 넘지 않습니다. helper는 symlink를 따르지 않고 descriptor로 전체 파일을 읽어
읽기 전후 identity를 다시 확인합니다. 중복·누락·추가 JSON key를 거부합니다. proof 적용
시점의 tracked worktree와 index도 receipt의 Git SHA에서 clean이어야 합니다. untracked
private 자료는 Git 검사 대상으로 확대하지 않습니다.

실제 운영 root는 `/home/hyunyoun/data/hy-home.docker`입니다. apply는 그 root의
device/inode를 확인하고 SMTP01은 `secrets/.smtp01-retirement.lock`에 exclusive
nonblocking lock을 사용합니다. lock은 nofollow·단일 regular file·0600이며
사용 후 지우지 않습니다. 다른 worktree의 같은 상대 경로는 동일 lock이 아닙니다.
읽기 전용 check는 lock 파일을 생성하거나 변경하지 않습니다. 퇴역 CLI는 lock을
스스로 획득하므로 다른 executor가 같은 lock을 잡은 채 CLI를 중첩 호출하지 않습니다.
CLN01은 별도의 호환되지 않는 lock과 allowlist를 사용하며 이 lock으로 직렬화되지 않습니다.
CLN01 CLI는 COMM-003과 이 SMTP old path를 대상으로 허용하지 않습니다.

총괄은 해당 host의 정확한 consumer recreate/start 경로와 source/private metadata
writer를 일시 정지시키고, 어떤 경로를 어떻게 멈췄는지 owning Task에 기록해야
합니다. 동일 lock은 협력하는 executor만 직렬화합니다. Docker daemon이나 다른
프로세스의 쓰기를 강제로 막지 않으므로, 두 quiescence 사실을 확인하지 못하면
apply를 실행하지 않습니다. 본 문서만으로 stop 명령이나 대상 부재를 가정하지 않습니다.
암호화 Restic 보존 자체는 recovery custody이지만 실행 중인 secrets parent bind는
read-only여도 퇴역을 차단합니다. operator는 receipt 시간 창 안에서 해당 reader를
정확히 멈추고 quiescence를 확인해야 합니다.

helper는 공개 source와 mount 증거를 반복 검사하고 metadata/old file을 atomic
quarantine으로 옮겨 identity와 내용을 확인합니다. 다른 writer의 새 파일을 덮어쓰지
않습니다. 성공 전 old pathname 부재와 private metadata postcondition을 검사합니다.
변경 이후 실패는 `unsafe_after_mutation`, `applied: true`, `completed: false`, exit 2로
보고합니다. 이를 무변경 실패나 퇴역 성공으로 취급하지 않고 현재 pathname과 보존된
quarantine을 제한된 로컬 프로세스에서 확인합니다. 평문 복제본을 영구 보관하지 않으며
필요한 custody·정리·복구는 정확한 대상에 대한 SMTP01/총괄 지시로 처리합니다.

퇴역 실행 코드는 `scripts/lib/ops/smtp_contract.py`입니다. 생성기의 전용 모드만
이 모듈을 호출합니다. SMTP01이 source·consumer·generator 계약을 수용하기 전에는
중복 파일을 삭제하지 않습니다. 과거 CLN01 초안의 target 변경이나 SMTP verdict 고정은
자동 적용하지 않고 이 계약과 실제 native 결과에 맞춰 검토합니다.

#### n8n Native Credential Handoff

기존 선택 업무의 PostgreSQL `opsflow_notifier`와 SMTP는 n8n에 저장된 서로 다른
Credential이다. [기존 P06 기록](../../../03.specs/0204-service-integration-security-and-operations/tasks/tsk-0014-p06-openbao-consumer-migration.md)은
PostgreSQL native 회전의 과거 격리 수용과 두 자격의 OpenBao 전달·갱신 및 SMTP
회전 미실행을 구분한다. [P05 notifier Task](../../../03.specs/0212-request-baseline-and-reconciliation/tasks/tsk-0044-opsflow-notifier-recovery.md)는
합성 Mailpit에서 동일 Credential ID 갱신 후 다음 Worker 실행의 소비와 정지 복원을
확인했다. Agent 렌더나 파일 교체만으로 n8n DB에 암호화된 Credential이 갱신되지 않는다.

후속 실행 전 owner는 각 실제 자격의 발급자·정본과 승인된 목적지, 보유 Credential ID,
설치 버전에서 지원하는 권한 있는 갱신 경로, 다음 실행·이전 값 거부 조건, 기존 유효
경로·폐기 시각 및 DB와 동일 암호화 키의 독립 복원 경계를 지정한다. 전송 중 실행의
즉시 전환은 가정하지 않는다. 실제 발급·회전·외부 전송은 별도 대상별 승인과 복구
준비가 필요하며 이 문서는 실행 권한을 부여하지 않는다.

#### P02 Public Catalog Checks

P02 공개 catalog 점검은 아래 세 절로 나뉜다.

##### Metadata Check

이 절차는 검토된 checkout의 공개 metadata와 staging view만 확인한다. OpenBao API,
private metadata·환경·credential 파일, HOME 서비스에 접속하지 않는다. 저장소 루트의
물리적 절대 경로에서 검증 의존성이 설치된 Python으로 실행하며, symlink 경로나 다른
checkout을 `--root`로 지정하지 않는다. 먼저 읽기 전용 검사를 실행한다.

```bash
python3 scripts/operations/secret-catalog.py --root "$PWD" check
```

네 입력은 catalog, schema, `secrets/SENSITIVE_ENV_VARS.md.example`,
`infra/secret-file-support.json`이다. 형식·분류·원본 표 일치가 유효하면 JSON의
`result`는 `P02_METADATA_VALID`, `entries`와 `aliases`는 실제 입력의 개수이며 exit 0이다.
`P02_METADATA_BLOCKED`와 exit 2는 형식·원본·경로·의존성 등 검사 실패이므로 중단한다.
이 결과는 credential 값 또는 권리·운영 상태를 검사한 결과가 아니다.

##### Staging Views

staging이 필요한 경우에만 operator-owned `.agent-work`와 그 안의 regular, single-link,
동일 소유자 `README.md`를 먼저 확인한다. 기존 타 작업자의 경로를 교체하거나 symlink,
공유 inode, 다른 소유자의 파일 권한을 고쳐서 통과시키지 않는다. 새 경로를 준비할 때는
소유자가 확인된 전용 checkout에서만 만들고 그 목적을 README에 기록한다.

```bash
python3 scripts/operations/secret-catalog.py --root "$PWD" render
python3 scripts/operations/secret-catalog.py --root "$PWD" check-views
```

`render`는 `.agent-work/p02-views`에 정확히 네 공개 출력 파일을 만들며
`STAGING_RENDERED`와 파일명 목록, exit 0을 반환한다. `check-views`는 네 입력에서 유도한
bytes와 모두 일치할 때만 `P02_VIEWS_MATCH`, exit 0이다. 불일치는 `P02_VIEW_DRIFT`,
exit 2다. 경로·소유권 등 안전 검사 실패는 `P02_METADATA_BLOCKED`, exit 2다.
파일별 교체는 전체 네 파일의 원자적 transaction을 뜻하지 않는다. 실패 후 부분 결과를
소비하지 말고 원인과 공개 입력을 검토한 뒤 동일 전용 staging을 다시 생성·검사한다.
private 파일 삭제나 runtime rollback을 이 절차의 정리로 수행하지 않는다.

##### Generation Refusal Probes

아래 두 거절 probe는 각각 독립적으로 실행한다. `check-generation`은 생성 적격성만
검사하며 secret을 발급하지 않는다. 두 명령 모두 `P02_GENERATION_BLOCKED`, exit 2가
정상 예상 결과이며, 일반 shell의 실패 코드와 구별해 기록한다.

```bash
python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-002
python3 scripts/operations/secret-catalog.py --root "$PWD" check-generation COMM-003
```

거절 대신 성공하거나 예상 출력과 다르면 중단하고 P02 catalog 담당자와 검토한다.
alias COMM-003은 실제 폐기 완료가 아니며 별도 credential/KV 대상을 만들 수 없다.
다른 crypto/bootstrap/recovery/LAB/unknown/migrated/retired 항목과 observed/consumed 항목도
guard가 거부해야 한다. 공개 staging만으로 실제 발급·수집·이관·delivery·reload·rotation·
복구를 수용하지 않는다. ACL mapping은 `BLOCKED_P01`이고 delivery는 Agent 전달이 확인된
`DEPLOYED` 항목만 `openbao_agent`다. 실제 pilot은 대상 ID·KV
path·P01 인증/복구·P03 신원·P04 DEV/S3 증거가 있어야 한다. 현재 HOME/P06 hold를 유지한다.

### Stop Conditions

trusted 작성자와 입력의 쓰기 중단을 확인한 뒤에만 검사한다(Safety Checks의 P06 Read-only Structure and SMTP Checks). `P02_METADATA_BLOCKED`와 exit 2는 중단하고(Actions의 Metadata Check), 거절 probe가 성공하거나 예상 출력과 다르면 중단한다(Actions의 Generation Refusal Probes). catalog 점검이 실패하면 생성·전환을 멈춘다(Rollback). 안전한 진행이 불가능하면 중단하고 @buenhyden에게 연락한다(Escalation).

## Validation

### Service Checks

catalog 점검 결과는 `P02_METADATA_VALID`, staging을 만든 경우 `P02_VIEWS_MATCH`, 두 거절 probe의
`P02_GENERATION_BLOCKED`(exit 2)여야 한다. 소비자 전환의 수용은 P06 Task가 따로 가진다.

### Evidence

catalog 점검의 상태 문자열(Service Checks)을 값 없이 Task에 기록한다.

## Recovery

### Rollback

catalog 점검이 실패하면 생성·전환을 멈추고 원인을 고친 뒤 다시 점검한다. 소비자 전환의 rollback은 consumer-migration README의 `rollback` 절차를 따른다.

### Escalation

credential, 파괴적 스토리지 변경, remote 변경, 또는 backup 부재로 안전한 진행이 불가능하면
중단하고 @buenhyden에게 연락한다.
