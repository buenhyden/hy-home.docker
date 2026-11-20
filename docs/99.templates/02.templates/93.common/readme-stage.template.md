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
layer: '{{LAYER}}'
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

#### Responsibility

##### Purpose

<!-- Author prompt: State what this stage or folder is for, who reads it, and what information it owns and lets flow in or out; separate fact from assumption and link the real owner. Do not manage Task status here. -->

{{PURPOSE_READERS_AND_OWNED_INFORMATION}}

##### Excluded Responsibilities

<!-- Author prompt: Name what this folder does not own and link the owner of each excluded concern; write the reason when nothing is excluded. -->

{{EXCLUDED_RESPONSIBILITIES_AND_OWNERS}}

#### Current Contents

##### Paths

<!-- Author prompt: List only documents or open changes that exist now, one Path and Purpose row per direct child. A document's own table without a Path column may follow; then name the subtypes, the canonical sources and the boundary to non-authoritative records. -->

| Path | Purpose |
| --- | --- |
| {{DIRECT_CHILD_PATH}} | {{DIRECT_CHILD_PURPOSE}} |

{{SUBTYPES_AUTHORITY_AND_RECORD_BOUNDARY}}

##### Owners

<!-- Author prompt: Name the owner of this README and the owner of a listed document only where that document or this README states it; say so in a sentence when it records none. -->

{{OWNERS}}

#### Usage

##### Entry Points

<!-- Author prompt: Link the requirement, design, task and operations documents that feed or consume this folder, the governing policy, and the template that shapes this document. -->

{{UPSTREAM_DOWNSTREAM_POLICY_AND_TEMPLATE_LINKS}}

##### Checks

<!-- Author prompt: Name the template, the review and approval path and the checks to run before changing this folder, and state status transitions, promotion and where an item goes when it leaves; write the reason when there is no transition. -->

{{REVIEW_CHECKS_TRANSITIONS_AND_EXIT}}

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
