---
title: "Validation Diagnostics"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
created: "2026-10-29"
---

# _workspace/diagnostics/validation

## Overview

`_workspace/diagnostics/validation`은 로컬 검사기(`scripts/validation/`)를
실행하며 만든 정제 결과를 잠시 두는 공간이며 Git이 무시합니다.

## Audience

- AI Agents
- Repository Maintainers

## Scope

작업 중 만들 수 있는 산출물:

- 검사 명령, 입력 revision, 위반 코드와 개수 요약
- 실행 시간 측정과 비교 메모

만들거나 남기지 않는 산출물:

- raw log, 로컬 로그, 진단 덤프 원문
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

## Structure

`README.md`만 추적됩니다. 작업별 하위 디렉터리는 무시되는 임시 공간입니다.

## Usage

1. 작업별로 `<task-slug>/` 하위 디렉터리를 씁니다.
2. 검사 판정은 현재 Task의 Evidence 표로 옮깁니다. 이곳의 파일을 증거 위치로 인용하지 않습니다.
3. 작업이 끝나면 남기거나 지웁니다. 복구할 authority가 없습니다.

## Related Documents

- [진단 README](../README.md)
