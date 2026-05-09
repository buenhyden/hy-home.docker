# Storybook Workspace

> Next.js와 Storybook 기반 UI 실험 및 디자인 시스템 템플릿 작업 공간

## Overview

`projects/storybook/`는 parent repo가 직접 관리하는 Storybook 관련 작업 공간입니다. 현재 직접 추적되는 구현 표면은 [`nextjs/`](nextjs/README.md)이며, Next.js 16, React 19, Storybook 10, Vitest, Playwright 기반 UI 개발과 검증을 다룹니다.

`projects/storybook/mcp`는 gitlink/submodule로 연결된 별도 소스입니다. parent repo README 최신화에서는 해당 내부 README를 직접 수정하지 않고, 필요한 경우 별도 저장소 작업으로 분리합니다.

## Audience

이 README의 주요 독자:

- Frontend Developers
- Design System Maintainers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- parent repo가 직접 추적하는 Storybook/Next.js 예제 작업 공간
- npm lockfile 기반 설치, 개발, 빌드, Storybook 실행 명령
- 하위 `nextjs/` README와 루트 프로젝트 문서 사이의 연결

### Out of Scope

- `projects/storybook/mcp` gitlink 내부 파일 직접 수정
- Docker Compose 서비스 정의와 Traefik production exposure
- Storybook 정적 산출물, coverage 결과, `node_modules/`
- 공식 제품 요구사항, 운영 정책, runbook 본문

## Structure

```text
storybook/
├── nextjs/    # Next.js 16 + React 19 + Storybook 10 workspace
├── mcp/       # Gitlink/submodule; edit in its own repository
└── README.md  # This file
```

## How to Work in This Area

1. Node 작업은 `projects/storybook/nextjs/`의 `package.json`과 lockfile을 기준으로 수행합니다.
2. parent repo에서 실행할 때는 `npm --prefix projects/storybook/nextjs <command>` 형태를 사용합니다.
3. Storybook MCP 관련 파일은 gitlink 내부 범위이므로 이 저장소의 README refresh diff에 포함하지 않습니다.
4. UI 템플릿이나 package script가 바뀌면 이 README와 [`nextjs/README.md`](nextjs/README.md)를 함께 갱신합니다.

## Available Scripts

| Command | Description |
| --- | --- |
| `npm ci --prefix projects/storybook/nextjs` | lockfile 기반 의존성 설치 |
| `npm --prefix projects/storybook/nextjs run dev` | Next.js 개발 서버 실행 |
| `npm --prefix projects/storybook/nextjs run storybook` | Storybook 개발 서버 실행 |
| `npm --prefix projects/storybook/nextjs run build` | Next.js production build |
| `npm --prefix projects/storybook/nextjs run build-storybook` | Storybook 정적 산출물 빌드 |
| `npm --prefix projects/storybook/nextjs run lint` | ESLint 실행 |

## Related References

- [Projects README](../README.md)
- [Next.js Storybook workspace](nextjs/README.md)
- [Root README](../../README.md)
- [README template](../../docs/99.templates/readme.template.md)
