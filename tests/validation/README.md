---
title: "Validation Contract Tests"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-27"
---

# tests/validation

## Overview

이 트리는 검증기와 entrypoint의 동작을 소유합니다. CLI 파싱, 렌더링, 실행
context 라우팅, 여러 검사를 묶는 gate 실행이 여기에 해당합니다. 개별
library의 단위 테스트는 짝이 되는 `tests/lib/<domain>/`에 둡니다.

## Audience

- Developers
- QA Engineers
- AI Agents

## Scope

- 포함: `scripts/validation/`과 `scripts/operations/` entrypoint의 동작,
  gate 계획과 실행 context, 여러 계약을 함께 확인하는 테스트.
- 제외: 단일 library 모듈의 내부 동작 테스트.

## Structure

직접 구성원은 `test_*.py` 테스트 모듈과 테스트 전용 지원 모듈입니다.
`lifecycle/` 하위 디렉터리는 문서 수명주기 CLI의 테스트를 담습니다. 각
테스트가 검증하는 스크립트는 [Script Manifest](../../scripts/manifest.yaml)의
`tests` 항목이 소유합니다.

## Usage

1. 새 entrypoint나 gate 동작을 바꾸면 이 트리에 실패하는 테스트를 먼저
   추가합니다.
2. 픽스처는 테스트 안에서 필요한 최소 입력만 만들어 씁니다.
3. 실행은 `python3 -m unittest discover -s tests/validation -t . -p 'test_*.py'`
   로 합니다.

## Related Documents

- [Test Surface](../README.md)
- [Library tests](../lib/README.md)
