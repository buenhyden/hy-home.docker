---
title: "Test Surface"
version: "1.0.1"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
created: "2026-02-21"
---

# tests

> 저장소 전역 검증과 테스트 자산의 진입점

## Overview

`tests/`는 저장소 전역 테스트와 검증 자산을 두는 공간입니다. 주요 품질
게이트는 `scripts/`와 GitHub Actions에 정의되어 있으며, 이 트리는
`scripts/lib/<domain>/`의 library-unit 소유권과 validation/entrypoint 소유권을
서로 분리합니다.

## Audience

이 README의 주요 독자:

- Developers
- QA Engineers
- Operators
- AI Agents

## Scope

### In Scope

- 저장소 전역 테스트 정책과 테스트 자산 위치 안내
- 여러 서비스나 문서 계약을 함께 검증하는 테스트 진입점
- CI에서 실행되는 검증 스크립트와의 연결

### Out of Scope

- 개별 서비스의 Docker Compose 원문
- `scripts/`가 소유하는 검증 스크립트 구현
- secret 값, credential, token, 인증서 원문
- 하위 프로젝트의 package-local 테스트 설정

## Structure

```text
tests/
├── README.md  # This file
├── fixtures/          # 독립 consumer가 필요한 고정 입력만 허용; 현재 비어 있음
├── lib/<domain>/      # scripts/lib/<domain>/ library-unit 테스트
└── validation/        # validation/entrypoint 및 실행-context 테스트
```

## How to Work in This Area

1. 새 테스트 자산을 만들기 전에 같은 검증이 이미 `scripts/` 또는 하위 프로젝트 package script에 있는지 확인합니다.
2. repository contract, doc traceability, Compose validation처럼 전역 검증에 가까운 항목은 [`../scripts/README.md`](../scripts/README.md)에 있는 기존 진입점을 우선 사용합니다.
3. `scripts/lib/<domain>/`의 주 책임을 검증하는 테스트는 같은 이름의
   `tests/lib/<domain>/`에 두고, CLI·entrypoint·실행 context 검증은
   `tests/validation/`에 둡니다.
4. 새 테스트 파일을 추가하면 실행 명령, 기대 결과, CI 연결 여부를 이 README 또는 관련 stage 문서에 기록합니다.
5. 테스트가 특정 service 또는 package에만 해당하면 해당 디렉터리 README에 위치와 실행법을 기록합니다.

운영 rehearsal의 재사용 입력은 `examples/operations/`가 소유합니다.
단일 필드 오류 입력은 테스트 builder로 만들며, production은 `tests/`를
읽지 않습니다. 전체 Python discovery는
`PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_*.py'`로 실행합니다.

문서 메타데이터 검증 테스트는
`PYTHONPATH=. python3 -m unittest discover -s tests/lib/document_governance/metadata -p 'test_*.py'`로
실행합니다. lifecycle entrypoint 검증은
`PYTHONPATH=. python3 -m unittest discover -s tests/validation/lifecycle -p 'test_*.py'`로
실행합니다. 두 inventory는 각각 5개 production 책임과 4개 등록 mode를
mirroring하며, 공통 fixture는 discovery 대상이 아닌 `_support.py`만 사용합니다.

changed/new blocking gate는 활성 상태입니다. `check-document-metadata.py
--mode check-changed --base-ref "$(git merge-base main HEAD)"`가 CI가 강제하는
차단 조건이며, base ref는 고정하지 않고 계산합니다. 인자 없이 실행하면 차단하지
않는 advisory inventory를 출력합니다.

## Related Documents

- [Root README](../README.md)
- [Scripts README](../scripts/README.md)
- [Documentation protocol](../docs/00.agent-governance/policies/documentation-protocol.md)
- [Task checklists](../docs/00.agent-governance/policies/task-checklists.md)
