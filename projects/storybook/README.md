---
title: "Storybook Workspace"
version: "1.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2025-11-24"
---

# Storybook Workspace

## Overview

`projects/storybook/nextjs/`는 저장소가 직접 관리하는 공유 UI 자산 작업공간입니다. 정적 Storybook, 내부 UI 패키지와 로컬 문서 MCP를 함께 소유합니다.

## Audience

내부 UI 개발자, 디자인 검토자와 운영 담당자입니다.

## Scope

공유 컴포넌트와 문서만 포함합니다. 신규 공공데이터·공무원·언어 학습 앱은 외부 프로젝트가 소유합니다.

## Structure

`nextjs/`에 npm lockfile, Storybook 설정, `packages/ui/`, 로컬 `mcp/`, 정적 origin Dockerfile이 있습니다.

## Tech Stack

버전과 peer dependency는 [하위 패키지](nextjs/README.md)의 npm manifest와 lockfile이 소유합니다.

## Configuration

정적 origin은 별도 Compose fragment로 선택형 root profile에 연결됩니다. Traefik이 HTTPS를 종료하고 기존 관리자 인증을 적용합니다. 문서 MCP는 Compose 밖의 로컬 프로세스이며 원격 접속은 비활성입니다.

## Validation

`npm ci --prefix projects/storybook/nextjs` 후 하위 README의 빌드·검사 명령을 사용합니다. Docker 실행 검사는 격리 범위를 확인한 뒤 수행합니다.

## Usage

UI 변경은 `nextjs/`에서 진행합니다. 외부 프로젝트는 검토된 패키지 계약을 소비하며 Storybook 소스 파일을 무관리 복사하지 않습니다.

## Related Documents

- [하위 Storybook 작업공간](nextjs/README.md)
- [프로젝트 인덱스](../README.md)
- [문서 인덱스](../../docs/README.md)
