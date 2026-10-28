---
title: "Repository Support Previews"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
created: "2026-10-29"
---

# _workspace/repo-support/previews

## Overview

`_workspace/repo-support/previews`는 변경을 적용하기 전에 만든 dry-run
미리보기를 잠시 두는 공간이며 Git이 무시합니다.

## Audience

- AI Agents
- Repository Maintainers

## Scope

작업 중 만들 수 있는 산출물:

- 이동·삭제·번호 전환 예정 목록
- 렌더링·생성 결과의 미리보기

만들거나 남기지 않는 산출물:

- raw log, 로컬 로그, 진단 덤프 원문
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

## Structure

`README.md`만 추적됩니다. 작업별 하위 디렉터리는 무시되는 임시 공간입니다.

## Usage

1. 작업별로 `<task-slug>/` 하위 디렉터리를 씁니다.
2. 승인이 필요한 변경은 미리보기를 근거로 현재 Task에 범위를 기록한 뒤 적용합니다.
3. 미리보기는 승인이나 적용 증거가 아닙니다.

## Related Documents

- [repo-support README](../README.md)
