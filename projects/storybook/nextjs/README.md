---
title: "Storybook Next.js Workspace"
version: "1.2.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-09"
created: "2026-02-01"
---

# Storybook Next.js Workspace

## Overview

이 작업공간은 공유 Storybook 정적 자산, 내부 UI 패키지와 로컬 문서 MCP의 소스입니다. Next.js 예제 앱은 Storybook 정적 origin과 별도이며 운영 배포 대상이 아닙니다.

## Audience

내부 UI 개발자, 운영자, 검증 담당자가 사용합니다.

## Scope

Storybook story, 검토된 `Button`·`AsyncState` 패키지와 디자인 토큰, 정적 빌드와 로컬 문서 MCP를 포함합니다. 신규 업무 앱, 원격 MCP 서비스, 사용자 전역 클라이언트 설정은 포함하지 않습니다.

## Structure

`src/stories/`는 공유 컴포넌트의 상태별 story와 상호작용·접근성 검증, `packages/ui/`는 코드 소비 계약, `.storybook/`은 manifest 설정, `mcp/`는 로컬 문서 서버와 revision 기록, `Dockerfile`과 `nginx.conf`는 정적 origin을 소유합니다.

## Tech Stack

npm lockfile이 Next.js, React, Storybook, TypeScript와 MCP 패키지 버전을 소유합니다. Node 빌더와 비특권 NGINX 이미지 참조는 `Dockerfile`이 소유합니다.

## Configuration

`npm ci` 후 `npm run build-storybook`은 `storybook-static/`과 `manifests/components.json`, `manifests/docs.json`, `revision.json`을 생성합니다. `STORYBOOK_SOURCE_REVISION`을 전달하면 revision 파일이 소스 커밋을 기록합니다. 전달하지 않으면 `uncommitted`로 표시합니다. revision 파일은 두 manifest의 SHA-256을 기록하며 로컬 MCP가 읽기 전 대조합니다.

문서 MCP 서버(`mcp/server.ts`)는 `@storybook/mcp`의 `docs-list`, `docs-show`, `docs-show-story`만 등록하고 manifest를 `revision.json`의 SHA-256과 대조한 뒤 읽습니다. 두 방식으로 실행합니다.

- 로컬 개발: `npm run mcp:docs`는 `127.0.0.1:7613/mcp`에서 인증 없이 loopback만 받습니다. 선택형 `STORYBOOK_MCP_PORT`는 1024~65535 범위입니다.
- 원격: `STORYBOOK_MCP_RESOURCE`(https 공개 URL), `STORYBOOK_MCP_ISSUER`(https Keycloak realm), `STORYBOOK_MCP_SCOPE`, `STORYBOOK_MCP_READER_GROUP`를 주면 모든 주소에서 듣고 Host를 공개 URL로 제한하며, RS256 서명·issuer·자기 URL audience·만료·그룹을 확인한 bearer token만 받습니다. 보호 자원 metadata를 `/.well-known/oauth-protected-resource/mcp`에 제공합니다. `npm run build:mcp`가 서버를 의존성까지 한 파일로 묶고 Dockerfile의 `mcp` target이 그 파일과 manifest만 담습니다. 배포 설정은 `infra/13-experience/storybook`, 클라이언트 설정은 GDE-0101이 소유합니다.

브라우저 로그인 쿠키를 MCP 인증으로 사용하지 않습니다.

Docker build context는 이 폴더입니다. `.dockerignore`가 환경 파일, secret, 의존성 캐시와 산출물을 제외합니다. origin은 내부 8080 포트에서 정적 파일만 제공하며 host 80/443을 열지 않습니다. 실제 자원 한도, 읽기 전용 root filesystem과 tmpfs는 Compose 서비스 정의가 소유합니다.

## Validation

```sh
npm ci
npm run lint
npm run typecheck
npm run build-storybook
npm run test:artifacts
npm run coverage
npm run build:mcp
```

`npm run coverage`는 Chromium에서 모든 story의 play 함수와 a11y 검사를 실행합니다. a11y 위반은 `error` 모드라 실패로 처리합니다.

정적 origin 브라우저와 MCP 프로토콜 검사는 Docker 격리 사전 점검 후 실행합니다. `revision.json`의 `uncommitted`는 배포 승인이 아닙니다.

TypeScript는 6.0.3에 고정합니다. 2026-10-09 기준 7.0.2와 7.1 nightly는 JavaScript compiler API를 제공하지 않아 `typescript-eslint`(지원 범위 6.1 미만)가 lint를 거부하고, Next.js는 `experimental.useTypeScriptCli: true`가 있어야 동작합니다. Storybook 빌드·docgen·story 시험과 MCP는 그 설정에서 7.x로 통과했습니다. 7.x 전환은 `typescript-eslint`가 7.x를 지원하는 릴리스를 낸 뒤 이 설정과 함께 진행합니다.

## Usage

컴포넌트 구현은 `packages/ui/`에서 변경합니다. story는 Storybook docgen을 위해 해당 원본을 직접 import하고, 생성 manifest와 외부 소비 계약은 `@hy-home/storybook-ui` 패키지를 사용합니다. 토큰 값은 `packages/ui/src/styles.css`의 CSS 변수가 정의합니다. create-storybook 예제(Header, Page, Configure)는 공유 UI가 아니므로 제거했고 manifest에는 검토된 컴포넌트만 남습니다. 패키지 소비자는 [공유 UI 패키지](packages/ui/README.md)의 타입·CSS·peer 계약을 따릅니다. 공개 레지스트리 배포에는 별도 라이선스와 승인이 필요합니다.

## Related Documents

- [상위 Storybook 작업공간](../README.md)
- [문서 인덱스](../../../docs/README.md)
