# projects

> 보조 애플리케이션과 실험용 프로젝트를 parent repo의 인프라 문서 체계와 연결하는 작업 공간

## Overview

`projects/`는 `hy-home.docker` 인프라 위에서 함께 관리되는 보조 프로젝트를 둡니다. 현재 parent repo가 직접 관리하는 주요 하위 프로젝트는 [`storybook/`](storybook/README.md)이며, Storybook 기반 디자인 시스템 템플릿과 Next.js 예제를 포함합니다.

이 경로는 인프라 계층(`infra/`)이나 공식 stage 문서(`docs/`)가 아니라, 로컬 개발과 검증을 위한 프로젝트 작업면입니다. 하위 프로젝트가 별도 gitlink 또는 외부 소스인 경우 parent repo README 최신화 범위와 분리해서 다룹니다.

## Audience

이 README의 주요 독자:

- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- parent repo가 직접 추적하는 보조 프로젝트 README와 진입점
- Storybook/Next.js 같은 예제 또는 디자인 시스템 작업 공간
- 하위 프로젝트와 루트 인프라/문서 체계 사이의 연결 설명

### Out of Scope

- `infra/` 서비스 정의와 운영 절차
- `docs/01`부터 `docs/10`까지의 공식 stage 산출물 본문
- gitlink/submodule 내부 파일의 직접 수정
- package manager 캐시, 빌드 산출물, `node_modules/`

## Structure

```text
projects/
├── storybook/  # Storybook 기반 디자인 시스템 및 Next.js 예제 작업 공간
└── README.md   # This file
```

## How to Work in This Area

1. 하위 프로젝트를 수정하기 전에 해당 프로젝트의 `README.md`와 package manifest를 먼저 확인합니다.
2. parent repo가 직접 추적하지 않는 gitlink/submodule 내부 파일은 별도 저장소 작업으로 분리합니다.
3. README를 갱신할 때는 [`../docs/99.templates/readme.template.md`](../docs/99.templates/readme.template.md)의 공통 구조를 따릅니다.
4. 인프라 노출, gateway, secret, 운영 절차가 바뀌면 관련 `infra/`, `docs/07.guides/`, `docs/08.operations/`, `docs/09.runbooks/` 문서도 함께 점검합니다.

## Related References

- [Root README](../README.md)
- [Docs hub](../docs/README.md)
- [README template](../docs/99.templates/readme.template.md)
- [Storybook project](storybook/README.md)
