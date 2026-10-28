---
title: "CI Diagnostics"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
created: "2026-10-29"
---

# _workspace/diagnostics/ci

## Overview

`_workspace/diagnostics/ci`는 GitHub Actions 등 원격 CI 실행을 조사할 때
내려받거나 요약한 정제 결과를 잠시 두는 공간이며 Git이 무시합니다.

## Audience

- AI Agents
- Repository Maintainers

## Scope

작업 중 만들 수 있는 산출물:

- run ID, job 이름, 후보 SHA, 결론을 담은 요약
- 실패 step의 정제된 발췌와 재현 메모

만들거나 남기지 않는 산출물:

- raw log, 로컬 로그, 진단 덤프 원문
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

## Structure

`README.md`만 추적됩니다. 실행별 하위 디렉터리는 무시되는 임시 공간입니다.

## Usage

1. 실행별로 `<run-id>/` 하위 디렉터리를 씁니다.
2. 원격 필수 검사의 결과는 PR에서 관측하고, 남길 판정은 현재 Task에 요약합니다.
3. 로그 원문을 내려받았다면 정제본만 남기고 원문은 지웁니다.

## Related Documents

- [진단 README](../README.md)
