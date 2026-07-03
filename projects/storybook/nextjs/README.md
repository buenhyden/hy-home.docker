# Storybook Next.js Workspace

> Next.js 16, React 19, Storybook 10 기반 UI 개발 및 검증 package

## Overview

`projects/storybook/nextjs/`는 Storybook UI 템플릿을 검증하는 Next.js workspace입니다. npm lockfile을 기준으로 의존성을 고정하고, Next.js pages router, Storybook stories, Vitest/Playwright 기반 브라우저 테스트 설정을 함께 보유합니다.

이 README는 초기 scaffold 안내가 아니라 현재 package manifest와 repository contract에 맞춘 작업 진입점입니다.

## Audience

이 README의 주요 독자:

- Frontend Developers
- QA Engineers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- `package.json` scripts와 npm lockfile 기반 작업 절차
- Next.js pages, Storybook stories, Storybook/Vitest 설정 위치
- 로컬 개발, lint, build, Storybook build 검증 명령

### Out of Scope

- Vercel 배포 절차
- `projects/storybook/mcp` gitlink 내부 MCP 구현
- `node_modules/`, `.next/`, Storybook 정적 build output
- 루트 Docker Compose 서비스 운영 절차

## Structure

```text
nextjs/
├── .storybook/        # Storybook framework and test setup
├── public/            # Static public assets
├── src/
│   ├── pages/         # Next.js pages router and API route sample
│   ├── stories/       # Storybook example components and stories
│   └── styles/        # Global CSS
├── package.json       # npm scripts and dependency contract
├── package-lock.json  # npm lockfile
├── vitest.config.ts   # Vitest browser test configuration
└── README.md          # This file
```

## Available Scripts

| Command | Description |
| --- | --- |
| `npm ci` | lockfile 기반 의존성 설치 |
| `npm run dev` | Next.js 개발 서버 실행 |
| `npm run storybook` | Storybook 개발 서버 실행 |
| `npm run build` | Next.js production build |
| `npm run build-storybook` | Storybook 정적 산출물 빌드 |
| `npm run lint` | ESLint 실행 |
| `npm run typecheck` | TypeScript typecheck 실행 |
| `npm run test` | Storybook Vitest 테스트 실행 |
| `npm run coverage` | Storybook Vitest coverage 실행; statements/branches/functions/lines 90% threshold 적용 |

Parent repo 루트에서 실행할 때는 `npm --prefix projects/storybook/nextjs <command>`를 사용합니다.

## How to Work in This Area

1. 의존성을 바꾸면 `package.json`과 `package-lock.json`을 함께 갱신합니다.
2. UI component 예제는 `src/stories/`에 두고 Storybook story와 함께 검증합니다.
3. Next.js app shell이나 API route 예시는 `src/pages/` 아래에서 관리합니다.
4. README 또는 package script를 바꾼 뒤에는 최소 `npm --prefix projects/storybook/nextjs run lint`와 관련 build/test 명령을 검토합니다.

## Related Documents

- [Storybook workspace](../README.md)
- [Projects README](../../README.md)
- [Root README](../../../README.md)
- [README template](../../../docs/99.templates/templates/common/readme.template.md)
