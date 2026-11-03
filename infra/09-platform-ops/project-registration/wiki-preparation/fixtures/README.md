---
title: "합성 허용·거부 fixture"
version: "0.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-02"
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

### P03 준비 평가 예시

P03은 이미 완료된 준비 패키지를 다음 여섯 가지 작은 오프라인 평가 사례에
연결합니다. 이는 계약 예시일 뿐이며, Wiki 런타임 생성, 원문 조회, 데이터베이스
프로비저닝 또는 실행 가능한 종단 간 결과를 뜻하지 않습니다.

| 사례 | 합성 계약 기대값 | 거부 또는 보류 기대값 |
| --- | --- | --- |
| rights | 원문에 명시적 권리 근거와 허용된 수명주기 상태가 있다 | 알 수 없거나 철회된 권리는 허용된 산출물로 공개할 수 없다 |
| ACL | 지정 독자가 정확히 파싱된 허용 목록에 있다 | 다른 프로젝트 또는 목록 밖 독자는 거부한다 |
| citation | 검색 결과가 revision, hash, 조회/효력 시간을 함께 묶는다 | 출처가 없으면 인용이나 결과를 주장하지 않는다 |
| revocation | 철회/삭제된 산출물은 검색, point query, 인용, 다운로드, 캐시에서 무효화된다 | watermark가 전진한 뒤 이전 generation이 다시 나타나면 안 된다 |
| no evidence | 불완전한 원문 또는 저장소 상태는 pending/failed로 남는다 | 비어 있거나 일부만 있는 상태를 fresh/successful로 표시하지 않는다 |
| failure and recovery | retry/dead-letter와 three-store 대조는 검증 전 비공개 pointer를 보존한다 | 미검증 generation, 이전 ACL 또는 콘텐츠를 되살리지 않는다 |

기존 valid/invalid fixture와 future-flow matrix가 이 사례의 source 계약을
제공합니다. 각 행이 런타임 수용으로 바뀌려면 미래의 Wiki 담당 Task가 자체 제품 및
종단 간 증거를 제공해야 합니다.

## Related Documents

문서 체계는 저장소 docs README 진입점을 통해 확인합니다.
