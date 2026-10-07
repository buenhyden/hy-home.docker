---
title: "Library Tests"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-07"
created: "2026-09-27"
---

# tests/lib

## Overview

`tests/lib/<domain>/`은 `scripts/lib/<domain>/`의 주 책임을 그대로 따라가는
library-unit 테스트 공간입니다. library 도메인마다 짝이 되는 테스트
디렉터리가 하나씩 있고, 여러 도메인에 걸친 검증과 entrypoint 동작은
`tests/validation/`이 맡습니다.

## Audience

- Developers
- QA Engineers
- AI Agents

## Scope

- 포함: `scripts/lib/<domain>/` 모듈의 동작 테스트.
- 제외: CLI 파싱, 렌더링, 실행 context 라우팅, 여러 도메인을 묶는 gate
  실행. 이들은 `tests/validation/`이 소유합니다.

## Structure

직접 하위 디렉터리는 `scripts/lib/`의 도메인 이름과 같습니다. 도메인과
테스트 파일의 정확한 대응은 [Script Manifest](../../scripts/manifest.yaml)의
`tests` 항목이 소유합니다.

## Usage

1. 유지하는 library 동작에는 추적되고 등록된 테스트 소유자가 있어야 합니다.
   `tests/lib/<domain>/`이 기본 위치이며, 여러 모듈이나 entrypoint를 함께
   검증하는 현재 테스트는 `tests/validation/`에서 그 동작을 소유할 수 있습니다.
   Script Manifest는 허용 경로·추적 여부·실제 API/fixture 사용을 검사하며,
   같은 보장을 위한 별도 mirror smoke를 요구하지 않습니다. 빈 디렉터리,
   bytecode cache, placeholder는 테스트 근거가 아닙니다.
   unit 모듈은 LOCAL full 계획에서 도달 가능해야 하며 hosted 계획에서는 제외됩니다.
2. 새 library 모듈을 추가하면 같은 변경에서 Script Manifest의 `tests`에
   테스트를 연결합니다.
3. 등록된 suite는 정확한 dotted module 이름으로 실행되므로, 모듈 경로를
   바꾸면 등록 이름도 함께 바꿉니다.

## Related Documents

- [Test Surface](../README.md)
- [Validation contract tests](../validation/README.md)
