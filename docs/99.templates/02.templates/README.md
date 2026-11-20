---
title: "Template Catalog"
version: "4.1.0"
type: "common/readme"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "templates"
---

# Template Catalog

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

이 디렉터리는 [`../registry.json`](../registry.json)이 등록한 복사용 원본을
담습니다. 문서 type과 template 원본의 정확한 대응은 Registry의
`template_roles`만 소유합니다. 이 README는 category 디렉터리로 가는 길만
안내하고 개별 template 파일은 목록으로 옮겨 적지 않습니다. 계약 설명은
[Stage 99 README](../README.md)에, 완성된 문서가 지켜야 할 규칙은 각 문서를
소유한 stage에 있습니다.

###### Audience
<!-- core-payload-level:4 -->

- Documentation Writers
- Repository Maintainers

###### Inputs and Outputs
<!-- core-payload-level:4 -->

- 포함: Registry `template_roles`가 가리키는 template 원본.

##### Excluded Responsibilities

- 제외: 완성된 문서, 과거 template, category별 README. 과거 template은 Git
  history로만 복구하며 현재 작성에 복사하지 않습니다.

#### Current Contents

##### Paths

###### Current Items
<!-- core-payload-level:4 -->

| Path | Purpose |
| --- | --- |
| [00.workspace/](00.workspace/) | 좁은 workspace Guide와 로컬 용어 source |
| [02.architecture/](02.architecture/) | Description과 ADR source |
| [93.common/](93.common/) | README source |
| [91.agent-governance/](91.agent-governance/) | 공유 governance source |
| [05.operations/](05.operations/) | 운영 역할별 source |
| [90.references/](90.references/) | reference pack과 member source |
| [01.requirements/](01.requirements/) | Requirement source |
| [92.runtime/](92.runtime/) | native provider projection source |
| [03.specs/](03.specs/) | Spec·Plan·Task와 interface source |

###### Classification
<!-- core-payload-level:4 -->

각 category 안의 template 원본만 정본이며 완성된 문서와 과거 template은 두지 않습니다(과거 template은 Git history로만 복구). template은 복사용 source이므로 복사해 만든 문서가 자기 profile의 수명주기를 시작합니다.

##### Owners

이 README의 소유자는 frontmatter `owner`의 `@buenhyden`입니다. 목록에 있는 각 항목의 소유자는 이 README가 따로 기록하지 않습니다.

#### Usage

##### Entry Points

###### Upstream and Downstream
<!-- core-payload-level:4 -->

- [Stage 99 authority](../README.md)

###### Policy and Templates
<!-- core-payload-level:4 -->

- [Registry](../registry.json)
- [Documentation protocol](../../00.workspace/03.process/documentation-protocol.md)
- 이 README의 양식 원본은 `common/readme-stage.template.md`이며 형식은 [Stage 99 Registry](../registry.json)의 profile이 소유합니다

##### Checks

###### Create and Review
<!-- core-payload-level:4 -->

1. [`../registry.json`](../registry.json)의 `template_roles`에서 역할을 찾습니다.
   일반 Markdown은 공통 정의 `source`를 복사합니다. `native_source`가 있는
   역할은 정의를 실제 출력에 넣지 않고 등록된 생성기가 그 native payload를
   읽도록 합니다. 디렉터리 이름만으로 양식을 고르지 않습니다.
2. Markdown의 모든 `{{UPPER_SNAKE_CASE}}` 자리 표시자를 채우고 template
   전용 HTML 작성 안내 주석을 지웁니다. 기계용 contract 원본은
   `__UPPER_SNAKE__` token을 씁니다.
3. 본문은 작성 안내 주석이 지정한 언어로 씁니다. 언어는 Registry profile의
   `language`가 소유합니다.
4. 선언된 `type`을 유지하고 profile이 식별자를 선언하면 저장된 high-water
   mark보다 큰 번호를 할당합니다.
5. 적용할 검사는 공통 agent governance의
   [verification matrix](../../00.workspace/04.quality/quality-standards.md#5-change-type-verification-matrix)로
   고릅니다. 실행 전에 `--explain`으로 선택된 gate를 확인하고, 안전하지
   않거나 쓸 수 없는 leaf는 정확한 이유와 함께 DEFER로 기록합니다. full
   또는 all-files 실행도 Task 범위와 controlled-wrapper 승인 경계를
   따릅니다.

###### Transition and Exit
<!-- core-payload-level:4 -->

이 README는 `navigation` 수명주기의 `active` 상태만 가지며 다른 상태로 전이하지 않습니다. 목록 항목을 추가·이동·삭제할 때 이 문서를 함께 갱신하고, 삭제한 항목의 이력은 Git이 기록합니다.

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
