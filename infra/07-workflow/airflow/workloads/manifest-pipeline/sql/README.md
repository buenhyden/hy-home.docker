---
title: "Manifest Publication SQL"
version: "0.2.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-13"
---

# Manifest Publication SQL

## Overview

P04 단독 소유의 versioned publication/outbox migration 초안입니다.
SQL 파일 존재는 실제 migration·권한·복구 수용을 뜻하지 않습니다.

## Scope

Ingest는 게시 함수, notifier는 claim/ack/retry, reader는 승인된 view만
소비합니다. Owner·migration capability는 runtime에 전달하지 않습니다.

## Structure

- [001_opsflow.sql](001_opsflow.sql): DB·role·기존 shape/ACL 검사와 원자적 게시 계약.
- [002_checks.sql](002_checks.sql): 합성 직접 호출·역할·lease 검사.
- [003_business_date.sql](003_business_date.sql): 같은 source의 UTC 업무일 중복을
  거부하는 version 2 migration.

## Usage

총괄이 함수 전용 provision·고정 이미지·빈 시험 대상·백업·복구 경계를 검토한
뒤 실행합니다. 새 빈 대상은 `001`과 그 hash로 `002`를 검증한 뒤 `003`을
적용하고, `003` hash로 `002`를 다시 검증합니다. `002`는 현재 version 1 또는
2의 최신 receipt/fingerprint만 수용합니다. 파일 재적용은 임의 schema upgrade를
허용하지 않습니다.
후속 변경은 새 version migration으로 관리합니다. P05는 복사본을 만들지 않고
이 파일의 검토된 version/hash·함수·view·lease·재시도 계약을 참조해야 합니다.

초기 `001` draft는 PostgreSQL 18 native 적용에서 fingerprint의 내부 `"char"`
catalog 값을 text와 직접 연결하다 SQLSTATE `42725`로 실패했고 transaction이
commit되지 않았습니다. 현재 bootstrap은 해당 catalog 값만 명시적으로 text로
변환하며 DDL·함수·권한 계약을 바꾸지 않습니다. 실패한 이전 draft hash는 수용된
version 1 receipt가 아닙니다. 별도 대상에서 이전 hash의 receipt가 발견되면 자동
승격하지 않고 DAG를 중지한 뒤 backup·schema fingerprint·적용 이력을 검토합니다.

이후 격리 복원 시험에서는 네 table과 한 sequence의 실제 권한이 같지만
`relacl`의 NULL 표현만 달라져 raw ACL 문자열 fingerprint가 실패했습니다. 현재
fingerprint는 권한을 가질 수 있는 relation의 NULL ACL을 객체 종류와 owner의
기본 ACL로 펼친 뒤 grantor·grantee(`PUBLIC` 포함)·권한 종류·grant option을 정렬된
JSON 배열로 기록합니다. 명시적인 빈 ACL은 기본 ACL로 바꾸지 않으며, index 같은
비권한 relation의 raw ACL metadata도 지우지 않습니다. Owner와 나머지 relation
구조 필드는 기존 signature에 그대로 남습니다. 이 수정 전 draft의 실패도 수용된
receipt가 아니며 기존 receipt를 자동 보정하지 않습니다.

### Migration boundary

기존 provisioner가 `opsflow_owner` NOLOGIN, 별도 `opsflow_migrator` LOGIN과
세 runtime LOGIN을 함수 전용으로 준비해야 합니다. Migrator만 owner에
ADMIN=false·INHERIT=false·SET=true membership을 갖습니다. 기존 넓은 grant나
미확정 membership·DB/schema/default ACL은 migration 전에 거부합니다.
이 SQL은 역할 생성·비밀번호 발급·기존 ACL의 자동 수정을 하지 않습니다.

호출자는 적용할 `001_opsflow.sql` 또는 `003_business_date.sql`의 SHA256을
각 실행의 `migration_sha256` psql 변수로 제공합니다. Version 1 장부에는
`001` 값과 당시 객체·함수·role·ACL fingerprint를 저장합니다. `003`은 모든
workload 기본 테이블을 10초 안에 잠그고 각 statement를 60초로 제한한 뒤
고정된 `001` SHA256, 유일한 version 1 행,
현재 fingerprint와 기존 UTC 업무일 충돌 부재를 DDL 전에 검사합니다. 하나라도
다르면 자동 수정 없이 전체 transaction을 중단합니다. 성공하면 version 1 행을
유지하고 version 2 hash/fingerprint를 새 행으로 기록합니다. 저장된 caller
hash만으로 실제 파일 적용을 증명하지 않습니다. 재적용은 항상 거부합니다.

