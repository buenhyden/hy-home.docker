---
title: "Document governance synthetic fixtures"
version: "0.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-11"
created: "2026-10-11"
---

# 문서 계약 합성 입력

## Overview

문서 경로·정체성 계약을 운영 값 없이 검증하는 합성 입력 모음입니다.

## Audience

문서 도구 구현자와 독립 검토 담당자입니다.

## Scope

문서 이동·Registry 등록·운영 실행을 수행하지 않습니다. 실제 전수 문서 분류와
승인된 변경 경로는 owning Task가 관리합니다.

## Structure

- [operations-moves](operations-moves/README.md): 정확한 경로·ID 매핑과 유형별 LAB
  문서 목적지의 합성 시험 자산입니다.

## Tech Stack

기존 Python unittest와 JSON 입력을 사용합니다.

## Configuration

합성 자료만 추가합니다. 비밀값·개인 식별자·실제 운영 로그를 넣지 않습니다.

## Validation

```sh
python3 -m unittest tests.lib.document_governance.test_operations_moves -v
```

## Usage

하위 폴더 README에서 시험 범위와 입력을 확인합니다. 새 합성 자산은 해당 계약의
시험 소유자가 관리하고 상위 fixture 진입점을 함께 갱신합니다.

## Related Documents

- [Fixture 진입점](../README.md)
- [문서 진입점](../../../docs/README.md)
