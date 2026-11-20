---
title: "디자인 시스템 가이드"
version: "1.0.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
---

# 디자인 시스템 가이드

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

#### Responsibility

##### Purpose

###### Purpose and Readers
<!-- core-payload-level:4 -->

디자인 시스템의 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.

###### Inputs and Outputs
<!-- core-payload-level:4 -->

이 폴더는 아래 문서의 가이드 역할만 소유한다. 구현과 운영 결과는 각 소유 문서와 Task에서 확인한다.

##### Excluded Responsibilities

실행 권한, 비밀값 원문, 새로운 서비스와 빈 분류 문서는 포함하지 않는다.

#### Current Contents

##### Paths

| Path | Purpose |
| --- | --- |
| `0101-storybook.md` | 공유 Storybook은 `projects/storybook/nextjs`의 UI story와 문서를 읽기 전용 정적 origin(`storybook`)과 문서 MCP(`storybook-mcp`)로 제공하는 선택형 `experience` 서비스다.  |

###### Current Items
<!-- core-payload-level:4 -->

| 문서 | 식별자 | 한 줄 역할 |
| --- | --- | --- |
| [Shared Storybook Usage Guide](0101-storybook.md) | `GDE-0101` | 공유 Storybook은 `projects/storybook/nextjs`의 UI story와 문서를 읽기 전용 정적 origin(`storybook`)과 문서 MCP(`storybook-mcp`)로 제공하는 선택형 `experience` 서비스다.  |

###### Classification
<!-- core-payload-level:4 -->

이 폴더의 문서는 모두 가이드 역할이며 `GDE-NNNN` 식별자를 쓴다. 같은 subject의 다른 역할 문서는 있는 경우 같은 번호와 slug로 다른 역할 폴더에 있다.

##### Owners

작성·검토 책임은 `@buenhyden`에게 있다. 같은 통제나 절차의 정본을 복제하지 않는다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [상위 가이드 분류](../README.md)
- [운영 문서](../../README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [문서 작성 계약](../../../00.workspace/03.process/documentation-protocol.md)
- [README 템플릿](../../../99.templates/02.templates/93.common/readme-stage.template.md): 이 README의 양식 원본이며 형식은 Stage 99 Registry의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

1. 식별자와 문서 제목으로 대상을 고른다.
2. 정상 구성과 사용 전제를 이해하고 필요한 통제와 실행 절차로 연결한다.
3. 변경 시 원래 식별자와 생성일을 보존하고 이 목록과 현재 링크를 함께 갱신한다.
4. 문서 경로·메타데이터·링크·운영 카탈로그 검사와 소유 Task의 실제 검증 결과를 확인한다.

###### Transition and Exit
<!-- core-payload-level:4 -->

문서는 `operational-policy` 수명주기(draft, in-review, active, deprecated, superseded, retired)를 따른다. superseded 또는 retired에 이른 문서는 [은퇴 전제 조건](../../../00.workspace/03.process/documentation-protocol.md#retirement-preconditions)을 모두 충족할 때에만 남아야 할 내용을 소유 문서에 요약한 뒤 삭제하고, 번호를 Registry `reserved_history`에 추가하며, 이 목록의 행과 링크를 같은 변경에서 제거한다.

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
