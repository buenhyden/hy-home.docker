---
title: "합성 허용·거부 fixture"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 합성 허용·거부 fixture

## Overview

각 schema에 valid/invalid JSON 한 쌍을 둡니다. [expectations.json](expectations.json)은 schema 형식 결과와 helper semantic 결과를 별도로 기록합니다. invalid fixture는 의도적으로 schema-valid이면서 semantic-invalid이며, 검사 경계를 혼동하지 않습니다. artifact.synthetic.txt는 생성한 공개 합성 bytes이며 비밀이나 실제 문서가 아닙니다. example-project·endpoint·참조 ID·수치는 모두 합성입니다. fixture Task ID는 기존 generic schema 형식의 합성 입력이며 P09 Task 발급 사실이 아닙니다. 유효 fixture는 source 형식·정합만 증명합니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[schema](../schemas/README.md), [기대 결과](expectations.json)

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
