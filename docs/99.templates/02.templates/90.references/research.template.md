---
title: '{{TITLE}}'
version: 0.1.0
type: reference/research
status: draft
owner: '{{OWNER}}'
document_scope:
  subject: '{{DOCUMENT_SUBJECT}}'
  layer: reference
updated: '{{UPDATED}}'
layer: references
artifact_id: '{{ARTIFACT_ID}}'
parent_ids:
- '{{PARENT_ID}}'
created: '{{CREATED}}'
---

# {{TITLE}}

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

<!-- 작성 규칙: 이 문서로 해결할 정보 필요와 실제 독자를 밝힌다. 본문 정책을 중복 복사하지 않는다. -->

Readers use the research payload below for this document's information and judgments.

### 책임과 적용 범위

<!-- 작성 규칙: 유지할 대상·적용과 제외 범위·책임자를 밝힌다. 메타데이터 자체가 실행 승인이나 인수 권한을 부여하지 않는다. -->

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

<!-- 작성 규칙: 실제로 존재하거나 명시적으로 생성할 입력, 제약, 전제를 구분한다. 확인한 사실과 가정을 혼동하지 않는다. -->

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

<!-- 작성 규칙: 해당 kind의 payload와 조건·표·필드 의미를 소유한다. 관련 없는 문서 역할과 Release 책임을 모든 문서에 복제하지 않는다. -->

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->

#### Question and Scope

##### Question

<!-- Author prompt: State the design question this research answers. -->

{{RESEARCH_QUESTION}}

##### Scope

<!-- Author prompt: Name what was read or run and what is out of scope. -->

{{OBSERVED_BOUNDARIES_AND_METHOD}}

#### Sources

##### Primary Sources

<!-- Author prompt: List the sources actually opened, with their location and the claims they support. -->

{{PRIMARY_SOURCES}}

##### Versions and Dates

<!-- Author prompt: List each source in the table: Source ID a stable identifier within this member, Source its location, Version the source's own version or "none", Checked At when it was opened, Finding what it actually supports, Application the use chosen here, and Limits what stays unconfirmed. -->

| Source ID | Source | Version | Checked At | Finding | Application | Limits |
| --- | --- | --- | --- | --- | --- | --- |
| {{SOURCE_ID}} | {{SOURCE}} | {{VERSION}} | {{CHECKED_AT}} | {{FINDING}} | {{APPLICATION}} | {{LIMITS}} |

#### Analysis

##### Findings

<!-- Author prompt: Record the dated observations and their interpretation, each with its source. -->

{{FINDINGS}}

##### Alternatives

<!-- Author prompt: Compare the alternatives the sources support; say so when none was compared. -->

{{ALTERNATIVES}}

#### Application and Limits

##### Design Implications

<!-- Author prompt: Name what the findings change, what is not adopted and how acceptance would be tested. -->

{{DESIGN_IMPLICATIONS}}

##### Unverified Conditions

<!-- Author prompt: Name the facts not observed and the limits of the interpretation. -->

{{UNVERIFIED_CONDITIONS}}

## 적용과 확인

### 적용 방법

<!-- 작성 규칙: 실제 독자가 문서 또는 연결된 native 출력을 사용하는 방법을 설명한다. 필요 없는 운영·승인 단계를 만들지 않는다. -->

Use the procedures or reading order stated in the role payload.

### 확인 기준

<!-- 작성 규칙: 문서 목적에 필요한 확인만 제시한다. 설계·구현·검증·사용자 인수를 구별하고 모든 문서에 코드 시험을 강요하지 않는다. -->

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

<!-- 작성 규칙: 정본 owner와 필요한 의존 관계의 목적을 적는다. 모든 문서의 양방향 링크나 과거 별칭을 강제하지 않는다. -->

The role payload retains the current owner and dependency references.

### 외부 근거

<!-- 작성 규칙: 외부 사실과 현재 설계의 적용·제외 이유를 구분한다. 출처가 실행 권한이나 성공 증거를 대신하지 않는다. -->

External basis and its limits remain those stated in the role payload; a citation grants no authority.
