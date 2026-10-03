---
title: "Storybook Next.js Workspace"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
created: "2026-02-01"
---

# Storybook Next.js Workspace

## Overview

이 작업공간은 공유 Storybook 정적 자산, 내부 UI 패키지와 로컬 문서 MCP의 소스입니다. Next.js 예제 앱은 Storybook 정적 origin과 별도이며 운영 배포 대상이 아닙니다.

## Audience

내부 UI 개발자, 운영자, 검증 담당자가 사용합니다.

## Scope

Storybook story, 검토된 Button 패키지, 정적 빌드와 로컬 문서 MCP를 포함합니다. 신규 업무 앱, 원격 MCP 서비스, 사용자 전역 클라이언트 설정은 포함하지 않습니다.

## Structure

`src/stories/`는 예제와 검증, `packages/ui/`는 코드 소비 계약, `.storybook/`은 manifest 설정, `mcp/`는 로컬 문서 서버와 revision 기록, `Dockerfile`과 `nginx.conf`는 정적 origin을 소유합니다.

## Tech Stack

npm lockfile이 Next.js, React, Storybook, TypeScript와 MCP 패키지 버전을 소유합니다. Node 빌더와 비특권 NGINX 이미지 참조는 `Dockerfile`이 소유합니다.

## Configuration

`npm ci` 후 `npm run build-storybook`은 `storybook-static/`과 `manifests/components.json`, `manifests/docs.json`, `revision.json`을 생성합니다. `STORYBOOK_SOURCE_REVISION`을 전달하면 revision 파일이 소스 커밋을 기록합니다. 전달하지 않으면 `uncommitted`로 표시합니다. revision 파일은 두 manifest의 SHA-256을 기록하며 로컬 MCP가 읽기 전 대조합니다.

`npm run mcp:docs`는 정적 빌드 후 `127.0.0.1:7613/mcp`에서 문서 도구만 제공합니다. 선택형 `STORYBOOK_MCP_PORT`는 1024~65535 범위입니다. 이 서버는 루트 Compose에 포함되지 않으며 원격 클라이언트에 공개하지 않습니다. `@storybook/mcp`가 제공하는 `docs-list`, `docs-show`, `docs-show-story`만 등록합니다. 브라우저 로그인 쿠키를 MCP 인증으로 사용하지 않습니다.

Docker build context는 이 폴더입니다. `.dockerignore`가 환경 파일, secret, 의존성 캐시와 산출물을 제외합니다. origin은 내부 8080 포트에서 정적 파일만 제공하며 host 80/443을 열지 않습니다. 실제 자원 한도, 읽기 전용 root filesystem과 tmpfs는 Compose 서비스 정의가 소유합니다.

## Validation

```sh
npm ci
npm run lint
npm run typecheck
npm run build-storybook
npm run test:artifacts
```

정적 origin 브라우저와 MCP 프로토콜 검사는 Docker 격리 사전 점검 후 실행합니다. `revision.json`의 `uncommitted`는 배포 승인이 아닙니다.

## How to Work in This Area

Button 구현은 `packages/ui/`에서 변경합니다. Button story는 Storybook docgen을 위해 해당 원본을 직접 import하고, 생성 manifest와 외부 소비 계약은 `@hy-home/storybook-ui` 패키지를 사용합니다. Header와 Page는 예제로 유지합니다. 패키지 소비자는 [공유 UI 패키지](packages/ui/README.md)의 타입·CSS·peer 계약을 따릅니다. 공개 레지스트리 배포에는 별도 라이선스와 승인이 필요합니다.

## Related Documents

- [상위 Storybook 작업공간](../README.md)
- [문서 인덱스](../../../docs/README.md)