`002_checks.sql`은 적용된 최신 migration의 SHA256을 `migration_sha256`으로
받습니다. 기존 workload 행이 모두 없는 승인된 독립 대상에만 실행하고
합성 행을 ROLLBACK하지만 identity sequence 증가는 되돌리지 않습니다.
따라서 폐기 가능한 독립 DB가 필요하며 행 rollback을 빈 대상 복원으로 보지 않습니다.
시험 session_user가 owner 및 각 client로 SET ROLE 가능한 별도 superuser 감사
capability를 먼저 검토해야 합니다. 시험을 통과시키기 위해
runtime membership을 추가하지 않습니다. 다른 DB의 CONNECT 거부·경합·객체 복원은
별도 native 시험입니다. 이 스크립트만으로 해당 경계를 확인했다고 기록하지 않습니다.

### Version 2 business-date invariant

Version 2는 `runs_source_business_date_uidx`로 같은 source와
`(captured_at AT TIME ZONE 'UTC')::date` 조합을 하나만 허용합니다. Version 1
데이터에 해당 충돌이 있으면 index를 만들거나 행을 삭제·수정하지 않고 migration이
실패합니다. 새 게시의 정확히 같은 시각 충돌은 기존 함수 오류로, 같은 UTC 날짜의
다른 시각 충돌은 이름 있는 unique index의 원자적 오류로 거부됩니다. `runs`
insert가 먼저 실패하므로 해당 호출은 document·현재 pointer·outbox를 남기지
않습니다. 기존 source별 advisory lock과 DB unique invariant가 직렬·경합 호출에
같은 규칙을 적용합니다.

Commit 전 실패는 transaction rollback으로 끝납니다. Commit 뒤 source rollback은
schema rollback이 아닙니다. 문제가 생기면 DAG를 일시 중지하고 accepted history와
outbox를 보존한 채, 검토된 backup을 별도의 빈 workload 복구 대상에 적용해
재검증합니다. 운영 데이터가 있는 대상에서 version 2 index나 장부 행을 임의로
제거하지 않으며 MNG DB reset, 공유 volume 삭제, 전체 stack restart를 하지 않습니다.

### P05 draft interface

Source version은 2입니다. Version 2는 아래 함수·view·lease 계약과 여섯 인자
`publish_manifest` signature를 바꾸지 않습니다. SQL·보안 검토 뒤 파일 hash를
고정하며, P05의 실제 소비자 검토와 native 수용은 아직 NOT_RUN입니다.

| 호출 | 입력 | 결과 |
| --- | --- | --- |
| `publish_manifest` | source, run ID, raw SHA256, captured_at, records JSONB, artifact key | published / historical / replayed |
| `claim_notification` | 없음 | id, run_id, source, row_count, lease_token, lease_until |
| `ack_notification` | id, lease_token | 유효 lease의 SMTP acceptance 여부 boolean |
| `retry_notification` | id, lease_token | 유효 lease의 retry/dead 전이 여부 boolean |
| `published_documents` / `delivery_status` | reader SELECT | 승인된 현재 문서 / 제한된 통지 장부 |

Lease는 10분이고 만료·stale token은 거부합니다. 최대 다섯 번 claim 후 dead로
종료하며 retry delay는 30×2^attempt seconds, 상한 900초입니다. 역사적 게시에는
새 outbox를 만들지 않고 기존 run의 최초 게시 결과를 유지합니다. 같은 source와
captured_at의 다른 입력 및 같은 source·UTC 업무일의 다른 입력은 전체 역사에서
거부합니다.

여섯 인자 SQL은 records·ID·hash 형식·artifact·유한 timestamp를 검증합니다.
원본 JSON 중복 key, 1MiB 상한, repository/ref·UTC business_date·원본 bytes의
authenticity는 parser/호출 경계이며 SQL에 전달되지 않습니다. 해시의 형식이나
caller 입력을 실제 Git 내용 인증으로 취급하지 않습니다.

Ack는 SMTP acceptance만 기록하며 실제 배달을 보장하지 않습니다. 안정된
run-derived Message-ID, at-least-once 중복 불확실성과 accepted event 복원 정합은
P05와 별도 native 검증에서 확인합니다. 현재 P05 소비자 검토와 native는 NOT_RUN입니다.

## Related Documents

- [배치](../README.md)
- [Library](../workflow_lib/README.md)
