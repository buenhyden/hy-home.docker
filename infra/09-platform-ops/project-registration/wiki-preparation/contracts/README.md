---
title: "Wiki 준비 계약 목록"
version: "0.2.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# Wiki 준비 계약 목록

## Overview

이 폴더는 P09의 일곱 준비 산출물로 연결되는 단일 계약 진입점입니다. 실제 앱, resource, credential, schedule 또는 blog-data write를 만들지 않습니다. 형식 schema와 pure helper의 semantic 결과는 분리되며, 어느 PASS도 원천 진위·권리·운영 readiness를 증명하지 않습니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

1. [제품 intake](../product-intake/README.md)
2. [미래 consumer manifest](../consumer-contract/README.md)
3. [source/artifact 계약](../source-artifact-contract/README.md)
4. [job/outbox/generation 모델](../job-outbox-generation/README.md)
5. [선택 후보 blog-data handoff](../blog-data-handoff/README.md)
6. [미래 사용자 흐름·E2E 수용](../future-flows/README.md)
7. [readiness matrix](../readiness/README.md)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

`../fixtures/expectations.json`은 각 fixture의 schema와 helper semantic 기대 결과를 분리합니다. 기존 generic registration schema와 validator는 test harness가 제공하는 parsed 입력으로만 사용합니다. 저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다.

## Usage

미래 consumer는 이 목록에서 책임 계약을 선택하고, 실제 resource 변경 전에 별도 수용 조건과 권한을 갖춰야 합니다.

### Idempotency Result Contract

helper는 `admission_idempotency_key`, `admission_sha256`, versioned receipt entries와 `state_record`를 반환합니다. Source `admission_idempotency_key`는 `H(project_id, contract, repository, ref, path)`이며 raw source idempotency key는 현재 content SHA로 보존하되 admission scope에는 넣지 않습니다. Source revision, content hash, timestamp와 processing version은 admission digest에서 제외합니다. Job admission은 raw dedup key를 유지한 stable non-state anchor를 사용합니다. Versioned receipt는 admission scope/anchor와 revision receipt를 함께 보존합니다. Source `state_record`는 `{admission_sha256, request_sha256, revision, state, history, surface_watermarks, artifact}`이고 `artifact`는 `{source_revision, content_sha256, versions}`입니다. Raw job dedup key와 blog document receipt key는 보존합니다.

다음 source/job 호출은 `admission_idempotency_key`로 key된 parsed `prior_states`와 complete `prior_receipts`를 제공해야 합니다. Source revision은 `generation`과 `evaluated_sequence`, 모든 surface watermark의 단조 증가를 포함합니다. caller policy의 `versions`는 최대 128개의 정확한 `{parser, chunker, embedding}` mapping allowlist이며, 각 값은 비어 있지 않고 `*` 문자를 포함할 수 없으며 중복 mapping은 허용하지 않습니다. 값은 exact 문자열로만 비교합니다. document `versions`는 그 중 하나와 정확히 같아야 합니다. 같은 generation에서는 `{source_revision, content_sha256, versions}` artifact 전체가 불변이고, 더 높은 source generation에서만 갱신된 caller policy가 허용하는 artifact revision/content/version 조합으로 바꿀 수 있습니다. allowed는 revoked/deleted로만, revoked는 revoked/deleted로만 진행하고 deleted는 terminal이며 history는 prior history의 prefix여야 합니다. Job revision은 `generation`, `transition_count`, `outbox_sequence`, `attempt`, `deletion_watermark`, `generation_watermark`의 단조 증가와 history prefix를 포함하며 terminal state는 reopen하지 않습니다. Stable admission anchor는 job의 non-state field와 backfill/retry/timeout/outbox identity를 묶습니다. Immutable admission digest 변경은 충돌이며, 같은 state revision에서 전체 payload가 다르면 충돌입니다.

helper는 caller가 제공한 authoritative frontier만 검사합니다. atomic store completeness, source authenticity, authorization, 실제 delete/restore 또는 I/O는 `NOT_RUN`이며 미래 exact Task에서 검증합니다. 이 문단이 idempotency와 frontier의 유일한 계약 정의입니다.

## Related Documents

[준비 패키지](../README.md), [schema](../schemas/README.md), [fixture](../fixtures/README.md)
