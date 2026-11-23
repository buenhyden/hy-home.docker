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

<!-- 작성 규칙: 이 문서로 해결할 정보 필요와 실제 독자를 밝힌다. 본문 정책을 중복 복사하지 않는다. -->

독자는 아래 역할 본문에서 이 문서가 제공하는 정보와 판단을 확인합니다.

### 책임과 적용 범위

<!-- 작성 규칙: 유지할 대상·적용과 제외 범위·책임자를 밝힌다. 메타데이터 자체가 실행 승인이나 인수 권한을 부여하지 않는다. -->

적용 대상과 유지 책임은 frontmatter와 역할 본문의 범위 선언이 소유합니다.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 실제로 존재하거나 명시적으로 생성할 입력, 제약, 전제를 구분한다. 확인한 사실과 가정을 혼동하지 않는다. -->

실제 입력과 전제는 아래 역할 본문의 해당 항목을 따릅니다.

### 본문과 규칙

<!-- 작성 규칙: 해당 kind의 payload와 조건·표·필드 의미를 소유한다. 관련 없는 문서 역할과 Release 책임을 모든 문서에 복제하지 않는다. -->

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

<!-- 작성 규칙: 실제 독자가 문서 또는 연결된 native 출력을 사용하는 방법을 설명한다. 필요 없는 운영·승인 단계를 만들지 않는다. -->

아래 역할 본문의 절차나 탐색 순서에 따라 사용합니다.

### 확인 기준

<!-- 작성 규칙: 문서 목적에 필요한 확인만 제시한다. 설계·구현·검증·사용자 인수를 구별하고 모든 문서에 코드 시험을 강요하지 않는다. -->

해당 문서에 선언된 확인 기준과 한계만 적용하며 실행·검증·인수를 구분합니다.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 정본 owner와 필요한 의존 관계의 목적을 적는다. 모든 문서의 양방향 링크나 과거 별칭을 강제하지 않는다. -->

현재 소유자와 의존 문서의 연결은 아래 역할 본문의 링크가 소유합니다.

### 외부 근거

<!-- 작성 규칙: 외부 사실과 현재 설계의 적용·제외 이유를 구분한다. 출처가 실행 권한이나 성공 증거를 대신하지 않는다. -->

외부 출처와 적용 한계는 아래 역할 본문에 선언된 범위이며 권한을 부여하지 않습니다.
