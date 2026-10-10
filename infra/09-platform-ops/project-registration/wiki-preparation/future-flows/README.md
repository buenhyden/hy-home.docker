---
title: "미래 사용자 흐름과 E2E 인수 시나리오"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-10"
---

# 미래 사용자 흐름과 E2E 인수 시나리오

## Overview

아래는 앱 구현 후의 인수 시나리오이며 실행 결과는 모두 NOT_RUN입니다.

| 흐름 | 정상 수용 | 실패·거부 수용 |
|---|---|---|
| 로그인·원천 선택 | issuer/audience와 사용자 ACL에 맞는 원천만 표시 | 로그아웃·만료·잘못된 audience·교차 프로젝트 거부 |
| 동기화·최신성 | revision/generation/지연 상태 표시 | 빈 원천·timeout·partial store를 최신 정상으로 표시하지 않음 |
| 탐색·인용 | 허용 artifact의 revision/hash/시각·근거 연결 | 삭제·철회·old generation의 query/download/citation/cache 모두 거부 |
| 후보 검토·선택 | 사람이 선택한 Literature 후보만 정확한 write set 인계 | 미선택·중복·추가 경로·stale base·hash 불일치 거부 |
| 재시도·취소 | 동일 key 재시도 중복 side effect 없음, 취소 상태 명시 | dead/timeout은 실패 원인을 값 노출 없이 표시 |
| 빈 환경 복원 | outbox·삭제 watermark·세 store 재검증 후 공개 | 이전 ACL/content resurrect 또는 미검증 generation 노출 거부 |

지연·부분 실패·취소·권한 거부·복원 중 UI는 진척과 미확인 상태를 분리해야 합니다. 미래 Wiki 앱의 owning exact Task가 이 조건을 executable E2E로 구현하고, P10은 전체 인프라 수용을 조정합니다. Storybook 앱 코드나 가짜 PASS는 작성하지 않습니다.

## Audience

인프라 담당자, 미래 consumer 작성자와 독립 검토자입니다.

## Scope

준비 문서·기계 schema·합성 검증에 한정합니다.

## Structure

[readiness](../readiness/README.md)

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
