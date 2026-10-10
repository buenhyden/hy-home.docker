---
title: "선택 후보의 blog-data 인계"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 선택 후보의 blog-data 인계

## Overview

원문 출력은 Literature 후보에만 머뭅니다. Permanent·Maps·출판물은 별도 사람 검토로 승격합니다. 이 단계는 실제 쓰기 권한·branch·PR을 생성하지 않습니다. 합성 approval은 운영 승인을 대체하지 않습니다.

handoff는 선택 candidate ID, 검토 base SHA, 정확한 허용 경로·expected hash·write set·approval selection·conflict policy·receipt/idempotency를 연결합니다. 선택하지 않은 후보의 추가 쓰기, 중복 경로·ID, hash 불일치, 다른 base SHA, stale receipt를 거절합니다. `write_set_sha256`은 경로·candidate ID·hash 순서로 정렬한 write set의 canonical JSON SHA-256입니다. `idempotency_key`는 `project_id`, `repository`, `base_sha`, 정렬 write set을 포함한 canonical JSON SHA-256입니다. stale base는 rebase 자동 쓰기 대신 거절하고 재검토합니다. 승인 한 번으로 전체 후보를 쓰지 않습니다.

미래 실제 소비자는 현재 branch HEAD와 base SHA 및 정책 승인을 다시 확인하고 기대 hash를 독립 검증한 뒤 정확한 write set만 transaction/PR에 적용해야 합니다. 검증 helper는 저장소 접근이나 쓰기를 수행하지 않습니다.

caller policy는 `project_id`, `repository`, `base_sha`, selected candidate ID와 exact write-set의 path/hash를 제공하며, document가 이를 넓힐 수 없습니다. `prior_receipts`는 `{idempotency_key: request_sha256}` mapping입니다. helper는 candidate와 write set 순서를 canonicalize해 request SHA-256을 계산하고, 같은 idempotency key가 같은 request SHA-256일 때만 재시도를 허용하며 다른 요청은 거절합니다. 이 receipt는 실제 blog-data write, branch 상태 또는 사람 승인 사실을 증명하지 않습니다.

여기의 document receipt key는 원본 합성 blog receipt key이며 fixture 값은 변경하지 않습니다. helper 결과 scoped key와 `prior_receipts` key의 관계는 [준비 계약의 Idempotency Result Contract](../contracts/README.md#idempotency-result-contract)가 소유합니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[schema](../schemas/blog-data-handoff.schema.json)

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
