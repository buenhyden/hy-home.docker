---
title: "Repository Support Analysis"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
created: "2026-10-29"
---

# _workspace/repo-support/analysis

## Overview

`_workspace/repo-support/analysis`는 저장소 조사에서 만든 분석 요약과 비교표를
잠시 두는 공간이며 Git이 무시합니다.

## Audience

- AI Agents
- Repository Maintainers

## Scope

작업 중 만들 수 있는 산출물:

- 소비자 추적, 호출 그래프, 중복 판정 같은 분석 결과
- 외부 자료와 저장소의 비교표

만들거나 남기지 않는 산출물:

- raw log, 로컬 로그, 진단 덤프 원문
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

## Structure

`README.md`만 추적됩니다. 작업별 하위 디렉터리는 무시되는 임시 공간입니다.

## Usage

1. 작업별로 `<task-slug>/` 하위 디렉터리를 씁니다.
2. 결론과 재현 방법을 현재 Task로 요약합니다.
3. 분석에 쓴 일회성 스크립트는 상시 QA로 등록하지 않습니다.

## Related Documents

- [repo-support README](../README.md)
