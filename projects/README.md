---
title: "Projects Surface"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-01-12"
---

# projects

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

> 보조 애플리케이션과 실험용 프로젝트를 parent repo의 인프라 문서 체계와 연결하는 작업 공간

#### Purpose

##### Audience

이 README의 주요 독자:

- Developers
- Documentation Writers

##### Outcome

###### Project Role
<!-- core-payload-level:4 -->

`projects/`는 `hy-home.docker` 인프라 위에서 함께 관리되는 보조 프로젝트를 둡니다. 현재 parent repo가 직접 관리하는 주요 하위 프로젝트는 [`storybook/`](storybook/README.md)이며, Storybook 기반 디자인 시스템 템플릿과 Next.js 예제를 포함합니다.

이 경로는 인프라 계층(`infra/`)이나 공식 stage 문서(`docs/`)가 아니라, 로컬 개발과 검증을 위한 프로젝트 작업면입니다. 하위 프로젝트가 별도 gitlink 또는 외부 소스인 경우 parent repo README 최신화 범위와 분리해서 다룹니다.

###### In Scope
<!-- core-payload-level:4 -->

- parent repo가 직접 추적하는 보조 프로젝트 README와 진입점
- Storybook/Next.js 같은 예제 또는 디자인 시스템 작업 공간
- 하위 프로젝트와 루트 인프라/문서 체계 사이의 연결 설명

###### Out of Scope
<!-- core-payload-level:4 -->

- `infra/` 서비스 정의와 운영 절차
- `docs/01`부터 `docs/05`, `docs/90`, `docs/98`, `docs/99`까지의 공식 stage 산출물 본문
- gitlink/submodule 내부 파일의 직접 수정
- package manager 캐시, 빌드 산출물, `node_modules/`

#### Getting Started

##### Prerequisites

없음: 이 디렉터리 자체에는 설치할 도구가 없으며, 각 하위 프로젝트의 도구는 해당 `README.md`와 package manifest가 정합니다.

##### First Use

1. 하위 프로젝트를 수정하기 전에 해당 프로젝트의 `README.md`와 package manifest를 먼저 확인합니다.
2. parent repo가 직접 추적하지 않는 gitlink/submodule 내부 파일은 별도 저장소 작업으로 분리합니다.
3. README를 갱신할 때는 `docs/99.templates/02.templates/93.common/readme-repository.template.md`의 공통 구조를 따릅니다.
4. 인프라 노출, gateway, secret, 운영 절차가 바뀌면 관련 `infra/`, `docs/03.specs/`, `docs/05.operations/` 문서도 함께 점검합니다.

#### Repository Map

##### Current Paths

| Path | Purpose |
| --- | --- |
| [storybook/](storybook/README.md) | Storybook 기반 디자인 시스템 및 Next.js 예제 작업 공간 |

###### Directories
<!-- core-payload-level:4 -->

```text
projects/
├── storybook/  # Storybook 기반 디자인 시스템 및 Next.js 예제 작업 공간
└── README.md   # This file
```

###### Canonical Entry Points
<!-- core-payload-level:4 -->

하위 프로젝트의 진입점은 [`storybook/README.md`](storybook/README.md)입니다.

##### Owners

이 문서의 유지 책임은 frontmatter의 `owner`인 `@buenhyden`에게 있습니다.

#### Support

##### Help

이 문서는 별도의 문의·이슈 보고 경로를 기록하지 않습니다.

##### Related Documentation

- [Root README](../README.md)
- [Docs hub](../docs/README.md)
- README template (`docs/99.templates/02.templates/93.common/readme-repository.template.md`)
- [Storybook project](storybook/README.md)

## 적용과 확인

### 적용 방법

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
