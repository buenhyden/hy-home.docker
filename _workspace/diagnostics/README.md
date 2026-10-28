---
title: "Workspace Diagnostics"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
created: "2026-10-29"
---

# _workspace/diagnostics

## Overview

`_workspace/diagnostics`는 검사와 CI를 진단하면서 만든 정제된 결과를 잠시 두는
공간이며 Git이 무시합니다. `ci/`는 원격 CI 실행을, `validation/`은 로컬
검사 실행을 다룹니다. 이 공간은 authority가 없고 Task 증거를 대신하지 않습니다.

## Audience

- AI Agents
- Repository Maintainers

## Scope

작업 중 만들 수 있는 산출물:

- 검사 명령, 입력 revision, 종료 코드, 실패 판정을 요약한 정제 결과
- secret과 raw log를 뺀 실패 재현 메모

만들거나 남기지 않는 산출물:

- raw log, 로컬 로그, 진단 덤프 원문
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

## Structure

`README.md`, `ci/README.md`, `validation/README.md`만 추적됩니다. 그 밖의
파일은 무시되는 임시 산출물입니다.

## Usage

1. 결과를 `ci/<run-or-task>/` 또는 `validation/<task-slug>/` 아래에 씁니다.
2. 남겨야 할 판정은 현재 Stage 03 Task의 Evidence로 요약해 옮깁니다.
3. 원본 진단 파일은 무시된 채로 두거나 삭제합니다.

## Related Documents

- [workspace README](../README.md)
- [CI 진단](ci/README.md)
- [검사 진단](validation/README.md)
