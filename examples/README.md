---
title: "Examples Surface"
version: "2.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
created: "2026-09-03"
---

# examples

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

> 새 서비스를 시작할 때 복사해서 쓰는 검증된 시드(seed) 모음

#### Purpose

##### Audience

- 새 컨테이너 서비스를 추가하려는 Developers
- 저장소의 컨테이너 하드닝 관례를 확인하려는 Reviewers

##### Outcome

###### Project Role
<!-- core-payload-level:4 -->

`examples/`는 두 개의 직접 하위 디렉터리를 둡니다. [`sample-web-service/`](sample-web-service/README.md)는
이 저장소의 컨테이너 관례를 그대로 담은 복사 가능한 시드이며, 정적 웹 서비스
형태로 Compose 정의, Dockerfile, nginx 설정, `.env.example`, 서비스 문서를 한
벌로 제공합니다. `operations/`는 운영 rehearsal과 검증
스크립트가 재사용하는 입력 fixture 모음이며 복사용 시드가 아닙니다.

이 경로는 실행 중인 인프라가 아닙니다. `infra/`가 실제 서비스 정의를 소유하고,
`examples/`는 그 관례를 배우고 복사하기 위한 출발점과 검증용 입력만
소유합니다.

###### In Scope
<!-- core-payload-level:4 -->

- 복사 가능한 서비스 시드와 각 시드의 README
- 시드가 보여주는 컨테이너·Compose·시크릿 주입 관례

###### Out of Scope
<!-- core-payload-level:4 -->

- `infra/`의 실제 서비스 정의와 운영 절차
- 시드를 복사한 뒤의 서비스별 설정값
- `docs/` stage 산출물 본문

#### Getting Started

##### Prerequisites

시드를 복사한 뒤 `docker compose config`와 `scripts/validation/validate-docker-compose.sh`로 검증하므로 Docker Compose가 필요합니다.

##### First Use

1. 시드 폴더 전체를 `infra/`의 대상 tier 아래로 복사합니다 → 원본 시드는 그대로 남습니다.
2. 복사본에서 서비스 이름, 이미지, 포트, 네트워크를 대상 서비스에 맞게 바꿉니다 → `docker compose config`가 성공합니다.
3. 시크릿은 값이 아니라 파일로 주입하고 `.env.example`만 추적합니다 → 평문 자격 증명이 커밋되지 않습니다.
4. 새 서비스 문서를 `docs/05.operations/README.md`의 해당 도메인에 추가합니다 → 운영 절차 소유자가 생깁니다.
5. `bash scripts/validation/validate-docker-compose.sh`를 실행합니다 → 종료 코드 `0`.

시드 자체를 고칠 때는 복사본 대신 `examples/` 원본을 고치고 그 변경이 기존
서비스에 적용되어야 하는지 함께 판단합니다.

#### Repository Map

##### Current Paths

| Path | Purpose |
| --- | --- |
| `operations/` | 운영 rehearsal/검증 입력 fixture (README 없음) |
| [sample-web-service/](sample-web-service/README.md) | 정적 웹 서비스 시드 (Compose, Dockerfile, nginx, 서비스 문서) |

###### Directories
<!-- core-payload-level:4 -->

```text
examples/
├── operations/           # 운영 rehearsal/검증 입력 fixture (README 없음)
├── sample-web-service/   # 정적 웹 서비스 시드 (Compose, Dockerfile, nginx, 서비스 문서)
└── README.md             # This file
```

###### Canonical Entry Points
<!-- core-payload-level:4 -->

복사 가능한 시드의 진입점은 [`sample-web-service/`](sample-web-service/README.md)입니다.

##### Owners

이 문서의 유지 책임은 frontmatter의 `owner`인 `@buenhyden`에게 있습니다.

#### Support

##### Help

이 문서는 별도의 문의·이슈 보고 경로를 기록하지 않습니다.

##### Related Documentation

- [Root README](../README.md)
- [Infrastructure surface](../infra/README.md)
- [Sample web service seed](sample-web-service/README.md)
- Operations (`docs/05.operations/README.md`)
- README template (`docs/99.templates/02.templates/93.common/readme-repository.template.md`)
- [Documentation index](../docs/README.md)

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
