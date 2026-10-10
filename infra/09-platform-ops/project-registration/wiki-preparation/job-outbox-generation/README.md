---
title: "Job·outbox·generation·복구 모델"
version: "0.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# Job·outbox·generation·복구 모델

## Overview

공개 job 상태는 pending→running→partial/succeeded/failed/cancelled, partial→running/failed/cancelled, failed→pending의 여섯 상태입니다. succeeded/cancelled는 terminal이며 새 업무는 새 job ID를 발급합니다. `dead`는 공개 schema나 generation pointer 상태가 아닌 `dead_letter`의 구조화된 disposal 기록으로만 다룹니다. `dead_letter`는 `disposition`(`none` 또는 `quarantined`), `reason`(null 또는 `retry-exhausted`), `replay_requires_approval=true`를 반드시 포함합니다. quarantined는 state가 failed이고 attempt가 max_attempts일 때만 가능하며, exhausted failure는 quarantine해야 합니다. 사람 승인 후의 manual replay는 미래 수용 조건이며 NOT_RUN입니다. at-least-once delivery는 dedup key로 처리합니다. attempt는 pending→running 횟수와 같아야 하고 backfill은 별도 선행 job ID를 요구합니다. retry는 max_attempts와 timeout 내에서 수행합니다.

PostgreSQL metadata/outbox, object artifact, Qdrant vector 간 전역 원자성을 가정하지 않습니다. PG outbox commit 후 side effect를 단계별 기록하고 동일 key replay 시 검증된 hash와 결과를 재사용합니다. 성공 또는 명시 terminal disposal 전 ack하지 않습니다. 세 store 검증·generation 일치·삭제 watermark 반영을 모두 만족한 generation만 공개 pointer로 지정합니다. partial 결과는 공개하지 않습니다.

복원은 backup checkpoint와 event log를 맞추고 삭제/권한 철회 우선 replay→object hash 검사→vector 재생성 또는 검증→ACL/cache 재평가→generation pointer 재검증 순서입니다. 미확인 store는 pending/failed로 남겨 pointer를 비공개로 유지합니다. RPO/RTO는 계획값이며 실제 복원 시간은 NOT_RUN입니다. P04/P05에는 Wiki workflow 대신 opsflow_dev 독립 배치의 합성 연결 자산만 인계합니다.

caller policy는 `job_id=example-job`, `dedup_key`와 `outbox.event_id=example-event`를 포함한 합성 job admission 범위를 제공합니다. 다음 job 호출은 raw dedup key, `{generation, transition_count, outbox_sequence, attempt, deletion_watermark, generation_watermark}`가 든 parsed `prior_states`, complete `prior_receipts`를 제공해야 합니다. revision/history/terminal-state 제약과 stable admission anchor의 backfill/retry/timeout/outbox identity binding은 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)가 유일하게 소유합니다. document는 이 exact identity와 dedup mapping을 넓힐 수 없고, helper는 delivery를 발생시키지 않습니다. 이 비교는 실제 outbox persistence, retry, dead-letter disposal 또는 recovery 실행의 증거가 아닙니다.

helper 결과의 scoped idempotency와 원본 dedup key의 관계는 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)가 소유합니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[schema](../schemas/job-outbox-handoff.schema.json)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Usage

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

## Related Documents

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.
