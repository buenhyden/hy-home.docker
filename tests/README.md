# tests

> 저장소 전역 검증과 테스트 자산의 진입점

## Overview

`tests/`는 개별 서비스 디렉터리에 묶이지 않는 전역 테스트와 검증 자산을 두는 공간입니다. 현재 이 저장소의 주요 품질 게이트는 `scripts/`와 GitHub Actions에 정의되어 있으며, 이 README는 테스트 관련 파일을 추가할 때의 위치와 검증 경계를 설명합니다.

구현 코드와 가까운 단위 테스트가 필요한 경우에는 해당 소스 또는 서비스 디렉터리 근처에 두고, 여러 계층을 가로지르는 통합, smoke, contract 성격의 테스트만 이 폴더에 둡니다.

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
└── README.md  # This file
```

## How to Work in This Area

1. 새 테스트 자산을 만들기 전에 같은 검증이 이미 `scripts/` 또는 하위 프로젝트 package script에 있는지 확인합니다.
2. repository contract, doc traceability, Compose validation처럼 전역 검증에 가까운 항목은 [`../scripts/README.md`](../scripts/README.md)에 있는 기존 진입점을 우선 사용합니다.
3. 새 테스트 파일을 추가하면 실행 명령, 기대 결과, CI 연결 여부를 이 README 또는 관련 stage 문서에 기록합니다.
4. 테스트가 특정 service 또는 package에만 해당하면 해당 디렉터리 README에 위치와 실행법을 기록합니다.

## Related References

- [Root README](../README.md)
- [Scripts README](../scripts/README.md)
- [Documentation protocol](../docs/00.agent-governance/rules/documentation-protocol.md)
- [Task checklists](../docs/00.agent-governance/rules/task-checklists.md)
