---
title: '{{TITLE}}'
version: 0.1.0
type: common/readme
status: active
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: workspace
updated: '{{UPDATED}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: Identify the information or judgment this document gives its readers; route to the role payload instead of copying its rules. -->

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

<!-- 작성 규칙: Name the maintained subject, scope and owner; do not grant authority through document metadata. -->

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: State actual inputs, constraints or preconditions, and distinguish facts from assumptions. -->

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

<!-- 작성 규칙: Keep the kind-specific payload here with its conditions, tables and one canonical responsibility. -->

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

#### Purpose

##### Audience

<!-- Author prompt: Name the primary reader of this project or folder as fact, apart from assumptions. -->

{{PRIMARY_READERS}}

##### Outcome

<!-- Author prompt: State the project or folder purpose, what is supported and what is a non-goal, and link the real owner of each excluded concern. -->

{{PROJECT_ROLE_SUPPORTED_SCOPE_AND_NON_GOALS}}

#### Getting Started

##### Prerequisites

{{REQUIRED_TOOLS_ENVIRONMENT_AND_PERMISSIONS}}

##### First Use

<!-- Author prompt: Give the first verified path: what to start or check and the expected result. -->

{{START_CHECK_AND_EXPECTED_RESULT}}

#### Repository Map

##### Current Paths

<!-- Author prompt: Route readers to implementation and existing documentation owners, one Path and Purpose row per direct child. Derive inventories from tracked sources instead of fixed counts. Describe lifecycle and validation entrypoints without copying Guide, Policy or Runbook procedures. Outside docs/, route numbered-stage documentation through docs/README.md. -->

<!-- Author prompt: Compose/Dockerfile declarations own runtime image tags and dependency pins; the curated machine-readable registry is a derived projection. Link the implementation authority; do not copy exact patch versions into narrative inventories. A necessary compatibility, advisory, workaround, migration or history literal requires a same-line comment `runtime-version-exception: migration — explain the concrete migration boundary` with the applicable category and a concrete reason. Document frontmatter versions are independent. -->

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{DIRECT_CHILD_PURPOSE}} |

{{DIRECTORY_PURPOSE_AND_ENTRY_POINTS}}

##### Owners

<!-- Author prompt: Name the maintainer or owner the folder states; say so in a sentence when it records none. -->

{{OWNERS}}

#### Support

##### Help

<!-- Author prompt: Name the contact and issue reporting route. -->

{{CONTACT_AND_ISSUE_REPORTING}}

##### Related Documentation

{{CURRENT_USAGE_DEVELOPMENT_AND_OPERATIONS_LINKS}}

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: Explain how the intended reader uses this document or its native output; do not invent an operational step. -->

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

<!-- 작성 규칙: Use only checks appropriate to this kind; distinguish implementation, verification and actual acceptance. -->

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: Use purpose-bearing owner and dependency references; reciprocal links are not universally required. -->

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

<!-- 작성 규칙: Identify external basis and its application or limits; a citation grants no execution or approval authority. -->

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
