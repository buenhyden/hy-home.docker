---
title: "Wiki 준비 패키지"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# Wiki 준비 패키지

## Overview

실제 Wiki 구현 전의 합성 계약과 미래 수용 기준을 정의합니다. SOURCE·UNIT·STATIC만 검증하며 ISOLATED·HOME·MIGRATION·ROTATION·RECOVERY·DELIVERY는 NOT_RUN입니다. owning Spec은 `SPEC-0204`이고 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[제품 intake](product-intake/README.md), [consumer](consumer-contract/README.md), [원천·artifact](source-artifact-contract/README.md), [job·복구](job-outbox-generation/README.md), [blog 인계](blog-data-handoff/README.md), [미래 흐름](future-flows/README.md), [readiness](readiness/README.md), [준비 계약](contracts/README.md), [schema](schemas/README.md), [fixture](fixtures/README.md), [통합 제안](integration-proposal/README.md)

## Tech Stack

기존 Python·jsonschema와 오프라인 JSON 문서를 사용합니다.

## Configuration

비밀값과 실제 환경 변수는 입력하지 않습니다.

## Validation

저장소 루트에서 활성화한 격리 venv에 `python -m pip install -r scripts/requirements.txt`를 실행한 뒤 `python -m unittest tests.lib.ops.test_wiki_preparation tests.validation.test_wiki_preparation_contracts -v`를 실행합니다. 시스템의 오래된 jsonschema는 검증 환경이 아닙니다. 단위검사는 native 실행 증거가 아닙니다.

## Usage

총괄의 공통 계약 통합 후 해당 증거를 Task에 연결합니다.

## Related Documents

[문서 진입점](../../../../docs/README.md), [project registration 계약](../README.md), 현재 Task ID는 `SPEC-0204-TSK-0008`입니다.
