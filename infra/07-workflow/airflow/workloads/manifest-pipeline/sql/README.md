---
title: "Manifest Publication SQL"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
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

## Usage

총괄이 함수 전용 provision·고정 이미지·빈 시험 대상·백업·복구 경계를 검토한
뒤 실행합니다. 파일 재적용은 임의 schema upgrade를 허용하지 않습니다.
후속 변경은 새 version migration으로 관리합니다. P05는 복사본을 만들지 않고
이 파일의 검토된 version/hash·함수·view·lease·재시도 계약을 참조해야 합니다.

### Migration boundary

기존 provisioner가 `opsflow_owner` NOLOGIN, 별도 `opsflow_migrator` LOGIN과
세 runtime LOGIN을 함수 전용으로 준비해야 합니다. Migrator만 owner에
ADMIN=false·INHERIT=false·SET=true membership을 갖습니다. 기존 넓은 grant나
미확정 membership·DB/schema/default ACL은 migration 전에 거부합니다.
이 SQL은 역할 생성·비밀번호 발급·기존 ACL의 자동 수정을 하지 않습니다.

호출자는 공개 `001_opsflow.sql`의 SHA256을 `migration_sha256` psql 변수로
제공합니다. Version1 장부에는 그 값과 현재 객체·함수·role·ACL fingerprint를
따로 저장합니다. 저장된 caller hash만으로 실제 파일 적용을 증명하지 않습니다.
재적용은 항상 거부하며, 별도 현재 fingerprint 검증 후 새 migration을 검토합니다.

`002_checks.sql`은 기존 workload 행이 모두 없는 승인된 독립 대상에만 실행하고
합성 행을 ROLLBACK하지만 identity sequence 증가는 되돌리지 않습니다.
따라서 폐기 가능한 독립 DB가 필요하며 행 rollback을 빈 대상 복원으로 보지 않습니다.
시험 session_user가 owner 및 각 client로 SET ROLE 가능한 별도 superuser 감사
capability를 먼저 검토해야 합니다. 시험을 통과시키기 위해
runtime membership을 추가하지 않습니다. 다른 DB의 CONNECT 거부·경합·객체 복원은
별도 native 시험입니다. 이 스크립트만으로 해당 경계를 확인했다고 기록하지 않습니다.

### P05 draft interface

Source version은 1입니다. SQL·보안 검토 뒤 파일 hash를 고정하며, P05의 실제
소비자 검토와 native 수용은 아직 NOT_RUN입니다.

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
captured_at의 다른 입력은 전체 역사에서 거부합니다.

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
