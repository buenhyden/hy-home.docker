---
title: "Repository Support Staging"
version: "1.0.0"
type: "common/repository-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-09-27"
---

# _workspace/repo-support

## Overview

`_workspace/repo-support`는 비밀이 아닌 저장소 지원 산출물을 잠시 두는
공간이며 Git이 무시합니다. agent 작업, migration, dry-run, 분석에서 생기는
짧은 수명의 파일을 둘 수 있는 `_workspace` 안의 유일한 승인 위치입니다.

이 디렉터리는 활성 문서 stage, archive, 운영 폴더, 런타임 설정, 장기 증거
보관소가 아닙니다.

## Audience

- AI Agents
- Repository Maintainers

## Scope

작업 중 만들 수 있는 산출물:

- 생성된 분석 요약
- ID, 경로, 계획된 작업 단위의 dry-run 미리보기
- migration ledger
- subagent 인계 파일
- 임시 비교표
- raw log나 비밀이 담긴 출력이 없는 검증 메모

만들거나 남기지 않는 산출물:

- 진단 덤프, 로컬 로그, raw log
- 인증 파일, token, credential, private key
- shell history, secret 값, token이 담긴 명령 출력
- secret 파일 본문 전체

## Structure

`README.md`만 추적됩니다. 작업별 하위 디렉터리는 무시되는 임시 공간이므로
이 README가 목록을 관리하지 않습니다.

## How to Work in This Area

작업을 마치기 전에 오래 남길 비밀 아닌 결과를 정본 owner로 옮깁니다.

- 구현 증거는 현재 `docs/03.specs/` package의 Task로 옮깁니다.
- 안정적인 참조 맥락은 `docs/90.references/`로 옮깁니다.
- 오래 유지할 거버넌스 규칙은 `.agents/governance/`의 해당 정책 owner로
  옮깁니다.
- 작업별 맥락은 현재 Task에 남기며 별도의 거버넌스 memory root는 두지
  않습니다.

사용자가 비밀 아닌 산출물의 승격을 명시적으로 승인하지 않는 한, 원본
임시 산출물은 무시된 상태로 둡니다.

## Related Documents

- [workspace README](../README.md)
