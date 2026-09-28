---
title: "Library Tests"
version: "1.0.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
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

## How to Work in This Area

1. 짝이 되는 디렉터리에는 추적되는 동작 테스트가 최소 하나 있어야 하며
   그 테스트는 public full profile에 등록되어야 합니다. 빈 디렉터리,
   로컬 bytecode cache, placeholder, 추적되지 않은 테스트는 소유 근거가
   되지 않습니다.
2. 새 library 모듈을 추가하면 같은 변경에서 Script Manifest의 `tests`에
   테스트를 연결합니다.
3. 등록된 suite는 정확한 dotted module 이름으로 실행되므로, 모듈 경로를
   바꾸면 등록 이름도 함께 바꿉니다.

## Related Documents

- [Test Surface](../README.md)
- [Validation contract tests](../validation/README.md)
